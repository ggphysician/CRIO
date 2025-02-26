import sqlite3
import json
import csv
import datetime
import re
import tkinter as tk
import time
from tkinter import filedialog

# Function to select CSV file using Tkinter
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    return file_path

# File name for export
output_file = 'compare_ETL.csv'

conn = sqlite3.connect('compare.sqlite')
cur = conn.cursor()

# Load CSV data-----------------------replace with "select_file()" to select a file not automate file
print("Select the parsed file")
fname_parsed = select_file()
if not fname_parsed:
    print("No file selected. Exiting.")
    exit()

fh_parsed = open(fname_parsed, encoding='utf-8-sig')

# Load CSV data original-----------------------replace with "select_file()" to select a file not automate file
print("Select original file for comparison")
fname_original = select_file() #original data prior to clean
if not fname_original:
    print("No file selected. Exiting.")
    exit()

fh_original = open(fname_original, encoding='utf-8-sig')


# Build SQLite tables
cur.executescript('''
DROP TABLE IF EXISTS Parsed;
DROP TABLE IF EXISTS Original;

CREATE TABLE Parsed (
    patient_key INTEGER NOT NULL PRIMARY KEY UNIQUE,
    diagnosis_parsed TEXT
);
                  
CREATE TABLE Original (
    multi_record TEXT NOT NULL PRIMARY KEY UNIQUE,
    diagnosis_original TEXT NOT NULL,
    patient_key_id INTEGER
);
                  
''')

medical_data = {}

#Trying to batch commits
batch_size = 500
count = 0

for line in fh_original:
    pieces = line.strip().split(',')
    
    #removing first row if first cell is blank
    if not pieces[0].strip():
        continue
    patient_key_id = pieces[4]
    #Taking into account erroneous commas in objects
    if len(pieces) > 9:  # Check if index 9 exists
        value = pieces[7] + pieces[8] # Concatenate lists
    else:
        value = pieces[7].strip()

    if len(pieces) > 9:  # Check if index 9 exists
        multi_record = pieces[9] # Concatenate lists
    else:
        multi_record = pieces[8]  # Just use pieces[8]

    category = pieces[5].strip()

    if category in ["Reason", "Finding"] and value and value not in ["[Not Done]", ""]:
        diagnosis = value

    else:
        continue

    # Insert into Table Original
    cur.execute('''INSERT OR IGNORE INTO Original (multi_record, diagnosis_original, patient_key_id)
        VALUES (?, ?, ?)''', (multi_record, diagnosis, patient_key_id))
      
    count += 1
    if count % batch_size == 0:  #is count a multiple of batch size
        print(f"Committing {count} records...")
        conn.commit()
        time.sleep(.01) #give time for commit
        print(f"Committed {count} records sucessfully")

count = 0

#skips first row of data
next(fh_parsed)

for line in fh_parsed:
    pieces = line.strip().split(',')
    patient_key = pieces[0]
    diagnosis = pieces[1]

    # print(f"patient_key {patient_key} and diagnosis {diagnosis}")
    # Insert into Table Parsed
    cur.execute('''INSERT OR IGNORE INTO Parsed (patient_key, diagnosis_parsed)
        VALUES (?, ?)''', (patient_key, diagnosis))


try:
    cur.execute('''
SELECT Original.patient_key_id, Original.diagnosis_original, Parsed.diagnosis_parsed, Parsed.patient_key 
FROM Parsed
INNER JOIN
	Original ON Parsed.patient_key = Original.patient_key_id;
    ''')

    results = cur.fetchall()

    # Define CSV headers
    headers = ["patient_key", "diagnosis_original", "diagnosis_parsed", "patient_key_id"]

    # Export to CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers) # Writes column headers
        writer.writerows(results) # Write data rows
    
    print(f"Exported Successfully to {output_file} 💾")


except sqlite3.Error as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"A general error occurred: {e}")

conn.commit()
conn.close()