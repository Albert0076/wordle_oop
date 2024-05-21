from collections import defaultdict
from wordfreq import zipf_frequency, top_n_list, word_frequency
from random import choice

LANG = "en"


class Wordle:
    def __init__(self, num_letters: int, word_dictionary: list):
        self._secret_word = ""
        self._guessed_word = ""
        self._num_letter = num_letters
        self._words = word_dictionary
        self.random_secret_word()


    def random_secret_word(self):
        self._secret_word = choice(self._secret_word)

    def set_secret_word(self, secret_word: str):
        self.validate_word(secret_word)
        self._secret_word = secret_word.upper()

    def get_secret_word(self):
        return self._secret_word

    def validate_word(self, input_word: str):
        if not isinstance(input_word, str):
            raise ValueError("Must Input Str", input_word)

        input_word = input_word.upper()
        if len(input_word) != self._num_letter:
            raise ValueError(f"Word must be {self._num_letter} letters long", input_word)

        if word_frequency(input_word, LANG) == 0.0:
            raise ValueError("Word is not in dictionary", input_word)

    def set_guessed_word(self, guessed_word: str):
        self.validate_word(guessed_word)
        self._guessed_word = guessed_word.upper()

    @property
    def matches(self):
        # "0" -> Not in word, "1" -> Incorrect Position, "2" -> Correct Position
        match_list = [[] for _ in range(self._num_letter)]
        letter_dict = defaultdict(lambda: 0)
        for i in range(self._num_letter):
            letter_dict[self._secret_word[i]] += 1

        for i in range(self._num_letter):
            if self._secret_word[i] == self._guessed_word[i]:
                match_list[i] = [2, self._guessed_word[i]]
                letter_dict[self._secret_word[i]] -= 1

        for i in range(self._num_letter):
            if letter_dict[self._guessed_word[i]] > 0:
                match_list[i] = [1, self._guessed_word[i]]
                letter_dict[self._guessed_word[i]] -= 1

        for i in range(self._num_letter):
            if not match_list[i]:
                match_list[i] = [0, self._guessed_word[i]]

        return self._guessed_word == self._secret_word, match_list


class Game:
    def __init__(self):
        self._interface = CLI(self)
        self._word_length: int = 0
        self._game_length: int = 0
        self._interface.setup()
        self._words = []
        self.read_dictionary()

    def read_dictionary(self):
        for word in top_n_list(LANG, 10000):
            if len(word) == self._word_length:
                self._words.append(word)

    def set_word_length(self, word_length: int):
        self._word_length = word_length

    def get_word_length(self):
        return self._word_length

    def set_game_length(self, game_length: int):
        self._game_length = game_length

    def get_game_length(self):
        return self._game_length

    def reset(self):
        self._word_length = 0
        self._game_length = 0

    def main_loop(self):
        count = 0
        current_wordle = Wordle(self._word_length, self._words)
        while count < self._game_length and not current_wordle.matches[0]:
            guessed_word = self._interface.get_word()
            try:
                current_wordle.set_guessed_word(guessed_word)
                self._interface.show_matches(current_wordle.matches[1])
                count += 1

            except ValueError:
                self._interface.not_valid_word(guessed_word)

        if current_wordle.matches[0]:
            self._interface.show_victory()

        else:
            self._interface.show_defeat()



class CLI:
    def __init__(self, game: Game):
        self._game = game

    def setup(self):
        pass

    def get_word(self):
        return "Tests"

    def not_valid_word(self, word: str):
        pass

    def show_matches(self, matches: list):
        pass

    def show_victory(self):
        pass

    def show_defeat(self):
        pass

