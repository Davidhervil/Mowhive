import pytest
from mowhive import read_mower_line, MowController, read_input, MowerObstructingPath, MowerObstructingPath, AttemptedOutOfBoundsMovement
from mowhive.mowerstate import CollitionProtocols

@pytest.mark.parametrize("case,expected", [
    (["5 5",
      "1 2 N",
      "LMLMLMLMM",
      "3 3 E",
      "MMRMMRMRRM",
     ], 
     ["1 3 N", "5 1 E"]),
    (["2 2",
      "0 0 N",
      "MMRMMRMRM",
      "2 0 E",
      "LLMMRMML",
     ], 
     ["1 1 W", "0 2 W"]),
     (["2 2",
      "0 0 N",
      "MMRMMRMRM",
      "0 2 E",
      "LLMMRMML",
     ], 
     ["1 0 W", "0 2 W"])
     ])
def test_successfull_default_swarm(case, expected):
    dims = case[0].split(" ")
    dimx = int(dims[0])
    dimy = int(dims[1])
    mow_hive = MowController(dimx, dimy)
    read_input(case[1:], mow_hive)
    mow_hive.move_swarm()

    state = mow_hive.show_current_state()
    assert state == expected


@pytest.mark.parametrize("case,expected", [
    (["5 5",
      "0 2 N",
      "LMLMLMLMM",
      "3 3 E",
      "MMRMMRMRRM",
     ], 
     ["1 3 N", "5 1 E"]),
     ])
def test_abort_collition_protocol_swarm_fail_outofbound(case, expected):
    with pytest.raises(AttemptedOutOfBoundsMovement):
        dims = case[0].split(" ")
        dimx = int(dims[0])
        dimy = int(dims[1])
        mow_hive = MowController(dimx, dimy, collition_protocol=CollitionProtocols.ABORT_ON_COLLITIONS)
        read_input(case[1:], mow_hive)
        mow_hive.move_swarm()

        state = mow_hive.show_current_state()
        assert state == expected

@pytest.mark.parametrize("case,expected", [
     (["2 2",
      "0 0 N",
      "MMRMMRMRM",
      "0 2 E",
      "LLMMRMML",
     ], 
     ["1 0 W", "0 2 W"])
     ])
def test_abort_collition_protocol_swarm_fail_obstructingmower(case, expected):
    with pytest.raises(MowerObstructingPath):
        dims = case[0].split(" ")
        dimx = int(dims[0])
        dimy = int(dims[1])
        mow_hive = MowController(dimx, dimy, collition_protocol=CollitionProtocols.ABORT_ON_COLLITIONS)
        read_input(case[1:], mow_hive)
        mow_hive.move_swarm()

        state = mow_hive.show_current_state()
        assert state == expected

@pytest.mark.parametrize("case,expected", [
     (["2 2",
      "0 0 N",
      "MMRMMRMRM",
      "0 2 E",
      "LLMMRMRM",
     ], 
     ["0 2 E", "1 2 E"])
     ])
def test_await_collition_protocol_swarm_await_on_collision(case,expected):
    dims = case[0].split(" ")
    dimx = int(dims[0])
    dimy = int(dims[1])
    mow_hive = MowController(dimx, dimy, collition_protocol=CollitionProtocols.AWAIT_ON_COLLITIONS)
    read_input(case[1:], mow_hive)
    mow_hive.move_swarm()

    state = mow_hive.show_current_state()
    assert state == expected