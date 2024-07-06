import csv
import os
from bs4 import BeautifulSoup # pip install beautifulsoup4

# Create a name for the program
print("=== Proteomic Analisys - Extraction and Process data from HTML files ===")

# Print the welcome message
print("\nThis program will read the HTML file and extract the data to two CSV files. This program is projected to solve easily the extration of proteins and their features for microbiology studies.\nResponsible science: Carla E. Octaviano Azevedo.\nDeveloper: Gabriel A. Azevedo.\n")

print("Resume: \n- The program read the HTML file and extracted the data to two CSV files. \n- The program is projected to solve easily the extration of proteins and their features for microbiology studies.")

# ask the name of the html file

#origin folder  
source_folder = "./data/"

#destiny folder
destiny_folder = "./results/"

def process_files(file):

    print("=== Initiating Phase 01")

    # Read the HTML file
    with open(file, 'r') as file:
        html_content = file.read()

    # Create a set to store unique combinations of WORD and last cell values
    unique_combinations = set()

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all div elements with id="bar"
    bar_divs = soup.find_all('div', id='bar')

    # Loop through each div with id="bar"
    for bar_div in bar_divs:
        # Find div with id="tit" inside the current bar_div
        tit_div = bar_div.find('div', id='tit')
        if tit_div:
            # Get the text inside the div with id="tit"
            word = tit_div.text.strip()

            # Find the next div with id="con" after the current bar_div
            con_div = bar_div.find_next_sibling('div', id='con')
            if con_div:
                # Find the table within the con_div
                table = con_div.find('table')
                if table:
                    # Find all rows in the table
                    rows = table.find_all('tr')

                    # Loop through each row and add unique combinations to the set
                    for row in rows:
                        cells = row.find_all('td')
                        if cells:
                            last_cell = cells[-1].text.strip()
                            if last_cell:
                                unique_combinations.add((word, last_cell))

    # Write unique combinations to a CSV file
    print("Writing temp csv file... ")
    with open('unique_combinations_data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header
        csv_writer.writerow(['WORD', 'LastCell'])
        
        # Write unique combinations
        for combo in unique_combinations:
            csv_writer.writerow(combo)

    print("=== Initiating Phase 02")
    # Writing features CSV file
    print("Writing features csv file... ")

    # Set to store features
    features_set = set()

    # Open the input CSV file
    with open('unique_combinations_data.csv', newline='', encoding='utf-8') as csvfile:
        # Create a CSV reader
        reader = csv.reader(csvfile, delimiter=';')
        # Skip the header
        next(reader, None)
        # Iterate over each row
        for row in reader:
            # Extract features from the row
            features = row[1:]
            # Update the set with unique features
            features_set.update(features)

    #convert type _io.TextIOWrapper to string
    file = str(file)

    #extract the value from name attribute as string e.g. "<_io.TextIOWrapper name='./data/aEV_protein.html' mode='r' encoding='cp1252'>unique_features.csv" to aEV_protein.html
    file = file.split("'")[1]

    #remove "./data/" from the string e.g. "./data/aEV_protein.html" to "aEV_protein.html"
    file = file.replace(source_folder, "")
    file = file + ".html"

    print("=========" + file)

    # Write the unique features to a new CSV file    
    unique_features_file = file + "unique_features.csv"

    with open(unique_features_file, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile, delimiter=';')
        # Write each feature to the CSV file
        for feature in features_set:
            writer.writerow([feature])

    print("Unique features saved to " + unique_features_file)

    print("=== Initiating Phase 03")
    # Reading the CSV file and organizing the features by code
    features_by_code = {}

    with open('unique_combinations_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            code = row[0]
            features = row[1:]

            if code not in features_by_code:
                features_by_code[code] = set()

            for feature in features:
                if feature.strip():  # check if the feature is not empty
                    features_by_code[code].add(feature.strip())

    # Writing the result to the new CSV file
    print("Writing final csv file... ")

    # get file name without extension and add "_final-results.csv"
    final_file = file + "_final-results.csv"
  
    with open(final_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for code, features in features_by_code.items():
            writer.writerow([code] + list(features))

    # move results to destiny folder
    os.rename(unique_features_file, destiny_folder + unique_features_file)
    os.rename(final_file, destiny_folder + final_file)

    print("Results saved to " + final_file)

    # delete the temporary files
    os.remove("unique_combinations_data.csv")

    print("\nFile processed successfully!")


# process the files inside the origin folder
for html_file in os.listdir(source_folder):
    if html_file.endswith(".html"):
        #extract the file name from io.TextIOWrapper as string e.g. "<_io.TextIOWrapper name='./data/aEV_protein.html' mode='r' encoding='cp1252'>unique_features.csv"
        html_file = str(html_file).split(".")[0]
        #remove "./data/" from the string e.g. "./data/aEV_protein.html" to "aEV_protein.html
        html_file = html_file.replace(source_folder, "")
        html_file = html_file + ".html"
        print("Processing file: " + html_file)

        process_files(source_folder + html_file)

print("\nAll files processed.")
print("List of files processed: ")
for html_file in os.listdir(source_folder):
    if html_file.endswith(".html"):
        print(html_file)

print("\Program Finished Successfully! Yay!")
