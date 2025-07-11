from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from servequery.legacy.metric_preset.metric_preset import AnyMetric
from servequery.legacy.metric_preset.metric_preset import MetricPreset
from servequery.legacy.metrics import DiversityMetric
from servequery.legacy.metrics import FBetaTopKMetric
from servequery.legacy.metrics import HitRateKMetric
from servequery.legacy.metrics import ItemBiasMetric
from servequery.legacy.metrics import MAPKMetric
from servequery.legacy.metrics import MRRKMetric
from servequery.legacy.metrics import NDCGKMetric
from servequery.legacy.metrics import NoveltyMetric
from servequery.legacy.metrics import PersonalizationMetric
from servequery.legacy.metrics import PopularityBias
from servequery.legacy.metrics import PrecisionTopKMetric
from servequery.legacy.metrics import RecallTopKMetric
from servequery.legacy.metrics import RecCasesTable
from servequery.legacy.metrics import ScoreDistribution
from servequery.legacy.metrics import SerendipityMetric
from servequery.legacy.metrics import UserBiasMetric
from servequery.legacy.pipeline.column_mapping import RecomType
from servequery.legacy.utils.data_preprocessing import DataDefinition


class RecsysPreset(MetricPreset):
    class Config:
        type_alias = "servequery:metric_preset:RecsysPreset"

    """Metric preset for recsys performance analysis.

    Contains metrics:
    - PrecisionTopKMetric
    - RecallTopKMetric
    - FBetaTopKMetric
    - MAPKMetric
    - NDCGKMetric
    - MRRKMetric
    - HitRateKMetric
    - PopularityBias
    - RecCasesTable
    - ScoreDistribution
    - PersonalizationMetric
    - DiversityMetric
    - SerendipityMetric
    - NoveltyMetric
    - ItemBiasMetric
    - UserBiasMetric
    """

    k: int
    min_rel_score: Optional[int]
    no_feedback_users: bool
    normalize_arp: bool
    user_ids: Optional[List[Union[int, str]]]
    display_features: Optional[List[str]]
    item_features: Optional[List[str]]
    user_bias_columns: Optional[List[str]]
    item_bias_columns: Optional[List[str]]

    def __init__(
        self,
        k: int,
        min_rel_score: Optional[int] = None,
        no_feedback_users: bool = False,
        normalize_arp: bool = False,
        user_ids: Optional[List[Union[int, str]]] = None,
        display_features: Optional[List[str]] = None,
        item_features: Optional[List[str]] = None,
        user_bias_columns: Optional[List[str]] = None,
        item_bias_columns: Optional[List[str]] = None,
    ):
        self.k = k
        self.min_rel_score = min_rel_score
        self.no_feedback_users = no_feedback_users
        self.normalize_arp = normalize_arp
        self.user_ids = user_ids
        self.display_features = display_features
        self.item_features = item_features
        self.user_bias_columns = user_bias_columns
        self.item_bias_columns = item_bias_columns
        super().__init__()

    def generate_metrics(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyMetric]:
        is_train_data = False
        if additional_data is not None:
            is_train_data = "current_train_data" in additional_data.keys()
        metrics: List[AnyMetric] = [
            PrecisionTopKMetric(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
            RecallTopKMetric(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
            FBetaTopKMetric(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
            MAPKMetric(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
            NDCGKMetric(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
            MRRKMetric(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
            HitRateKMetric(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
        ]
        if is_train_data:
            metrics.append(PopularityBias(k=self.k, normalize_arp=self.normalize_arp))
        metrics.append(RecCasesTable(user_ids=self.user_ids, display_features=self.display_features))
        if data_definition.recommendations_type == RecomType.SCORE:
            metrics.append(ScoreDistribution(k=self.k))
        metrics.append(PersonalizationMetric(k=self.k))
        if self.item_features is not None:
            metrics.append(DiversityMetric(k=self.k, item_features=self.item_features))
        if self.item_features is not None and is_train_data:
            metrics.append(SerendipityMetric(k=self.k, item_features=self.item_features))
        if is_train_data:
            metrics.append(NoveltyMetric(k=self.k))
        if self.item_bias_columns is not None and is_train_data:
            for col in self.item_bias_columns:
                metrics.append(ItemBiasMetric(k=self.k, column_name=col))
        if self.user_bias_columns is not None and is_train_data:
            for col in self.user_bias_columns:
                metrics.append(UserBiasMetric(column_name=col))
        return metrics
