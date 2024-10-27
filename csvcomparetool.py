import pandas as pd
import os 
import logging
from pathlib import Path

def validate_paths(path1, path2):
    if not os.path.exists(path1):
        logging.error(f"CSV file not found: {path1}")
        return False
    if not os.path.exists(path2):
        logging.error(f"CSV file not found: {path2}")
        return False
    return True

def validate_columns(path1, path2, identifier):
    db_1 = pd.read_csv(path1)
    db_2 = pd.read_csv(path2)

    if identifier not in db_1.columns:
        logging.error(f"Column '{identifier}' not found in {path1}")
        return False
    if identifier not in db_2.columns:
        logging.error(f"Column '{identifier}' not found in {path2}")
        return False
    return True

def find_differences(path1, path2, identifier1, identifier2):

    df_1 = pd.read_csv(path1, dtype=str)
    df_2 = pd.read_csv(path2, dtype=str)

    dict_1 = {}
    dict_2 = {}
    differences = []

    for i, row in df_1.iterrows():
        unique_identifier = row[identifier1] + row[identifier2]
        dict_1[unique_identifier] = str(row.values)
    
    for i, row in df_2.iterrows():
        unique_identifier = row[identifier1] + row[identifier2]
        dict_2[unique_identifier] = str(row.values)

    for key, value in dict_1.items():
        if key not in dict_2:
            diff = f"{key} not in SECOND file"
            differences.append(diff)
            continue

        if value != dict_2[key]:
            diff = f"Files are different for {key} -> \n FIRST: {value} \nSECOND: {dict_2[key]}"
            differences.append(diff)

        dict_2.pop(key)

    if len(dict_2) != 0:
        for key, value in dict_2.items():
            diff = f"{key} not in FIRST file"
            differences.append(diff)

    return differences

def main():
    cwd = str(Path.cwd())
    path1 = cwd + "\\file1.csv"
    path2 = cwd + "\\file2.csv"
    identifier1 = "IDENTIFIER"
    identifier2 = "GROUP"

    if not validate_paths(path1, path2):
        print("CSV file paths are invalid. Please check the file paths and try again.")
        return

    if not validate_columns(path1, path2, identifier1):
        print("Invalid column. Please check column identifier and try again.")
        return

    differences = find_differences(path1, path2, identifier1, identifier2)

    if differences:
        print("Differences found:")
        for difference in differences:
            print(difference)
            print("\n")


if __name__ == "__main__":
    main()
