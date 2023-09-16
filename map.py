from rng import rng
import math
import pygame as pg
import copy

# grid is a 2d grid of chunks of tiles
class Map():
    def __init__(self, chunk_size, roughness, gradient, load_distance,  tile_size, offset, min_value, max_value):
        self.chunk_size = chunk_size
        self.offset = offset
        self.roughness = roughness
        self.gradient = gradient
        self.load_distance = load_distance
        self.tile_size = tile_size
        self.pixels_per_chunk = tile_size*chunk_size
        self.loaded_chunks = {}
        self.blank_map =[]
        self.min_value = min_value
        self.max_value = max_value
        for x in range(chunk_size):
            self.blank_map.append([])
            for y in range(chunk_size):
                self.blank_map[x].append(0)
    
    def load_chunk(self, y_grid, x_grid):
        map = set_edges(copy.deepcopy(self.blank_map), self.chunk_size-1, x_grid, y_grid, self.gradient, self.offset, self.roughness)
        map= daimond_square(x_grid, y_grid, self.chunk_size-1, map, self.gradient, self.roughness, self.min_value, self.max_value)
        self.loaded_chunks[(y_grid, x_grid)] = map
  
    def check_loaded_chunks(self, x_pos, y_pos):
        x_grid = x_pos//(self.chunk_size)
        y_grid = y_pos//(self.chunk_size)
        search_range = self.load_distance//self.chunk_size+1
        for x in range(-search_range, search_range):
            for y in range(-search_range, search_range):
                if (x+x_grid,y+y_grid) not in self.loaded_chunks:
                    self.load_chunk(x,y)
    
    def draw_grid_lines(self, surface, x_left, y_top, x_right, y_bottom):
        pg.draw.line(surface, pg.Color(255), (x_left, y_top), (x_right, y_top))
        pg.draw.line(surface, pg.Color(255), (x_left, y_bottom), (x_right, y_bottom))
        pg.draw.line(surface, pg.Color(255), (x_right, y_top), (x_right, y_bottom))
        pg.draw.line(surface, pg.Color(255), (x_left, y_top), (x_left, y_bottom))
              
    def draw_visible_map(self, surface, x_pos, y_pos):
        size = surface.get_size()
        max_y = size[1]-self.tile_size
        max_x = size[0]-self.tile_size
        x_num_chunks = math.ceil(size[0]/self.pixels_per_chunk)
        y_num_chunks = math.ceil(size[0]/self.pixels_per_chunk)
        for y_grid in range(y_num_chunks):
            y_relative = y_grid*self.pixels_per_chunk-y_pos
            for x_grid in range(x_num_chunks):
                if (y_grid, x_grid) not in self.loaded_chunks:
                    self.load_chunk(y_grid, x_grid)
                current_chunk = self.loaded_chunks[(y_grid, x_grid)]
                x_relative = x_grid*self.pixels_per_chunk-x_pos
                for y_tile in range(self.chunk_size):
                    y_pixel = y_tile*self.tile_size+y_relative
                    if y_pixel > max_y:
                        break
                    for x_tile in range(self.chunk_size):
                        x_pixel = x_tile*self.tile_size+x_relative
                        if x_pixel > max_x:
                            break
                        self.draw_tile(surface, x_pixel, y_pixel, int(current_chunk[x_tile][y_tile]))
                        
                self.draw_grid_lines(surface, x_grid*self.pixels_per_chunk, y_grid*self.pixels_per_chunk, (x_grid+1)*self.pixels_per_chunk, (y_grid+1)*self.pixels_per_chunk)
                pg.display.flip()
    def draw_tile(self, surface, x_pixel, y_pixel, tile):
        pg.draw.rect(surface, pg.Color(tile, tile, tile), pg.Rect(x_pixel, y_pixel, x_pixel+self.tile_size, y_pixel+self.tile_size))
                            
        
def set_edges(map, chunk_size, grid_x, grid_y, gradient, offset, roughness):
    print(f'##############{grid_y, grid_x }###################')
    grid_x = grid_x*chunk_size
    grid_y = grid_y*chunk_size
   

    map[0][0] = rng.randomFloatOne([grid_y, grid_x])*gradient*2+offset
    map[chunk_size][0] = rng.randomFloatOne([grid_y+chunk_size, grid_x ])*gradient*2+offset
    map[0][chunk_size] = rng.randomFloatOne([grid_y, grid_x+chunk_size])*gradient*2+offset
    map[chunk_size][chunk_size] = rng.randomFloatOne([grid_y+chunk_size, grid_x+chunk_size])*gradient*2+offset
    print('tl', [grid_y, grid_x], map[0][0])
    print('tr', [grid_y, grid_x+chunk_size ], map[0][chunk_size] )
    print('bl', [grid_y, grid_x+chunk_size ], map[chunk_size][0])
    print('br', [grid_x+chunk_size ,grid_y+chunk_size], map[chunk_size][chunk_size])
    vertical_displace(grid_x, grid_y, map, chunk_size,chunk_size, grid_x, grid_y, gradient, 0, 255,roughness,y_local = 0)
    horizontal_displace(grid_x, grid_y, map, chunk_size,chunk_size, grid_x, grid_y, gradient, 0, 255,roughness, x_local = 0)
    return map

def vertical_displace(x_origin, y_origin, map, size, original_size, grid_x, grid_y, gradient, min_value, max_value,roughness, y_local = 0):
    if size <2:
        return map
    half_size= size//2
    #left
    avg = (map[y_local][0] + map[y_local+size][0]) / 2
    map[y_local + half_size][0] = randomise_and_clamp(avg, [y_origin + y_local+half_size, x_origin], gradient,  min_value, max_value)
    #right
    avg = (map[y_local][original_size] + map[y_local][original_size]) / 2
    # print(f'right edge seed { x_origin + original_size}')
    # print(f'left edge seed { x_origin}')
    map[y_local + half_size][original_size] = randomise_and_clamp(avg, [y_origin + y_local+half_size, x_origin + original_size], gradient,  min_value, max_value)
    vertical_displace(x_origin, y_origin, map, half_size, original_size, grid_x, grid_y, gradient*roughness, min_value, max_value,roughness, y_local = y_local)
    vertical_displace(x_origin, y_origin, map, half_size, original_size, grid_x, grid_y, gradient*roughness, min_value, max_value,roughness, y_local = y_local+half_size)
    
def horizontal_displace(x_origin, y_origin, map, size, original_size, grid_x, grid_y, gradient, min_value, max_value,roughness, x_local = 0):
    if size <2:
        return map
    half_size= size//2
    #top
    avg = (map[0][x_local] + map[0][x_local+size]) / 2
    map[0][x_local + half_size] = randomise_and_clamp(avg, [y_origin , x_origin+x_local+half_size], gradient,  min_value, max_value)
    print('top displace', [y_origin , x_origin+x_local+half_size])
    #right
    avg = (map[x_local][original_size] + map[x_local][original_size]) / 2
    map[original_size][x_local + half_size] = randomise_and_clamp(avg, [y_origin + original_size, x_origin + x_local+half_size], gradient,  min_value, max_value)
    print('bottom displace', [y_origin + original_size, x_origin + x_local+half_size])
    horizontal_displace(x_origin, y_origin, map, half_size, original_size, grid_x, grid_y, gradient*roughness, min_value, max_value,roughness, x_local = x_local)
    horizontal_displace(x_origin, y_origin, map, half_size, original_size, grid_x, grid_y, gradient*roughness, min_value, max_value,roughness, x_local = x_local+half_size)

        
def randomise_and_clamp(value, seed, random_magnitude,  min_value, max_value):
    value = value + ((rng.randomFloatOne(seed)-0.5)*2 )* random_magnitude
    tmp1 = min(value, max_value)
    tmp2 = max(tmp1, min_value)
    return max(min(value, max_value), min_value)
           
def daimond_square(x_origin, y_origin, size, map, gradient, roughness, min_value, max_value, x_local=0, y_local=0):
    if size < 2:
        return map
    half_size = size // 2
    # Diamond
    avg = (map[y_local][x_local] + map[y_local][x_local + size] + map[y_local + size][x_local] + map[y_local + size][x_local + size]) / 4
    map[y_local+half_size][x_local + half_size] = randomise_and_clamp(avg, [y_origin + y_local+half_size, x_origin + x_local+half_size], gradient,  min_value, max_value)
    # Square
    # Left
    if map[y_local + half_size][x_local] == 0:
        avg = (map[y_local][x_local] + map[y_local+size][x_local]) / 2
        map[y_local + half_size][x_local] = randomise_and_clamp(avg, [y_origin + y_local+half_size, x_origin + x_local], gradient,  min_value, max_value)
    # Top
    if map[y_local][x_local + half_size] == 0:
        avg = (map[y_local][x_local] + map[y_local][x_local+size]) / 2
        map[y_local][x_local + half_size] = randomise_and_clamp(avg, [y_origin + y_local, x_origin + x_local+half_size], gradient,  min_value, max_value)
    # Right
    if map[y_local + half_size][x_local + size] == 0:
        avg = (map[y_local][x_local+size] + map[y_local + size][x_local + size]) / 2
        map[y_local + half_size][x_local + size] = randomise_and_clamp(avg, [y_origin + y_local+half_size, x_origin + x_local+size], gradient,  min_value, max_value)
    # Bottom
    if map[y_local + size][x_local + half_size] == 0:
        avg = (map[y_local+size][x_local] + map[y_local + size][x_local + size]) / 2
        map[y_local + size][x_local + half_size] = randomise_and_clamp(avg, [y_origin + y_local+size, x_origin + x_local+half_size], gradient,  min_value, max_value)

    daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness,  min_value, max_value, x_local, y_local)
    daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness, min_value, max_value,  x_local + half_size, y_local)
    daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness, min_value, max_value,  x_local, y_local + half_size)
    daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness, min_value, max_value,  x_local + half_size, y_local + half_size)

    return map


    
# def daimond_square(x_origin, y_origin, size, map, gradient, roughness, x_local=0, y_local=0):
#     if size < 2:
#         return map

#     half_size = size // 2

#     # Diamond
#     avg = (map[x_local][y_local] + map[x_local][y_local + size] + map[x_local + size][y_local] + map[x_local + size][y_local + size]) / 4
#     map[x_local][y_local + half_size] = avg + rng.randomFloatOne([x_origin + x_local, y_origin + y_local]) * gradient

#     # Square
#     # Top
#     avg = (map[x_local][y_local] + map[x_local + size][y_local]) / 2
#     map[x_local + half_size][y_local] = avg + rng.randomFloatOne([x_local + half_size + x_origin, y_local + y_origin]) * gradient

#     # Left
#     avg = (map[x_local][y_local] + map[x_local][y_local + size]) / 2
#     map[x_local][y_local + half_size] = avg + rng.randomFloatOne([x_origin + x_local, y_origin + y_local + half_size]) * gradient

#     # Bottom
#     avg = (map[x_local][y_local + size] + map[x_local + size][y_local + size]) / 2
#     map[x_local + size][y_local + half_size] = avg + rng.randomFloatOne([x_origin + x_local + size, y_origin + y_local + half_size]) * gradient

#     # Right
#     avg = (map[x_local + size][y_local] + map[x_local + size][y_local + size]) / 2
#     map[x_local + size][y_local + half_size] = avg + rng.randomFloatOne([x_origin + x_local, y_origin + y_local]) * gradient

#     # Recursive calls with half the size
#     daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness, x_local, y_local)
#     daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness, x_local + half_size, y_local)
#     daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness, x_local, y_local + half_size)
#     daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness, x_local + half_size, y_local + half_size)

#     return map

