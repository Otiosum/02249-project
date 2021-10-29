import argparse
import sys
from swe_instance import SWEInstance
from swe_solver import SWESolver

def main(f_input : str, is_verbose : bool):
    print_more = True  # Change to False when submitting on codejudge

    if f_input == "":
        f_input = sys.stdin.readlines()
    swe_instance = SWEInstance(f_input, is_verbose)
    #swe_instance.print_swe_state(False)

    swe_solver = SWESolver(swe_instance)
    swe_solver.create_alphabet_from_s()
    swe_solver.find_valid_words()
    if print_more:
        print(swe_instance.s)
        print("Alphabet of s: {}".format(swe_solver.s_alphabet))
        print(swe_solver.filtered_words)
        print("Max length of word: {}".format(swe_solver.max_word_len))
        print("")
    swe_solver.find_matching_t_in_s()
    swe_solver.is_substring_in_s()

    if print_more:
        for key in swe_solver.chosen_substrings:
            print("{}: | ".format(key),end='')
            for tup in swe_solver.chosen_tuples[key]:
                print("{} | ".format(",".join(tup)),end='')
            print("\n")

    res = swe_solver.recusrive_count(0)
    if res:
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
