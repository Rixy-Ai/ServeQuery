from servequery.legacy.features import text_part_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class BeginsWith(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:BeginsWith"

    prefix: str
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_part_feature.BeginsWith(
            column_name,
            self.prefix,
            self.case_sensitive,
            self.display_name,
        )


class EndsWith(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:EndsWith"

    suffix: str
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_part_feature.EndsWith(
            column_name,
            self.suffix,
            self.case_sensitive,
            self.display_name,
        )
