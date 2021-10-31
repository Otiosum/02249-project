from swe_instance import SWEInstance
import itertools

class SWESolver2:
    def __init__(self, instance : SWEInstance):
        self.instance = instance
        self.s_alphabet = set()
        self.s_alphabet_str = ""
        self.Gammas = [*self.instance.r]
        self.filtered_r = []
        self.solution = []
        self.R = []
        
        # --- Pre-processing (filter out impossible words and create structures)

    def create_alphabet_from_s(self):
        for _, letter in enumerate(self.instance.s):
            self.s_alphabet.add(letter)

        self.s_alphabet_str = "".join(self.s_alphabet)
        
    def find_valid_words(self):
        for i in range(len(self.Gammas)):
            self.filtered_r.append([])
            for word in self.instance.r[self.Gammas[i]]:
                if word in self.instance.s:
                    self.filtered_r[i].append(word)
                    
    def heuristic(self):
        for i in range(len(self.filtered_r)):
            self.filtered_r[i] = sorted(self.filtered_r[i], key=lambda x : (-self.instance.s.count(x), len(x)))
            
    def possibilities(self):
        for element in itertools.product(*self.filtered_r):
            self.R.append(element)
            
    def solve(self): 
        self.create_alphabet_from_s()
        self.find_valid_words()
        self.heuristic()
        self.possibilities()
        count = 0 
        find_solution = False
        while count < len(self.R) and not find_solution:
            self.solution = self.R[count]
            all_t_valid = True 
            for t in self.instance.t: 
                e_t = self.e(t)
                if not (e_t in self.instance.s):
                    all_t_valid = False
            if all_t_valid:
                find_solution = True
            count += 1
        if find_solution:
            self.print_solution()
        else:
            print("NO")
            
    def e(self, t):
        e_t = ""
        for letter in t:
            if letter in "abcdefghijklmnopqrstuvwxyz":
                e_t += letter
            else:
                index = self.Gammas.index(letter)
                e_t += self.solution[index]
        return e_t
    
    def print_solution(self):
        for i in range(len(self.Gammas)):
            print(self.Gammas[i] + " : " + self.solution[i])
            
        
