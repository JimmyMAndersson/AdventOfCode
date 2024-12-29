import os
from collections import defaultdict
from queue import Queue

# --- Part Two ---
# There are still way too many results to go through them all. You'll have to find the LAN party another way and go there yourself.
#
# Since it doesn't seem like any employees are around, you figure they must all be at the LAN party. If that's true, the LAN party will be the largest set of computers that are all connected to each other. That is, for each computer at the LAN party, that computer will have a connection to every other computer at the LAN party.
#
# In the above example, the largest set of computers that are all connected to each other is made up of co, de, ka, and ta. Each computer in this set has a connection to every other computer in the set:
#
# ka-co
# ta-co
# de-co
# ta-ka
# de-ta
# ka-de
# The LAN party posters say that the password to get into the LAN party is the name of every computer at the LAN party, sorted alphabetically, then joined together with commas. (The people running the LAN party are clearly a bunch of nerds.) In this example, the password would be co,de,ka,ta.
#
# What is the password to get into the LAN party?


if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        connections = defaultdict(set)

        for line in file:
            _from, _to = line.strip().split('-')
            connections[_from].add(_to)
            connections[_to].add(_from)
        
        queue = Queue()
        visited = set()

        for computer in connections:
            for connection in connections[computer]:
                queue.put(set([computer, connection]))
        
        largest_set = set()

        while not queue.empty():
            current = queue.get()

            if len(current) > len(largest_set):
                largest_set = current

            intersection = set.intersection(*[connections[computer] for computer in current]) - current
            
            for computer in intersection:
                new_set = current.union(set([computer]))
                if tuple(sorted(new_set)) in visited:
                    continue
            
                visited.add(tuple(sorted(new_set)))
                queue.put(new_set)
        
        print(','.join(sorted(largest_set)))