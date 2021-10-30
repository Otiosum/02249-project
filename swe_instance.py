import sys

# Notations - subject to change to something more readable
# k = number of t strings
# s = the string
# t = encoded strings which are part of the expansion function
# r = words which are mapped to letters in t

class SWEInstance:
    def __init__(self, f_input, is_verbose : bool):
        line_iter = 0

        # --- Read k
        line = f_input[line_iter].split("\n")[0]
        if line.isnumeric() is False:
            print ("NO")
            if is_verbose:
                print("[v] k was not a number")
            sys.exit(1)

        self.k = int(line)

        # --- Read string s
        line_iter += 1
        line = f_input[line_iter].split("\n")[0]
        if not self.is_in_sigma_alphabet(line):
            print ("NO")
            if (is_verbose):
                print("[v] s does not match Sigma alphabet")
            sys.exit(1)

        self.s = line

        # --- Read strings t (k times)
        line_iter += 1
        self.t = []
        for i in range(self.k):
            line = f_input[line_iter + i].split("\n")[0]
            if not self.is_in_gamma_alphabet(line.upper()):
                print ("NO")
                if is_verbose:
                    print("[v] t does not match Gamma alphabet")
                sys.exit(1)

            self.t.append(line)

        line_iter += (i + 1)

        # Verify this is false: len(t) > k
        line = f_input[line_iter].split("\n")[0]
        if self.is_in_gamma_alphabet(line.upper()):
            print("NO")
            if is_verbose:
                print("[v] amount of t strings exceeds k")
            sys.exit(1)

        # --- Read G(at most size 26) - each G contains R_j
        self.r = {}
        for j in range(len(f_input) - line_iter):
            key, vals = (f_input[line_iter + j].split("\n")[0]).split(":")
            if not self.is_in_gamma_alphabet(key):
                print("NO")
                if is_verbose:
                    print("[v] Key of R subset is not in Gamma alphabet")
                sys.exit(1)

            self.r[key] = []
            for word in vals.split(","):
                if not self.is_in_sigma_alphabet(word):
                    print("NO")
                    if is_verbose:
                        print("[v] Word of R subset is not in Sigma alphabet")
                    sys.exit(1)

                self.r[key].append(word)

    def is_in_sigma_alphabet(self, line: str) -> bool:
        for _, char in enumerate(line):
            if char not in "abcdefghijklmnopqrstuvwxyz":
                return False
        return True

    def is_in_gamma_alphabet(self, line: str) -> bool:
        for _, char in enumerate(line):
            if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                return False
        return True

    def print_swe_state(self, is_verbose : bool):
        print("k: {}".format(self.k))
        print("s: {}".format(self.s))
        print("t: ", end='')
        self.print_t_strings()
        print("r:")
        self.print_r_subsets(is_verbose)

    def print_r_subsets(self, is_verbose : bool):
        for key in self.r:
            if is_verbose:
                print("{} : ".format(key), end='')
                for it in self.r[key]:
                    print("{} ".format(it),end='')
                print("\n")
            else:
                print("{} : {} items".format(key, len(self.r[key])))

    def print_t_strings(self):
        for it in self.t:
            print("{} ".format(it),end='')
        print("")
