from enum import Enum
from typing import Tuple
import numpy as np

class Guard:
    class Direction(Enum):
        UP = '^'
        RIGHT = '>'
        DOWN = 'v'
        LEFT = '<'

        def forward(self):
            if self == Guard.Direction.UP:
                return (-1, 0)
            elif self == Guard.Direction.RIGHT:
                return (0, 1)
            elif self == Guard.Direction.DOWN:
                return (1, 0)
            else:
                return (0, -1)
        
        def turn_right(self):
            if self == Guard.Direction.UP:
                return Guard.Direction.RIGHT
            elif self == Guard.Direction.RIGHT:
                return Guard.Direction.DOWN
            elif self == Guard.Direction.DOWN:
                return Guard.Direction.LEFT
            elif self == Guard.Direction.LEFT:
                return Guard.Direction.UP
    
    class StopReason(Enum):
        LOOP = 0
        OUT_OF_BOUNDS = 1

    def __init__(self, map: np.ndarray, obstacle_location: Tuple[int, int] = None):
        self.__map = map
        self.__obstacle_location = obstacle_location
        
        for direction in Guard.Direction.__members__.values():
            if direction.value in self.__map:
                self.direction = direction
                self.location = tuple(x.item() for x in np.where(map == direction.value))
                self.visited = set()
                self.visited_with_direction = set()
                break

    def __next_location(self) -> Tuple[int, int]:
        return tuple(x + off for x, off in zip(self.location, self.direction.forward()))
    
    def __should_turn_right(self) -> bool:
        return self.__map[self.__next_location()] == '#' or self.__next_location() == self.__obstacle_location
    
    def __should_move(self) -> bool:
        next_location = self.__next_location()
        if next_location[0] < 0 or next_location[0] >= self.__map.shape[0]:
            return False
        if next_location[1] < 0 or next_location[1] >= self.__map.shape[1]:
            return False
        
        return True
    
    def move(self) -> StopReason:
        if (self.location, self.direction) in self.visited_with_direction:
            return Guard.StopReason.LOOP
        
        self.visited.add(self.location)
        self.visited_with_direction.add((self.location, self.direction))
        
        if not self.__should_move():
            return Guard.StopReason.OUT_OF_BOUNDS
        elif self.__should_turn_right():
            self.direction = self.direction.turn_right()
            return None
        else:
            self.location = self.__next_location()
            return None
