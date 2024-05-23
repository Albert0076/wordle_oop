from collections import defaultdict
from wordfreq import zipf_frequency, top_n_list
from random import choice
from colorama import Fore
import pyinputplus

LANG = "en"
LETTERS = [chr(i) for i in range(65, 91)]


def get_word_list(word_length: int = 5, number_of_words: int = 10_000):
    return [word for word in top_n_list(LANG, number_of_words)
            if len(word) == word_length and word.isalpha()]


class Wordle:
    def __init__(self, num_letters: int, word_dictionary: list):
        self._secret_word = ""
        self._guessed_word = " " * num_letters
        self._num_letters = num_letters
        self._words = word_dictionary
        self.random_secret_word()

    def random_secret_word(self):
        self._secret_word = choice(self._words).upper()

    def set_secret_word(self, secret_word: str):
        self.validate_word(secret_word)
        self._secret_word = secret_word.upper()

    def get_secret_word(self):
        return self._secret_word

    def validate_word(self, input_word: str):
        if not isinstance(input_word, str):
            raise ValueError("Must Input Str")

        input_word = input_word.upper()
        if len(input_word) != self._num_letters:
            raise ValueError(f"Word must be {self._num_letters} letters long")

        if zipf_frequency(input_word, LANG) <= 0.5 or not input_word.isalpha():
            raise ValueError(f"Word: {input_word} is not in dictionary")

    def set_guessed_word(self, guessed_word: str):
        self.validate_word(guessed_word)
        self._guessed_word = guessed_word.upper()

    @property
    def matches(self):
        # "0" -> Not in word, "1" -> Incorrect Position, "2" -> Correct Position
        match_list = [[self._guessed_word[i], 0] for i in range(self._num_letters)]
        letter_dict = defaultdict(lambda: 0)
        for char in self._secret_word:
            letter_dict[char] += 1

        for i in range(self._num_letters):
            if self._secret_word[i] == self._guessed_word[i]:
                match_list[i][1] = 2
                letter_dict[self._secret_word[i]] -= 1

        for i in range(self._num_letters):
            if letter_dict[self._guessed_word[i]] > 0 and match_list[i][1] == 0:
                match_list[i][1] = 1
                letter_dict[self._guessed_word[i]] -= 1

        return match_list

    @property
    def correct_word(self):
        return self._secret_word == self._guessed_word

    def __repr__(self):
        return f"Wordle({self._secret_word})"


class Game:
    def __init__(self, word_length: int = 5, game_length: int = 6):
        self._word_length = word_length
        self._game_length = game_length
        self._words = get_word_list(word_length=self._word_length)
        self._wordle = Wordle(self._word_length, self._words)
        self.current_round: int = 0
        self._letters_remaining = defaultdict(lambda: True)

    def set_word_length(self, word_length: int):
        self._word_length = word_length

    def get_word_length(self):
        return self._word_length

    def set_game_length(self, game_length: int):
        self._game_length = game_length

    def get_game_length(self):
        return self._game_length

    def get_secret_word(self):
        return self._wordle.get_secret_word()

    def reset(self):
        self._word_length = 0
        self._game_length = 0

    def set_guess_word(self, input_word: str):
        try:
            self._wordle.set_guessed_word(input_word)
            self.update_remaining_letters(input_word)

        except ValueError as error:
            raise ValueError(error)

    def game_finished(self):
        return self.current_round >= self._game_length

    def correct_word(self):
        return self._wordle.correct_word

    def update_remaining_letters(self, input_word):
        letters = self._wordle.get_secret_word()
        for char in input_word:
            if not char in letters:
                self._letters_remaining[char] = False

    def get_remaining_letters(self):
        return [letter for letter in LETTERS if self._letters_remaining[letter]]

    def get_matches(self):
        return self._wordle.matches

    def __repr__(self):
        return f"Game({self._word_length})"


class CLI:
    def __init__(self):
        self.game = None
        self.setup()

    def setup(self):
        if pyinputplus.inputYesNo("Use default rules?") == "no":
            word_length = pyinputplus.inputInt("Enter word length: ", min=3)
            game_length = pyinputplus.inputInt("Enter number of rounds: ", min=1)
            self.game = Game(word_length, game_length)

        else:
            self.game = Game()

    def main_loop(self):
        while not (self.game.game_finished() or self.game.correct_word()):
            print(f"{self.game.get_game_length() - self.game.current_round} guesses remaining")
            if pyinputplus.inputYesNo("See remaining letters?") == "yes":
                self.show_remaining_letters()
            user_guess = pyinputplus.inputStr("")
            try:
                self.game.set_guess_word(user_guess)

                for match in self.game.get_matches():
                    if match[1] == 2:
                        print(Fore.GREEN + match[0], end="")

                    elif match[1] == 1:
                        print(Fore.YELLOW + match[0], end="")

                    else:
                        print(Fore.RED + match[0], end="")

                print(Fore.RESET + "\n")

                self.game.current_round += 1

            except ValueError:
                print("Invalid word")

        if self.game.game_finished():
            print(f"You ran out of guesses. The correct word was {self.game.get_secret_word()}.")

        else:
            print("Well done!")

    def show_remaining_letters(self):
        remaining_letters = self.game.get_remaining_letters()
        print(f"Remaining letters are: {remaining_letters}")


if __name__ == "__main__":
    interface = CLI()
    interface.main_loop()
