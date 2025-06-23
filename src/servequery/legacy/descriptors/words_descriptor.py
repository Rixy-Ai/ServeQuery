from typing import List

from servequery.legacy.features import words_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class ExcludesWords(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:ExcludesWords"

    words_list: List[str]
    mode: str = "all"
    lemmatize: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return words_feature.ExcludesWords(
            column_name,
            self.words_list,
            self.mode,
            self.lemmatize,
            self.display_name,
        )


class IncludesWords(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:IncludesWords"

    words_list: List[str]
    mode: str = "any"
    lemmatize: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return words_feature.IncludesWords(
            column_name,
            self.words_list,
            self.mode,
            self.lemmatize,
            self.display_name,
        )


class WordMatch(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:WordMatch"

    with_column: str
    mode: str = "any"
    lemmatize: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return words_feature.WordMatch(
            columns=[column_name, self.with_column],
            mode=self.mode,
            lemmatize=self.lemmatize,
            display_name=self.display_name,
        )


class WordNoMatch(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:WordNoMatch"

    with_column: str
    mode: str = "any"
    lemmatize: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return words_feature.WordNoMatch(
            columns=[column_name, self.with_column],
            mode=self.mode,
            lemmatize=self.lemmatize,
            display_name=self.display_name,
        )
