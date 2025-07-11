from typing import List

from servequery.legacy.features import text_contains_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class Contains(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:Contains"

    items: List[str]
    mode: str = "any"
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_contains_feature.Contains(
            column_name,
            self.items,
            self.case_sensitive,
            self.mode,
            self.display_name,
        )


class DoesNotContain(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:DoesNotContain"

    items: List[str]
    mode: str = "all"
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_contains_feature.DoesNotContain(
            column_name,
            self.items,
            self.case_sensitive,
            self.mode,
            self.display_name,
        )


class ItemMatch(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:ItemMatch"

    with_column: str
    mode: str = "any"
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_contains_feature.ItemMatch(
            columns=[column_name, self.with_column],
            case_sensitive=self.case_sensitive,
            mode=self.mode,
            display_name=self.display_name,
        )


class ItemNoMatch(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:ItemNoMatch"

    with_column: str
    mode: str = "any"
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_contains_feature.ItemNoMatch(
            columns=[column_name, self.with_column],
            case_sensitive=self.case_sensitive,
            mode=self.mode,
            display_name=self.display_name,
        )
