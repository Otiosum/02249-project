import argparse
import sys
from swe_instance import SWEInstance
from swe_solver import SWESolver
from swe_tree import SWETree

def main(f_input : str, is_verbose : bool):
    print_more = False  # Change to False when submitting on codejudge

    if f_input == "":
        f_input = sys.stdin.readlines()
    swe_instance = SWEInstance(f_input, is_verbose)

    swe_solver = SWESolver(swe_instance)
    swe_solver.create_alphabet_from_s()
    swe_solver.find_valid_words()
    swe_solver.create_all_substrings()
    swe_solver.choose_substrings_in_s()

    if print_more:
        print("BEFORE FILTER: {}".format(f'{swe_solver.count_total_combinations():,}'))

    swe_solver.filter_chosen_substrings()
    res_heuristic = swe_solver.find_t_with_whole_alphabet()

    if print_more:
        print("AFTER FILTER: {}".format(f'{swe_solver.count_total_combinations():,}'))
        print("")
        print(swe_instance.s)
        print("Alphabet of s: {}".format(swe_solver.s_alphabet))
        print(swe_solver.filtered_words)
        print("Max length of word: {}".format(swe_solver.max_word_len))
        print("")

        for key in swe_solver.chosen_tuples:
            print("{} ({}): | ".format(key,len(swe_solver.chosen_tuples[key])),end='')
            for tup in swe_solver.chosen_tuples[key]:
                print("{} | ".format(",".join(tup)),end='')
            print("\n")
        print("ANSWER:")
        print("Alphabet heuristic: YES") if res_heuristic else print("Alphabet heuristic: NO")

    swe_tree = SWETree(swe_solver.chosen_tuples, False)
    res = swe_solver.tree_search(swe_tree)

    if res:
        if res_heuristic:
            swe_solver.cleanup_post_alphabet_heuristic()
        for key in sorted(swe_instance.r):
            val = swe_solver.selection[key]
            if not val == "":
                print("{}:{}".format(key, val))
    else:
        print("NO")

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="Path to file with problem instance")
    parser.add_argument("-v", action="store_true", help="Print information will be more verbose")
    args = parser.parse_args()

    lines = ""
    if args.f is not None:
        with open(args.f, 'r', encoding="utf-8", newline='') as r:
            lines = r.readlines()
        r.close()

    main(lines, args.v)
