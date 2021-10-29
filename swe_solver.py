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

        self.filtered_t = set()
        for it in instance.t:
            self.filtered_t.add(it)

    # --- Pre-processing (filter out impossible words and create structures)

    def create_alphabet_from_s(self):
        for _, letter in enumerate(self.instance.s):
            self.s_alphabet.add(letter)

        self.s_alphabet_str = "".join(self.s_alphabet)

    def find_valid_words(self):
        for it in self.filtered_t:
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

    def create_all_substrings(self):
        for it in self.filtered_t:
            if it not in self.possible_tuples:
                self.possible_tuples[it] = []
                self.possible_substrings[it] = []
                self.chosen_substrings[it] = []
                self.chosen_tuples[it] = []

            # Make input list of words
            self.possible_tuples[it] = self.get_all_substrings_for_t(it)

        for key in self.possible_tuples:
            for tup in self.possible_tuples[key]:
                self.possible_substrings[key].append("".join(tup))

    def get_all_substrings_for_t(self, t : 'str'):
        poss_input = []
        for _, letter in enumerate(t):
            if letter.islower():
                poss_input.append(letter)
            else:
                poss_input.append(self.filtered_words[letter])

        return set(itertools.product(*poss_input))

    def choose_substrings_in_s(self) -> bool:
        for it in self.filtered_t:
            flag = False
            for tup in self.possible_tuples[it]:
                joined_tup = "".join(tup)
                if joined_tup in self.instance.s:
                    flag = True
                    self.chosen_tuples[it].append(tup)
                    self.chosen_substrings[it].append(joined_tup)
            if not flag:
                return
        return

    def filter_chosen_substrings(self):
        # Given letter(i) = letter(j) in 't', w(i) = w(j) in substring
        for it in self.filtered_t:
            duplicate_map = {}
            for _, letter in enumerate(it):
                if letter not in duplicate_map:
                    duplicate_map[letter] = []

                duplicate_map[letter].append(_)

            for key in duplicate_map:
                if len(duplicate_map[key]) > 1:
                    candidates = copy.deepcopy(self.chosen_tuples[it])
                    for cand in candidates:
                        for i in range(1, len(duplicate_map[key])):
                            if not cand[duplicate_map[key][0]] == cand[duplicate_map[key][i]]:
                                self.chosen_tuples[it].remove(cand)

    # ---- Look through substrings to find valid combination

    def fill_selection(self, t_index, c_index):
        target_t = list(self.filtered_t)[t_index]
        for _, letter in enumerate(target_t):
            if letter.isupper():
                if self.selection[letter] == "":
                    self.selection[letter] = self.chosen_tuples[target_t][c_index][_]
                    self.selection_modified[letter] = t_index

    def rem_selection(self, t_index):
        target_t = list(self.filtered_t)[t_index]
        for _, letter in enumerate(target_t):
            if letter.isupper():
                if self.selection_modified[letter] == t_index:
                    self.selection[letter] = ""

    def verify_candidates(self, t_index):
        if t_index >= len(self.filtered_t):
            return False
        if self.verify_t(self.selection):
            return True
        else:
            self.rem_selection(t_index)
        return False

    def recursive_count(self, t_index):
        for i, item in enumerate(self.chosen_tuples[list(self.filtered_t)[t_index]]):
            self.fill_selection(t_index, i)
            if t_index + 1 < len(self.filtered_t):
                if not self.recursive_count(t_index + 1):
                    self.rem_selection(t_index)
                else:
                    return True
            else:
                if self.verify_t(self.selection):
                    return True
                else:
                    self.rem_selection(t_index)
        return False

    def verify_t(self, selection):
        new_t = {}
        temp_chosen = {}
        for it in self.filtered_t:
            modded_it = ""
            for _, letter in enumerate(it):
                if letter.islower() or selection[letter] == "":
                    modded_it += letter
                else:
                    modded_it += selection[letter]
            new_t[modded_it] = it

        for key in new_t:
            temp_chosen[key] = self.get_all_substrings_for_t(key)
            copy_temp_chosen = copy.deepcopy(temp_chosen[key])

            # Check if new possibilities exist in s
            for tup in copy_temp_chosen:
                joined_tup = "".join(tup)
                if joined_tup not in self.chosen_substrings[new_t[key]]:
                    temp_chosen[key].remove(tup)

            if len(temp_chosen[key]) == 0:
                return False
        return True

    # --- Util

    def is_word_in_dictionary(self, word : str) -> bool:
        for _, letter in enumerate(word):
            if letter not in self.s_alphabet_str:
                return False
        return True

    def count_total_combinations(self):
        total_combs = 1
        for key in self.chosen_tuples:
            total_combs *= len(self.chosen_tuples[key])
        return total_combs