import random
import re
from collections import defaultdict

class MarkovModel:
    def __init__(self):
        """
        self.model: A dictionary where keys are tuples of two words (prefix) and values are lists of possible following words (suffix).
        """
        self.model = defaultdict(list)
        self.START_TOKEN = "<START>"
        self.END_TOKEN = "<END>"

    def _tokenize(self, text: str) -> list:
        return re.findall(r"[\w']+|[.,!?;]", text.lower())

    def learn(self, text: str):
        words = self._tokenize(text)

        if not words:
            return

        tokens = [self.START_TOKEN] * 2 + words + [self.END_TOKEN]

        for i in range(len(tokens) - 2):
            prefix1, prefix2, suffix = tokens[i], tokens[i+1], tokens[i+2]
            key = (prefix1, prefix2)
            self.model[key].append(suffix)

    def generate(self, max_words: int = 30) -> str:
        if not self.model:
            return "I haven't learned enough to speak... (This is hardcoded)"

        current_prefix = (self.START_TOKEN, self.START_TOKEN)
        output_words = []

        for _ in range(max_words):
            possible_suffixes = self.model.get(current_prefix)
            
            if not possible_suffixes:
                break

            next_word = random.choice(possible_suffixes)

            if next_word == self.END_TOKEN:
                break
            
            output_words.append(next_word)
            current_prefix = (current_prefix[1], next_word)

        return self._format_output(output_words)

    def _format_output(self, words: list) -> str:
        if not words:
            return "Could not generate a sentence."
        
        sentence = " ".join(words)
        sentence = re.sub(r'\s+([.,!?;])', r'\1', sentence) # Remove janky spacing
        return sentence.capitalize()