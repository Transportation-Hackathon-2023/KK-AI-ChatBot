import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Test sentence
sentence = "The quick brown fox jumps over the lazy dog."

# Parse the sentence
doc = nlp(sentence)

# Loop through each word's text and POS tag
for token in doc:
    print(f"{token.text} -> {token.pos_}")
