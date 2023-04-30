# Gili Wolf 315144907
import sys

# this function itreate on a given string and tries to find sub sequences which repeats more than 3 times (included)
# if it finds a suitable sub suquence, it is added to a dictorney as the sub sequences is the key, 
# and the amount of repits are the value
# temp_substr - the "window" of where it search the repeated sequence
# micro_set - the hypothetical sub seq
# algorithem: i - position of the first charcter of both the temp_substr and micro_set
#             m - the length of the current micro_set
#             j - amount of possible temp_substr which starts with a[i]
#             itreating over the 3 above indexes in order to check every possible sub seqs,
#             if after 1 iteration the temp_count (number of repeats) doesn't increase,
#             the algorithem continues to next possible sub seq.
def find_ssr(a):
    if (len(a) == 0):
        print("empty string")
        return
    global count
    count = 0
    dict ={}
    flag = False
    for i in range(len(a)):
        for m in range (1,len(a)):
            if (m * 3 > len(a)):
                count = 0
                break
            for j in range(i+1, len(a) + 1):
                flag = False
                temp_substr = a[i:i + (m * (count + 1)):]
                micro_set = a[i:i+m:]
                temp_count = temp_substr.count(micro_set)
                if temp_count > count:
                    count = temp_count 
                else:
                    count = 0
                    break
            if (temp_count >= 3):
                if (micro_set in dict.keys()):
                     if (dict[micro_set] >= temp_count):
                        count = 0
                        continue
                dict[micro_set] = temp_count
                count = 0
    if (len(dict)==0):
        return None
    else:
        return dict



# this function gets an str represents dna seq and returns in mRNA trancrived seq
# algorithem : 1. reverse the str
#              2. upper case all the str
#              3. transcribe
def transcribe(a):
    reverse_str = a[::-1]
    upper_str = reverse_str.upper()
    transcribed_str = ""
    for i in upper_str:
        if i == "A":
            transcribed_str += 'U'
        elif i == "T":
            transcribed_str += 'A'
        elif i == "C":
            transcribed_str += 'G'
        elif i == "G":
            transcribed_str += 'C'
    return transcribed_str

aa_table = {"UUU":"F", "UUC":"F", "UUA":"L", "UUG":"L",
       "UCU":"S", "UCC":"s", "UCA":"S", "UCG":"S",
       "UAU":"Y", "UAC":"Y", "UAA":"STOP", "UAG":"STOP",
       "UGU":"C", "UGC":"C", "UGA":"STOP", "UGG":"W",
       "CUU":"L", "CUC":"L", "CUA":"L", "CUG":"L",
       "CCU":"P", "CCC":"P", "CCA":"P", "CCG":"P",
       "CAU":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
       "CGU":"R", "CGC":"R", "CGA":"R", "CGG":"R",
       "AUU":"I", "AUC":"I", "AUA":"I", "AUG":"M",
       "ACU":"T", "ACC":"T", "ACA":"T", "ACG":"T",
       "AAU":"N", "AAC":"N", "AAA":"K", "AAG":"K",
       "AGU":"S", "AGC":"S", "AGA":"R", "AGG":"R",
       "GUU":"V", "GUC":"V", "GUA":"V", "GUG":"V",
       "GCU":"A", "GCC":"A", "GCA":"A", "GCG":"A",
       "GAU":"D", "GAC":"D", "GAA":"E", "GAG":"E",
       "GGU":"G", "GGC":"G", "GGA":"G", "GGG":"G"}

# this function finds the first AUG codon (met) in the givan a seq, and returns its index
# return None if there is not such codon
def start_met(a, reading_frame):
    j = 0
    for i in range(reading_frame, len(a), 3):
        if i > len(a) - 3:
            return None
        codon = a[i: i +3]
        if (aa_table[codon] == "M"):
                return i
    return None

# this function translate the given a seq from its 1st met until 'stop codon' or the end of the seq
# returns a tuple of (protein (list of aa), length of protein (aa wise), the index of the first nt after the stop codon)
def mRNAtoAA(a, first_met):
    protein =[]
    j = 0
    for i in range(first_met, len(a), 3):
        if i  > (len(a) - 3):
                return (protein, j, None)
        codon = a[i: i+3]
        if (aa_table[codon] == "STOP"):
                return (protein, j, i + 3)
        protein += aa_table[codon]
        j += 1

# this function translates a given mRNA seq into aa list 
# algorithem : * search for first met 
#              * add protein to map according to its translation
#              * search for more reading frames and add other translated proteins
#              * return the longest (aa wise) protein in the mRNA
# retirn none if the mRNA is a non-coding seq
def translate(a, reading_frame):
    protein_map ={}
    first_met = start_met(a, reading_frame)
    if first_met is not None:
        protein = mRNAtoAA(a, first_met)
        protein_map[protein[1]] = protein[0]
        i = 0
    else:
        return None
    while ( type(protein[2]) != None or type(first_met) != None):
        first_met = start_met(a[protein[2]: len(a)], 0)
        if first_met is not None:
            protein = mRNAtoAA(a[protein[2] + first_met: len(a)], first_met)
            protein_map[protein[1]] = protein[0]
        else:
            break
        
    return(protein_map[max(protein_map.keys())])


def main(ssr_dna_seq, dna_to_rna, rna_to_aa, reading_frame):
    if ssr_dna_seq is not None:
        ssr_dict = find_ssr(ssr_dna_seq)
        ssr_list = sorted(ssr_dict.keys())
        start = True
        for key in ssr_list:
            if (start):
                start = False
            else:
                print(";", end = "")
            print(key, ",", ssr_dict[key], end = "")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
