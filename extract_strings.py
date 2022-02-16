'''
Name: John Schaal
Date: 2022-02-16
Script: Scripting Assignment #8 - Process a memory dump and extract all relevant strings
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
ASSIGNMENT_NUMBER = "Scripting Assignment #8 - Process a memory dump and extract all relevant strings."
CHUNK_SIZE = 1024

# End of Script Constants

# Script Functions

# Print student assignment information to screen.
def studentDetails():
    print(STUDENT_NAME, COMPLETION_DATE, ASSIGNMENT_NUMBER, "", sep="\n")

# Permit user to specify a file to be processed.
def getFile():
    file = input("Enter binary file to be processed: ")
    return file

# This function will take a binary file as input and search for unique strings between 5-15 characters.
# As currently written, the output of this function will be used as the input of the printResults() function.
def stringSearch(file):
    wordPattern = re.compile(b'[a-zA-Z]{5,15}')
    wordDictionary = {}
    with open(file, 'rb') as binaryFile:
        prevChunk = b''
        while True:
            chunk = binaryFile.read(CHUNK_SIZE)
            if chunk:
                joinedChunk = prevChunk + chunk
                words = wordPattern.findall(joinedChunk)
                
                # Search for words in chunk.
                try:
                    for eachWord in words:
                        eachWord = eachWord.lower()
                        try:
                            value = wordDictionary[eachWord]
                            value += 1
                            wordDictionary[eachWord] = value
                        except:
                            wordDictionary[eachWord] = 1
                except Exception as err:
                    print("Failed to enumerate words in current chunk.")
                    print(err)
                    
                # Set prevChunk to the last 20 characters of the current chunk.
                prevChunk = chunk[-20:]
            else:
                break
            
    wordTable = PrettyTable(["Occurances", "String"])
    for key, value in wordDictionary.items():
        wordTable.add_row([value, key.decode("ascii", "ignore")])
    return wordTable

# This function will print a PrettyTable from an input table variable.
# As currently written, the input of this function is produced by the stringSearch() function.
def printResults(tableToProcess):
    print("\n", "Results")
    print(tableToProcess.get_string(sortby="Occurances", reversesort=True))

# Main function.
def main():
    try:
        studentDetails()
        try:
            file = getFile()
            try:
                stringResults = stringSearch(file)
                try:
                    printResults(stringResults)
                except Exception as err:
                    print("Failed to print results:", err)
            except Exception as err:
                print("Failed to get strings:", err)
        except Exception as err:
            print("Failed to get file:", err)
    except Exception as err:
        print("Failed to print student details:", err)       
        
# End of Script Functions
        
# Script Classes
# End of Script Classes

# Main Script Starts Here

if __name__ == "__main__":
    main()