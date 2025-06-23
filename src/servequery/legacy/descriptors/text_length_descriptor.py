from servequery.legacy.features import text_length_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class TextLength(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:TextLength"

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_length_feature.TextLength(column_name, self.display_name)
