import os
import sys
import getopt
import random
import csv
import subprocess
import hashlib

CHAR_LIST = ["^", "v", ">", "<"]
START = 7000
STOP = 9000

def get_input_name(path):
    filename, extension = os.path.splitext(path)
    count = 1

    while os.path.exists(path):
        path = f"{filename}_{count}{extension}"
        count += 1
    
    return path

def generate_data():
    return "".join([
        random.choice(CHAR_LIST)
        for _ in range(random.randint(START, STOP))])

def create_file(path):
    with open(path, "w") as f:
        f.write(generate_data())

def run_test(path, script):
    return int(subprocess.run([
        "python", script, "--input", path
        ], capture_output=True).stdout.decode().strip())

def get_result(name=None):
    if name is None:
        path = get_input_name("./input.txt")
    else:
        path = get_input_name(f"./{name}_input.txt")

    create_file(path)
    answer_1 = run_test(path, "altranmas.py")
    answer_2 = run_test(path, "altranmas_part_2.py")
    filename = path.split('.')[1].split("/")[1]
    return {"path": filename, "part_1":answer_1, "part_2":answer_2}

def write_answers(answers):
    with open("./answers.csv", "a", newline="") as c:
        csv.DictWriter(c, fieldnames=answers[0].keys()).writerows(answers)

def run(name=None):
    if name is not None:
        set_seed(name)
    answers = []
    # for _ in range(int(input("number of inputs to generate: "))):
    answers.append(get_result(name))
    
    write_answers(answers)

def set_seed(name):
    random.seed(int(hashlib.sha256(name.encode('utf-8')).hexdigest(), 16))

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["name="])
    except getopt.GetOptError:
        print('generate_input.py --name <inputfile>')
        sys.exit(2)
    
    name = None
    for opt, arg in opts:
        if opt == "--name":
            name = arg

    run(name)
