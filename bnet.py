#!/usr/local/bin/python3
import sys
from collections import defaultdict
from itertools import product

class BayesianNetwork:
    probability = 0

    def __init__(self, events, evidence):
        self.network = {
            'B': {True: 0.001, False: 0.999},
            'E': {True: 0.002, False: 0.998},
            'A': {
                (True, True, True): 0.95,
                (True, True, False): 0.94,
                (True, False, True): 0.29,
                (True, False, False): 0.001,
                (False, True, True): 1 - 0.95,
                (False, True, False): 1 - 0.94,
                (False, False, True): 1 - 0.29,
                (False, False, False): 1 - 0.001
            },
            'J': {
                (True, True): 0.90,
                (True, False): 0.05,
                (False, True): 1 - 0.90,
                (False, False): 1 - 0.05
            },
            'M': {
                (True, True): 0.70,
                (True, False): 0.01,
                (False, True): 1 - 0.70,
                (False, False): 1 - 0.01
            }
        }

        if not evidence:
            for combo in self.get_missing_combos(events):
                combo.update(events)
                self.probability += self.computeProbability(
                    combo['B'],
                    combo['E'],
                    combo['A'],
                    combo['J'],
                    combo['M']
                )
        else:
            events.update(evidence)
            numerator = 0
            denominator = 0

            for combo in self.get_missing_combos(events):
                combo.update(events)
                numerator += self.computeProbability(
                    combo['B'],
                    combo['E'],
                    combo['A'],
                    combo['J'],
                    combo['M']
                )
            
            for combo in self.get_missing_combos(evidence):
                combo.update(evidence)
                denominator += self.computeProbability(
                    combo['B'],
                    combo['E'],
                    combo['A'],
                    combo['J'],
                    combo['M']
                )
            
            self.probability = numerator/denominator
            
    
    def computeProbability(self, b, e, a, j, m):
        probability_b = self.network['B'][b]
        probability_e = self.network['E'][e]
        probability_a_given_be = self.network['A'][(a, b, e)]
        probability_j_given_a = self.network['J'][(j, a)]
        probability_m_given_a = self.network['M'][(m, a)]
        joint_probability = probability_b * probability_e * probability_a_given_be * probability_j_given_a * probability_m_given_a

        return joint_probability
    
    def get_missing_combos(self, events):
        missing = list(set(['B', 'E', 'A', 'J', 'M']) - set(events.keys()))
            
        combinations = list(product([True, False], repeat=len(missing)))

        all_combos = []
        for combo in combinations:
            current_combo = {var: events.get(var, value) for var, value in zip(missing, combo)}
            all_combos.append(current_combo)
        
        return all_combos


if __name__ == '__main__':
    events = defaultdict(lambda: None)
    evidence = defaultdict(lambda: None)
    shift_to_evidence = False

    for arg in sys.argv[1:]:
        if 'given' in arg.lower():
            shift_to_evidence = True
            continue

        if shift_to_evidence:
            evidence[arg[0]] = True if arg[1] == 't' else False
        else:
            events[arg[0]] = True if arg[1] == 't' else False
    
    bnet = BayesianNetwork(events, evidence)
    print(f"Probability = {bnet.probability:.10}")
        

