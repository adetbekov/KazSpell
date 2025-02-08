import random
from .base import BaseMistaker

class TypographicalMistaker(BaseMistaker):
    """
    Generates typographical errors in text.
    Errors include:
    - Swapping adjacent characters
    - Deleting a character
    - Adding an extra character
    - Replacing a character
    """

    def __init__(self, error_probability=0.2, chars="қазахтылырынеңбөп"):
        """
        Args:
            error_probability (float): Probability of introducing an error.
            chars (str): Allowed characters for replacements and insertions.
        """
        super().__init__(error_probability)
        self.chars = "АӘБВГҒДЕЁЖЗИЙКҚЛМНҢОӨПРСТУҰҮФХҺЦЧШЩЫІЭЮЯабвгғдеёжзийкқлмнңоөпрстуұүфхһцчшщыіэюя" or chars

    def make_mistake(self, text: str) -> str:
        """
        Introduces typographical errors into the input text.

        Args:
            text (str): The original text.

        Returns:
            str: The text with typographical errors.
        """
        words = text.split()  # Split text into words
        for i, word in enumerate(words):
            if self.should_apply_error():
                # Randomly choose an error type
                operation = random.choice(["swap", "delete", "insert", "replace"])
                if operation == "swap":
                    words[i] = self.swap_adjacent(word)
                elif operation == "delete":
                    words[i] = self.random_delete(word)
                elif operation == "insert":
                    words[i] = self.random_insert(word, self.chars)
                elif operation == "replace":
                    words[i] = self.random_replace(word, self.chars)
        return " ".join(words)
