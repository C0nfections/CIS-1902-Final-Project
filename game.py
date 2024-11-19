import random
from dataclasses import dataclass

GRID_SIZE = 4
TILE_SIZE = 800 // GRID_SIZE
VELOCITY = 50

@dataclass
class Position:
    row: int
    col: int
    
    def __hash__(self):
        return hash((self.row, self.col))
    
    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.row == other.row and self.col == other.col

class Tile:
    def __init__(self, value: int, row: int, col: int):
        self.value = value
        self.pos = Position(row, col)
        self.x = col * TILE_SIZE
        self.y = row * TILE_SIZE
        self.vx = 0
        self.vy = 0
        self.merging = False
        self.moved = False
        
    def update(self) -> bool:
        if abs(self.vx) < 0.1 and abs(self.vy) < 0.1:
            self.vx = 0
            self.vy = 0
            return False
            
        target_x = self.pos.col * TILE_SIZE
        target_y = self.pos.row * TILE_SIZE
        
        dx = target_x - self.x
        dy = target_y - self.y
        
        if abs(dx) < abs(self.vx):
            self.x = target_x
            self.vx = 0
        else:
            self.x += self.vx
            
        if abs(dy) < abs(self.vy):
            self.y = target_y
            self.vy = 0
        else:
            self.y += self.vy
        
        return self.vx != 0 or self.vy != 0

    def stop(self):
        self.vx = 0
        self.vy = 0
        self.x = self.pos.col * TILE_SIZE
        self.y = self.pos.row * TILE_SIZE

class Board:
    def __init__(self):
        self.tiles: dict[Position, Tile] = {}
        self.moving_tiles: set[Tile] = set()
        
    def get_tile(self, pos: Position) -> Tile | None:
        return self.tiles.get(pos)
        
    def add_tile(self, tile: Tile):
        self.tiles[tile.pos] = tile
        
    def remove_tile(self, pos: Position):
        if pos in self.tiles:
            del self.tiles[pos]
            
    def get_empty_positions(self) -> list[Position]:
        empty = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                pos = Position(row, col)
                if pos not in self.tiles:
                    empty.append(pos)
        return empty

    def start_move(self, tile: Tile, direction: tuple[int, int]):
        dx, dy = direction
        tile.vx = dx * VELOCITY
        tile.vy = dy * VELOCITY
        self.moving_tiles.add(tile)

class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.best_score = self.load_best_score()
        self.moving = False
        self.moved_this_turn = False
        self.reset()

    def reset(self):
        self.board = Board()
        self.score = 0
        self.moving = False
        self.moved_this_turn = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = self.board.get_empty_positions()
        if empty:
            pos = random.choice(empty)
            value = 4 if random.random() > 0.9 else 2
            new_tile = Tile(value, pos.row, pos.col)
            self.board.add_tile(new_tile)

    def find_farthest_position(self, pos: Position, dy: int, dx: int) -> tuple[Position, bool]:
        prev = Position(pos.row, pos.col)
        while True:
            next_pos = Position(prev.row + dy, prev.col + dx)
            if not (0 <= next_pos.row < GRID_SIZE and 0 <= next_pos.col < GRID_SIZE):
                return prev, False
            
            next_tile = self.board.get_tile(next_pos)
            if next_tile is None:
                prev = next_pos
            elif next_tile.value == self.board.get_tile(pos).value and not next_tile.merging:
                return next_pos, True
            else:
                return prev, False

    def process_movement(self, direction: str):
        if self.moving:
            return
            
        velocity_map = {
            'left': (0, -1),
            'right': (0, 1),
            'up': (-1, 0),
            'down': (1, 0)
        }
        dy, dx = velocity_map[direction]
        
        self.moved_this_turn = False
        for tile in self.board.tiles.values():
            tile.merging = False
            tile.moved = False
        
        positions = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
        if dx > 0:  # right
            positions.sort(key=lambda p: p[1], reverse=True)
        elif dx < 0:  # left
            positions.sort(key=lambda p: p[1])
        elif dy > 0:  # down
            positions.sort(key=lambda p: p[0], reverse=True)
        else:  # up
            positions.sort(key=lambda p: p[0])
            
        pending_merges = {}
        
        for row, col in positions:
            pos = Position(row, col)
            tile = self.board.get_tile(pos)
            
            if tile is None:
                continue
                
            farthest_pos, will_merge = self.find_farthest_position(pos, dy, dx)
            
            if farthest_pos.row == row and farthest_pos.col == col:
                continue
                
            self.board.remove_tile(pos)
            
            if will_merge:
                if farthest_pos not in pending_merges:
                    pending_merges[farthest_pos] = []
                pending_merges[farthest_pos].append(tile)
                tile.merging = True
            else:
                tile.pos = farthest_pos
                self.board.add_tile(tile)
            
            tile.moved = True
            
            final_x = farthest_pos.col * TILE_SIZE
            final_y = farthest_pos.row * TILE_SIZE + 100
            
            dx_pixels = final_x - tile.x
            dy_pixels = final_y - tile.y
            distance = (dx_pixels ** 2 + dy_pixels ** 2) ** 0.5
            
            if distance > 0:
                tile.vx = (dx_pixels / distance) * VELOCITY
                tile.vy = (dy_pixels / distance) * VELOCITY
                self.board.moving_tiles.add(tile)
                self.moved_this_turn = True
        
        for pos, tiles in pending_merges.items():
            existing_tile = self.board.get_tile(pos)
            if existing_tile:
                tiles.append(existing_tile)
            
            keeper = tiles[0]
            keeper.value *= 2
            keeper.pos = pos
            keeper.moved = True
            self.score += keeper.value
            if self.score > self.best_score:
                self.best_score = self.score
                self.save_best_score()
            
            self.board.add_tile(keeper)
            
            for tile in tiles[1:]:
                if tile in self.board.moving_tiles:
                    self.board.moving_tiles.remove(tile)
        
        if self.moved_this_turn:
            self.moving = True

    def update(self) -> None:
        if not self.moving:
            return
            
        still_moving = False
        
        for tile in list(self.board.moving_tiles):
            if tile.update():
                still_moving = True
            else:
                self.board.moving_tiles.remove(tile)
        
        if not still_moving:
            self.moving = False
            for tile in self.board.tiles.values():
                tile.stop()
                tile.merging = False
            
            if self.moved_this_turn:
                self.add_random_tile()
                self.moved_this_turn = False

    # def load_final_score(self) -> int:
    #     try:
    #         with open('final_score.txt', 'r') as f:
    #             score = f.read().strip()
    #             return int(score) if score.isdigit() else -1
    #     except (FileNotFoundError, IOError, ValueError):
    #         return -1

    def load_best_score(self) -> int:
        try:
            with open('best_score.txt', 'r') as f:
                score = f.read().strip()
                return int(score) if score.isdigit() else 0
        except (FileNotFoundError, IOError, ValueError):
            return 0
        
    # def save_final_score(self) -> None:
    #     try:
    #         with open('best_score.txt', 'w') as f:
    #             f.write(str(self.score))
    #     except IOError:
    #         print("Warning: Could not save final score")

    def save_best_score(self) -> None:
        try:
            with open('best_score.txt', 'w') as f:
                f.write(str(self.best_score))
        except IOError:
            print("Warning: Could not save best score")


    def get_score(self) -> int:
        return self.score
    
    def is_game_over(self) -> bool:
        if len(self.board.tiles) < GRID_SIZE * GRID_SIZE:
            return False
            
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                pos = Position(r, c)
                tile = self.board.get_tile(pos)
                if tile:
                    for dr, dc in [(0, 1), (1, 0)]:
                        next_pos = Position(r + dr, c + dc)
                        if (0 <= next_pos.row < GRID_SIZE and 
                            0 <= next_pos.col < GRID_SIZE):
                            next_tile = self.board.get_tile(next_pos)
                            if next_tile and tile.value == next_tile.value:
                                return False
        return True