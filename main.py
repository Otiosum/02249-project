import argparse
import sys
from swe_instance import SWEInstance

def main(f_input : str):
    if f_input is "":
        f_input = sys.stdin.readlines()
    swe_instance = SWEInstance(f_input)
    swe_instance.print_swe_state(False)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="Path to file with problem instance")
    args = parser.parse_args()

    lines = ""
    if args.f is not None:
        with open(args.f, 'r', encoding="utf-8", newline='') as r:
            lines = r.readlines()
        r.close()

    main(lines)
