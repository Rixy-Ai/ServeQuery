from servequery.legacy.features import sentence_count_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class SentenceCount(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:SentenceCount"

    def feature(self, column_name: str) -> GeneratedFeature:
        return sentence_count_feature.SentenceCount(column_name, self.display_name)
