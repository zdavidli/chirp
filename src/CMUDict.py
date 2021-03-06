import pickle
import copy

ALL_PHONEMES = {'IY', 'W', 'DH', 'Y', 'HH', 'CH', 'JH', 'ZH', 'EH', 'NG', 'TH', 'AA', 'B', 'AE', 'D', 'G', 'F', 'AH', 'K', 'M', 'L', 'AO', 'N', 'IH', 'S', 'R', 'EY', 'T', 'AW', 'V', 'AY', 'Z', 'ER', 'P', 'UW', 'SH', 'UH', 'OY', 'OW'}

exampleWords = dict()
exampleWords['IY'] = ['Eat', 'fEEt']
exampleWords['W'] = ['We', 'Wand']
exampleWords['DH'] = ['THee', 'THat']
exampleWords['Y'] = ['Yes', 'Yield']
exampleWords['HH'] = ['He', 'Head']
exampleWords['CH'] = ['CHeese', 'watCH']
exampleWords['JH'] = ['Jump', 'Jack']
exampleWords['ZH'] = ['sieZUre', 'Genre']
exampleWords['EH'] = ['hEllo', 'Eddie']
exampleWords['NG'] = ['piNG', 'haNG']
exampleWords['TH'] = ['THree', 'wiTH']
exampleWords['AA'] = ['Awesome', 'Odd']
exampleWords['B'] = ['Bat', 'haBitat']
exampleWords['AE'] = ['At', 'hAt']
exampleWords['D'] = ['Day', 'haD']
exampleWords['G'] = ['Green', 'raG']
exampleWords['F'] = ['Fee', 'halF']
exampleWords['AH'] = ['hUt', 'bUt']
exampleWords['K'] = ['Key', 'hacK']
exampleWords['M'] = ['Me', 'haM']
exampleWords['L'] = ['Lee', 'beLL']
exampleWords['AO'] = ['bOUght', 'OUght']
exampleWords['N'] = ['Need', 'haNd']
exampleWords['IH'] = ['It', 'hId']
exampleWords['S'] = ['Sea', 'hiSS']
exampleWords['R'] = ['Read', 'Ramble']
exampleWords['EY'] = ['Ate', 'hAY']
exampleWords['T'] = ['Tea', 'haT']
exampleWords['AW'] = ['cOW', 'mOUth']
exampleWords['V'] = ['Vision', 'haVE']
exampleWords['AY'] = ['rIde', 'I']
exampleWords['Z'] = ['Zebra', 'haS']
exampleWords['ER'] = ['hURt', 'bURgER']
exampleWords['P'] = ['Pen', 'hiP']
exampleWords['UW'] = ['shOE', 'bOO']
exampleWords['SH'] = ['SHe', 'slaSH']
exampleWords['UH'] = ['hUg', 'rUg']
exampleWords['OY'] = ['tOY', 'bOY']
exampleWords['OW'] = ['bOAt', 'OAt']


class CMUDict:
    word2phonemes_dict = []
    phonemes = copy.copy(ALL_PHONEMES)

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