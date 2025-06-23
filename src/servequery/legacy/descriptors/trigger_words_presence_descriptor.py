from typing import List

from servequery.legacy.features import trigger_words_presence_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class TriggerWordsPresence(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:TriggerWordsPresence"

    words_list: List[str]
    lemmatize: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return trigger_words_presence_feature.TriggerWordsPresent(
            column_name,
            self.words_list,
            self.lemmatize,
            self.display_name,
        )
