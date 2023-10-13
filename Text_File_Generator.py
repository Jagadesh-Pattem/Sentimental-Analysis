import os
import requests
import pandas as pd
from Utils import Word_Utils, Logger
from bs4 import BeautifulSoup

Input_File_Path = 'Input.xlsx'
Log_File = Logger()
#All the text-files will be present here
Folder_Path = 'Text_Files/'
Extension = ".txt"
Separator = "-"*150+"\n\n"
#Creating the text file folder if it is not present
os.makedirs(Folder_Path, exist_ok=True)
Data_Frame = pd.read_excel(Input_File_Path)

#Some files have content in the div with following parameters 
Type1_Attr_Dict = {'class': 'td-post-content tagdiv-type'}

#Other files have content nested inside two div containers
#The outer div has following parameters
Type2_Outer_Div_Attr_Dict = {'data-td-block-uid': 'tdi_130'}

#The inner div has following parameters
Type2_Inner_Div_Attr_Dict = {'class': 'tdb-block-inner td-fix-index'}

#Creating a text file for URL in each row
for index, row in Data_Frame.iterrows():
    print(f"URL_{index} Extracting text from {row['URL']}")
    Log_File.log_event(f"URL_{index}\nWorking on {row['URL']}\n")
    
    try:
        #Sending a HTML request for the URL
        URL_HTML = requests.get(row['URL'])
        Log_File.log_event("URL Accessed\n")
        
        #If the page is not found text file is not created.
        if URL_HTML.status_code == 404:
            Log_File.log_event(f"Page not found\n{row['URL']}\n")
            Log_File.log_event(Separator)
            continue
        
        #Creating a soup object on the content returned by request response
        soup = BeautifulSoup(URL_HTML.content, 'html5lib')
        
        #Extracting the title of the HTML Page
        Title = soup.find('title')
        
        #Appending the Title to the Text_Content variable
        Text_File_Content = Title.text+'\n'
        
        #Finding the Div in which the Body content is present
        Text_in_HTML = soup.find('div', attrs = Type1_Attr_Dict)
        
        #If None is returned then it means page is of type-2
        if Text_in_HTML == None:
            #Accessing the outer Div
            Outer_Div = soup.find('div', attrs = Type2_Outer_Div_Attr_Dict)
            #Accessing the inner Div
            Text_in_HTML= Outer_Div.find('div', 
                                         attrs = Type2_Inner_Div_Attr_Dict)
        
        #Once the Div with the content is found we are extracting the 
        #paragraph text with in that div. This gives the text content in the
        #page.
        for para in Text_in_HTML.findAll('p'):
            Text_File_Content = Text_File_Content+para.text+'\n'
        Log_File.log_event("Text extracted from URL\n")
        
        #Cleaning the URL as the file name can't be same as URL because it 
        #gives error
        simplified_URL = Word_Utils.URL_Cleaner(row['URL'])
        File_Name = f"{Folder_Path}{simplified_URL}_{row['URL_ID']}{Extension}"
        
        #Creating the text file and writing the content inside it
        with open(File_Name, "w", encoding="utf-8") as File:
            File.write(Text_File_Content)
            File.close()
    
        Log_File.log_event(f"File created:\t {File_Name}\n")
        Log_File.log_event(Separator)
        
    except requests.exceptions.ConnectionError:
        #This happens when there is no internet connection
        Log_File.log_event("A connection error occurred. \
                           Please check your internet connection.\n")
        Log_File.log_event(Separator)
        
    except requests.exceptions.Timeout:
        #This happens when the connection is timed out
        Log_File.log_event("The request timed out.\n")
        Log_File.log_event(Separator)
        
    except requests.exceptions.HTTPError as e:
        #Then happens when the http response code is more than 400
        Log_File.log_event("HTTP Error:\n", e)
        Log_File.log_event(Separator)
        
    except requests.exceptions.RequestException as e:
        #This is a generic exception
        Log_File.log_event("An error occurred:\n", e)
        Log_File.log_event(Separator)