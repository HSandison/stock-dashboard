import pandas as pd
import chardet

def check_encoding(file_path):
    """
    Check the file encoding by using chardet.
    Returns the most likely encoding detected.
    """
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def inspect_csv(file_path):
    """
    Interrogate the CSV file to find out issues with encoding, column names, etc.
    """
    # Check the file encoding
    encoding = check_encoding(file_path)
    print(f"Detected file encoding: {encoding}")

    # Try reading the CSV with the detected encoding
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        print("\nCSV file loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading CSV file: {e}")
        return

    # Show raw column names (before any processing)
    print("\nRaw column names from the uploaded file:")
    print(df.columns)

    # Show first few rows of the data
    print("\nFirst few rows of the dataset:")
    print(df.head())

    # Clean up column names: strip spaces, convert to lowercase
    df.columns = [col.strip().lower().replace("\xa0", "").replace("\n", "").replace("\r", "").replace(" ", "_") for col in df.columns]

    # Show cleaned column names
    print("\nCleaned column names (lowercase, cleaned):")
    print(df.columns)

    # Check if required columns 'category' and 'item' are present
    if 'category' in df.columns and 'item' in df.columns:
        print("\nThe required columns 'category' and 'item' are present.")
    else:
        print("\n❌ Missing one or both of the required columns: 'category' and 'item'")

    # Check for hidden or unexpected characters in the first few rows
    print("\nInspecting first few rows for any hidden characters:")
    for column in df.columns:
        print(f"\nColumn: '{column}'")
        print(df[column].head(10))  # Print first 10 entries in each column

if __name__ == "__main__":
    # Path to your CSV file
    file_path = 'items-2025-03-25-2025-04-02 (2).csv'  # Change this to the path of your CSV file

    # Run the inspection
    inspect_csv(file_path)
