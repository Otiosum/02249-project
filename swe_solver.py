from swe_instance import SWEInstance
import itertools
import copy

class SWESolver:
    def __init__(self, instance : SWEInstance):
        self.instance = instance
        self.s_alphabet = set()
        self.s_alphabet_str = ""
        self.filtered_words = {}
        self.max_word_len = 0
        self.possible_substrings = {}
        self.possible_tuples = {}
        self.chosen_substrings = {}
        self.chosen_tuples = {}

        self.selection = {}
        self.selection_modified = {}
        for key in self.instance.r:
            if key not in self.selection:
                self.selection[key] = ""
                self.selection_modified[key] = -1


    def create_alphabet_from_s(self):
        for _, letter in enumerate(self.instance.s):
            self.s_alphabet.add(letter)

        self.s_alphabet_str = "".join(self.s_alphabet)

    def find_valid_words(self):
        for it in self.instance.t:
            for _, letter in enumerate(it):
                if self.instance.is_in_gamma_alphabet(letter):
                    if letter not in self.filtered_words:
                        self.filtered_words[letter] = set()

                    # words which have letters not in s are not valid
                    for word in self.instance.r[letter]:
                        if self.is_word_in_dictionary(word):
                            # words which are not a substring of s are not valid
                            if word in self.instance.s:
                                self.filtered_words[letter].add(word)

                                if len(word) > self.max_word_len:
                                    self.max_word_len = len(word)
                                # words which do not contain the 't' are not valid
                                #if letter.lower() in word and word not in self.filtered_words[letter]:

    def find_matches_for_t(self, t : 'str'):
        poss_input = []
        for _, letter in enumerate(t):
            if letter.islower():
                poss_input.append(letter)
            else:
                poss_input.append(self.filtered_words[letter])

        return set(itertools.product(*poss_input))

    def find_matching_t_in_s(self):
        for it in self.instance.t:
            if it not in self.possible_tuples:
                self.possible_tuples[it] = []
                self.possible_substrings[it] = []
                self.chosen_substrings[it] = []
                self.chosen_tuples[it] = []

            # Make input list of words
            self.possible_tuples[it] = self.find_matches_for_t(it)

        for key in self.possible_tuples:
            for tup in self.possible_tuples[key]:
                self.possible_substrings[key].append("".join(tup))

        # print("ALL POSSIBLE SUBSTRINGS:")
        # for key in self.possible_substrings:
        #     print("{}: ".format(key),end='')
        #     print(self.possible_substrings[key])
        #     print("")

    def is_substring_in_s(self) -> bool:
        for it in self.instance.t:
            flag = False
            for tup in self.possible_tuples[it]:
                joined_tup = "".join(tup)
                if joined_tup in self.instance.s:
                    flag = True
                    self.chosen_tuples[it].append(tup)
                    self.chosen_substrings[it].append(joined_tup)
            if not flag:
                return False
        return True

    def fill_selection(self, t_index, c_index):
        target_t = list(self.instance.t)[t_index]
        for _, letter in enumerate(target_t):
            if letter.isupper():
                if self.selection[letter] == "":
                    self.selection[letter] = self.chosen_tuples[target_t][c_index][_]
                    self.selection_modified[letter] = t_index

    def rem_selection(self, t_index):
        target_t = list(self.instance.t)[t_index]
        for _, letter in enumerate(target_t):
            if letter.isupper():
                if self.selection_modified[letter] == t_index:
                    self.selection[letter] = ""

    def recusrive_count(self, t_index):
        if t_index >= len(self.instance.t):
            return False
        for i, item in enumerate(self.chosen_tuples[list(self.instance.t)[t_index]]):
            self.fill_selection(t_index, i)
            if not self.recusrive_count(t_index + 1):
                if self.verify_t(self.selection):
                    return True
                else:
                    self.rem_selection(t_index)
            else:
                return True
        self.rem_selection(t_index)
        return False

    def verify_t(self, selection):
        new_t = []
        temp_chosen = {}
        for it in self.instance.t:
            modded_it = ""
            for _, letter in enumerate(it):
                if letter.islower() or selection[letter] == "":
                    modded_it += letter
                else:
                    modded_it += selection[letter]
            new_t.append(modded_it)

        for new_it in new_t:
            temp_chosen[new_it] = self.find_matches_for_t(new_it)
            copy_temp_chosen = copy.deepcopy(temp_chosen[new_it])

            # Check if new possibilities exist in s
            for tup in copy_temp_chosen:
                joined_tup = "".join(tup)
                if joined_tup not in self.instance.s:
                    temp_chosen[new_it].remove(tup)

            if len(temp_chosen[new_it]) == 0:
                return False
        return True

    def is_word_in_dictionary(self, word : str) -> bool:
        for _, letter in enumerate(word):
            if letter not in self.s_alphabet_str:
                return False
        return True