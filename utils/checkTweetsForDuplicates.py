import pandas as pd

def DuplicateFinder(csv_file_path):
    # Reading file
    df = pd.read_csv(csv_file_path)

    # Check for duplicates
    id_counts = df['id'].value_counts()
    duplicates = id_counts[id_counts > 1]

    # Duplicate handling
    if not duplicates.empty:
        print(f"Found {len(duplicates)} duplicates:")
        for _, row in duplicates.iterrows():
            print(f"ID: {row['id']}")
        return True

    else:
        print("No duplicates found.")
        return False

