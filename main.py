import argparse
import sys
from swe_instance import SWEInstance
from swe_solver import SWESolver

def main(f_input : str, is_verbose : bool):
    if f_input is "":
        f_input = sys.stdin.readlines()
    swe_instance = SWEInstance(f_input, is_verbose)
    #swe_instance.print_swe_state(False)

    swe_solver = SWESolver(swe_instance)
    swe_solver.create_alphabet_from_s()
    swe_solver.compute_substrings()
    print(swe_instance.s)
    print(swe_solver.filtered_words)
    print("Max length of word: {}".format(swe_solver.max_word_len))
    print("")
    swe_solver.find_matching_t_in_s()

    res = swe_solver.is_substring_in_s()
    print("YES") if res else print("NO")

    for key in swe_solver.chosen_substrings:
        print("{}: {}".format(key, swe_solver.chosen_substrings[key]))
        print("")

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
