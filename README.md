# CRIO
Files for cleaning CRIO Data

Overview:
This Python script automates the cleaning, standardization, and matching of medical diagnoses using fuzzy string matching and an abbreviation dictionary. It processes raw patient diagnosis data, replaces abbreviations, and applies fuzzy matching (Levenshtein distance) to improve consistency before storing the results in an SQLite database.

Steps to use:
1.  Please run Crio_codes.py to start.  This will build a database of reference CRIO definitions.  The software will ask you to name the database - please name your database "clean.sqlite"
2.  Please run Clean.py.  You will be asked to select the file that requires cleaning.  Please then name the newly cleaned file when prompted.
3.  Please run compare.py.  You will be asked to selec the cleaned file and the original file.  This code will build a new database to allow efficient comparison of original data and newly "clean" data.  It will be saved as a "compare_ETL.csv"

Why This Matters In clinical research and medical data management, inconsistencies in diagnosis data can affect analysis and decision-making. This tool streamlines data preparation, ensuring better accuracy for downstream processes like querying, reporting, and machine learning applications.

Requirements to run:
python
SQLite

Libraries to run:
sqlite3
csv
datetime
re
tkinter
time
rapidfuzz

About the Author 👋 GG (GitHub: ggphysician) is an Emergency Medicine physician, clinical researcher, and data professional with expertise in clinical trials, data automation, and medical informatics.

Founder of GP Data Services, a company focused on data governance & automation in clinical research. Experience in Python, SQL, data parsing, and automation for research and business applications. Passionate about solving inefficiencies in clinical workflows using technology and AI-driven solutions.

Future Plans This project is part of a growing portfolio of automation tools. Next steps are to combine into a single python file.  I am also planning on learning pandas library for more efficient handling of larger files.

Future enhancements: ✅ Support for additional medical data formats ✅ Integration with OCR tools for scanned medical records ✅ Implementation of ML-driven diagnosis categorization
