from abc import ABC, abstractmethod
import random
import string

class BaseMistaker(ABC):
    """
    Abstract base class for generating text errors across various categories.
    Provides reusable methods and a consistent interface for subclasses.
    """

    def __init__(self, error_probability=0.2):
        """
        Initialize the BaseMistaker.
        Args:
            error_probability (float): The likelihood of introducing an error.
        """
        self.error_probability = error_probability

    @abstractmethod
    def make_mistake(self, text: str) -> str:
        """
        Abstract method to generate a mistake in the given text.
        Must be implemented by subclasses.
        """
        pass

    def should_apply_error(self) -> bool:
        """
        Determines whether to apply an error based on the probability.
        """
        return random.random() < self.error_probability

    def random_insert(self, word: str, chars=string.ascii_letters) -> str:
        """
        Inserts a random character into a word.
        """
        idx = random.randint(0, len(word))
        return word[:idx] + random.choice(chars) + word[idx:]

    def random_replace(self, word: str, chars=string.ascii_letters) -> str:
        """
        Replaces a random character in a word with another random character.
        """
        if not word:
            return word
        idx = random.randint(0, len(word) - 1)
        return word[:idx] + random.choice(chars) + word[idx + 1:]

    def random_delete(self, word: str) -> str:
        """
        Deletes a random character from a word.
        """
        if len(word) <= 1:
            return word
        idx = random.randint(0, len(word) - 1)
        return word[:idx] + word[idx + 1:]

    def swap_adjacent(self, word: str) -> str:
        """
        Swaps two adjacent characters in a word.
        """
        if len(word) <= 1:
            return word
        idx = random.randint(0, len(word) - 2)
        return word[:idx] + word[idx + 1] + word[idx] + word[idx + 2:]

    def merge_words(self, words: list) -> list:
        """
        Merges two adjacent words by removing the space.
        """
        if len(words) < 2:
            return words
        idx = random.randint(0, len(words) - 2)
        words[idx] = words[idx] + words[idx + 1]
        del words[idx + 1]
        return words

    def modify_case(self, word: str) -> str:
        """
        Randomly changes the case of a character in a word.
        """
        if not word:
            return word
        idx = random.randint(0, len(word) - 1)
        char = word[idx]
        if char.islower():
            char = char.upper()
        else:
            char = char.lower()
        return word[:idx] + char + word[idx + 1:]
