from servequery.legacy.features import contains_link_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class ContainsLink(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:ContainsLink"

    def feature(self, column_name: str) -> GeneratedFeature:
        return contains_link_feature.ContainsLink(column_name, self.display_name)
