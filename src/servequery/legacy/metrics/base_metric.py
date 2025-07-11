from typing import Dict
from typing import Optional
from typing import Type
from typing import Union

from servequery.legacy.base_metric import Metric
from servequery.legacy.utils.generators import BaseGenerator
from servequery.legacy.utils.generators import make_generator_by_columns


def generate_column_metrics(
    metric_class: Type[Metric],
    columns: Optional[Union[str, list]] = None,
    parameters: Optional[Dict] = None,
    skip_id_column: bool = False,
) -> BaseGenerator[Metric]:
    """Function for generating metrics for columns"""
    return make_generator_by_columns(
        base_class=metric_class,
        columns=columns,
        parameters=parameters,
        skip_id_column=skip_id_column,
    )
