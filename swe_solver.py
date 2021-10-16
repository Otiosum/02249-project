from swe_instance import SWEInstance
import itertools


class SWESolver:
    def __init__(self, instance : SWEInstance):
        self.instance = instance
        self.s_alphabet = set()
        self.s_alphabet_str = ""
        self.filtered_words = {}
        self.max_word_len = 0
        self.possible_substrings = {}

    def create_alphabet_from_s(self):
        for _, letter in enumerate(self.instance.s):
            self.s_alphabet.add(letter)

        self.s_alphabet_str = "".join(self.s_alphabet)

    def compute_substrings(self):
        for it in self.instance.t:
            for _, letter in enumerate(it):
                if self.instance.is_in_gamma_alphabet(letter):
                    if letter not in self.filtered_words:
                        self.filtered_words[letter] = []

                    # words which have letters not in s are not valid
                    for word in self.instance.r[letter]:
                        if self.is_word_in_dictionary(word):
                            # words which are not a substring of s are not valid
                            if word in self.instance.s:
                                # words which do not contain the 't' are not valid
                                if letter.lower() in word and word not in self.filtered_words[letter]:
                                    self.filtered_words[letter].append(word)

                                    if len(word) > self.max_word_len:
                                        self.max_word_len = len(word)

    def find_matching_t_in_s(self):
        # index_map = {}
        # # Extract positions of each distinct letter in s into sorted list
        # for _, letter in enumerate(self.instance.s):
        #     if letter not in index_map:
        #         index_map[letter] = []

        #     index_map[letter].append(_)
        # print(index_map)

        # print("")
        # for it in self.instance.t:
        #     print("{}: ".format(it), end='')
        #     for _, letter in enumerate(it):
        #         print("{} ".format(index_map[letter.lower()]),end='')
        #     print("")

        # Make every possible combo using t, and filtered words
        possibilities = {}
        for it in self.instance.t:
            if it not in possibilities:
                possibilities[it] = []
                self.possible_substrings[it] = []

            # Make input list of words
            poss_input = []
            for _, letter in enumerate(it):
                if self.instance.is_in_gamma_alphabet(letter):
                    poss_input.append(self.filtered_words[letter])

            possibilities[it] = list(itertools.product(*poss_input))

        for key in possibilities:
            for tup in possibilities[key]:
                self.possible_substrings[key].append("".join(tup))

        print("ALL POSSIBLE SUBSTRINGS:")
        for key in self.possible_substrings:
            print("{}: ".format(key),end='')
            print(self.possible_substrings[key])

    def is_substring_in_s(self) -> bool:
        for it in self.instance.t:
            flag = False
            for substr in self.possible_substrings:
                if substr in self.instance.s:
                    flag = True
                    break
            if not flag:
                return False
        return True

    def is_word_in_dictionary(self, word : str) -> bool:
        for _, letter in enumerate(word):
            if letter not in self.s_alphabet_str:
                return False
        return True