from servequery.legacy.features import is_valid_sql_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class IsValidSQL(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:IsValidSQL"

    def feature(self, column_name: str) -> GeneratedFeature:
        return is_valid_sql_feature.IsValidSQL(column_name, self.display_name)
