#!/usr/local/bin/python3
from collections import defaultdict
import sys

def calculate_posterior_prob():
    for j in range(n):
        curr_observation = observations[j]
        output_file.write(f"\nAfter Observation {j+1} = {curr_observation}:\n\n")

        total_prob = 0.0
        for i in range(1, 6):
            prob = prob_cache[f'h{i}']
            total_prob += prior_probs[f'h{i}'][curr_observation] * prob            

        for i in range(1, 6):
            prob = prob_cache[f'h{i}']
            numerator = (prior_probs[f'h{i}'][curr_observation] * prob)
            prob_cache[f'h{i}'] = (numerator / total_prob) if total_prob != 0 else 0.0
    
        for i in range(1, 6):
            output_file.write(f"P(h{i} | Q) = {prob_cache[f'h{i}']:.12}\n")

        prob_C_given_Q = sum(prob_cache[f'h{i}'] * prior_probs[f'h{i}']['C'] for i in range(1, 6))
        
        output_file.write(f"\nProbability that the next candy we pick will be C, given Q: {prob_C_given_Q:.12}\n")
        output_file.write(f"Probability that the next candy we pick will be L, given Q: {1 - prob_C_given_Q:.12}\n")

    return prob_cache

def calculate_default_prob():
    output_file.write("\n")
    for hypothesis, info in prior_probs.items():
        prob = info['prob']
        output_file.write(f"P({hypothesis}) = {prob:.12}\n")

    prob_C_given_Q = sum(prior_probs[h]['prob'] * prior_probs[h]['C'] for h in prior_probs)

    output_file.write(f"\nProbability that the next candy we pick will be C, given Q: {prob_C_given_Q:.12}\n")
    output_file.write(f"Probability that the next candy we pick will be L, given Q: {1 - prob_C_given_Q:.12}\n")

if __name__ == '__main__':
    # read only dict:
    prior_probs = {
        'h1': {
            'prob': 0.1,
            'C': 1,
            'L': 0
        },
        'h2': {
            'prob': 0.2,
            'C': 0.75,
            'L': 0.25
        },
        'h3': {
            'prob': 0.4,
            'C': 0.5,
            'L': 0.5
        },
        'h4': {
            'prob': 0.2,
            'C': 0.25,
            'L': 0.75
        },
        'h5': {
            'prob': 0.1,
            'C': 0,
            'L': 1
        }
    }

    # mutable dict:
    prob_cache = defaultdict(float)

    with open('result.txt', 'w') as output_file:
        observations = sys.argv[1].strip() if len(sys.argv[1:]) == 1 else ""
        n = len(observations)

        if observations.count('C') + observations.count('L') != n:
            exit('Invalid Inputs!')

        output_file.write(f"Observation Sequence Q: {observations}\n")
        output_file.write(f"Length of Q: {n}\n")
        
        for i in range(1, 6):
            prob_cache[f'h{i}'] = prior_probs[f'h{i}']['prob']
        
        if n == 0:
            calculate_default_prob()
        else:
            calculate_posterior_prob()