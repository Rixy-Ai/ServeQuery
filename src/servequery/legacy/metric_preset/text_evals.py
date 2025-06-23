from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from servequery.legacy.descriptors import OOV
from servequery.legacy.descriptors import NonLetterCharacterPercentage
from servequery.legacy.descriptors import SentenceCount
from servequery.legacy.descriptors import Sentiment
from servequery.legacy.descriptors import TextLength
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.metric_preset.metric_preset import AnyMetric
from servequery.legacy.metric_preset.metric_preset import MetricPreset
from servequery.legacy.metrics import ColumnSummaryMetric
from servequery.legacy.utils.data_preprocessing import DataDefinition


class TextEvals(MetricPreset):
    class Config:
        type_alias = "servequery:metric_preset:TextEvals"

    column_name: str
    descriptors: Optional[List[FeatureDescriptor]] = None

    def __init__(self, column_name: str, descriptors: Optional[List[FeatureDescriptor]] = None):
        self.column_name: str = column_name
        self.descriptors: Optional[List[FeatureDescriptor]] = descriptors
        super().__init__()

    def generate_metrics(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyMetric]:
        descriptors = self.descriptors or [
            TextLength(),
            SentenceCount(),
            Sentiment(),
            OOV(),
            NonLetterCharacterPercentage(),
        ]
        return [ColumnSummaryMetric(desc.on(self.column_name)) for desc in descriptors]
