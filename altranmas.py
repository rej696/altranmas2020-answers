"""Altranmas Coding Challenge Part 1

Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location,
and then an elf traffic controller at the North Pole tells him where to move next.
The elf consults it's XFacts software \(Courtesy of Altranmas Corp.\) to determine
a suitable direction for Santa to move his sleigh. Moves are always exactly one
house to the north \(^\), south \(v\), east \(>\), or west \(<\). After each move,
Santa delivers another present to the house at his new location.

However, unbeknownst to Santa or the elf traffic controller, there is a critical
bug in the software and so the directions are a little off... Santa ends up
visiting some houses more than once. How many houses receive at least one present?

For example:

- \> delivers presents to 2 houses: one at the starting location, and one to the east.
- ^>v< delivers presents to 4 houses in a square, including twice to the house at
    his starting/ending location.
- ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.
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

def read_file(path, cur_loc, coords):
    with open(path, "r") as f:
        for char in f.read():
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

def run(path):
    current_location = {"x": 0, "y": 0}
    visited_coordinates = {0:{0: 1}}

    current_location, visited_coordinates = read_file(
        path, current_location, visited_coordinates)

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
        print(f"Santa delivers presents to {result} different houses!")
    else:
        print(result)
