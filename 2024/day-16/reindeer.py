from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from functools import partial

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def next(self, location):
        if self == Direction.NORTH:
            return (location[0] - 1, location[1])
        elif self == Direction.EAST:
            return (location[0], location[1] + 1)
        elif self == Direction.SOUTH:
            return (location[0] + 1, location[1])
        elif self == Direction.WEST:
            return (location[0], location[1] - 1)
    
    def turn_left(self, times):
        return Direction((self.value - times) % 4)
    
    def turn_right(self, times):
        return Direction((self.value + times) % 4)

@dataclass(order=True)
class Reindeer:
    location: tuple[int, int] = field(compare=False)
    direction: Direction = field(compare=False)
    path: set[tuple[int, int]] = field(default_factory=set, compare=False)
    score: int = 0

    def move(self, direction):
        num_left_turns = (self.direction.value - direction.value) % len(Direction)
        num_right_turns = (direction.value - self.direction.value) % len(Direction)
        turns = np.minimum(num_left_turns, num_right_turns)
        self.score += turns * 1000
        self.direction = direction
            
        self.location = direction.next(self.location)
        self.score += 1
        
        self.path.add(self.location)
    
    def neighbor_tiles(self):
        mapper = partial(Direction.next, location=self.location)
        return list(map(mapper, Direction))
