import csv
import os
from bs4 import BeautifulSoup

# The name for the program
print("=== Proteomic Analisys - Extract unique files from Keywords ===")


print("Reading CSV file...")
html_file = "./results/aEV_protein.html_peptides.csv"
output_file = "./results/aEV_unique_proteins.csv"

# Check if the file exists  
if not os.path.exists(html_file):
    print("Error: The file does not exist")
    exit(1)

# 1. Open the csv file and read every line. 
# 2. Extract the data from the first column saving it in a list only if it is not already in the list
# 3. Extract the data to a csv

# Open the csv file
proteins = []
with open(html_file, "r") as file:

    # Open the csv file separated by semi-colon
    reader = csv.reader(file, delimiter=";")
    if not reader:
        print("Error: The file is empty")
        exit(1)
    # Read every line
    for row in reader:
        if row and row[0] != "Protein":
            # Extract the first column
            protein = row[0]
            # Check if the protein is not already in the list
            if protein not in proteins:
                proteins.append(protein)

# Save the unique proteins in a csv file
with open("./results/aEV_unique_proteins.csv", "w") as file:
    writer = csv.writer(file)
    for protein in proteins:
        writer.writerow([protein])

#remove the empty lines from the csv file
with open("./results/aEV_unique_proteins.csv", "r") as file:
    lines = file.readlines()
    lines = [line for line in lines if line.strip()]    
with open("./results/aEV_unique_proteins.csv", "w") as file:
    file.writelines(lines)

print("Unique proteins extracted and saved in 'results/unique_proteins.csv'")
print("Done!")