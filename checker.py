import sys
import os
import subprocess


def run_on_input(stud_sol, input):
    # will return the student output as list
    input = input.strip().replace("  ", " ").split(" ")
    command = ["python", stud_sol]
    command.extend(input)
    p = subprocess.run(command, capture_output=True, text=True)
    return (p.stdout.strip().replace("  ", " ").replace("\n\n", "\n").split("\n"), p.stderr)


"""def check_srr(deserved_srrs, out):
    srrs_d = deserved_srrs.split(";")
    srrs_out = out.split(";")
    mistakes = 0
    if not all([s in srrs_out for s in srrs_d]) or not all([s in srrs_d for s in srrs_out]):
        print("WRONG srr list !!! should be: {}, but got: {}".format(srrs_d, out))
        mistakes = +1
    srr_numbers = [int(s.split(",")[-1]) for s in srrs_out]
    if not all([srr_numbers[i] <= srr_numbers[i + 1] for i in range(len(srr_numbers) - 1)]):
        print("WRONG srr order !!!")
        mistakes = +1
    return mistakes"""


def check_output(outs, deserved_outs):
    mistakes = 0
    for des, out in zip(deserved_outs, outs):
        if des != out:
            mistakes += 1
            print("WRONG OUTPUT!!! should be: {}, but got: {}".format(des, out))
    return mistakes


if __name__ == "__main__":
    solution = sys.argv[1]
    if not os.path.exists(solution):
        print("ERROR!!! pythom solution file {} , not found".format(solution))
        exit(0)
    input1 = "ATCAAATCAAATCAAGAGAGAGGGGG CttGAT AUGCAUGAACUAGAUGAACAUGCAGAUCUAACGUG 1"
    print("\nchecking on first input: ", input1, "...")
    outs, err = run_on_input(solution, input1)
    if err:
        print("ERROR!!! your program crasing with err{}".format(err))
        exit(0)
    print("your output is: ", outs)
    deserved_outs = [
        "A,3;AG,4;ATCAA,3;G,5;GA,3",
        "RNA sequence: AUCAAG",
        "Translation: M;N;M;Q;I",
    ]
    mistakes = check_output(outs, deserved_outs)
    input2 = "ATCA CttGAT AUGUAACGUG 2"
    print("\nchecking on second input: ", input2)
    outs, err = run_on_input(solution, input2)
    if err:
        print("ERROR!!! your program crashing with err{}".format(err))
        exit(0)
    print("your output is: ", outs)
    deserved_outs = [
        "No simple repeats in DNA sequence",
        "RNA sequence: AUCAAG",
        "Non-coding RNA",
    ]
    mistakes += check_output(outs, deserved_outs)

    print("\nfinished checking, you have {} mistakes".format(mistakes))
