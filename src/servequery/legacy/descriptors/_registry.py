from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneralDescriptor
from servequery.pydantic_utils import register_type_alias

register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.custom_descriptor.CustomColumnEval",
    "servequery:descriptor:CustomColumnEval",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.hf_descriptor.HuggingFaceModel",
    "servequery:descriptor:HuggingFaceModel",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.hf_descriptor.HuggingFaceToxicityModel",
    "servequery:descriptor:HuggingFaceToxicityModel",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.is_valid_python_descriptor.IsValidPython",
    "servequery:descriptor:IsValidPython",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.json_schema_match_descriptor.JSONSchemaMatch",
    "servequery:descriptor:JSONSchemaMatch",
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.llm_judges.BiasLLMEval", "servequery:descriptor:BiasLLMEval"
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.llm_judges.BinaryClassificationLLMEval",
    "servequery:descriptor:BinaryClassificationLLMEval",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.llm_judges.ContextQualityLLMEval",
    "servequery:descriptor:ContextQualityLLMEval",
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.llm_judges.DeclineLLMEval", "servequery:descriptor:DeclineLLMEval"
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.llm_judges.LLMEval", "servequery:descriptor:LLMEval"
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.llm_judges.NegativityLLMEval",
    "servequery:descriptor:NegativityLLMEval",
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.llm_judges.PIILLMEval", "servequery:descriptor:PIILLMEval"
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.llm_judges.ToxicityLLMEval", "servequery:descriptor:ToxicityLLMEval"
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.llm_judges.CorrectnessLLMEval",
    "servequery:descriptor:CorrectnessLLMEval",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.llm_judges.FaithfulnessLLMEval",
    "servequery:descriptor:FaithfulnessLLMEval",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.llm_judges.CompletenessLLMEval",
    "servequery:descriptor:CompletenessLLMEval",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.non_letter_character_percentage_descriptor.NonLetterCharacterPercentage",
    "servequery:descriptor:NonLetterCharacterPercentage",
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.oov_words_percentage_descriptor.OOV", "servequery:descriptor:OOV"
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.openai_descriptor.OpenAIPrompting",
    "servequery:descriptor:OpenAIPrompting",
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.regexp_descriptor.RegExp", "servequery:descriptor:RegExp"
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.semantic_similarity.SemanticSimilarity",
    "servequery:descriptor:SemanticSimilarity",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.BERTScore_descriptor.BERTScore",
    "servequery:descriptor:BERTScore",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.sentence_count_descriptor.SentenceCount",
    "servequery:descriptor:SentenceCount",
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.sentiment_descriptor.Sentiment", "servequery:descriptor:Sentiment"
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.text_contains_descriptor.Contains", "servequery:descriptor:Contains"
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.text_contains_descriptor.DoesNotContain",
    "servequery:descriptor:DoesNotContain",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.text_contains_descriptor.ItemMatch",
    "servequery:descriptor:ItemMatch",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.text_contains_descriptor.ItemNoMatch",
    "servequery:descriptor:ItemNoMatch",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.text_length_descriptor.TextLength",
    "servequery:descriptor:TextLength",
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.text_part_descriptor.BeginsWith", "servequery:descriptor:BeginsWith"
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.text_part_descriptor.EndsWith", "servequery:descriptor:EndsWith"
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.trigger_words_presence_descriptor.TriggerWordsPresence",
    "servequery:descriptor:TriggerWordsPresence",
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.word_count_descriptor.WordCount", "servequery:descriptor:WordCount"
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.words_descriptor.ExcludesWords",
    "servequery:descriptor:ExcludesWords",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.words_descriptor.IncludesWords",
    "servequery:descriptor:IncludesWords",
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.words_descriptor.WordMatch", "servequery:descriptor:WordMatch"
)
register_type_alias(
    FeatureDescriptor, "servequery.legacy.descriptors.words_descriptor.WordNoMatch", "servequery:descriptor:WordNoMatch"
)
register_type_alias(
    GeneralDescriptor,
    "servequery.legacy.descriptors.custom_descriptor.CustomPairColumnEval",
    "servequery:descriptor:CustomPairColumnEval",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.is_valid_sql_descriptor.IsValidSQL",
    "servequery:descriptor:IsValidSQL",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.json_match_descriptor.JSONMatch",
    "servequery:descriptor:JSONMatch",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.contains_link_descriptor.ContainsLink",
    "servequery:descriptor:ContainsLink",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.exact_match_descriptor.ExactMatch",
    "servequery:descriptor:ExactMatch",
)
register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.is_valid_json_descriptor.IsValidJSON",
    "servequery:descriptor:IsValidJSON",
)

register_type_alias(
    FeatureDescriptor,
    "servequery.legacy.descriptors.llm_judges.MulticlassClassificationLLMEval",
    "servequery:descriptor:MulticlassClassificationLLMEval",
)
