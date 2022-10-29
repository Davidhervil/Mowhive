from typing import Tuple
from .mowerstate import Cardinal, Movements
from .mowcontroller import MowController

def read_mower_line(line: str)-> Tuple[int, int, Cardinal]:
    m_data = line.split(" ")
    x = int(m_data[0])
    y = int(m_data[1])
    orientation = Cardinal[m_data[2]]
    return x,y,orientation

def read_input(stream, controller: MowController):
    i = 0
    for line in stream:
        line = line.strip("\n")
        if i % 2 == 0: # Mowner
            x,y,orientation = read_mower_line(line)
            controller.register_mower(x, y, orientation)
        else:
            path = list(map(lambda op: Movements[op], line))
            controller.mowers[-1].desired_path = path
        i+=1