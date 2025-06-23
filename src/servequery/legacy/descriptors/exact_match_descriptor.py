from servequery.legacy.features.exact_match_feature import ExactMatchFeature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeatures


class ExactMatch(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:ExactMatch"

    with_column: str

    def feature(self, column_name: str) -> GeneratedFeatures:
        return ExactMatchFeature(columns=[column_name, self.with_column], display_name=self.display_name)
