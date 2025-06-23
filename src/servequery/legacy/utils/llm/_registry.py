# ruff: noqa: E501
# fmt: off
from servequery.legacy.utils.llm.prompts import PromptBlock
from servequery.legacy.utils.llm.prompts import PromptTemplate
from servequery.pydantic_utils import register_type_alias

register_type_alias(PromptBlock, "servequery.legacy.utils.llm.prompts.Anchor", "servequery:prompt_block:Anchor")
register_type_alias(PromptBlock, "servequery.legacy.utils.llm.prompts.JsonOutputFormatBlock", "servequery:prompt_block:JsonOutputFormatBlock")
register_type_alias(PromptBlock, "servequery.legacy.utils.llm.prompts.NoopOutputFormat", "servequery:prompt_block:NoopOutputFormat")
register_type_alias(PromptBlock, "servequery.legacy.utils.llm.prompts.SimpleBlock", "servequery:prompt_block:SimpleBlock")
register_type_alias(PromptBlock, "servequery.legacy.utils.llm.prompts.StringFormatBlock", "servequery:prompt_block:StringFormatBlock")
register_type_alias(PromptBlock, "servequery.legacy.utils.llm.prompts.StringListFormatBlock", "servequery:prompt_block:StringListFormatBlock")
register_type_alias(PromptTemplate, "servequery.legacy.utils.llm.prompts.BlockPromptTemplate", "servequery:prompt_template:BlockPromptTemplate")
