# Gili Wolf 315144907
import sys


class Cell(object):
    def __init__(self, name, genome):
        self.name = name
        self.genome = genome

    # this function makes a string representaion of self according to the template - "<name, length of genome>"
    def __str__(self):
        cell_str = "<"
        cell_str += self.name
        cell_str += ", "
        cell_str += str(len(self.genome))
        cell_str += ">"
        return cell_str
    
    def reset_index(self, index):
        return int(index) % len(self.genome)
        
    # this function itreates over a given string and tries to find sub sequences which repeats more than 3 times (included)
    # if it finds a suitable sub suquence, it is added to a dictorney as the sub sequences is the key, 
    # and the amount of repeats are the value
    # temp_substr - the "window" of where it search the repeated sequence
    # micro_set - the hypothetical sub seq
    # algorithem: i - position of the first charcter of both the temp_substr and micro_set
    #             m - the length of the current micro_set
    #             j - amount of possible temp_substr which starts with a[i]
    #             itreating over the 3 above indexes in order to check every possible sub seqs,
    #             if after 1 iteration the temp_count (number of repeats) doesn't increase,
    #             the algorithem continues to next possible sub seq.
    def find_ssr(self, index):
        index = self.reset_index(index)
        a = self.genome[index][0]
        if (len(a) == 0):
            print("empty string")
            return
        global count
        count = 0
        dict_ssr ={}
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
                    if (micro_set in dict_ssr.keys()):
                        if (dict_ssr[micro_set] >= temp_count):
                            count = 0
                            continue
                    dict_ssr[micro_set] = temp_count
                    count = 0
        if (len(dict_ssr)==0):
            return None
        else:
            return dict_ssr



    # this function gets an str represents dna seq and returns in mRNA trancrived seq
    # algorithem : 1. reverse the str
    #              2. upper case all the str
    #              3. transcribe
    def transcribe(self, index):
        index = self.reset_index(index)
        a = self.genome[index][0]
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

    # table of mRNA codon as keys, and their matching AA as values
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
    def start_met(self, a, reading_frame):
        j = 0
        for i in range(int(reading_frame), len(a), 3):
            if i > len(a) - 3:
                return None
            codon = a[i: i +3]
            if (self.aa_table[codon] == "M"):
                    return i
        return None

    # this function translate the given a seq from its 1st met until 'stop codon' or the end of the seq
    # returns a tuple of (protein (list of aa), length of protein (aa wise), the index of the first nt after the stop codon)
    def mRNAtoAA(self,a, first_met):
        protein =[]
        j = 0
        for i in range(first_met, len(a), 3):
            if i  > (len(a) - 3):
                    return (protein, j, None)
            codon = a[i: i+3]
            if (self.aa_table[codon] == "STOP"):
                    return (protein, j, i + 3)
            protein += self.aa_table[codon]
            j += 1
        return (protein, j, i)

    # this function translates a given mRNA seq into aa list 
    # algorithem : * search for first met 
    #              * add protein to map according to its translation
    #              * search for more reading frames and add other translated proteins
    #              * return the longest (aa wise) protein in the mRNA
    # retirn none if the mRNA is a non-coding seq
    def translate(self, index):
        index = self.reset_index(index)
        a = self.transcribe(index)
        reading_frame = self.genome[index][1]
        protein_map ={}
        first_met = self.start_met(a, reading_frame)
        if first_met is not None:
            protein = self.mRNAtoAA(a, first_met)
            protein_map[protein[1]] = protein[0]
            i = 0
        else:
            return None
        while ( type(protein[2]) != None or type(first_met) != None):
            first_met = self.start_met(a[protein[2]: len(a)], 0)
            if first_met is not None:
                protein = self.mRNAtoAA(a[protein[2] + first_met: len(a)], first_met)
                protein_map[protein[1]] = protein[0]
            else:
                break
            
        return(protein_map[max(protein_map.keys())])
    
    # this function returns a list of tuples of (gene ssr, gene transalation) for each gene in the cell's genome
    def repertoire(self):
        genome_repertoire = []
        for i in range(len(self.genome)):
            genome_repertoire.append((self.find_ssr(i), self.translate(i)))
        return genome_repertoire
    
class StemCell(Cell):
    def __init__(self, genome):
        super().__init__("Stem Cell", genome)
    
    # operator override- returns a list - 1. self  2 - num. new deep copy stem cells
    def __mul__(self, num):
        if (num < 1):
            print("error- can only multiply positive numbers")
            return
        num = int(num)
        cells_list = [self]
        for i in range(num - 1):
            temp_name = self.name
            temp_list = self.genome_deep_copy()
            cells_list.append(StemCell(temp_list))
        return cells_list
    
    # this function return a deep copy list of the self genome 
    def genome_deep_copy(self):
        temp_list = []
        for gene in self.genome:
            temp_list.append((gene[0], gene[1]))
        return temp_list

    # using the mul override to return a list of self + new deep copy stemcell
    def mitosis(self):
        return self * 2
    
    # according to the cell name- returns a new diffentiated cell using builder functions
    def differentiate(self, cell_name, parameters):
        if cell_name == "Nerve Cell":
            return self.nerve_cell_builder(parameters)
        elif cell_name == "Muscle Cell":
            return self.muscle_cell_builder(parameters)
        else:
            print("stem cell doesn't support in ", cell_name, " cell differentiate")
        
    def  nerve_cell_builder(self, parameters):
        new_name = "Nerve Cell"
        return self.NerveCell(self, new_name, parameters)

    def  muscle_cell_builder(self, parameters):
        new_name = "Muscle Cell"
        list_of_parameters = parameters.split(",")
        file_path = list_of_parameters[0]
        threshhold= list_of_parameters[1]
        return self.MuscleCell(self, new_name, file_path, threshhold)

    class NerveCell(Cell):
        def __init__(self,stem_cell,name, coefficient):
            if not isinstance(stem_cell, StemCell):
                raise TypeError("Expected an instance of StemCell.")   
            self.coeiicient = coefficient
            super().__init__(name, stem_cell.genome_deep_copy())

        def receive(self, signal):
            self.signal = signal
        
        def send(self):
            return float(self.signal) * float(self.coeiicient)

    class MuscleCell(Cell):
        def __init__(self, stem_cell, name, path, threshold):
            if not isinstance(stem_cell, StemCell):
                raise TypeError("Expected an instance of StemCell.") 
            # CHECK PATH!!!
            assert open(path, 'w'), "Muscle cell can't open file"
            self.file = open(path, 'w')
            self.threshold = threshold
            super().__init__(name, stem_cell.genome_deep_copy())

        def recieve(self, signal):
            if float(signal) >= float(self.threshold):
                # NEED TO CHANGE TO PRINT INTO FILE!!!
                signal_str = str(signal)
                signal_str += ", I like to move it\n"
                self.file.write(signal_str)
                
    
class NerveNetwork:
    def __init__(self, muscle_cell, nerve_cells):
        if not any(isinstance(cell, StemCell.NerveCell) for cell in nerve_cells):
            raise TypeError("nerve network contains object which is not nerve cell")
        if not isinstance(muscle_cell, StemCell.MuscleCell): 
               print("nerve network recieved none muscle cell")
        self.muscle_cell = muscle_cell
        self.nerve_cells = nerve_cells
    
    def send_signal(self, signal):
        for cell in self.nerve_cells:
           cell.receive(signal)
           signal = cell.send()
        self.muscle_cell.recieve(signal)
    
    def __str__(self):
        self_str = ""
        for cell in self.nerve_cells:
            self_str += str(cell)
            self_str += "\n"
        self_str +=(str(self.muscle_cell))
        return self_str

# checks if cell type is legal , if not raises type error, else returns the type
def cell_type(type):
    str_type = str(type)
    if str_type != 'MC' and str_type != 'NC':
        raise TypeError("File illegal")
    else:
        return type
# check if dna chars are legal, if so return a list of the seperated dna fragments
def dna_prep(dna):
    upper_str = dna.upper()
    DNA_chars = {'A', 'T', 'C', 'G', ','}
    for char in upper_str:
        if char not in DNA_chars:
            raise TypeError("File illegal")
    return upper_str.split(',')

# check if reading frames chars are legal, if so return a list of the seperated reading frame
def r_freams_check(rf):
    rf_chars = {'1', '2', '0', ','}
    for char in rf:
        if char not in rf_chars:
            raise TypeError("File illegal")
    str_rf = str(rf)
    return str_rf.split(',')

# gets 2 list - 1. dna seqs 2. reading frames 
# creats and returns a list of synchronized tuples of dna seq and its reading frame
def create_genome(DNA_seqs, r_freams):
    dna_list = dna_prep(DNA_seqs)
    rf_list = r_freams_check(r_freams)
    if len(dna_list) != len(rf_list):
        raise TypeError("File illegal")
    genome = []
    for i, dna in enumerate(dna_list):
        genome.append((dna, rf_list[i]))
    return genome

# creats new stem cell, and returns a differentiated muscle cell
def MC_factory(genome, parameters):
    stem_cell = StemCell(genome)
    mc = stem_cell.differentiate("Muscle Cell", parameters)
    return mc

# creats new stem cell, mitosis the cell into 2 stem cells, and returns a list of the 2 differentiated nerve cell
def NC_factory(genome, parameter):
    stem_cell = StemCell(genome)
    stem_cells = stem_cell.mitosis()
    nc_list = []
    for cell in stem_cells:
        nc = cell.differentiate("Nerve Cell", parameter)
        nc_list.append(nc)
    return nc_list

# gets a gemone's repertoire and prints it according to the exercise's instructions
def print_repretoire(rep):
        
    for r in rep:
            ssr_dict = r[0]
            if (ssr_dict is not None):
                ssr_list = sorted(ssr_dict.keys())
                start = True
                for key in ssr_list:
                    if (start):
                        start = False
                    else:
                        print(";", sep = "",end = "")
                    print(key, ",", ssr_dict[key], sep = "", end = "")
                print()
            else:
                print("No simple repeats in DNA sequence")
        
            protein = r[1]
            if (protein is not None):
                print("Translation: " , end="")
                start = True
                for aa in protein:
                    if (start):
                            start = False
                    else:
                        print(";", sep = "",end = "")
                    print(aa, end= "")
                print()
            else: 
                print("Non-coding RNA")
        
def main(file_path, signals):
    with open(file_path) as file:
        flag_first = True
        NC_list = []
        MC = None
        for line in file:
            if (flag_first):
                flag_first = False
                continue
            seperated_line = line.split('\t')
            c_type = cell_type(seperated_line[0])
            genome = create_genome(seperated_line[1], seperated_line[2])
            clean_parameters = str(seperated_line[3]).rstrip("\n")
            if c_type == 'NC':
                nc = NC_factory(genome, clean_parameters)
                NC_list += nc
            else:
                MC = MC_factory(genome, clean_parameters)
        if MC is not None and len(NC_list) > 0:
            network = NerveNetwork(MC, NC_list)
            print(network)
            seperated_signals = signals.split(',')
            for s in seperated_signals:
                network.send_signal(s)
            rep = MC.repertoire()
            print_repretoire(rep)

        else: 
            print("File illegal")


main("input.txt","50,200,300")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
