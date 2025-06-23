# ruff: noqa: E501
# fmt: off
from servequery.core.datasets import ColumnCondition
from servequery.pydantic_utils import register_type_alias

register_type_alias(ColumnCondition, "servequery.tests.descriptors.EqualsColumnCondition", "servequery:column_condition:EqualsColumnCondition")
register_type_alias(ColumnCondition, "servequery.tests.descriptors.GreaterColumnCondition", "servequery:column_condition:GreaterColumnCondition")
register_type_alias(ColumnCondition, "servequery.tests.descriptors.GreaterEqualColumnCondition", "servequery:column_condition:GreaterEqualColumnCondition")
register_type_alias(ColumnCondition, "servequery.tests.descriptors.IsInColumnCondition", "servequery:column_condition:IsInColumnCondition")
register_type_alias(ColumnCondition, "servequery.tests.descriptors.IsNotInColumnCondition", "servequery:column_condition:IsNotInColumnCondition")
register_type_alias(ColumnCondition, "servequery.tests.descriptors.LessColumnCondition", "servequery:column_condition:LessColumnCondition")
register_type_alias(ColumnCondition, "servequery.tests.descriptors.LessEqualColumnCondition", "servequery:column_condition:LessEqualColumnCondition")
register_type_alias(ColumnCondition, "servequery.tests.descriptors.NotEqualsColumnCondition", "servequery:column_condition:NotEqualsColumnCondition")
