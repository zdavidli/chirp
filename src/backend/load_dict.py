def load_dict():
    status_inc = 10000

    file_in = list()
    with open('cmudict-0.7b.txt', 'r') as f:
        for line in f:
            if line[0].isalpha():
                file_in.append(line.strip())

    #output dictionary of words to pronunciations
    output = {}

    count = 0
    for line in file_in:
        count += 1
        #process entries in cmudict
        parts = line.split()

        #handle multiple pronunciations
        if parts[0][-1] == ")":
            word = parts[0][:-3]
        else:
            word = parts[0]
        #word is key in dictionary to list of pronunciation(s)

        pronunciation = parts[1:]
        #map phoneme to stress in pronunciation
        stresses = []
        for el in pronunciation:
            stress = {}
            if el[-1].isdigit():
                if el[-1] == '0' or el[-1] == '1' or el[-1] == '2':
                    stress[el[:-1]] = el[-1]
            else:
                stress[el] = 0
            stresses.append(stress)

        try:
            output[word].append(stresses)
        except KeyError:
            output[word] = [stresses]
        if count % status_inc == 0:
            print(count, len(output))
    return output

import cPickle as pickle

d = load_dict()
pickle.dump(d, open( "dict.p", "wb" ) )
