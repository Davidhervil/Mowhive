from .mowerstate import Movements, Mower

class MownerRegisterException(Exception):
    def __str__(self) -> str:
        return f"{super().__str__()} Could not register Mower."

class PlaceOccupied(MownerRegisterException):
    def __init__(self, x:int, y:int, *args: object):
        super().__init__(*args)
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"{super().__str__()} Coordinates ({self.x}, {self.y}) are already occupied."

class InvalidOperationExecution(Exception):
    def __init__(self, operation: Movements, *args: object):
        super().__init__(*args)
        self.operation = operation

    def __str__(self) -> str:
        return f"{super().__str__()} Operation {self.operation} could not be executed."

class MovementException(Exception):
    def __init__(self, m: Mower, *args: object) -> None:
        self.mower = m
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{super().__str__()} Cannot move {self.mower}. "

class AttemptedOutOfBoundsMovement(MovementException):
    def __str__(self) -> str:
        return f"{super().__str__()} Attempted to move mower out of plateau bounds."

class MowerObstructingPath(MovementException):
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"{super().__str__()} Coordinates ({self.x}, {self.y}) are already occupied by a mower."

class UnknownObstacleinPath(MovementException):
    def __str__(self) -> str:
        return f"{super().__str__()} Unknown Obstacle in front of mower."
