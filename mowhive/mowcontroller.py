import enum
from queue import Queue
from typing import List, Tuple, Optional
from .mowerstate import Mower, Cardinal, Coord, CollitionProtocols, MovementResult, MovementSucess, Movements, ObstructingMower, OutOfBounds, UnknownObstacle
from .errors import AttemptedOutOfBoundsMovement, InvalidOperationExecution, PlaceOccupied, MowerObstructingPath, UnknownObstacleinPath

# Thought as North East South West, 
# how much you'd need to add to a coordinate to displace in that direction
DISPLACEMENT_OPERATIONS = [Coord(0,1), Coord(1,0), Coord(0,-1), Coord(-1,0)]


class MowController:
    def __init__(self, plateau_size_x: int, plateau_size_y: int, collition_protocol: CollitionProtocols = CollitionProtocols.STOP_ON_COLLITIONS, ignore_unregisterable_mowers=False):
        self.mowers: List[Mower] = []
        self.plateau_size: Tuple[int, int] = (plateau_size_x, plateau_size_y)
        self.ignore_unregisterable_mowers = ignore_unregisterable_mowers
        #TODO implement collition protocols
        self.collition_protocol = collition_protocol
    
    def who_is_there_c(self, c: Coord) -> int:
        """ Returns the index of the mower in the coordinate c present in controller.mowers.
            If there is none, None will be returned
            
            :param c: Coord to check
        """
        return self.who_is_there(c.x, c.y)
    
    def who_is_there(self, x: int, y: int) -> int:
        """ Returns the index of the mower in the x and y coordinates present in controller.mowers.
            If there is none, None will be returned
            
            :param x: x coordinate to check
            :param y: y coordinate to check
        """
        for i, m in enumerate(self.mowers):
            if m.location.x == x and m.location.y == y:
                return i

    def is_a_mower_there_c(self, c: Coord)-> bool:
        """ Returns a boolean according to whether there is a mower in the Coord c's x and y components
            
            :param c: Coord to check
        """
        return self.is_a_mower_there(c.x, c.y)

    def is_a_mower_there(self, x: int, y:int)-> bool:
        """ Returns a boolean according to whether there is a mower in the x and y coordinate
            
            :param x: x coordinate to check
            :param y: y coordinate to check
        """
        return any(m.location.x == x and m.location.y == y for m in self.mowers)

    def register_mower(self, x: int, y: int, o: Cardinal, desired_path: Optional[List[Movements]]=None) -> bool:
        """ Register mower in controller with the respective coordinates, orientation and optional desired path

            :param x: x coordinate of mower
            :param y: y coordinate of mower
            :param o: Orientation of mower of type Cardinal
            :param desired_path: Optional desired path, List[Movements] with default None
        """
        if self.is_a_mower_there(x,y):
            if self.ignore_unregisterable_mowers:
                return False
            else:
                raise PlaceOccupied(x,y)
        
        self.mowers.append(Mower(Coord(x,y), o, desired_path))
        return True
    
    def move_mower(self, mow_id: int) -> MovementResult:
        """ Move mower towards the direction it is facing

            :param mow_id: index of mower in MowerController.mowers
        """
        mowie = self.mowers[mow_id]
        destination_coord = mowie.location + DISPLACEMENT_OPERATIONS[mowie.orientation.value]

        # Check that is within the plateau
        if 0 <= destination_coord.x <= self.plateau_size[0] and 0 <= destination_coord.y <= self.plateau_size[1]:
            if self.is_a_mower_there_c(destination_coord):
                who_is = self.who_is_there_c(destination_coord)
                return ObstructingMower(who_is)
            else:
                mowie.location = destination_coord
                return MovementSucess()
        else:
            return OutOfBounds()
        
    def rotate_mower(self, mow_id: int, direction: Movements) -> MovementResult:
        """ Rotate mower in mow_id according to direction

            :param mow_id: index of mower in MowerController.mowers
            :param direction: direction of type Movements. Should be L or R
        """
        if direction not in [Movements.L, Movements.R]:
            raise InvalidOperationExecution(direction, "Tried to use a Movement that is not of rotation kind.")

        mowie = self.mowers[mow_id]
        final_direction_value = (mowie.orientation.value + direction.value) % len(Cardinal)
        final_direction = Cardinal(final_direction_value)
        mowie.orientation = final_direction
        return MovementSucess()
    
    def move_swarm(self):
        """ Perform mower movement simulation/execution
            we use a queue to allow for AWAIT_ON_COLLITIONS protocol
            but if not needed, a simple cycle around the mowers is enough
        """
        to_process: Queue[Tuple[int, Mower]] = Queue()
        for i, m in enumerate(self.mowers):
            to_process.put((i,m))

        deferred = 0
        # Continue until all mowers are ready or all are deferred (in case of AWAIT_ON_COLLITIONS) 
        while to_process.qsize() !=0 and deferred != len(self.mowers):
            i, m = to_process.get()
            if m.desired_path:
                # Try to complete the mower's route
                while len(m.desired_path) != 0:
                    operation = m.desired_path[0]
                    result = MovementResult()

                    if operation in [Movements.L, Movements.R]:
                        result = self.rotate_mower(i, operation)
                    elif operation == Movements.M:
                        result = self.move_mower(i)

                    # All good
                    if type(result) is MovementSucess:
                        deferred = 0
                        m.desired_path.pop(0)
                    
                    # Something came up, work according protocols
                    # Ignore collitions
                    if self.collition_protocol is CollitionProtocols.STOP_ON_COLLITIONS:
                        if type(result) in [ObstructingMower, OutOfBounds, UnknownObstacle]:
                            m.desired_path.pop(0)                    
                    
                    # Abort on colliition
                    elif self.collition_protocol is CollitionProtocols.ABORT_ON_COLLITIONS:
                        if type(result) is ObstructingMower:
                            raise MowerObstructingPath( self.mowers[result.mow_int].location.x,
                                                        self.mowers[result.mow_int].location.y)
                        elif type(result) is OutOfBounds:
                            raise AttemptedOutOfBoundsMovement(m)
                        elif type(result) is UnknownObstacle:
                            raise UnknownObstacleinPath(m)
                    
                    # Await on colliition
                    elif self.collition_protocol is CollitionProtocols.AWAIT_ON_COLLITIONS:
                        # Requeue mower in hope the obstructing one will move
                        if type(result) is ObstructingMower:
                            deferred +=1
                            to_process.put((i,m))
                            break
                        # Ignore other situations
                        elif type(result) in [OutOfBounds, UnknownObstacle]:
                            deferred = 0
                            m.desired_path.pop(0)

    def show_current_state(self):
        out = []
        for m in self.mowers:
            out.append(f"{m.location.x} {m.location.y} {m.orientation.name}")
        return out
    
    def print_current_state(self):
        for s in self.show_current_state():
            print(s)