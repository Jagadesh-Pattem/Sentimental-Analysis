"""
For faster search operations I have created a Trie each for:
    1) Stop_Words
    2) Positive Words
    3) Negative words
"""
import Utils

#Stop_Word file paths
AUDITOR_FILE_PATH = "StopWords\StopWords_Auditor.txt"
CURRENCIES_FILE_PATH = "StopWords\StopWords_Currencies.txt"
DATES_AND_NUMBERS_FILE_PATH = "StopWords\StopWords_DatesandNumbers.txt"
GENERIC_FILE_PATH = "StopWords\StopWords_Generic.txt"
GENERIC_LONG_FILE_PATH = "StopWords\StopWords_GenericLong.txt"
GEOGRAPHIC_FILE_PATH = "StopWords\StopWords_Geographic.txt"
NAMES_FILE_PATH = "StopWords\StopWords_Names.txt"

#Positive and negative file paths
POSITIVE_WORD_FILE_PATH = "MasterDictionary\positive-words.txt"
NEGATIVE_WORD_FILE_PATH = "MasterDictionary\\negative-words.txt"

#All the stop words will be populated into this
STOP_WORDS_LIST = []
Stop_Word_File_Array = [AUDITOR_FILE_PATH, CURRENCIES_FILE_PATH, 
                        DATES_AND_NUMBERS_FILE_PATH, GENERIC_FILE_PATH, 
                        GENERIC_LONG_FILE_PATH, GEOGRAPHIC_FILE_PATH, 
                        NAMES_FILE_PATH]

for file in Stop_Word_File_Array:
    File = open(file, "r")
    Text_in_File = File.read()
    Lines_in_File = Text_in_File.split('\n')
    #Extracting word from each line pnly the word before | is a stop-word
    #Everything after | is an explaination for this word.
    #So splitting the line with | as delimitor and getting the first element
    for line in Lines_in_File:
        STOP_WORDS_LIST.append(line.split('|')[0].strip())

POSITIVE_FILE = open(POSITIVE_WORD_FILE_PATH, "r")
NEGATIVE_FILE = open(NEGATIVE_WORD_FILE_PATH, "r")

#In every line there is a word in Positive and negative word file
POSITIVE_WORDS_LIST = POSITIVE_FILE.read().split('\n')
NEGATIVE_WORDS_LIST = NEGATIVE_FILE.read().split('\n')

#Creating a TRIE each for Stop, Positive, Negative words.
STOP_WORDS_TRIE = Utils.Trie_Utils()
POSITIVE_WORDS_TRIE = Utils.Trie_Utils()
NEGATIVE_WORDS_TRIE = Utils.Trie_Utils()

#Populating the tries with their corresponding words lists
for word in STOP_WORDS_LIST:
    STOP_WORDS_TRIE.insert(word.lower())
    
for word in POSITIVE_WORDS_LIST:
    POSITIVE_WORDS_TRIE.insert(word.lower())
    
for word in NEGATIVE_WORDS_LIST:
    NEGATIVE_WORDS_TRIE.insert(word.lower())