import csv
import os
from bs4 import BeautifulSoup

# The name for the program
print("=== Proteomic Analisys - Find Peptides from Keywords ===")

print("Reading HTML file...")

# ask the name of the html file
# html_file = input("Enter the name of the HTML file: ")
# Setup 
html_file = "aEV_protein.html"

#origin folder  
origin_folder = "./data/"

#destiny folder
destiny_folder = "./results/"

keywordsToFind = ["Phosphorylation", "Acetylation"]
print("Keywords to find: ", keywordsToFind)

##################################

# Read the HTML file
print("Reading HTML file...")
with open(html_file, 'r') as file:
    html_content = file.read()

# Create a BeautifulSoup object
print("Creating BeautifulSoup object...")
soup = BeautifulSoup(html_content, 'html.parser')

# Find all div elements with id="bar"
print("Finding all div elements with id='bar'...")
bar_divs = soup.find_all('div', id='bar')

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
        
        mytable = ""
        
        if con_div is not None:
            mytable = con_div.find('table', class_='mytable')
        else:
            print("con_div is None")
            # or raise an exception
            # raise ValueError("con_div is None")
        
        if mytable is not None:
           
            if isinstance(mytable, str):
                mytable = BeautifulSoup(mytable, 'html.parser')
            
            peptide_tables = mytable.find_all('table', class_='mytable')
            
            for table in peptide_tables:
                thead = table.find('thead')
                first_cell_head = thead.find('th')
                print("mytable_ ")
               
                if first_cell_head and 'peptide' in first_cell_head.text.lower():
                    tbody = table.find('tbody')
                    rows = tbody.find_all('tr')
                    for row in rows:
                        last_cell = row.find_all('td')[-1]
                        print("Last Cell:" + last_cell.text)
        else:
            print("No table with class 'mytable' found")
print("\nProgram finished successfully.")