# ruff: noqa: E501
# fmt: off
from servequery.core.datasets import Descriptor
from servequery.pydantic_utils import register_type_alias

register_type_alias(Descriptor, "servequery.core.datasets.FeatureDescriptor", "servequery:descriptor_v2:FeatureDescriptor")
register_type_alias(Descriptor, "servequery.descriptors._context_relevance.ContextRelevance", "servequery:descriptor_v2:ContextRelevance")
register_type_alias(Descriptor, "servequery.descriptors._custom_descriptors.CustomColumnDescriptor", "servequery:descriptor_v2:CustomColumnDescriptor")
register_type_alias(Descriptor, "servequery.descriptors._custom_descriptors.CustomDescriptor", "servequery:descriptor_v2:CustomDescriptor")
register_type_alias(Descriptor, "servequery.descriptors._text_length.TextLength", "servequery:descriptor_v2:TextLength")

register_type_alias(Descriptor, "servequery.core.datasets.ColumnTest", "servequery:descriptor_v2:ColumnTest")
register_type_alias(Descriptor, "servequery.core.datasets.SingleInputDescriptor", "servequery:descriptor_v2:SingleInputDescriptor")
register_type_alias(Descriptor, "servequery.core.datasets.TestSummary", "servequery:descriptor_v2:TestSummary")

register_type_alias(Descriptor, "servequery.descriptors.llm_judges.GenericLLMDescriptor", "servequery:descriptor_v2:GenericLLMDescriptor")
