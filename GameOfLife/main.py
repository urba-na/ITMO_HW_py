# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from PIL import Image, ImageDraw
import argparse

DEFAULT_FILE = 'GOL.csv'
OUTPUT_FILE_CSV = 'gen.csv'
OUTPUT_FILE_PNG = 'gen.png'
DEFAULT_GENERATION = 10
CELL_SIZE = 20
BORDER_WIDTH = 2
BASE_COLOUR = "#00FF00"

DEBUG = False

def get_cell_colour(age):
    '''
    @requires: age - число - возраст ячейки
    @modifies: None
    @effects: None
    @raises: None
    @returns: (0, new_colour, 0) - где new_colour - оттенок базового цвета,
        который с возрастом ячейки темнеет на 50 ед
    '''
    new_colour = max(50, 255 - age * 50)
    return (0, new_colour, 0)

 
def live_neighbors(grid, row, col):
    '''
    @requires: grid - список списков, значения в котором могут быть:
                0 - если клетка мертвая
                1 - если клетка живая
                размер всех вложенных списков должен быть одинаковым.
                Пример:
                [ [0, 1, 0],
                  [0, 0, 0],
                  [1, 1, 0]
                ]
                row - 0 <= row <= количество строк в списке
                col - 0 <= col <= количество элементов в строке 
    @modifies: None
    @effects: None
    @raises: None
    @returns: nb - число, количество живых клеток-соседей
    '''
    
    nb = 0;
    
    rows = len(grid)
    cols = len(grid[0])
    min_r = row - 1 if row >= 1 else 0
    max_r = row + 1 if row < rows - 1 else row
    min_c = col - 1 if col >= 1 else 0
    max_c = col + 1 if col < cols - 1 else col
    for idx_y in range(min_r, max_r + 1):
        for idx_x in range(min_c, max_c + 1):
            if idx_y == row and idx_x == col:
                continue
            if grid[idx_y][idx_x] > 0:
                nb += 1
    
    return nb
           
def model(grid):
    '''
    @requires: grid - список списков, значения в котором могут быть:
                0 - если клетка мертвая
                1 - если клетка живая
                размер всех вложенных списков должен быть одинаковым.
                Пример:
                [ [0, 1, 0],
                  [0, 0, 0],
                  [1, 1, 0]
                ]
    @modifies: None
    @effects: None
    @raises: None
    @returns: new_grid - список списков, со значением ячеек, соответствующим
              новому поколению
              правила:
              1. Любая живая клетка, имеющая менее двух живых соседей, погибает.
              2. Любая живая клетка, имеющая два или три живых соседа, продолжает жить в следующем поколении.
              3. Любая живая клетка, имеющая более трех живых соседей, погибает.
              4. Любая мертвая клетка, имеющая ровно три живых соседа, становится живой клеткой.    
            '''
    rows, cols = len(grid), len(grid[0])
    new_grid = [[ 0 for _ in range(cols)] for _ in range(rows)] # новое поле со всеми 0
    
    cell_age = 0
    for row in range(rows):
        for col in range(cols):
            live_nb = live_neighbors(grid, row, col)
            cell_age = grid[row][col]
            
            #1st rule
            if live_nb < 2 and cell_age > 0:
                new_grid[row][col] = 0
            #2nd rule
            elif 2 <= live_nb <= 3 and cell_age > 0:
                new_grid[row][col] = cell_age + 1
            #3rd rule
            elif live_nb > 3 and cell_age > 0:
                new_grid[row][col] = 0
            #4th rule
            elif cell_age == 0 and live_nb == 3:
                new_grid[row][col] = 1
            else:
                new_grid[row][col] = 0
                    
    #print(new_grid)
    
    return new_grid

def read_input(filename):
    '''
    @requires: filename - строка, соответствующая имени файла в формате csv
    @modifies: None
    @effects: None
    @raises: None
    @returns: grid - список списков, соответствующий прочитанному файлу,
              значения в котором могут быть:
              0 - если клетка мертвая
              1 - есди клетка живая
              размер всех вложенных списков должен быть одинаковым 
    '''
     
    grid = []  
    with open(filename, 'r') as input_file:
      lines = input_file.readlines()
      for line in lines:
            line = line.strip()
            line = line.split(";")
            line = [int(elem) for elem in line]
            grid.append(line)        
    return grid

def write_output(grid, filename, generation):
    '''
    @requires: grid - список списков
               filename - строка, соответствующая имени файла в формате csv
               generation - число, номер текущего шага выполнения 
    @modifies: None
    @effects: создает и записывает в папку текстовый файл в формате csv
    @raises: None
    @returns: count - число, количество записанных знаков в файле 
    '''
    count = 0
    with open(str(generation) + '_' + filename, 'w') as file:
        for row in grid:
            output_row = ';'.join(map(str, row))
            count = count + file.write(output_row + '\n')

    return count

def write_png(grid, filename, generation, DEBUG = False):
    '''
    @requires: grid - список списков
               filename - строка, соответствующая имени файла в формате csv
               generation - число, номер текущего шага выполнения  
    @modifies: None
    @effects: создает и записывает в текущую папку изображение в формате png
    @raises: None
    @returns: None
    '''
    rows, cols = len(grid), len(grid[0])
    
    im_width = cols * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH
    im_height = rows * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH
   
    im = Image.new(mode = "RGB", size = (im_width, im_height))
    draw = ImageDraw.Draw(im)
    
    for r in range(rows + 1):
        y = r * (CELL_SIZE + BORDER_WIDTH)
        draw.line(xy=(0, y, im_width, y), fill=(BASE_COLOUR), width=BORDER_WIDTH)
        
    for c in range(cols + 1):
        x = c * (CELL_SIZE + BORDER_WIDTH)
        draw.line(xy=(x, 0, x, im_height), fill=(BASE_COLOUR), width=BORDER_WIDTH)
     
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] > 0:
                color = get_cell_colour(grid[r][c])
                x1 = c * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH
                y1 = r * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                draw.rectangle((x1,y1,x2,y2), fill=(color))
        
    im.save(str(generation) + "_" + filename)
   
    if DEBUG:
        return im.size, str(generation) + "_" + filename
    

parser = argparse.ArgumentParser(description='GOL')
parser.add_argument("input_file", nargs='?', default = DEFAULT_FILE, help = "имя csv файла")
parser.add_argument("generation", nargs='?', default = DEFAULT_GENERATION,  type = int, help = "количество шагов")

args = parser.parse_args()
input_file = args.input_file
generation = args.generation

try:
    grid = read_input(input_file)
except OSError:  
    print(f"Не получилось найти файл {input_file}, используется файл по умолчанию")
    grid = read_input(DEFAULT_FILE)
    
'''
test_cases
'''

if DEBUG:
    #model tests
    expected = \
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 2, 2, 2, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    actual_model = model(grid)
    if actual_model != expected:
        print('Test model 1 failed')
        
    expected = \
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 2, 0, 1, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 3, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
             [0, 0, 0, 0, 1, 3, 3, 0, 0, 0],
             [0, 0, 0, 0, 0, 2, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    actual_model = model(model(grid))
    if actual_model != expected:
        print('Test model 2 failed')
    
    #live_neighbors tests    
    actual = live_neighbors(grid, 4, 3)
    expected = 1
    if actual != expected:
        print('Test_live_neighbors 1 failed')
    actual = live_neighbors(grid, 5, 6)
    expected = 4
    if actual != expected:
        print('Test_live_neighbors 2 failed')
    actual = live_neighbors(grid, 6, 5)
    expected = 3
    if actual != expected:
        print('Test_live_neighbors 3 failed')
    
    #write_output tests  
    expected = 200
    gen_1 = actual_model
    sys_answer = write_output(gen_1, OUTPUT_FILE_CSV, 1)
   
    if expected != sys_answer:
        print('Test_write_output 1 failed')
    
    gen_2 = model(model(grid))
    sys_answer = write_output(gen_2, OUTPUT_FILE_CSV, 2)
    
    if expected != sys_answer:
        print('Test_write_output 2 failed')
        
    #write_png tests
    expected_size, expected_name = (222,222), "1_gen.png"
    actual_size, actual_name = write_png(grid, OUTPUT_FILE_PNG, 1, DEBUG)
    if expected_size != actual_size or expected_name != actual_name:
        print('Test_write_png 1 failed')
    
    expected_size, expected_name = (222,222), "2_gen.png"
    actual_size, actual_name = write_png(grid, OUTPUT_FILE_PNG, 2, DEBUG)
    if expected_size != actual_size or expected_name != actual_name:
        print('Test_write_png 1 failed')
    
    #get_cell_colour test
    expected = (0, 255,0)
    actual = get_cell_colour(0)
    if expected != actual:
        print('Test_get_cell_color 1 failed')
    
    expected = (0, 205,0)
    actual = get_cell_colour(1)
    if expected != actual:
        print('Test_get_cell_color 2 failed')
else:
    
    for gen in range(generation):
        grid = model(grid)
        write_output(grid, OUTPUT_FILE_CSV, gen + 1)
        write_png(grid, OUTPUT_FILE_PNG, gen + 1)

    print('Files created')    
    
    
    
    
