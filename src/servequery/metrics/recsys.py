from abc import ABC
from typing import ClassVar
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

from servequery.core.metric_types import BoundTest
from servequery.core.metric_types import SingleValue
from servequery.core.metric_types import SingleValueCalculation
from servequery.core.metric_types import SingleValueMetric
from servequery.core.metric_types import TMetricResult
from servequery.core.report import Context
from servequery.core.report import Report
from servequery.legacy.metrics import FBetaTopKMetric
from servequery.legacy.metrics import HitRateKMetric
from servequery.legacy.metrics import MAPKMetric
from servequery.legacy.metrics import MRRKMetric
from servequery.legacy.metrics import NDCGKMetric
from servequery.legacy.metrics import PrecisionTopKMetric
from servequery.legacy.metrics import RecallTopKMetric
from servequery.legacy.metrics.recsys.base_top_k import TopKMetric
from servequery.legacy.metrics.recsys.base_top_k import TopKMetricResult
from servequery.legacy.metrics.recsys.scores_distribution import ScoreDistribution as ScoreDistributionLegacy
from servequery.legacy.metrics.recsys.scores_distribution import ScoreDistributionResult
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.metrics._legacy import LegacyMetricCalculation
from servequery.tests import Reference
from servequery.tests import eq


class TopKBase(SingleValueMetric):
    k: int
    min_rel_score: Optional[int] = None
    no_feedback_users: bool = False

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


TTopKBase = TypeVar("TTopKBase", bound=TopKBase)


class LegacyTopKCalculation(
    LegacyMetricCalculation[
        SingleValue,
        TTopKBase,
        TopKMetricResult,
        TopKMetric,
    ],
    SingleValueCalculation,
    Generic[TTopKBase],
    ABC,
):
    __legacy_metric_type__: ClassVar[Type[TopKMetric]]

    def legacy_metric(self):
        return self.__legacy_metric_type__(
            k=self.metric.k, min_rel_score=self.metric.min_rel_score, no_feedback_users=self.metric.no_feedback_users
        )

    def calculate_value(
        self, context: "Context", legacy_result: TopKMetricResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = self.result(legacy_result.current[legacy_result.k - 1])
        if legacy_result.reference is None:
            return current
        return current, self.result(legacy_result.reference[legacy_result.k - 1])


class NDCG(TopKBase):
    pass


class NDCGCalculation(LegacyTopKCalculation[NDCG]):
    __legacy_metric_type__: ClassVar = NDCGKMetric

    def display_name(self) -> str:
        return "NDCG@k"


class MRR(TopKBase):
    pass


class MRRCalculation(LegacyTopKCalculation[MRR]):
    __legacy_metric_type__: ClassVar = MRRKMetric

    def display_name(self) -> str:
        return "MRR@k"


class HitRate(TopKBase):
    pass


class HitRateCalculation(LegacyTopKCalculation[HitRate]):
    __legacy_metric_type__: ClassVar = HitRateKMetric

    def display_name(self) -> str:
        return "HitRate@k"


class MAP(TopKBase):
    pass


class MAPCalculation(LegacyTopKCalculation[MAP]):
    __legacy_metric_type__: ClassVar = MAPKMetric

    def display_name(self) -> str:
        return "MAP@k"


class RecallTopK(TopKBase):
    pass


class RecallTopKCalculation(LegacyTopKCalculation[RecallTopK]):
    __legacy_metric_type__: ClassVar = RecallTopKMetric

    def display_name(self) -> str:
        return "Recall@k"


class PrecisionTopK(TopKBase):
    pass


class PrecisionTopKCalculation(LegacyTopKCalculation[PrecisionTopK]):
    __legacy_metric_type__: ClassVar = PrecisionTopKMetric

    def display_name(self) -> str:
        return "Precision@k"


class FBetaTopK(TopKBase):
    beta: Optional[float] = 1.0


class FBetaTopKCalculation(LegacyTopKCalculation[FBetaTopK]):
    def display_name(self) -> str:
        return f"F{self.metric.beta}@k"

    def legacy_metric(self):
        return FBetaTopKMetric(
            k=self.metric.k,
            min_rel_score=self.metric.min_rel_score,
            no_feedback_users=self.metric.no_feedback_users,
            beta=self.metric.beta,
        )


class ScoreDistribution(SingleValueMetric):
    k: int

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_single(self.get_fingerprint()),
        ]


class ScoreDistributionCalculation(
    LegacyMetricCalculation[SingleValue, ScoreDistribution, ScoreDistributionResult, ScoreDistributionLegacy],
    SingleValueCalculation,
):
    def legacy_metric(self) -> ScoreDistributionLegacy:
        return ScoreDistributionLegacy(k=self.metric.k)

    def calculate_value(
        self, context: "Context", legacy_result: ScoreDistributionResult, render: List[BaseWidgetInfo]
    ) -> TMetricResult:
        current = self.result(legacy_result.current_entropy)
        if legacy_result.reference_entropy is None:
            return current
        return current, self.result(legacy_result.reference_entropy)

    def display_name(self) -> str:
        return "Score distribution"


def main():
    import pandas as pd

    def create_snapshot(i):
        df = pd.DataFrame(
            {
                "user_id": [i % 3 for i in range(i + 5)],
                "target": [0.5 for i in range(i + 5)],
                "prediction": [0.5 for i in range(i + 5)],
            }
        )
        from servequery.core.datasets import DataDefinition
        from servequery.core.datasets import Dataset
        from servequery.core.datasets import Recsys

        dataset = Dataset.from_pandas(
            df, data_definition=DataDefinition(numerical_columns=["target", "prediction"], ranking=[Recsys()])
        )
        report = Report(
            [
                NDCG(k=3, no_feedback_users=True),
                MRR(k=3),
                HitRate(k=3),
                ScoreDistribution(k=3),
                MAP(k=3),
                RecallTopK(k=3),
                PrecisionTopK(k=3),
                FBetaTopK(k=3),
            ]
        )
        snapshot_v2 = report.run(dataset, None)

        from servequery.ui.backport import snapshot_v2_to_v1

        snapshot_v1 = snapshot_v2_to_v1(snapshot_v2)
        return snapshot_v1

    sn = create_snapshot(10)
    sn.save("ndcg.json")


if __name__ == "__main__":
    main()
