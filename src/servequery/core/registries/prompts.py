from servequery.llm.prompts.content import PromptContent
from servequery.pydantic_utils import register_type_alias

register_type_alias(
    PromptContent,
    "servequery.llm.prompts.content.MessagesPromptContent",
    "servequery:prompt_content:MessagesPromptContent",
)
register_type_alias(
    PromptContent, "servequery.llm.prompts.content.TextPromptContent", "servequery:prompt_content:TextPromptContent"
)
