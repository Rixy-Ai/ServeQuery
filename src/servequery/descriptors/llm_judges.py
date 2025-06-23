from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from servequery import ColumnType
from servequery import Dataset
from servequery._pydantic_compat import PrivateAttr
from servequery.core.datasets import AnyDescriptorTest
from servequery.core.datasets import DatasetColumn
from servequery.core.datasets import Descriptor
from servequery.legacy.base_metric import DisplayName
from servequery.legacy.options.base import Options
from servequery.legacy.utils.llm.wrapper import LLMMessage as LegacyLLMMessage
from servequery.legacy.utils.llm.wrapper import LLMRequest
from servequery.legacy.utils.llm.wrapper import LLMWrapper
from servequery.legacy.utils.llm.wrapper import get_llm_wrapper
from servequery.llm.models import LLMMessage
from servequery.llm.prompts.content import MessagesPromptContent
from servequery.llm.prompts.content import PromptContent
from servequery.llm.templates import *  # noqa: F403


class GenericLLMDescriptor(Descriptor):
    input_columns: Dict[str, str]
    provider: str
    model: str
    prompt: PromptContent

    _llm_wrapper: Optional[LLMWrapper] = PrivateAttr(None)

    def __init__(
        self,
        provider: str,
        model: str,
        input_columns: Dict[str, str],
        prompt: Union[List[LLMMessage], PromptContent],
        alias: str,
        tests: Optional[List[AnyDescriptorTest]] = None,
        **data: Any,
    ):
        self.prompt = MessagesPromptContent(messages=prompt) if isinstance(prompt, list) else prompt
        self.input_columns = input_columns
        self.model = model
        self.provider = provider
        super().__init__(alias, tests, **data)

    def get_llm_wrapper(self, options: Options) -> LLMWrapper:
        if self._llm_wrapper is None:
            self._llm_wrapper = get_llm_wrapper(self.provider, self.model, options)
        return self._llm_wrapper

    def _fmt_messages(self, values: Dict[str, Any]) -> List[LegacyLLMMessage]:
        return [LegacyLLMMessage(m.role, m.content.format(**values)) for m in self.prompt.as_messages()]

    def iterate_messages(self, dataset: Dataset) -> Iterator[LLMRequest[str]]:
        for _, column_values in (
            dataset.as_dataframe()[list(self.input_columns)].rename(columns=self.input_columns).iterrows()
        ):
            yield LLMRequest(
                messages=self._fmt_messages(column_values.to_dict()), response_parser=lambda x: x, response_type=str
            )

    def generate_data(
        self, dataset: "Dataset", options: Options
    ) -> Union[DatasetColumn, Dict[DisplayName, DatasetColumn]]:
        result = self.get_llm_wrapper(options).run_batch_sync(requests=self.iterate_messages(dataset))

        return DatasetColumn(ColumnType.Text, pd.Series(result))
