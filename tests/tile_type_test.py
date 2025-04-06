import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.panda_util.tilemap import Tile

tilemap = TileMap(10, 10)
print(", ".join([tile.name for tile in tilemap.TileType]))

