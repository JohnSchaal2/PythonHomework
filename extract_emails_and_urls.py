'''
Name: John Schaal
Date: 2022-02-16
Script: Scripting Assignment #7 - Extract e-mail address and urls from the memory dump provided.
'''

# Script Module Importing
# Python Standard Library Modules
import re       #Regular Expressions

# Import 3rd Party Modules
from prettytable import PrettyTable     #PrettyTable

# End of Script Module Importing

# Script Constants
# Psuedo Constants

STUDENT_NAME  = "Name: John Schaal"
COMPLETION_DATE = "Date: 2022-02-16"
ASSIGNMENT_NUMBER = "Script: Scripting Assignment #7 - Extract e-mail address and urls from the memory dump provided."
CHUNK_SIZE = 1024

# End of Script Constants

# Script Functions

# Print student assignment information to screen.
def studentDetails():
    print(STUDENT_NAME, COMPLETION_DATE, ASSIGNMENT_NUMBER, "", sep="\n")
    
def getFile():
    # Permit user to specify a file to be processed.
    file = input("Enter binary file to be processed: ")
    return file

# This function will take a binary file as input and search for emails.
def emailSearch(file):
    emailPattern = re.compile(b'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}')
    emailDictionary = {}
    with open(file, 'rb') as binaryFile:
        prevChunk = b''
        while True:
            chunk = binaryFile.read(CHUNK_SIZE)
            if chunk:
                joinedChunk = prevChunk + chunk
                emails = emailPattern.findall(joinedChunk)
                
                # Search for emails in chunk.
                try:
                    for eachEmail in emails:
                        eachEmail = eachEmail.lower()
                        try:
                            value = emailDictionary[eachEmail]
                            value += 1
                            emailDictionary[eachEmail] = value
                        except:
                            emailDictionary[eachEmail] = 1
                except Exception as err:
                    print("Failed to enumerate words in current chunk.")
                    print(err)
                        
                # Set prevChunk to the last 20 characters of the current chunk.
                prevChunk = chunk[-20:]
            else:
                break
            
    emailTable = PrettyTable(["Occurances", "Email Address"])
    for key, value in emailDictionary.items():
        emailTable.add_row([value, key.decode("ascii", "ignore")])
    return emailTable

# This function will take a binary file as input and search for URLs.
def urlSearch(file):
    urlPattern = re.compile(b'\w+:\/\/[\w@][\w.:@]+\/?[\w.\.?=%&=\-@$,]*')
    urlDictionary = {}
    with open(file, 'rb') as binaryFile:
        prevChunk = b''
        while True:
            chunk = binaryFile.read(CHUNK_SIZE)
            if chunk:
                joinedChunk = prevChunk + chunk
                urls = urlPattern.findall(joinedChunk)
                
                # Search for URLs in current chunk.
                for eachUrl in urls:
                    eachUrl = eachUrl.lower()
                    try:
                        value = urlDictionary[eachUrl]
                        value += 1
                        urlDictionary[eachUrl] = value
                    except:
                        urlDictionary[eachUrl] = 1
                        
                # Set prevChunk to the last 20 characters of the current chunk.
                prevChunk = chunk[-20:]                
            else:
                break
            
        urlTable = PrettyTable(["Occurances", "URL Address"])
        for key, value in urlDictionary.items():
            urlTable.add_row([value, key.decode("ascii", "ignore")])
        return urlTable

# This function will print a PrettyTable from an input table variable.
def printResults(tableToProcess, tableName):
    print("\n", (tableName+"Results"))
    print(tableToProcess.get_string(sortby="Occurances", reversesort=True))

# Main function.
def main():
    try:
        studentDetails()
        try:
            file = getFile()
            try:
                emailResults = emailSearch(file)
                try:
                    urlResults = urlSearch(file)
                    try:
                        printResults(emailResults, "Email")
                        try:
                            printResults(urlResults, "URL")
                        except Exception as err:
                            print("Failed to print URL table:", err)
                    except Exception as err:
                        print("Failed to print Email table:", err)
                except Exception as err:
                    print("Failed to parse URLs:", err)
            except Exception as err:
                print("Failed to parse emails:", err)
        except Exception as err:
            print("Failed to get file:", err)
    except Exception as err:
        print("Failed to print student details.", err)
        
# End of Script Functions
        
# Script Classes
# End of Script Classes

# Main Script Starts Here

if __name__ == "__main__":
    main()