from swe_instance import SWEInstance


class SWESolver:
    def __init__(self, instance : SWEInstance):
        self.instance = instance
        self.s_alphabet = set()
        self.s_alphabet_str = ""
        self.filtered_words = {}

    def create_alphabet_from_s(self):
        for _, letter in enumerate(self.instance.s):
            self.s_alphabet.add(letter)

        self.s_alphabet_str = "".join(self.s_alphabet)

    def compute_substrings(self):
        for it in self.instance.t:
            for _, letter in enumerate(it):
                if letter not in self.filtered_words:
                    self.filtered_words[letter] = []

                # words which have letters not in s are not valid
                for word in self.instance.r[letter]:
                    if self.is_word_in_dictionary(word):
                        # words which are not a substring of s are not valid
                        if word in self.instance.s:
                            self.filtered_words[letter].append(word)


    def is_word_in_dictionary(self, word : str) -> bool:
        for _, letter in enumerate(word):
            if letter not in self.s_alphabet_str:
                return False
        return True