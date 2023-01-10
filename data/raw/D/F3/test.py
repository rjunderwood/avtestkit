import os
import csv

# Set the directory where the text files are located
directory = os.getcwd()

# Loop through every file in the directory
for filename in os.listdir(directory):
    # Check if the file is a text file
    if filename.endswith(".txt"):
        # Open the file and read through it line by line
        with open(os.path.join(directory, filename)) as f:
            printed_ = False
            reader = csv.reader(f)
            for row in reader:
              
                # Check if the row has 4 0.00 values
                if row[3] == '0.00' and row[4] == '0.00' and row[6] == '0.00' and row[7] == '0.00' and printed_ == False:
                    # Print the first value in the row and the filename
                    print(row[0], filename)
                    printed_ = True
