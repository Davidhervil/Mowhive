import sys
from mowhive.utils import Cardinal, Movements, read_input, read_mower_line
from mowhive.mowcontroller import MowController

if __name__ == "__main__":
    """ It is assumed that data will come in through the standard input
    """
    dimx = 0
    dimy = 0
    mow_hive = None
    line = input()
    dims = line.split(" ")
    dimx = int(dims[0])
    dimy = int(dims[1])
    mow_hive = MowController(dimx, dimy, ignore_unregisterable_mowers=False)
    read_input(sys.stdin, mow_hive)

    mow_hive.move_swarm()
    state = mow_hive.show_current_state()
    mow_hive.print_current_state()