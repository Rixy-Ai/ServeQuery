from servequery.legacy.metrics.recsys.base_top_k import TopKMetric
from servequery.legacy.metrics.recsys.base_top_k import TopKMetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer


class RecallTopKMetric(TopKMetric):
    class Config:
        type_alias = "servequery:metric:RecallTopKMetric"

    def key(self):
        return "recall"


@default_renderer(wrap_type=RecallTopKMetric)
class RecallTopKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "recall@k"
    header = "Recall"
