import nltk
from nltk.tokenize import word_tokenize
import spacy
from spacy.matcher import PhraseMatcher


class small_language_processer():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")

    def filter_allowed_string(self, s):
        allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+,.?:!$% ")
        return ''.join(c for c in s if c in allowed)

    ## takes a string of set and returns interested topics/keywords
    def extract_keywords(self, text: str) -> set:
    # Removes hyphen and convert to lower
        text = self.filter_allowed_string(text)
        doc = self.nlp(text)

        keywords = set()
        unwanted = set()

        for ent in doc.ents:
                if ent.label_ in {"EVENT", "FAC", "GPE", "LANGUAGE", "LAW", "LOC", "NORP", "ORG", "PERSON", "PRODUCT", "WORK_OF_ART"}:
                    keywords.add(ent.text)
                else:
                    unwanted.add(ent.text)

        def is_single_symbol(keyword):
            return len(keyword) == 1 and not keyword.isalnum()


        for chunk in doc.noun_chunks:

            clean_chunk = []

            if chunk in unwanted:
                continue

            for token in chunk:
                if token.pos_ == 'PRON':
                    break

                if token.pos_ in {'ADJ', 'NOUN', 'PROPN'}:
                    clean_chunk.append(token.text)

            if len(clean_chunk) > 2 or len(clean_chunk) == 0:
                continue
            else:
                keyword = ' '.join(clean_chunk)
                if not is_single_symbol(keyword):
                    keywords.add(keyword)

        return keywords
