from dataclasses import dataclass, field

@dataclass(order=True, unsafe_hash=True)
class Tile:
    location: tuple[int, int] = field(compare=False)
    distance: int = field(compare=True, default_factory=int)

    def neighbors(self):
        x, y = self.location
        candidates = [
            Tile((x, y - 1), self.distance + 1),
            Tile((x, y + 1), self.distance + 1),
            Tile((x - 1, y), self.distance + 1),
            Tile((x + 1, y), self.distance + 1)
        ]
        
        return [tile for tile in candidates if 0 <= tile.location[0] <= 70 and 0 <= tile.location[1] <= 70]
