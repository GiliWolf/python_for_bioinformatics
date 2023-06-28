# Gili Wolf 315144907
import matplotlib.pyplot as plt
import re
from Bio.Seq import Seq
from Bio import SeqIO
import numpy as np
import subprocess
import time
import sys

# builds a figure using 2 graphs and saves it
def first_part_figure(fasta_paths, prosites):
    plt.subplot(1,2,1)
    plt.scatter = length_graph_builder(fasta_paths[0],fasta_paths[1], prosites)
    plt.subplot(1,2,2)
    plt.bar = percentage_graph_builder(fasta_paths[0], prosites)
    plt.suptitle('part 1 output')
    plt.tight_layout()
    # plt.show()
    plt.savefig("315144907.png")

# gets seqs records from the path, and for each prosite patterns gets lengths of all the motifs found in the fasta file
# returns a dictonary with length of motif as a key and number of it accurences as a value
def motifs_lengths(FASTA_path_1, prosite_patterns):
    fasta_1_records = list(SeqIO.parse(FASTA_path_1, "fasta"))
    name_fasta_1 = str(FASTA_path_1).rstrip(".fasta")
    regex_patterns_list = prosite_patterns_into_regex(prosite_patterns)
    fasta_1_motifs_lengths = []
    for regex in regex_patterns_list:
        fasta_1_motifs_lengths += count_motifs_lengths(regex[0],fasta_1_records)
    fasta_1_length_dict = same_length_count(fasta_1_motifs_lengths)
    return fasta_1_length_dict, name_fasta_1

# builds a scatter graphs of number of lengths accurences for 2 fasta files, returns a plot:
# x - length og motifs
# y - logaritmic number of accurences 
def length_graph_builder(FASTA_path_1, FASTA_path_2, prosite_patterns):
    fasta_1_length_dict, name_fasta_1 = motifs_lengths(FASTA_path_1, prosite_patterns)
    fasta_2_length_dict, name_fasta_2 = motifs_lengths(FASTA_path_2, prosite_patterns)
    # print(fasta_1_length_dict, " from ", name_fasta_1)
    # print(fasta_2_length_dict, " from ", name_fasta_2)
    lengths_fasta_1 = np.array([length for length in fasta_1_length_dict.keys()])
    occ_1 = [count for count in fasta_1_length_dict.values()]
    occurrences_fasta_1 = np.array(np.log10(occ_1))
    lengths_fasta_2 = np.array([length for length in fasta_2_length_dict.keys()])
    occ_2 = [count for count in fasta_2_length_dict.values()]
    occurrences_fasta_2 = np.array(np.log10(occ_2))
    plt.scatter(lengths_fasta_1, occurrences_fasta_1, color = 'r')
    plt.scatter(lengths_fasta_2, occurrences_fasta_2, color = 'b')
    plt.legend([str(name_fasta_1), str(name_fasta_2)], loc = 'upper left')
    plt.xlabel("length of motif")
    plt.ylabel("logaritmic length accurences")
    plt.title(' Motifs lengthes accurences')
    return plt



    
#returns a dictonary with the length as key and number of its accurences 
def same_length_count(list_of_lengths):
    length_counts = {}
    for length in list_of_lengths:
        if length in length_counts:
            length_counts[length] += 1
        else:
            length_counts[length] = 1
    return length_counts

# gets seqs records from the path, and for each prosite patterns gets count of all the motifs found in the fasta file
# returns a tuple list of (number of accurences, pattern name)
def cal_motifs_propotions(FASTA_path, prosite_patterns):
    fasta_records = list(SeqIO.parse(FASTA_path, "fasta"))
    regex_patterns_list = prosite_patterns_into_regex(prosite_patterns)
    motifs_count_list = []
    motifs_total_count = 0
    # for each regex- count number of mptifs and appaned to the list (num of motifs, pattern name)
    for regex in regex_patterns_list:
        temp_re_count = count_motifs(regex[0], fasta_records)
        motifs_count_list.append((temp_re_count, regex[1]))
        motifs_total_count += temp_re_count
    # calculate propotions and build a graph out od data
    # print(motifs_count_list, " of ", FASTA_path, " total count: ", motifs_total_count)
    motifs_proportion_list = cal_motifs_proportion(motifs_count_list, motifs_total_count)
    return motifs_proportion_list
   

#builds a pie chart out of tuple list of propotions and name of patterns
def percentage_graph_builder(FASTA_path, prosite_pattern):
    motifs_proportion_list = cal_motifs_propotions(FASTA_path, prosite_pattern)
    # seperate propotions and patterns name
    propotions = list(map(lambda x: x[0], motifs_proportion_list))
    prosite_names = list(map(lambda x: x[1], motifs_proportion_list))
    #change to precentage and build pie chart accordinly 
    precentages = [prop * 100 for prop in propotions]
    data = np.array(precentages)
    x = [1,2,3,4,5]
    plt.bar(prosite_names, data)
    # plt.legend(prosite_names, loc = 'lower left', fontsize = 'xx-small')
    plt.xticks(fontsize = 8, rotation = 45)
    fasta_name = str(FASTA_path).rstrip('.fasta')
    title = 'patterns motifs percantages\n from '+ fasta_name
    plt.title(title)
    # plt.show()
    return plt



# calculate the proption for each motifs count and returns the list of tuples (proprotion, pattern name)
def cal_motifs_proportion(motifs_list, total_count):
    if int(total_count) == 0:
        raise Exception("total count is zero")
    motifs_proportion_list = []
    for motif in motifs_list:
        proportion = motif[0] / total_count
        motifs_proportion_list.append((proportion, motif[1]))
    return motifs_proportion_list

# returns a list of lengths of all of the motifs found from that regex from all of the records
def count_motifs_lengths(regex, records):
    re_str = str(regex)
    compiled_re = re.compile(re_str)
    lengths = []
    for record in records:
        matches = compiled_re.findall(str(record.seq))
        temp_lenghths = [len(m) for m in matches]
        lengths += temp_lenghths
    return lengths

# return number of motifs of the regex from all the records
def count_motifs(regex, records):
    re_str = str(regex)
    compiled_re = re.compile(re_str)
    temp_count = 0
    for record in records:
        matches = compiled_re.findall(str(record.seq))
        temp_count += len(matches)
    return temp_count
    

# def get_records_from_fasta(FASTA_path):
#     with open(FASTA_path) as FASTA_file:
#         records = SeqIO.parse(FASTA_file, "fasta")
#         return records
    

# parse the text file and returns a tuple: (list of fasta path files, fastq path, tuple list of prosite patten and name)
def parse_text_file(file_path):
    fasta_paths = []
    prosites = []
    with open(file_path) as file:
         #seperate each line
        for i, line in enumerate(file):
            # first 3 lines contains fasta paths 
            if (i < 3):
                fasta_paths.append(str(line).strip())
                continue
            # forth line is fastq path
            if (i == 3):
                fastq_path = str(line).strip()
                continue
            # rest of line contains prosite pattern and the pattern's name
            # added to prosites list as tuples
            temp_prosite = str(line).strip().split(";")
            prosites.append((temp_prosite[0], temp_prosite[1]))
    return fasta_paths, fastq_path, prosites

# changes prosite patterns' chars into regex like wise chars
# return a new tuple list of (pattern's regex, pattern name)
def prosite_patterns_into_regex(prosite_patterns_list):
    regex_list = []
    for prosite in prosite_patterns_list:
        pattern = str(prosite[0])
        pattern = pattern.replace("-", "")
        pattern = pattern.replace("X", ".")
        pattern = pattern.replace("x", ".")
        pattern = pattern.replace("{","[^").replace("}", "]")
        pattern = pattern.replace("(","{").replace(")", "}")
        pattern = pattern.replace("<", r"\A")
        pattern = pattern.replace(">", r"\Z")
        raw_string = r"{}".format(pattern)
        regex_list.append((raw_string, prosite[1]))
    return regex_list

# get number of reads by searching a given pattern in the fastp output
def get_reads(pattern, fastp_output):
    filtered_output = str(fastp_output).replace('\n', "")
    match = re.search(pattern, filtered_output)
    if match:
        reads = int(match.group(1))
        return reads
    else:
        print("did not find the pattern:", pattern)
        return
# return diffence between before filtered reaads and after filtered reads  
def cal_reads_diff(fastp_output):
    filtered_output = str(fastp_output).replace('\n', "")
    before_pattern = r"before filtering:total reads: (\d+)"
    after_pattern = r"after filtering:total reads: (\d+)"
    before_reads = get_reads(before_pattern, fastp_output)
    after_reads = get_reads(after_pattern, fastp_output)
    return before_reads - after_reads
    

# run fastq file on fastq programm from a given path for a limited 5 seconds
# returns the procees output
def run_fastq_on_fastp(fastp_path, fastq_path):
    try:
        # fastp_str = fastp_path.
        run_commands = fastp_path + " --in1 "+ '"' + fastq_path + '"' +" --out1 /dev/null -j /dev/null -h /dev/null"
        # Start the process and tun for 5 seconds
        process = subprocess.run(run_commands,capture_output=True, text=True, shell=True, timeout=5)
        
        if process.returncode != 0:
            # process crashed
            raise subprocess.CalledProcessError("fastp crashed")
        return process.stderr

    except FileNotFoundError:
        print("fastp path is illegal")


def main(fastp_path, txt_file_path):
    fasta_paths, fastq_path, prosites = parse_text_file(txt_file_path)
    first_part_figure(fasta_paths, prosites)
    output = run_fastq_on_fastp(fastp_path, fastq_path)
    print(cal_reads_diff(output))

if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2])
    except:
        print("invalid number of arguments")


