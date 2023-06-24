# Gili Wolf 315144907
import matplotlib.pyplot as plt
import re
from Bio.Seq import Seq
from Bio import SeqIO



def relative_percentage_graph(FASTA_path, prosite_patterns):
    fasta_records = SeqIO.parse(FASTA_path, "fasta")
    regex_patterns_list = prosite_patterns_into_regex(prosite_patterns)
    motifs_count_list = []
    motifs_total_count = 0
    for regex in regex_patterns_list:
        temp_re_count = count_motifs(regex[0], fasta_records)
        motifs_count_list.append((temp_re_count, regex[1]))
        motifs_total_count += temp_re_count
    # print(motifs_count_list)
    motifs_proportion_list = cal_motifs_proportion(motifs_count_list, motifs_total_count)
    # print(motifs_proportion_list)

def percentage_graph_builder(motifs_proportion_list):
    pass
# calculate the proption for each motifs count and returns the list of tuples (proprotion, pattern name)
def cal_motifs_proportion(motifs_list, total_count):
    if int(total_count) == 0:
        raise Exception("total count is zero")
    motifs_proportion_list = []
    for motif in motifs_list:
        proportion = motif[0] / total_count
        motifs_proportion_list.append((proportion, motif[1]))
    return motifs_proportion_list
        
# return number of motifs of the regex from all the records
def count_motifs(regex, records):
    re_str = str(regex)
    re.compile(re_str)
    temp_count = 0
    for record in records:
        matches = re.findall(re_str, str(record.seq))
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
        pattern = pattern.replace("(", "{")
        pattern = pattern.replace("<", r"\A")
        pattern = pattern.replace(">", r"\Z")
        raw_string = r"{}".format(pattern)
        regex_list.append((pattern, prosite[1]))
    return regex_list



datata = parse_text_file("text.txt")
# regex_list = prosite_patterns_into_regex(datata[2])
relative_percentage_graph(datata[0][0], datata[2])

print ("ki")
