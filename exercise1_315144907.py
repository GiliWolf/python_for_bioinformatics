# Gili Wolf 315144907
import sys

def find_ssr(a):
    if (len(a) == 0):
        print("empty string")
        return
    # micro_set= str(a[0])
    # temp_substr = str(a[0])
    global count
    count = 0
    # i  = 0
    # j = 1
    dict ={}
    flag = False
    for i in range(len(a)):
        for m in range (1,len(a)):
            if (m * 3 > len(a)):
                count = 0
                break
            for j in range(i+1, len(a) + 1):
                flag = False
                # if (m * (count + 1) > len(a)):
                #         break
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
        count = 0
    count = 0
    print(dict)
find_ssr("ATCAAATCAAATCAAGAGAGAGGGGG")
