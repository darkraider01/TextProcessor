from src.text_analyzer import TextAnalyzer

class TextAnalysis:
    def __init__(self):
        self.analyzer = TextAnalyzer()

    def analyze_text(self, text):
        """Perform comprehensive text analysis and return results."""
        self.analyzer.load_text(text)

        tokens = self.analyzer.word_tokenization()

        results = {
            'Sentences': len(self.analyzer.sentence_splitting()),
            'Word Tokens': len(tokens),
            'POS Tags': self.analyzer.pos_tagging()[:5],  # Show first 5 POS tags
            'Sentiment': self.analyzer.sentiment_analysis(),
            'Language': self.analyzer.language_detection()
            
        }

        

        return results

    

    