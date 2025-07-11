import json
from inspect import isabstract
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import pandas as pd
import pytest

from servequery import ColumnType
from servequery._pydantic_compat import parse_obj_as
from servequery.core.datasets import ColumnTest
from servequery.core.datasets import Dataset
from servequery.core.datasets import DatasetColumn
from servequery.core.datasets import Descriptor
from servequery.core.datasets import FeatureDescriptor
from servequery.core.datasets import TestSummary
from servequery.descriptors import ContextRelevance
from servequery.descriptors import CustomColumnDescriptor
from servequery.descriptors import CustomDescriptor
from servequery.descriptors import TextLength
from servequery.descriptors.llm_judges import GenericLLMDescriptor
from servequery.legacy.options.base import Options
from servequery.legacy.utils.llm.base import LLMMessage
from servequery.legacy.utils.llm.wrapper import LLMResult
from servequery.legacy.utils.llm.wrapper import LLMWrapper
from servequery.legacy.utils.llm.wrapper import llm_provider
from servequery.tests import eq
from tests.conftest import load_all_subtypes

from .test_feature_descriptors import MockGeneratedFeature

int_data = pd.Series([1, 2, 3], name="int")
str_data = pd.Series(["a", "b", "c"], name="str")


@llm_provider("mock_d", None)
class MockLLMWrapper(LLMWrapper):
    def __init__(self, model: str, options: Options):
        self.model = model

    async def complete(self, messages: List[LLMMessage]) -> LLMResult[str]:
        return LLMResult("\n".join(m.content for m in messages), 0, 0)


def custom_descr(dataset: Dataset) -> DatasetColumn:
    return DatasetColumn(ColumnType.Numerical, pd.Series([1] * len(dataset.as_dataframe())))


def custom_col_descr(col: DatasetColumn) -> DatasetColumn:
    return DatasetColumn(ColumnType.Numerical, col.data)


@pytest.fixture(autouse=True)
def mock_semantic_scoring(mocker):
    from servequery.descriptors._context_relevance import MeanAggregation
    from servequery.descriptors._context_relevance import semantic_similarity_scoring as sss

    def semantic_scoring_mock(question: DatasetColumn, context: DatasetColumn, options) -> DatasetColumn:
        return DatasetColumn(ColumnType.Numerical, pd.Series([1] * len(question.data)))

    mocker.patch(f"{sss.__module__}.{sss.__name__}", new=semantic_scoring_mock)
    mocker.patch(
        f"{sss.__module__}.METHODS",
        new={
            "semantic_similarity": (semantic_scoring_mock, MeanAggregation),
        },
    )


all_descriptors: List[Tuple[Descriptor, Union[pd.Series, pd.DataFrame], Dict[str, pd.Series]]] = [
    (
        FeatureDescriptor(feature=MockGeneratedFeature(column="str", field="a"), alias="res"),
        str_data,
        {"a1702de9f83a993ea3cb4701ca9d17f7.str": pd.Series(["aa", "ba", "ca"])},
    ),
    (TextLength(column_name="str", alias="res"), str_data, {"res": pd.Series([1, 1, 1])}),
    (CustomColumnDescriptor(column_name="int", func=custom_col_descr, alias="res"), int_data, {"res": int_data}),
    (CustomDescriptor(func=custom_descr, alias="res"), int_data, {"res": pd.Series([1, 1, 1])}),
    (TestSummary(alias="res"), int_data, {"res": pd.Series([1, 0, 0])}),
    (
        ContextRelevance(alias="res", input="i", contexts="c"),
        pd.DataFrame({"i": ["input"], "c": ["context"]}),
        {"res": pd.Series([1])},
    ),
    (
        GenericLLMDescriptor(
            alias="res",
            provider="mock_d",
            model="",
            input_columns={"aaa": "data"},
            prompt=[{"role": "system", "content": "a"}, {"role": "user", "content": "{data}"}],
        ),
        pd.DataFrame({"aaa": ["x", "y"]}),
        {"res": pd.Series(["a\nx", "a\ny"])},
    ),
]


def test_descriptors_tested():
    tested_desc_set = {type(p) for p, _, _ in all_descriptors}
    load_all_subtypes(Descriptor)
    all_desc_types = set(s for s in Descriptor.__subclasses__() if not isabstract(s))
    assert tested_desc_set == all_desc_types, "Missing tests for descriptors " + ", ".join(
        f'({t.__name__}(alias="res"), pd.Series(), {{"res":pd.Series()}})' for t in all_desc_types - tested_desc_set
    )


@pytest.mark.parametrize("descriptor,data,result", all_descriptors)
def test_descriptors(descriptor: Descriptor, data: Union[pd.Series, pd.DataFrame], result: Dict[str, pd.Series]):
    df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
    dataset = Dataset.from_pandas(df)
    if isinstance(descriptor, TestSummary):
        dataset.add_descriptor(ColumnTest(str(df.columns[0]), eq(1)))
    dataset.add_descriptor(descriptor)

    res_df = dataset.as_dataframe()
    for col, value in result.items():
        assert col in set(res_df.columns), f"no column {col}, cols: {res_df.columns}"
        assert res_df[col].tolist() == value.tolist()

    payload = json.loads(descriptor.json())
    descriptor2 = parse_obj_as(Descriptor, payload)
    assert descriptor2 == descriptor
