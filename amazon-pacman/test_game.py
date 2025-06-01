import pytest
from player import Player
from ghost import Ghost
from maze import Maze
from utils import CELL_SIZE

def test_player_initialization():
    player = Player()
    assert player is not None
    assert hasattr(player, 'rect')
    assert hasattr(player, 'direction')

def test_ghost_initialization():
    ghost = Ghost('blinky', (0, 0))
    assert ghost is not None
    assert ghost.name == 'blinky'
    assert hasattr(ghost, 'rect')

def test_maze_initialization():
    maze = Maze()
    assert maze is not None
    assert hasattr(maze, 'layout')
    assert CELL_SIZE > 0