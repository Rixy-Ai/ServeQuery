from servequery.legacy.metrics.recsys.base_top_k import TopKMetric
from servequery.legacy.metrics.recsys.base_top_k import TopKMetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer


class MARKMetric(TopKMetric):
    class Config:
        type_alias = "servequery:metric:MARKMetric"

    def key(self):
        return "mar"


@default_renderer(wrap_type=MARKMetric)
class MARKMetricRenderer(TopKMetricRenderer):
    yaxis_name = "mar@k"
    header = "MAR"
