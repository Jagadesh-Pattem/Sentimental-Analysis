import os
import datetime
from nltk.corpus import stopwords
from nltk import SyllableTokenizer

class Logger:
    #This class creates a log file with current time stamp as file name.
    def __init__(self):
        
        #All the logs will be present in the below folder
        self.log_folder_path = "logs/"
        
        #Creating the folder if not present
        os.makedirs(self.log_folder_path, exist_ok="True")
        
        #Getting the current time stamp
        current_timestamp = datetime.datetime.now()
        
        #Formatting the time stamp string so that file name wont create issue
        timestamp_str = current_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        self.Log_File_Path = f"{self.log_folder_path}{timestamp_str}.txt"
        
        #This will create the file if not present
        self.Log_File = open(self.Log_File_Path, "a")
    
    def log_event(self, Event):
        #Logging the event into the log file
        self.Log_File.write(Event)
        
    def close(self):
        #Closing the log file
        self.Log_File.close()


#Basic structute of a Trie node
class TrieNode:
    def __init__(self):
        #children points to the sub-trie
        self.children = {}
        #This variable says if the word is completed until here or not
        self.is_end_of_word = False


class Trie_Utils:
    #Creating the root Trie node
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """
        Traverse from root and check if each character is present.
        Once a character is found the goto next level and check if next char
        in the word is present.
        
        If not present then create a sub-trie for the remaining chars
        At end of the word make is_end_of_word = True
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
   
    
class Word_Utils:
    
    def URL_Cleaner(URL):
        
        #This will clean the URL so that no issue is created by file_name
        #Removing the protocols at the start of URL
        Protocol_Cleaner = URL.replace('https://', '').replace('www.', '')
        
        #Trimming the subols in the URL
        Symbol_Cleaner = Protocol_Cleaner.replace('/', '_').replace('-', '_')\
                                                          .replace('.', '_')
                                                          
        #Returning the cleaned URL for assigning it as file name
        return Symbol_Cleaner
    
    def Syllable_Count(word):
        syllable_tokenizer = SyllableTokenizer()
        
        #Returning the Syllable count
        return len(syllable_tokenizer.tokenize(word))
    
    def Word_Cleaner(Word_List):
        """
        Cleaning the text by removing the stop words of the english.
        Stop words of english is found using stopwords module in nltk
        """
        
        Stop_Word_Count = 0
        Stop_Words = set(stopwords.words('english'))
        Total_Word_Count = len(Word_List)
        for word in Word_List:
            if word in Stop_Words:
                Stop_Word_Count += 1
        #Returning the total clean word count
        return Total_Word_Count - Stop_Word_Count