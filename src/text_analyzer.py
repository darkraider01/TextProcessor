import nltk
import spacy
from textblob import TextBlob
from langdetect import detect
from nltk.tokenize import word_tokenize
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
import logging

class TextAnalyzer:
    def __init__(self, filter_file=None):
        # Initialize NLP models
        self.nlp = spacy.load('en_core_web_sm')
        self.text = ""
        self.processed_text = ""
        self.filter_words = self._load_filter_words(filter_file) if filter_file else set()

    def _load_filter_words(self, filter_file):
        """Load filter words from a text file."""
        filter_words = set()
        try:
            with open(filter_file, 'r', encoding='utf-8') as file:
                for line in file:
                    filter_words.add(line.strip().lower())  # Add each word to the set
        except Exception as e:
            logging.error(f"Error loading filter words from {filter_file}: {e}")
        return filter_words

    def load_text(self, text):
        """Load text for processing."""
        self.text = text
        self.processed_text = self.text.lower()

    def sentence_splitting(self):
        """Split text into sentences."""
        sentences = nltk.sent_tokenize(self.processed_text)
        return [s.lower() for s in sentences]

    def word_tokenization(self):
        """Tokenize text into words."""
        tokens = word_tokenize(self.processed_text)
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

    def score_text(self):
        """Calculate a score based on filtered words and sentiment analysis."""
        tokens = self.word_tokenization()
        filtered_tokens = [t for t in tokens if t in self.filter_words]
        num_filtered_tokens = len(filtered_tokens)

        # Calculate vulnerability score (scale of 10)
        vulnerability_score = min(10, (num_filtered_tokens / len(tokens)) * 10) if tokens else 0

        # Perform sentiment analysis on the filtered tokens
        if filtered_tokens:
            filtered_text = ' '.join(filtered_tokens)
            sentiment = TextBlob(filtered_text).sentiment.polarity
            # Sentiment score on a scale of 1-10
            sentiment_score = round((sentiment + 1) * 4.5)  # -1 maps to 1, 1 maps to 10
        else:
            sentiment_score = 0

        # Combined score (average of vulnerability and sentiment score)
        combined_score = (vulnerability_score + sentiment_score) / 2
        return round(min(10, combined_score), 2)
