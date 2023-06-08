import sys
import os
import subprocess


def run_on_input(stud_sol, input):
    " will return the student output as list(output splited by " " "
    input = input.strip().replace("  ", " ").split(" ")
    command = ["python", stud_sol]
    command.extend(input)
    p = subprocess.run(command, capture_output=True, text=True)
    return (p.stdout.strip().replace("  ", " ").replace("\n\n", "\n").split("\n"), p.stderr)




def check_output(outs):
    mistakes = 0
    deserved_outs = [
        "<Nerve Cell, 3>",
        "<Nerve Cell, 3>",
        "<Nerve Cell, 1>",
        "<Nerve Cell, 1>",
        "<Nerve Cell, 1>",
        "<Nerve Cell, 1>",
        "<Muscle Cell, 3>",
        "A,3;AG,4;ATCAA,3;G,5;GA,3",
        "Translation: M;P;P;L;S",
        "No simple repeats in DNA sequence",
        "Non-coding RNA",
        "ATG,3",
        "Translation: M;H;H;H",
    ]
    for des, out in zip(deserved_outs, outs):
        if des != out:
            mistakes += 1
            print("WRONG OUTPUT!!! should be: {}, but got: {}".format(des, out))
    return mistakes


def check_file(file="output.txt"):
    if not os.path.exists(file):
        print("ERROR!!! no output file")
        exit()
    file_deservesed = ["12.700799999999997, I like to move it\n","50.80319999999999, I like to move it\n", "76.20479999999999, I like to move it\n"]
    mistakes = 0
    with open(file, "r") as fd:
        file_lines = fd.readlines()
        if len(file_deservesed) != len(file_lines):
            print(
                "ERROR!!! file should have {} lines, but have {} lines".format(
                    len(file_deservesed), len(file_lines)
                )
            )
            exit()
        for des, out in zip(file_deservesed, file_lines):
            if des != out:
                mistakes += 1
                print("WRONG OUTPUT!!! should be {}, but got: {}".format(des, out))
    return mistakes


if __name__ == "__main__":
    solution = sys.argv[1]
    if not os.path.exists(solution):
        print("ERROR!!! pythom solution file {} , not found".format(solution))
        exit(0)
    input = "input_ex2_fixed.txt 50,200,300"
    print("input is: ", input)
    outs, err = run_on_input(solution, input)
    if err:
        print("ERROR!!! your program crasing with err{}".format(err))
        exit(0)
    print("your output is: ", outs)
    mistakes = check_output(outs)
    mistakes += check_file()
    print("finished  checking with {} mistakes".format(mistakes))
