from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from servequery.legacy.metric_preset.metric_preset import AnyMetric
from servequery.legacy.metric_preset.metric_preset import MetricPreset
from servequery.legacy.metrics import RegressionAbsPercentageErrorPlot
from servequery.legacy.metrics import RegressionErrorBiasTable
from servequery.legacy.metrics import RegressionErrorDistribution
from servequery.legacy.metrics import RegressionErrorNormality
from servequery.legacy.metrics import RegressionErrorPlot
from servequery.legacy.metrics import RegressionPredictedVsActualPlot
from servequery.legacy.metrics import RegressionPredictedVsActualScatter
from servequery.legacy.metrics import RegressionQualityMetric
from servequery.legacy.metrics import RegressionTopErrorMetric
from servequery.legacy.utils.data_preprocessing import DataDefinition


class RegressionPreset(MetricPreset):
    class Config:
        type_alias = "servequery:metric_preset:RegressionPreset"

    """Metric preset for Regression performance analysis.

    Contains metrics:
    - RegressionQualityMetric
    - RegressionPredictedVsActualScatter
    - RegressionPredictedVsActualPlot
    - RegressionErrorPlot
    - RegressionAbsPercentageErrorPlot
    - RegressionErrorDistribution
    - RegressionErrorNormality
    - RegressionTopErrorMetric
    - RegressionErrorBiasTable
    """

    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        self.columns = columns
        super().__init__()

    def generate_metrics(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyMetric]:
        return [
            RegressionQualityMetric(),
            RegressionPredictedVsActualScatter(),
            RegressionPredictedVsActualPlot(),
            RegressionErrorPlot(),
            RegressionAbsPercentageErrorPlot(),
            RegressionErrorDistribution(),
            RegressionErrorNormality(),
            RegressionTopErrorMetric(),
            RegressionErrorBiasTable(columns=self.columns),
        ]
