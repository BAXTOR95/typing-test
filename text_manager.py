import requests
from googletrans import Translator, LANGUAGES
from wonderwords import RandomSentence


class TextManager:
    """A manager for generating and translating text for typing practice.

    Attributes:
        translator (Translator): A Translator object from googletrans library.
        sentence_generator (RandomSentence): A RandomSentence object from wonderwords library.
    """

    def __init__(self):
        """Initialize the TextManager with a Translator and RandomSentence generator."""
        self.translator = Translator()
        self.sentence_generator = RandomSentence()

    def create_paragraph(self, n=60):
        """Create a paragraph consisting of random sentences.

        Args:
            n (int): Number of sentences to generate.

        Returns:
            A string containing the generated paragraph or None if an error occurs.
        """
        try:
            paragraph = " ".join(self.sentence_generator.sentence() for _ in range(n))
            return paragraph
        except Exception as e:
            print(f"Error generating paragraph: {e}")
            return None

    def translate_paragraph(self, paragraph, dest_language='es'):
        """Translate a given paragraph to the specified destination language.

        Args:
            paragraph (str): The paragraph to translate.
            dest_language (str): The two-letter language code of the translation target language.

        Returns:
            The translated paragraph as a string, or None if an error occurs.
        """
        if paragraph is None:
            return None
        try:
            translated_paragraph = self.translator.translate(
                paragraph, src='en', dest=dest_language
            )
            # Properly space the period followed by a space in the translated text
            return translated_paragraph.text.replace(".", ". ")
        except Exception as e:
            print(f"Error translating paragraph: {e}")
            return None


if __name__ == "__main__":
    # Example usage
    text_manager = TextManager()
    paragraph = text_manager.create_paragraph()
    print("Original paragraph:")
    print(paragraph)

    translated_paragraph = text_manager.translate_paragraph(paragraph)
    print("\nTranslated paragraph:")
    print(translated_paragraph)
