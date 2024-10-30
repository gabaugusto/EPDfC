import csv
import os
from bs4 import BeautifulSoup

# The name for the program
print("=== Proteomic Analisys - Extract unique files from Keywords ===")


print("Reading CSV file...")
base_file = "./results/2024-10-30-vEV_PTM_protein.html_peptides.csv"
output_file = "./results/2024-10-30-vEV_PTM_protein_unique_proteins.csv"

# Check if the file exists  
if not os.path.exists(base_file):
    print("Error: The file does not exist")
    exit(1)

# 1. Open the csv file and read every line. 
# 2. Extract the data from the first column saving it in a list only if it is not already in the list
# 3. Extract the data to a csv

# Open the csv file
proteins = []
with open(base_file, "r") as file:

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
with open(output_file, "w") as file:
    writer = csv.writer(file)
    for protein in proteins:
        writer.writerow([protein])

#remove the empty lines from the csv file
with open(output_file, "r") as file:
    lines = file.readlines()
    lines = [line for line in lines if line.strip()]    
with open(output_file, "w") as file:
    file.writelines(lines)

print("Unique proteins extracted and saved in " + output_file)
print("Done!")