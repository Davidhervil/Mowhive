import pytest

from mowhive import Cardinal, Coord, MovementSucess, Mower, MowController, Movements
from mowhive.errors import InvalidOperationExecution, PlaceOccupied
from mowhive.mowerstate import ObstructingMower, OutOfBounds


@pytest.mark.parametrize("plateau_size,unregistered_mowers,expected_mowers,ignore_unregisterable,ignored", 
[
    ((5,5),
     [ 
        (1,1,Cardinal.N),
        (1,2,Cardinal.S),
        (2,1,Cardinal.E),
        (2,2,Cardinal.W)
     ],
     [
        Mower(Coord(1,1),Cardinal.N),
        Mower(Coord(1,2),Cardinal.S),
        Mower(Coord(2,1),Cardinal.E),
        Mower(Coord(2,2),Cardinal.W),
     ],
     False,
     False,
    ),
    ((5,5),
     [ 
        (1,1,Cardinal.N),
        (1,2,Cardinal.S),
        (1,1,Cardinal.E),
        (2,2,Cardinal.W)
     ],
     [
        Mower(Coord(1,1),Cardinal.N),
        Mower(Coord(1,2),Cardinal.S),
        Mower(Coord(2,2),Cardinal.W),
     ],
     True,
     True,
    ),
])
def test_register_mowner_success(plateau_size, unregistered_mowers, expected_mowers, ignore_unregisterable, ignored):
    mow_hive = MowController(plateau_size[0], plateau_size[1], ignore_unregisterable_mowers=ignore_unregisterable)
    sucessful_registration = True
    for um in unregistered_mowers:
        sucessful_registration &= mow_hive.register_mower(um[0], um[1], um[2])
    
    assert len(mow_hive.mowers) == len(expected_mowers)
    assert mow_hive.mowers == expected_mowers
    assert sucessful_registration == (not ignored)

@pytest.mark.parametrize("plateau_size,unregistered_mowers,expected_mowers,ignore_unregisterable", 
[
    ((5,5),
     [
        (1,1,Cardinal.N),
        (1,2,Cardinal.S),
        (1,1,Cardinal.E),
        (2,2,Cardinal.W)
     ],
     [
        Mower(Coord(1,1),Cardinal.N),
        Mower(Coord(1,2),Cardinal.S),
        Mower(Coord(2,2),Cardinal.W),
     ],
     False,
    ),
])
def test_register_mowner_failed(plateau_size, unregistered_mowers, expected_mowers, ignore_unregisterable):
    with pytest.raises(PlaceOccupied):
        mow_hive = MowController(plateau_size[0], plateau_size[1], ignore_unregisterable_mowers=ignore_unregisterable)
        sucessful_registration = True
        for um in unregistered_mowers:
            sucessful_registration &= mow_hive.register_mower(um[0], um[1], um[2])
        
        assert len(mow_hive.mowers) == len(expected_mowers)
        assert mow_hive.mowers == expected_mowers


@pytest.mark.parametrize("plateau_size,unregistered_mower,expected_mower,expected_result", 
[
    ((5,5),
     (1,1,Cardinal.N),
     Mower(Coord(1,2),Cardinal.N),
     MovementSucess()
    ),
    ((5,5),
     (1,1,Cardinal.S),
     Mower(Coord(1,0),Cardinal.S),
     MovementSucess()
    ),
    ((5,5),
     (1,1,Cardinal.E),
     Mower(Coord(2,1),Cardinal.E),
     MovementSucess()
    ),
    ((5,5),
     (1,1,Cardinal.W),
     Mower(Coord(0,1),Cardinal.W),
     MovementSucess()
    ),
])
def test_move_mowner(plateau_size, unregistered_mower, expected_mower, expected_result):
    mow_hive = MowController(plateau_size[0], plateau_size[1])
    mow_hive.register_mower(unregistered_mower[0], unregistered_mower[1], unregistered_mower[2])
    result = mow_hive.move_mower(0)
    assert type(result) is type(expected_result)
    assert mow_hive.mowers[0] == expected_mower

@pytest.mark.parametrize("plateau_size,unregistered_mower,expected_mower,expected_result", 
[
    ((5,5),
     (5,5,Cardinal.N),
     Mower(Coord(5,5),Cardinal.N),
     OutOfBounds()
    ),
    ((5,5),
     (5,5,Cardinal.E),
     Mower(Coord(5,5),Cardinal.E),
     OutOfBounds()
    ),
    ((5,5),
     (0,0,Cardinal.S),
     Mower(Coord(0,0),Cardinal.S),
     OutOfBounds()
    ),
    ((5,5),
     (0,0,Cardinal.W),
     Mower(Coord(0,0),Cardinal.W),
     OutOfBounds()
    ),
])
def test_move_mowner_outofbounds(plateau_size, unregistered_mower, expected_mower, expected_result):
    mow_hive = MowController(plateau_size[0], plateau_size[1])
    mow_hive.register_mower(unregistered_mower[0], unregistered_mower[1], unregistered_mower[2])
    result = mow_hive.move_mower(0)
    assert type(result) is type(expected_result)
    assert mow_hive.mowers[0] == expected_mower

@pytest.mark.parametrize("plateau_size,unregistered_mower,obstructing_mower,expected_mower, expected_result", 
[
    ((5,5),
     (1,1,Cardinal.N),
     (1,2,Cardinal.N),
     Mower(Coord(1,1),Cardinal.N),
     ObstructingMower(1)
    ),
    ((5,5),
     (1,1,Cardinal.S),
     (1,0,Cardinal.S),
     Mower(Coord(1,1),Cardinal.S),
     ObstructingMower(1)
    ),
    ((5,5),
     (1,1,Cardinal.E),
     (2,1,Cardinal.E),
     Mower(Coord(1,1),Cardinal.E),
     ObstructingMower(1)
    ),
    ((5,5),
     (1,1,Cardinal.W),
     (0,1,Cardinal.W),
     Mower(Coord(1,1),Cardinal.W),
     ObstructingMower(1)
    ),
])
def test_move_mowner_obstructing_mower(plateau_size, unregistered_mower, obstructing_mower, expected_mower, expected_result):
    mow_hive = MowController(plateau_size[0], plateau_size[1])
    mow_hive.register_mower(unregistered_mower[0], unregistered_mower[1], unregistered_mower[2])
    mow_hive.register_mower(obstructing_mower[0], obstructing_mower[1], obstructing_mower[2])
    result = mow_hive.move_mower(0)
    assert type(result) is type(expected_result)
    assert result.mow_int == 1
    assert mow_hive.mowers[0] == expected_mower

@pytest.mark.parametrize("plateau_size,unregistered_mower,operation,expected_mower,expected_result", 
[
    ((5,5),
     (1,1,Cardinal.N),
     Movements.L,
     Mower(Coord(1,1),Cardinal.W),
     MovementSucess()
    ),
    ((5,5),
     (1,1,Cardinal.S),
     Movements.L,
     Mower(Coord(1,1),Cardinal.E),
     MovementSucess()
    ),
    ((5,5),
     (1,1,Cardinal.E),
     Movements.R,
     Mower(Coord(1,1),Cardinal.S),
     MovementSucess()
    ),
    ((5,5),
     (1,1,Cardinal.W),
     Movements.R,
     Mower(Coord(1,1),Cardinal.N),
     MovementSucess()
    ),
])
def test_rotate_mowner(plateau_size, unregistered_mower, operation, expected_mower, expected_result):
    mow_hive = MowController(plateau_size[0], plateau_size[1])
    mow_hive.register_mower(unregistered_mower[0], unregistered_mower[1], unregistered_mower[2])
    result = mow_hive.rotate_mower(0, operation)
    assert type(result) is type(expected_result)
    assert mow_hive.mowers[0] == expected_mower


@pytest.mark.parametrize("plateau_size,unregistered_mower,operation,expected_mower,expected_result", 
[
    ((5,5),
     (1,1,Cardinal.N),
     Movements.M,
     Mower(Coord(1,1),Cardinal.W),
     MovementSucess()
    ),
])
def test_rotate_mowner_fail(plateau_size, unregistered_mower, operation, expected_mower, expected_result):
    with pytest.raises(InvalidOperationExecution):
        mow_hive = MowController(plateau_size[0], plateau_size[1])
        mow_hive.register_mower(unregistered_mower[0], unregistered_mower[1], unregistered_mower[2])
        result = mow_hive.rotate_mower(0, operation)
        assert type(result) is type(expected_result)
        assert mow_hive.mowers[0] == expected_mower