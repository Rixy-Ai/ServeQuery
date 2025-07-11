from typing import Dict
from typing import Optional

from sklearn.metrics import classification_report

from servequery._pydantic_compat import Field
from servequery._pydantic_compat import parse_obj_as
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.metric_results import Label


class ClassMetric(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ClassMetric"

    precision: float
    recall: float
    f1: float
    roc_auc: Optional[float] = None
    support: Optional[float] = None


ClassesMetrics = Dict[Label, ClassMetric]


class ClassificationReport(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ClassificationReport"
        smart_union = True

    classes: ClassesMetrics
    accuracy: float
    macro_avg: ClassMetric = Field(alias="macro avg")
    weighted_avg: ClassMetric = Field(alias="weighted avg")

    @classmethod
    def create(
        cls,
        y_true,
        y_pred,
        *,
        class_metrics=None,
        target_names=None,
        sample_weight=None,
        digits=2,
        zero_division="warn",
    ) -> "ClassificationReport":
        classes = set(c for c in y_true.unique())
        report = classification_report(
            y_true,
            y_pred,
            labels=class_metrics,
            target_names=target_names,
            sample_weight=sample_weight,
            digits=digits,
            output_dict=True,
            zero_division=zero_division,
        )
        for v in report.values():
            if not isinstance(v, dict):
                continue
            v["f1"] = v.pop("f1-score")
        class_metrics = {str(k): parse_obj_as(ClassMetric, report[str(k)]) for k in classes}
        other = {str(k): v for k, v in report.items() if k not in [str(cl) for cl in classes]}
        return parse_obj_as(cls, {"classes": class_metrics, **other})
