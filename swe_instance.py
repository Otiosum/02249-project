import sys

# Notations - subject to change to something more readable
# k = number of t strings
# s = the string
# t = encoded strings which are part of the expansion function
# r = words which are mapped to letters in t

class SWEInstance:
    def __init__(self, f_input):
        line_iter = 0

        # --- Read k
        line = f_input[line_iter].split("\n")[0]
        if line.isnumeric() is False:
            print ("NO")
            sys.exit(1)

        self.k = int(line)

        # --- Read string s
        line_iter += 1
        line = f_input[line_iter].split("\n")[0]
        if not self.is_in_sigma_alphabet(line):
            print ("NO")
            sys.exit(1)

        self.s = line

        # --- Read strings t (k times)
        line_iter += 1
        self.t = []
        for i in range(self.k):
            line = f_input[line_iter + i].split("\n")[0]
            if not self.is_in_gamma_alphabet(line.upper()):
                print ("NO")
                sys.exit(1)

            self.t.append(line)

        # --- Read G(at most size 26) - each G contains R_j
        line_iter += (i + 1)
        self.r = {}
        for j in range(len(f_input) - line_iter):
            key, vals = (f_input[line_iter + j].split("\n")[0]).split(":")
            if not self.is_in_gamma_alphabet(key):
                print("NO")
                sys.exit(1)

            self.r[key] = []
            for word in vals.split(","):
                if not self.is_in_sigma_alphabet(word):
                    print("NO")
                    sys.exit(1)

                self.r[key].append(word)
        self.solution = []

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
        
    # Print self.solution
    def print_solution(self, Gammas):
        for i in range(len(Gammas)):
            print(Gammas[i] + " : " + self.solution[i])
        
    # Return True if self.solution is a valid solution
    def isSolution(self, Gammas):
        strings = []
        for t in self.t:
            newString = ""
            for char in t:
                if char in "abcdefghijklmnopqrstuvwxyz":
                    newString = newString + char
                elif char in Gammas:
                    newString = newString + self.solution[Gammas.index(char)]
                else: 
                    return False
            strings.append(newString)
        valid = True
        count = 0
        while valid and count < len(strings):
            valid = strings[count] in self.s
            count += 1
        return valid
            
    # Try all the possibilities
    def findSolution(self, Gammas, counter):
        if counter == len(Gammas):
            if self.isSolution(Gammas):
                return True
            else: 
                return False
        else : 
            for element in self.r[Gammas[counter]]:
                self.solution[counter] = element
                solved = self.findSolution(Gammas, counter + 1)
                if solved:
                    return True
            return False
        
    def solve(self):
        Gammas = [*self.r]
        self.solution = [0] * len(Gammas)
        solved = self.findSolution(Gammas, 0)
        if solved:
            self.print_solution(Gammas)
        else:
            print("NO")
        
        
        
    
    
    
        
        
