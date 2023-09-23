from rng import rng
import math
import pygame as pg
import copy


class Chunk():
    def __init__(self, tiles, map):
        self.tiles = tiles
        self.map = map
        self.surface = pg.Surface((self.map.pixels_per_chunk, self.map.pixels_per_chunk))
        size = self.surface.get_size()
        self.draw_surface()
        
    def draw_surface(self):
        for x in range(self.map.chunk_size):
            for y in range(self.map.chunk_size):
                self.draw_tile(self.surface, x*self.map.tile_size,y*self.map.tile_size, int(self.tiles[x][y]))
                
    def draw_tile(self, surface, x_pixel, y_pixel, tile):
        pg.draw.rect(surface, pg.Color(tile, tile, tile), pg.Rect(x_pixel, y_pixel, x_pixel+self.map.tile_size, y_pixel+self.map.tile_size))          

        
        
# grid is a 2d grid of chunks of tiles
class Map():
    def __init__(self, chunk_size, roughness, gradient, load_distance,  tile_size, offset, min_value, max_value, blend_factor = 0):
        self.chunk_size = chunk_size
        self.offset = offset
        self.roughness = roughness
        self.gradient = gradient
        self.load_distance = load_distance
        self.tile_size = tile_size
        self.pixels_per_chunk = tile_size*chunk_size
        self.blend_factor = blend_factor
        self.loaded_chunks = {}
        self.blank_chunk =[]
        self.min_value = min_value
        self.max_value = max_value
        for x in range(chunk_size):
            self.blank_chunk.append([])
            for y in range(chunk_size):
                self.blank_chunk[x].append(None)
        
        while chunk_size >2:
            chunk_size/=2
            gradient /=2
        self.final_gradient = gradient
        self.check_loaded_chunks
    
    def load_chunk(self, chunk_grid):
        x_origin = chunk_grid[0]*self.chunk_size
        y_origin = chunk_grid[1]*self.chunk_size
        tiles = set_edges(copy.deepcopy(self.blank_chunk), self.chunk_size-1, chunk_grid[0], chunk_grid[1], self.gradient*2,self.final_gradient,  self.offset, self.roughness,self.min_value, self.max_value)
        tiles= daimond_square(x_origin, y_origin, self.chunk_size-1, tiles, self.gradient, self.roughness, self.min_value, self.max_value)
        reset_edges(tiles, x_origin, y_origin, self.chunk_size, self.final_gradient*4, self.min_value, self.max_value)
        self.loaded_chunks[chunk_grid] = Chunk(tiles, self)
        return self.loaded_chunks[chunk_grid]
  
    def check_loaded_chunks(self, chunk_grid):
        x_grid = chunk_grid[0]//(self.chunk_size)
        y_grid = chunk_grid[1]//(self.chunk_size)
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
        
    # def draw_visible_map(self, surface, x_pos, y_pos):
    #     size = surface.get_size()
    #     camera_x_grid = x_pos // self.pixels_per_chunk
    #     camera_y_grid = y_pos // self.pixels_per_chunk
    #     x_num_chunks = math.ceil(size[0] / self.pixels_per_chunk)
    #     y_num_chunks = math.ceil(size[1] / self.pixels_per_chunk)

    #     for y_grid in range(y_num_chunks):
    #         for x_grid in range(x_num_chunks):
            
    #             chunk_grid = (camera_x_grid + x_grid, camera_y_grid + y_grid)
    #             x_relative = x_grid * self.pixels_per_chunk
    #             y_relative = y_grid * self.pixels_per_chunk

    #             if chunk_grid not in self.loaded_chunks:
    #                 self.load_chunk(chunk_grid)
    #                 # self.loaded_chunks[chunk_grid].surface.fill((0, 0, 0))  # Clear the chunk's surface

    #             current_chunk = self.loaded_chunks[chunk_grid]
    #             surface.blit(current_chunk.surface, (x_relative - x_pos, y_relative - y_pos))
    #             pg.display.flip()

    #     # Update the display once, outside the loop
        
              
    def draw_visible_map(self, surface, x_pos, y_pos):
        size = surface.get_size()
        drawnChunks =[]
        camera_x_grid = x_pos//self.pixels_per_chunk
        camera_y_grid = y_pos//self.pixels_per_chunk
        x_num_chunks = math.ceil(size[0]/self.pixels_per_chunk)
        y_num_chunks = math.ceil(size[1]/self.pixels_per_chunk)
        for y_grid in range(-y_num_chunks,1 ):
            chunk_y = camera_y_grid-y_grid
            y_relative = chunk_y*self.pixels_per_chunk-y_pos
            for x_grid in range(-x_num_chunks, 1):
                chunk_x = camera_x_grid-x_grid
                chunk_grid = (chunk_x, chunk_y)
                x_relative = chunk_x*self.pixels_per_chunk-x_pos
                drawnChunks.append((chunk_grid, (x_relative,y_relative )))
                
                if (chunk_grid) not in self.loaded_chunks:
                    self.load_chunk(chunk_grid)
                current_chunk = self.loaded_chunks[chunk_grid]
                surface.blit(current_chunk.surface, (x_relative,y_relative ))
        
                # for y_tile in range(self.chunk_size):
                #     y_pixel = y_tile*self.tile_size+y_relative
                #     if y_pixel > max_y_pixel:
                #         break
                #     for x_tile in range(self.chunk_size):
                #         x_pixel = x_tile*self.tile_size+x_relative
                #         if x_pixel > max_x_pixel:
                #             break
                #         self.draw_tile(surface, x_pixel, y_pixel, int(current_chunk.tiles[y_tile][x_tile]))
                        
                self.draw_grid_lines(surface, x_grid*self.pixels_per_chunk, y_grid*self.pixels_per_chunk, (x_grid+1)*self.pixels_per_chunk, (y_grid+1)*self.pixels_per_chunk)
        pg.display.flip()
        print(drawnChunks)
    def draw_tile(self, surface, x_pixel, y_pixel, tile):
        pg.draw.rect(surface, pg.Color(tile, tile, tile), pg.Rect(x_pixel, y_pixel, x_pixel+self.tile_size, y_pixel+self.tile_size))
                            
        
def set_edges(map, chunk_size, grid_x, grid_y, gradient,final_gradient, offset, roughness, min_value, max_value):
    print(grid_x, grid_y)
    grid_x = grid_x*chunk_size
    grid_y = grid_y*chunk_size
    map[0][0] = get_corner([ grid_x, grid_y], gradient, min_value, max_value)+offset
    map[0][chunk_size] = get_corner([ grid_x, grid_y+chunk_size ], gradient,  min_value, max_value) +offset #bottomLeft
    map[chunk_size][0] = get_corner([grid_x+chunk_size, grid_y], gradient, min_value, max_value)+offset
    map[chunk_size][chunk_size] = get_corner([grid_x+chunk_size, grid_y+chunk_size], gradient, min_value, max_value) +offset
    vertical_displace(grid_x, grid_y, map, chunk_size,chunk_size, grid_x, grid_y, gradient,final_gradient, 0, 255,roughness,y_local = 0)
    horizontal_displace(grid_x, grid_y, map, chunk_size,chunk_size, grid_x, grid_y, gradient,final_gradient, 0, 255,roughness, x_local = 0)
    return map

def get_corner(seed, gradient,  min_value, max_value,modifier=[''], extra_randomisation=0, blur_method = 'same'):
    if extra_randomisation == 0:
        return clamp(rng.randomFloatOne(seed)*gradient, min_value, max_value)
    value = rng.randomFloatOne(seed)*gradient + (rng.randomFloatOne(seed+[modifier])-0.5)*4*final_gradient
    return clamp(value, min_value, max_value)

def get_edge(value, seed, gradient, final_gradient, modifier, min_value, max_value):
    value = value+ rng.randomFloatOne(seed)*gradient + (rng.randomFloatOne(seed+[modifier])-0.5)*4*final_gradient
    return clamp(value, min_value, max_value)


def reset_edges(map, x_origin, y_origin, chunk_size, final_gradient, min_value, max_value):
        for z in range(1, chunk_size-1):
            sum_top = 0
            sum_bottom = 0
            sum_left = 0
            sum_right = 0
            for i in [0,1]:
                for j in [-1,1]:
                    sum_top+= map[j+z][i]
                    sum_bottom+= map[j+z][chunk_size-1-i]
                    sum_left+= map[i][j+z]
                    sum_right += map[chunk_size-1-i][j+z]
            map[z][0] = randomise_and_clamp(sum_top/4, [x_origin+z, y_origin], final_gradient,  min_value, max_value)
            map[z][chunk_size-1] = randomise_and_clamp(sum_bottom/4, [ x_origin+z, y_origin+chunk_size-1], final_gradient,  min_value, max_value)
            map[0][z] = randomise_and_clamp(sum_left/4, [ x_origin, y_origin+z], final_gradient,  min_value, max_value)
            map[chunk_size-1][z] = randomise_and_clamp(sum_right/4, [x_origin+chunk_size-1, y_origin+z ], final_gradient,  min_value, max_value)
        sum = map[0][1]+map[1][0]+map[1][1]
        map[0][0]= randomise_and_clamp(sum/3, [x_origin+z, y_origin], final_gradient,  min_value, max_value)
        sum = map[chunk_size-2][1]+map[chunk_size-2][0]+map[chunk_size-1][1]
        map[chunk_size-1][0]= randomise_and_clamp(sum/3, [x_origin+chunk_size-1, y_origin], final_gradient,  min_value, max_value)
        sum = map[chunk_size-2][chunk_size-2]+map[chunk_size-2][chunk_size-1]+map[chunk_size-1][chunk_size-2]
        map[chunk_size-1][chunk_size-1]= randomise_and_clamp(sum/3, [x_origin+chunk_size-1, y_origin+chunk_size-1], final_gradient,  min_value, max_value)
        sum = map[0][chunk_size-2]+map[1][chunk_size-2]+map[1][chunk_size-1]
        map[0][chunk_size-1]= randomise_and_clamp(sum/3, [x_origin, y_origin+chunk_size-1], final_gradient,  min_value, max_value)

      

def vertical_displace(x_origin, y_origin, map, size, original_size, grid_x, grid_y, gradient,final_gradient, min_value, max_value,roughness, y_local = 0):
    if size <2:
        return map
    half_size= size//2
    #left
    avg = (map[0][y_local] + map[0][y_local+size]) / 2
    map[0][y_local + half_size] = clamp(randomise(avg, [x_origin, y_origin + y_local+half_size], gradient), min_value, max_value)
    #right
    avg = (map[original_size][y_local] + map[original_size][y_local+size]) / 2
    map[original_size][y_local + half_size] = clamp(randomise(avg, [ x_origin + original_size, y_origin + y_local+half_size], gradient), min_value, max_value)
    # print(f'right displace { [x_origin + original_size, y_origin + y_local+half_size]} {map[original_size][y_local + half_size]}')
    # print(f'left displace { [x_origin, y_origin + y_local+half_size]} {map[0][y_local + half_size]}')
    vertical_displace(x_origin, y_origin, map, half_size, original_size, grid_x, grid_y, gradient*roughness, final_gradient, min_value, max_value,roughness, y_local = y_local)
    vertical_displace(x_origin, y_origin, map, half_size, original_size, grid_x, grid_y, gradient*roughness, final_gradient, min_value, max_value,roughness, y_local = y_local+half_size)

def horizontal_displace(x_origin, y_origin, map, size, original_size, grid_x, grid_y, gradient,final_gradient, min_value, max_value,roughness, x_local = 0 ):
    if size <2:
        return map
    half_size= size//2
    #top
    avg = (map[x_local][0] + map[x_local+size][0]) / 2
    map[x_local + half_size][0] = clamp(randomise(avg, [x_origin+x_local+half_size, y_origin], gradient), min_value, max_value)
    
    #bottom
    avg = (map[x_local] [original_size]+ map[x_local+size][original_size]) / 2
    map[x_local + half_size][original_size] = clamp(randomise(avg, [x_origin + x_local+half_size, y_origin + original_size], gradient), min_value, max_value)
    # print('bottom displace', [x_origin + x_local+half_size, y_origin + original_size], map[x_local + half_size][original_size] )
    # print('top displace', [x_origin+x_local+half_size, y_origin], map[x_local + half_size][0])
    horizontal_displace(x_origin, y_origin, map, half_size, original_size, grid_x, grid_y, gradient*roughness,final_gradient, min_value, max_value,roughness, x_local = x_local)
    horizontal_displace(x_origin, y_origin, map, half_size, original_size, grid_x, grid_y, gradient*roughness,final_gradient, min_value, max_value,roughness, x_local = x_local+half_size)

        
def randomise_and_clamp(value, seed, random_magnitude,  min_value, max_value):
    return clamp(randomise(value , seed,  random_magnitude), min_value, max_value)

def randomise(value, seed, random_magnitude): 
    return value + ((rng.randomFloatOne(seed)-0.5)*2 )* random_magnitude  
 
def clamp(value, min_value, max_value):
    if value< min_value:
        return min_value
    if value>max_value:
        return max_value
    else:
        return value
           
def daimond_square(x_origin, y_origin, size, map, gradient, roughness, min_value, max_value, x_local=0, y_local=0):
    if size < 2:
        return map
    half_size = size // 2
    # Diamond

    avg = (map[x_local][y_local] + map[x_local][y_local + size] + map[x_local + size][y_local] + map[x_local + size][y_local + size]) / 4
    map[x_local+half_size][y_local + half_size] = randomise_and_clamp(avg, [x_origin + x_local+half_size, y_origin + y_local+half_size], gradient,  min_value, max_value)
    # Square
    # Left
    avg = (map[x_local][y_local] + map[x_local][y_local+size]) / 2
    if map[x_local][y_local + half_size] == None:
        map[x_local][y_local + half_size] = randomise_and_clamp(avg, [x_origin + x_local, y_origin + y_local+half_size], gradient,  min_value, max_value)
    # Top

    avg = (map[x_local][y_local] + map[x_local+size][y_local]) / 2
    if map[x_local + half_size][y_local] == None:
        map[x_local + half_size][y_local] = randomise_and_clamp(avg, [x_origin + x_local+half_size, y_origin + y_local], gradient,  min_value, max_value)
    
    # Right
    avg = (map[x_local+size][y_local] + map[x_local + size][y_local + size]) / 2
    if map[x_local + size][y_local + half_size] == None:
        map[x_local + size][y_local + half_size] = randomise_and_clamp(avg, [ x_origin + x_local+size, y_origin + y_local+half_size], gradient,  min_value, max_value)
    # Bottom
    avg = (map[x_local][y_local+size] + map[x_local + size][y_local + size]) / 2
    if map[x_local + half_size][y_local + size] == None:
        map[x_local + half_size][y_local + size] = randomise_and_clamp(avg, [ x_origin + x_local+half_size, y_origin + y_local+size,], gradient,  min_value, max_value)


    daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness,  min_value, max_value, x_local, y_local)
    daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness, min_value, max_value,  x_local + half_size, y_local)
    daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness, min_value, max_value,  x_local, y_local + half_size)
    daimond_square(x_origin, y_origin, half_size, map, gradient * roughness, roughness, min_value, max_value,  x_local + half_size, y_local + half_size)

    return map
