from .types.vector import Vector
from enum import Enum

class Tile():
    def __init__(self, tile_type, name : str, position : Vector = None):
        self.type = tile_type
        self.name = name
        self.position = position
        self.found = False  # Added found attribute

    def __str__(self):
        return self.name
    
    def print_info(self):
        print(self.name, self.type, self.position.x + 1, self.position.y + 1)

class TileMap():
    def __init__(self, width : int, height : int):
        self.generate_tile_types()
        self.width = width
        self.height = height
        self.tiles = [[Tile(self.TileType.EMPTY, "Empty", Vector(x, y)) for y in range(height)] for x in range(width)]

    def get_tile(self, x : int, y : int) -> Tile:
        return self.tiles[x][y]
    
    def set_tile(self, x : int, y : int, tile : Tile):
        self.tiles[x][y] = tile
    
    def generate_tile_types(self, type_names=None) -> Enum:
        """
        Generate a new TileType-like enum with the given type names.
        
        Args:
            type_names (list, optional): List of strings representing tile type names.
                Defaults to standard tile types if None.
            
        Returns:
            Enum: A new Enum class with the given type names as members
        """
        if type_names is None:
            type_names = ["WALL", "FLOOR"]
        base_types = {
            'EMPTY': 0,
        }
        self.TileType = Enum('TileType', {**base_types, **{name: i+len(base_types) for i, name in enumerate(type_names)}})        

    
