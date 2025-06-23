from servequery.legacy.features import is_valid_python_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class IsValidPython(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:IsValidPython"

    def feature(self, column_name: str) -> GeneratedFeature:
        return is_valid_python_feature.IsValidPython(column_name, self.display_name)
