

import nltk
import spacy
from textblob import TextBlob
from langdetect import detect
from nltk.tokenize import word_tokenize
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures

class TextAnalyzer:
    def __init__(self):
        # Initialize NLP models
        self.nlp = spacy.load('en_core_web_sm')
        self.text = ""
        self.processed_text = ""

    def load_text(self, text):
        """Load text for processing."""
        self.text = text
        self.processed_text = self.text.lower()

    def sentence_splitting(self):
        """Split text into sentences."""
        sentences = nltk.sent_tokenize(self.processed_text)
        # Ensure the sentences are in lowercase to match the test expectations
        return [s.lower() for s in sentences]

    def word_tokenization(self):
        """Tokenize text into words."""
        tokens = word_tokenize(self.processed_text)
        # Ensure the tokens are in lowercase to match the test expectations
        return [t.lower() for t in tokens]

    def pos_tagging(self):
        """Tag parts of speech in the text."""
        tokens = self.word_tokenization()
        return nltk.pos_tag(tokens)

    def bigram_analysis(self):
        """Analyze bigrams in the text."""
        tokens = self.word_tokenization()
        bigram_finder = BigramCollocationFinder.from_words(tokens)
        return bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 10)

    def trigram_analysis(self):
        """Analyze trigrams in the text."""
        tokens = self.word_tokenization()
        trigram_finder = TrigramCollocationFinder.from_words(tokens)
        return trigram_finder.nbest(TrigramAssocMeasures.likelihood_ratio, 10)

    def collocations(self):
        """Identify word collocations."""
        tokens = self.word_tokenization()
        bigram_finder = BigramCollocationFinder.from_words(tokens)
        return bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 10)

    def concordance(self, word):
        """Find occurrences of a word within its context."""
        text = nltk.Text(self.word_tokenization())
        return text.concordance(word)


    def sentiment_analysis(self):
        """Analyze the sentiment of the text."""
        blob = TextBlob(self.processed_text)
        return blob.sentiment

    def language_detection(self):
        """Detect the language of the text."""
        return detect(self.processed_text)


    

   