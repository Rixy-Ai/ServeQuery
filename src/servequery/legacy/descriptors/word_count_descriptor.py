from servequery.legacy.features import word_count_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class WordCount(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:WordCount"

    def feature(self, column_name: str) -> GeneratedFeature:
        return word_count_feature.WordCount(column_name, self.display_name)
