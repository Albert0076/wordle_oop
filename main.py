from collections import defaultdict


class Wordle:
    def __init__(self, num_letters: int):
        self._secret_word = ""
        self._guessed_word = ""
        self._num_letter = num_letters
        self._words = []
        self.read_dictionary()

    def read_dictionary(self):
        with open("words.txt", "r") as file:
            for line in file.readlines():
                line = line.strip()
                if len(line) == self._num_letter:
                    self._words.append(line.upper())

    def set_secret_word(self, secret_word: str):
        self.validate_word(secret_word)
        self._secret_word = secret_word.upper()

    def get_secret_word(self):
        return self._secret_word

    def validate_word(self, input_word: str):
        if not isinstance(input_word, str):
            raise ValueError("Must Input Str")

        input_word = input_word.upper()
        if len(input_word) != self._num_letter:
            raise ValueError(f"Word must be {self._num_letter} letters long")

        if not input_word in self._words:
            raise ValueError("Word is not in dictionary")

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

        return match_list
