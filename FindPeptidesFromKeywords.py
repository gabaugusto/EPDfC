import csv
import os
from bs4 import BeautifulSoup

# The name for the program
print("=== Proteomic Analisys - Find Peptides from Keywords ===")


# ask the name of the html file
# html_file = input("Enter the name of the HTML file: ")
# Setup 
print("Reading HTML file...")
html_file = "vEV_protein.html"

#origin folder  
origin_folder = "./data/"

#destiny folder
destiny_folder = "./results/"

keywordsToFind = ["Phosphorylation"]
print("Keywords to find: ", keywordsToFind)

##################################

# Read the HTML file inside the data folder
print("Reading HTML file...")
with open(origin_folder + html_file, 'r') as file:
    html_content = file.read()

# Create a BeautifulSoup object
print("Creating BeautifulSoup object...")
soup = BeautifulSoup(html_content, 'html.parser')

# Find all div elements with id="bar"
print("Finding all div elements with id='bar'...")
bar_divs = soup.find_all('div', id='bar')

mytable = []

# Loop through each div with id="bar"
for bar_div in bar_divs:

    # Check if there is a div with id="tit" inside it
    tit_div = bar_div.find('div', id='tit')
    if tit_div:

        # Save the value of the div with id="tit" inside a variable called "accession"
        accession = tit_div.text
        print(accession)

        # Look for the next sibling of the id="bar" div with an id="con"
        con_div = bar_div.find_next_sibling('div', id='con')

        if con_div is not None:

            # add the tables inside the array mytable 
            if con_div.find('table', class_='mytable'):
                mytable.append(con_div.find('table', class_='mytable'))

                if mytable is not None:

                    # get the text from last cell of every mytable row
                    for table in mytable:
                        rows = table.find_all('tr')
                        for row in rows:
                            cells = row.find_all('td')
                            if cells:
                                last_cell = cells[-1]

                                # if last_cell.text contains any of words in keywordsToFind array print last cell text
                                if any(keyword in last_cell.text for keyword in keywordsToFind):
                                    first_cell = cells[0]
                                    second_cell = cells[-2]
                                    third_cell = cells[-3]
                                    # print(accession, first_cell.text, second_cell.text, third_cell.text, last_cell.text)

                                    # lets save every row in a csv file separated by semicolon

                                    # create the file if it does not exist

                                    if not os.path.isfile(destiny_folder + html_file +"_peptides.csv"):
                                        with open(destiny_folder + html_file + "_peptides.csv", 'w') as file:
                                            writer = csv.writer(file, delimiter=';')
                                            writer.writerow(["Accession", "Peptide", "Start", "End", "Description"])
                                            writer.writerow([accession, first_cell.text, second_cell.text, third_cell.text, last_cell.text])
                                            print ("File created: ", destiny_folder + html_file + "_peptides.csv")
                                    # if the file exists

                                    else:
                                        with open(destiny_folder + html_file + "_peptides.csv", 'a') as file:
                                            writer = csv.writer(file, delimiter=';')
                                            writer.writerow([accession, first_cell.text, second_cell.text, third_cell.text, last_cell.text])    
                                            print ("File updated: ", destiny_folder + html_file + "_peptides.csv")



            else:
                print("No table with class 'mytable' found")
                
print("\nProgram finished successfully.")