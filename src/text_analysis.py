from text_analyzer import TextAnalyzer

class TextAnalysis:
    def __init__(self, filter_file=None):
        self.analyzer = TextAnalyzer(filter_file)
        self.filter_words = self.analyzer.filter_words  # Use filter words loaded in TextAnalyzer

    def calculate_text_score(self, filtered_tokens, sentiment_score):
        """Calculate a score based on the occurrence of filtered words and their sentiment."""
        if not filtered_tokens:
            return 0

        # Calculate average sentiment of filtered tokens
        average_sentiment = sentiment_score / len(filtered_tokens) if filtered_tokens else 0
        
        # Calculate text score
        text_score = min(10, (len(filtered_tokens) * average_sentiment) * 10)  # Scale to 1-10
        
        return round(text_score, 2)

    def analyze_text(self, text):
        """Perform comprehensive text analysis and return results."""
        self.analyzer.load_text(text)

        tokens = self.analyzer.word_tokenization()
        filtered_tokens = [t for t in tokens if t in self.filter_words]
        num_filtered_tokens = len(filtered_tokens)

        # Calculate sentiment of filtered tokens
        filtered_text = ' '.join(filtered_tokens)
        sentiment = self.analyzer.sentiment_analysis()
        sentiment_score = sentiment.polarity

        # Calculate vulnerability score (scale of 10)
        vulnerability_score = min(10, (num_filtered_tokens / len(tokens)) * 10) if tokens else 0

        # Calculate text score
        text_score = self.calculate_text_score(filtered_tokens, sentiment_score)

        results = {
            'Sentences': len(self.analyzer.sentence_splitting()),
            'Word Tokens': len(tokens),
            'Filtered Tokens': num_filtered_tokens,
            'Vulnerability Score': round(vulnerability_score, 2),
            'POS Tags': self.analyzer.pos_tagging()[:5],  # Show first 5 POS tags
            'Sentiment': {
                'Polarity': sentiment.polarity,
                'Subjectivity': sentiment.subjectivity
            },
            'Language': self.analyzer.language_detection(),
            'Text Score': text_score  # Add text score based on filtered words
        }

        return results
