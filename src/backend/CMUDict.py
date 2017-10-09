import cPickle as pickle

class CMUDict:

    dictionary = []

    phonemes = set(['IY', 'W', 'DH', 'Y', 'HH', 'CH', 'JH', 'ZH', 'EH', 'NG', 
					'TH', 'AA', 'B', 'AE', 'D', 'G', 'F', 'AH', 'K', 'M', 'L', 
					'AO', 'N', 'IH', 'S', 'R', 'EY', 'T', 'AW', 'V', 'AY', 'Z', 
					'ER', 'P', 'UW', 'SH', 'UH', 'OY', 'OW'])

    def __init__(self, filename):
        dictionary = self.gen_dict(filename)

    #generate dictionary from file
    def gen_dict(self, infile):
        file_in = list()
        with open(infile, 'r') as f:
            for line in f:
                if line[0].isalpha():
                    file_in.append(line.strip())

        #output dictionary of words to pronunciations
        output = {}

        for line in file_in:
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
                if el[-1] == '0' or el[-1] == '1' or el[-1] == '2':
                    stress[el[:-1]] = el[-1]
                else:
                    stress[el] = 0
                stresses.append(stress)
            try:
                output[word].append(stresses)
            except KeyError:
                output[word] = [stresses]

        #save file to pickle file
        pickle.dump(output, open('dict.p', "wb" ))

    def load_dict(self, filename):
        with open(filename, 'r') as f:
            self.dictionary = pickle.load(f)
        return self.dictionary
:
	def get_dict():
		return self.dictionary
	
	def get_phoneme_set():
		return self.phonemes

cmudict = CMUDict('cmudict-0.7b.txt')
d = cmudict.load_dict('dict.p')
