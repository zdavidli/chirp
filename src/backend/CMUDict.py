import cPickle as pickle

ALL_PHONEMES = {'IY', 'W', 'DH', 'Y', 'HH', 'CH', 'JH', 'ZH', 'EH', 'NG', 'TH', 'AA', 'B', 'AE', 'D', 'G', 'F', 'AH', 'K', 'M', 'L', 'AO', 'N', 'IH', 'S', 'R', 'EY', 'T', 'AW', 'V', 'AY', 'Z', 'ER', 'P', 'UW', 'SH', 'UH', 'OY', 'OW'}

class CMUDict:
    word2phonemes_dict = []
    phonemes = {'IY', 'W', 'DH', 'Y', 'HH', 'CH', 'JH', 'ZH', 'EH', 'NG', 'TH', 'AA', 'B', 'AE', 'D', 'G', 'F', 'AH', 'K', 'M', 'L', 'AO', 'N', 'IH', 'S', 'R', 'EY', 'T', 'AW', 'V', 'AY', 'Z', 'ER', 'P', 'UW', 'SH', 'UH', 'OY', 'OW'}

    def __init__(self):
        self.word2phonemes_dict = []
        
    #generate dictionary from file
    """ 
    Input: Dictionary file (CMUDict)
    Output: None
    Generate dictionary from file and save to dictionary in class
    """
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
                
                if el[-1] == '0' or el[-1] == '1' or el[-1] == '2':
                    stress = (el[:-1], int(el[-1]))
                else:
                    stress = (el, 0)
                stresses.append(stress)
            try:
                output[word].append(stresses)
            except KeyError:
                output[word] = [stresses]

		self.dictionary = output
        #save file to pickle file
        pickle.dump(output, open('dict.p', "wb" ))

    def load_dict(self, filename):
        with open(filename, 'r') as f:
            self.word2phonemes_dict = pickle.load(f)    

    def get_dict(self):
        return self.word2phonemes_dict
    
    def get_phonemes(self):
        return self.phonemes
        
    """
    Input: Single word to decompose into phonemes
    Output: List of possible pronunciations of word, 
            pronunciations are lists of sets of phonemes mapped to stresses
            
    Example: 
        get_phonemes("HELLO")
    Output: [[{'HH': 0}, {'AH': '0'}, {'L': 0}, {'OW': '1'}], [{'HH': 0}, {'EH': '0'}, {'L': 0}, {'OW': '1'}]]
    """
    def get_phonemes_from_text(self, word):
        pronunciations = self.word2phonemes_dict[word.upper()]
        return pronunciations