import cPickle as pickle

class CMUDict:
    word2phonemes_dict = []
    phonemes = {'IY', 'W', 'DH', 'Y', 'HH', 'CH', 'JH', 'ZH', 'EH', 'NG', 'TH', 'AA', 'B', 'AE', 'D', 'G', 'F', 'AH', 'K', 'M', 'L', 'AO', 'N', 'IH', 'S', 'R', 'EY', 'T', 'AW', 'V', 'AY', 'Z', 'ER', 'P', 'UW', 'SH', 'UH', 'OY', 'OW'}

    def __init__(self):
        self.word2phonemes_dict = []
        
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
            self.word2phonemes_dict = pickle.load(f)    

    def get_dict(self):
        return self.word2phonemes_dict
    
    def get_phonemes(self):
        return self.phonemes
        
    def get_phonemes_from_text(self, word):
        pronunciations = self.word2phonemes_dict[word.upper()]
        return pronunciations