# Gili Wolf 315144907
import matplotlib.pyplot as plt
import re
from Bio.Seq import Seq
from Bio import SeqIO
import numpy as np

def first_part_figure(plt1,plt2):
    plt.subplot(1,2,1)
    plt.plot = plt1
    plt.subplot(1,2,2)
    plt.plot = plt2
    plt.title('part 1 output', loc='center')
    plt.show()

def motifs_lengths_scatter_plot(FASTA_path_1, FASTA_path_2, prosite_patterns):
    fasta_1_records = list(SeqIO.parse(FASTA_path_1, "fasta"))
    fasta_2_records = list(SeqIO.parse(FASTA_path_2, "fasta"))
    name_fasta_1 = str(FASTA_path_1).rstrip(".fasta")
    name_fasta_2 = str(FASTA_path_2).rstrip(".fasta")
    regex_patterns_list = prosite_patterns_into_regex(prosite_patterns)
    fasta_1_motifs_lengths = []
    fasta_2_motifs_lengths= []
    for regex in regex_patterns_list:
        fasta_1_motifs_lengths += count_motifs_lengths(regex[0],fasta_1_records)
        fasta_2_motifs_lengths += count_motifs_lengths(regex[0],fasta_2_records)
    fasta_1_length_dict = same_length_count(fasta_1_motifs_lengths)
    fasta_2_length_dict = same_length_count(fasta_2_motifs_lengths)
    graph = length_graph_builder(fasta_1_length_dict,fasta_2_length_dict, name_fasta_1, name_fasta_2)
    return graph

def length_graph_builder(fasta_1_length_dict,fasta_2_length_dict, name_fasta_1, name_fasta_2):
    lengths_fasta_1 = np.array([length for length in fasta_1_length_dict.keys()])
    occurrences_fasta_1 = np.array([count for count in fasta_1_length_dict.values()])
    lengths_fasta_2 = np.array([length for length in fasta_2_length_dict.keys()])
    occurrences_fasta_2 = np.array([count for count in fasta_2_length_dict.values()])
    plt.scatter(lengths_fasta_1, occurrences_fasta_1, color = 'r')
    plt.scatter(lengths_fasta_2, occurrences_fasta_2, color = 'b')
    plt.legend(['fasta1', 'fasta2'], loc = 'upper left')
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


def relative_percentage_graph(FASTA_path, prosite_patterns):
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
    motifs_proportion_list = cal_motifs_proportion(motifs_count_list, motifs_total_count)
    graph = percentage_graph_builder(motifs_proportion_list)
    return graph

#builds a pie chart out of tuple list of propotions and name of patterns
def percentage_graph_builder(motifs_proportion_list):
    # seperate propotions and patterns name
    propotions = list(map(lambda x: x[0], motifs_proportion_list))
    prosite_names = list(map(lambda x: x[1], motifs_proportion_list))
    #change to precentage and build pie chart accordinly 
    precentages = [prop * 100 for prop in propotions]
    data = np.array(precentages)
    plt.pie(data, autopct='%1.1f%%', radius= 0.7)
    plt.legend(prosite_names, loc = 'upper right', fontsize = 'x-small')
    plt.title('patterns motifs percantages')
    plt.show()
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
    return (fasta_paths, fastq_path, prosites)

#changes prosite patterns' chars into regex like wise chars
# return a new tuple list of (pattern's regex, pattern name)
def prosite_patterns_into_regex(prosite_patterns_list):
    regex_list = []
    for prosite in prosite_patterns_list:
        pattern = str(prosite[0])
        # if "X" in pattern:
        pattern = pattern.replace("-", "")
        pattern = pattern.replace("X", ".")
        pattern = pattern.replace("x", ".")
        pattern = pattern.replace("{","[^").replace("}", "]")
        pattern = pattern.replace("(","{").replace(")", "}")
        # pattern = pattern.replace("{", "#")
        # pattern = pattern.replace("}", "%")
        # pattern = pattern.replace("(", "{")
        pattern = pattern.replace("<", r"\A")
        pattern = pattern.replace(">", r"\Z")
        raw_string = r"{}".format(pattern)
        regex_list.append((raw_string, prosite[1]))
    return regex_list



datata = parse_text_file("text.txt")
# regex_list = prosite_patterns_into_regex(datata[2])
g1 = motifs_lengths_scatter_plot(datata[0][0],datata[0][1], datata[2])
g2 = relative_percentage_graph(datata[0][0], datata[2])
first_part_figure(g1, g2)
# print ("ki")
