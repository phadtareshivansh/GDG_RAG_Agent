"""
Day 1 - Exercise 1: Text Cleaning Utility [WORKBOOK]
=====================================================

Small utility to clean and tokenize text for learning exercises.
"""

import re
import string


class TextCleaner:
    """
    A friendly text cleaning assistant.
    """

    def __init__(self):
        """Initialize the cleaner and store punctuation characters."""
        # store punctuation characters from the string module
        self.punctuation = string.punctuation
        print("TextCleaner ready!")

    def clean_text(self, text: str) -> str:
        """Clean text by lowercasing, removing non-alphanumeric chars and normalizing spaces.

        Args:
            text: input string

        Returns:
            cleaned string
        """
        # Step 1 - lowercase
        text = text.lower()
        # Step 2 - strip leading/trailing whitespace
        text = text.strip()
        # Step 3 - remove any character that is not a-z, 0-9 or whitespace
        text = re.sub(r'[^a-z0-9\s]', '', text)
        # Step 4 - collapse multiple whitespace into single space
        text = re.sub(r'\s+', ' ', text)
        return text

    def tokenize(self, text: str) -> list:
        """Return a list of tokens (words) from the text.

        This cleans the text first and then splits on whitespace.
        """
        cleaned = self.clean_text(text)
        tokens = cleaned.split() if cleaned else []
        return tokens

    def get_word_count(self, text: str) -> int:
        """Return number of words in the text."""
        tokens = self.tokenize(text)
        return len(tokens)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("TEXT CLEANING DEMO - Let's clean some messy text!")
    print("=" * 70 + "\n")

    cleaner = TextCleaner()

    test_cases = [
        "  Hello, World!!!  ",
        "Email: support@gdg.dev",
        "Price: $99.99 (AMAZING Deal!!!)",
        "Python     is     AWESOME!!!",
        "Check out: https://gdg.community.dev"
    ]

    for i, messy_text in enumerate(test_cases, 1):
        clean_text = cleaner.clean_text(messy_text)
        word_count = cleaner.get_word_count(messy_text)

        print(f"Example {i}:")
        print(f"  Original: '{messy_text}'")
        print(f"  Cleaned:  '{clean_text}'")
        print(f"  Words:    {word_count}")
        print()