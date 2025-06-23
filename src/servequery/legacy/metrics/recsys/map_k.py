from servequery.legacy.metrics.recsys.base_top_k import TopKMetric
from servequery.legacy.metrics.recsys.base_top_k import TopKMetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer


class MAPKMetric(TopKMetric):
    class Config:
        type_alias = "servequery:metric:MAPKMetric"

    def key(self):
        return "map"


@default_renderer(wrap_type=MAPKMetric)
class MAPKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "map@k"
    header = "MAP"
