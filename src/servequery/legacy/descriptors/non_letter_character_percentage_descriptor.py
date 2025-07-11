from servequery.legacy.features import non_letter_character_percentage_feature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class NonLetterCharacterPercentage(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:NonLetterCharacterPercentage"

    def feature(self, column_name: str) -> GeneratedFeature:
        return non_letter_character_percentage_feature.NonLetterCharacterPercentage(column_name, self.display_name)
