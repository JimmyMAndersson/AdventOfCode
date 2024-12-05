import numpy as np
import os

# --- Part Two ---
# While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.
#
# For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:
#
# 75,97,47,61,53 becomes 97,75,47,61,53.
# 61,13,29 becomes 61,29,13.
# 97,13,75,29,47 becomes 97,75,47,29,13.
# After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.
#
# Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?

def create_rule_dict(rules):
    rule_dict = {}
    for [value, key] in rules:
        if key in rule_dict:
            rule_dict[key].add(value)
        else:
            rule_dict[key] = { value }
    
    return rule_dict

def is_valid_update(update, rule_dict):
    for idx in np.arange(update.shape[0]):
        if update[idx] in rule_dict:
            if len(rule_dict[update[idx]].intersection(update[idx+1:])) > 0:
                return False
    return True

def correct_update(update, rule_dict):
    while not is_valid_update(update, rule_dict):
        for idx in np.arange(update.shape[0]):
            page = update[idx]
            following_pages = update[idx+1:]
            
            if page in rule_dict:
                intersection = rule_dict[page].intersection(following_pages)
                
                if len(intersection) > 0:
                    swap_idx = np.argwhere(update == list(intersection)[0]).item()
                    update[idx], update[swap_idx] = update[swap_idx], update[idx]

    return update

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = [line.strip() for line in file.readlines()]
        rules = np.array([line.split('|') for line in data if '|' in line], dtype=int)
        updates = [np.array(line.split(','), dtype=int) for line in data if ',' in line]

        rule_dict = create_rule_dict(rules)
        
        invalid_updates = []
        for update in updates:
            if not is_valid_update(update, rule_dict):
                invalid_updates.append(update)
                correct_update(update, rule_dict)
        
        middle_page_sum = np.sum([update[update.shape[0] // 2] for update in invalid_updates])
        print(middle_page_sum)
