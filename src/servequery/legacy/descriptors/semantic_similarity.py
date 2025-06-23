from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeatures
from servequery.legacy.features.semantic_similarity_feature import SemanticSimilarityFeature


class SemanticSimilarity(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:SemanticSimilarity"

    with_column: str

    def feature(self, column_name: str) -> GeneratedFeatures:
        return SemanticSimilarityFeature(columns=[column_name, self.with_column], display_name=self.display_name)
