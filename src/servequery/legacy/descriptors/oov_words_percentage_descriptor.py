from typing import Tuple

from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature
from servequery.legacy.features.OOV_words_percentage_feature import OOVWordsPercentage


class OOV(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:OOV"

    ignore_words: Tuple = ()

    def feature(self, column_name: str) -> GeneratedFeature:
        return OOVWordsPercentage(column_name, self.ignore_words, self.display_name)
