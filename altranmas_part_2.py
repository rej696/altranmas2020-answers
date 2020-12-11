"""Altranmas Coding Challenge Part 2

The next year, to speed up the process, Santa hires an apprentice, Neil,
to deliver presents with him.

Santa and Neil start at the same location (delivering two presents to
the same starting house), then take turns moving based on instructions
from the elf traffic controller, who is still using the same buggy
software as the previous year.

This year, how many houses receive at least one present?

For example:

- ^v delivers presents to 3 houses, because Santa goes north,
    and then Neil goes south.
- ^>v< now delivers presents to 3 houses, and Santa and Neil
    end up back where they started.
- ^v^v^v^v^v now delivers presents to 11 houses, with Santa
    going one direction and Neil going the other.

Use the same input as before.

Answer: 2639
"""
import sys
import getopt

def update_count(visited_coordinates, x, y):
    try:
        visited_coordinates[x][y] += 1
    except KeyError:
        try:
            visited_coordinates[x].update({y: 1})
        except KeyError:
            visited_coordinates.update({x: {y: 1}})
    
    return visited_coordinates

def move_east(loc, count):
    loc["x"] += 1
    return loc, update_count(count, loc["x"], loc["y"])

def move_west(loc, count):
    loc["x"] -= 1
    return loc, update_count(count, loc["x"], loc["y"])

def move_north(loc, count):
    loc["y"] += 1
    return loc, update_count(count, loc["x"], loc["y"])

def move_south(loc, count):
    loc["y"] -= 1
    return loc, update_count(count, loc["x"], loc["y"])

def move(cur_loc, coords, char):
    if char == "<":
        cur_loc, coords = move_west(cur_loc, coords)
    elif char == ">":
        cur_loc, coords = move_east(cur_loc, coords)
    elif char == "^":
        cur_loc, coords = move_north(cur_loc, coords)
    elif char == "v":
        cur_loc, coords = move_south(cur_loc, coords)
    else:
        print(f"ERROR! {char} is not a valid direction")
    
    return cur_loc, coords

def read_file(path, santa_loc, neil_loc, coords):
    is_real_santa = True
    with open(path, "r") as f:
        for char in f.read():
            if is_real_santa:
                santa_loc, coords = move(santa_loc, coords, char)
            else:
                neil_loc, coords = move(neil_loc, coords, char)
            
            is_real_santa = not is_real_santa
    
    return santa_loc, neil_loc, coords

def run(path):
    santa_location = {"x": 0, "y": 0}
    neil_location = {"x": 0, "y": 0}
    visited_coordinates = {0:{0: 1}}

    santa_location, neil_location, visited_coordinates = read_file(
        path,
        santa_location,
        neil_location,
        visited_coordinates)

    count = 0
    for x in visited_coordinates.keys():
        for y in visited_coordinates[x].keys():
            if visited_coordinates[x][y] > 0:
                count += 1
    
    return count

if __name__ == "__main__":

    path = "./input.txt"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "v", ["input="])
    except getopt.GetOptError:
        print('altranmas.py -v --input <inputfile>')
        sys.exit(2)
    
    verbose = False

    for opt, arg in opts:
        if opt == "-v":
            verbose = True
        elif opt == "--input":
            path = arg

    result = run(path)
    if verbose:
        print(f"Santa and Neil deliver presents to {result} different houses!")
    else:
        print(result)

    
