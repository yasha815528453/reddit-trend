import nltk
from nltk.tokenize import word_tokenize
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")


class small_language_processer():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    ## takes a string of set and returns interested topics/keywords
    def extract_keywords(self, text: str) -> set:
    # Removes hyphen and convert to lower
        text = text.replace("-", " ").lower()
        doc = nlp(text)

        keywords = set()

        def is_single_symbol(keyword):
            return len(keyword) == 1 and not keyword.isalnum()


        def contains_number(s):
            return any(char.isdigit() for char in s)




        # Extract named entities, excluding specific types and those containing numbers or emojis
        for ent in doc.ents:
            if ent.label_ not in {"MONEY", "DATE", "TIME", "QUANTITY"} and not contains_number(ent.text):
                keywords.add(ent.text)

        for chunk in doc.noun_chunks:
            if not any(token.pos_ in {'PRON', 'ADJ', 'INTJ', 'AUX', 'ADV', 'ADP'} or token.is_stop for token in chunk) and not any(token.is_punct or "-" in token.text for token in chunk) and not contains_number(chunk.text):
                # Simplify chunks to the last two words if longer than two words
                words = chunk.text.split()
                simplified_chunk = ' '.join(words[-2:]) if len(words) > 2 else chunk.text
                keywords.add(simplified_chunk)

        # Extract additional nouns, excluding those that are part of noun chunks/entities, or contain numbers or emojis
        for token in doc:
            if token.pos_ == 'NOUN' and not token.is_punct and token.dep_ != "compound" and not contains_number(token.text) and not is_single_symbol(token.text):
                is_part_of_chunk_or_entity = any(token.text in keyword for keyword in keywords)
                if not is_part_of_chunk_or_entity:
                    keywords.add(token.text)

        return keywords
