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

