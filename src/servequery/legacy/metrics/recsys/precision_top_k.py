from servequery.legacy.metrics.recsys.base_top_k import TopKMetric
from servequery.legacy.metrics.recsys.base_top_k import TopKMetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer


class PrecisionTopKMetric(TopKMetric):
    class Config:
        type_alias = "servequery:metric:PrecisionTopKMetric"

    def key(self):
        return "precision"


@default_renderer(wrap_type=PrecisionTopKMetric)
class PrecisionTopKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "precision@k"
    header = "Precision"
