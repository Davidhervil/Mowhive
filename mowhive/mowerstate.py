from enum import Enum
from typing import Optional, List

class Cardinal(Enum):
    N = 0
    E = 1
    S = 2
    W = 3

class Movements(Enum):
    # We take advantage of the algebraic properties of the modulo N set (modulo 4 in this case) 
    L = len(Cardinal) - 1
    R = 1
    M = 2

class MovementResult:
    pass

class MovementSucess(MovementResult):
    pass

class ObstructingMower(MovementResult):
    def __init__(self, mow_id: int) -> None:
        self.mow_int = mow_id

class OutOfBounds(MovementResult):
    pass

class UnknownObstacle(MovementResult):
    pass

class CollitionProtocols(Enum):
    STOP_ON_COLLITIONS=0
    ABORT_ON_COLLITIONS=1
    AWAIT_ON_COLLITIONS=3

class Coord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Coord(self.x +other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

class Mower:
    def __init__(self, location: Coord, orientation: Cardinal, desired_path: Optional[List[Movements]]=None):
        self.location = location
        self.orientation = orientation
        self.desired_path = desired_path
    
    def __str__(self):
        return f"Mower<location:{self.location}, orientation:{self.orientation.name}, remaining_path:{self.desired_path}>"
    
    def __eq__(self, other) -> bool:
        return self.location == other.location and self.orientation == other.orientation 