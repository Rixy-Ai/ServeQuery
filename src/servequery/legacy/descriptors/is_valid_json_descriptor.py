from servequery.legacy.features import is_valid_json_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class IsValidJSON(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:IsValidJSON"

    def feature(self, column_name: str) -> GeneratedFeature:
        return is_valid_json_feature.IsValidJSON(column_name, self.display_name)
