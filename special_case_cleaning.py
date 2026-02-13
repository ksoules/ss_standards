import pandas as pd
import os

# Define the subfolder containing the CSV files
data_folder = "ms_2026"

def process_ky_ms(input_file, output_file):
    """
    Process KY_MS_edited.csv: Concatenate columns C and D (index 2 and 3) with a '+' separator
    """
    print(f"Processing {input_file}...")
    
    # Read the CSV file
    df = pd.read_csv(input_file, header=None, encoding='utf-8')
    
    # Concatenate columns at index 2 and 3 with '+'
    df[2] = df[2].astype(str) + ' + ' + df[3].astype(str)
    
    # Drop the old column D (index 3)
    df = df.drop(columns=[3])
    
    # Save to output file
    df.to_csv(output_file, index=False, header=False, encoding='utf-8')
    print(f"Saved to {output_file}")
    print(f"Shape: {df.shape}\n")

def process_mn_ms(input_file, output_file):
    """
    Process MN_MS_edited.csv: Concatenate columns C and D + E (index 2 and 3 and 4) with a '+' separator
    """
    print(f"Processing {input_file}...")
    
    # Read the CSV file
    df = pd.read_csv(input_file, header=None, encoding='utf-8')
    
    # Concatenate columns at index 2 and 3 with '+'
    df[2] = df[2].astype(str) + ' + ' + df[3].astype(str) + ' + ' + df[4].astype(str)
    
    # Drop the old column D (index 3)
    df = df.drop(columns=[3, 4])
    
    # Save to output file
    df.to_csv(output_file, index=False, header=False, encoding='utf-8')
    print(f"Saved to {output_file}")
    print(f"Shape: {df.shape}\n")

def process_oh_ms(input_file, output_file):
    """
    Process OH_MS_edited.csv: Insert a blank column between C and D (new blank column at index 3)
    """
    print(f"Processing {input_file}...")
    
    # Read the CSV file
    df = pd.read_csv(input_file, header=None, encoding='utf-8')
    
    # Insert a blank column at index 3
    df.insert(3, 'blank_col', '')
    
    # Save to output file
    df.to_csv(output_file, index=False, header=False, encoding='utf-8')
    print(f"Saved to {output_file}")
    print(f"Shape: {df.shape}\n")


def process_al(input_file, output_file):
    """
    Process AL_edited.csv: Starting from row 4 (index 3), split column 2 at '/'
    Left part stays in column 2, right part goes to new column 3
    """
    print(f"Processing {input_file}...")
    
    # Read the CSV file as raw rows
    import csv
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Process each row starting from index 3 (4th row)
    new_rows = []
    for row in rows:
        
        # Split grade and course title

        if len(row) > 2 and '/' in row[1]:
            parts = row[1].split('/', 1)
            # Insert new column at index 2
            new_row = row[:2] + [''] + row[2:]
            new_row[1] = parts[0]  # Left part stays in column 2
            new_row[2] = parts[1]  # Right part goes to column 3
        else:
            # No slash, just insert blank column at index 3
            new_row = row[:2] + [''] + row[2:]
    
        
        # Secend Step: Split indicator and standard text

        if len(new_row) > 3 and '.' in new_row[3]:
            parts = new_row[3].split('.', 1)
            new_row = new_row[:4] + [''] + new_row[4:]
            new_row[3] = parts[0]
            new_row[4] = parts[1]

        else:
            new_row = new_row[:4] + [''] + new_row[5:]

        new_rows.append(new_row)
    
        # Write to output file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)
    
    print(f"Saved to {output_file}")
    print(f"Rows processed: {len(new_rows)}\n")
 

def process_hi(input_file, output_file):
    
    """ process Hawaii file to split grade and course name at the ':' 
    """
    
    print(f"Processing {input_file}...")
    
    # Read the CSV file as raw rows
    import csv
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Process each row starting from index 3 (4th row)
    new_rows = []
    for row in rows:
        
        # Split grade and course title
        if len(row) > 2 and ':' in row[1]:
            parts = row[1].split(':', 1)
            # Insert new column at index 2
            new_row = row[:2] + [''] + row[2:]
            new_row[1] = parts[0]  # Left part stays in column 2
            new_row[2] = parts[1]  # Right part goes to column 3
        else:
            # No slash, just insert blank column at index 3
            new_row = row[:2] + [''] + row[2:]
    
        new_rows.append(new_row)
    
        # Write to output file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)
    
    print(f"Saved to {output_file}")
    print(f"Rows processed: {len(new_rows)}\n")

def process_mo(input_file, output_file):
    
    """ process MO file to split indicator and standard at the '|' 
    """
    
    print(f"Processing {input_file}...")
    
    # Read the CSV file as raw rows
    import csv
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Process each row starting from index 3 (4th row)
    new_rows = []
    for row in rows:
        
        # Split grade and course title
        if len(row) > 3 and '|' in row[3]:
            parts = row[3].split('|', 1)
            # Insert new column at index 2
            new_row = row[:3] + [''] + row[3:]
            new_row[3] = parts[0]  # Left part stays in column 4
            new_row[4] = parts[1]  # Right part goes to column 5
        else:
            # No slash, just insert blank column at index 3
            new_row = row[:3] + [''] + row[3:]
    
        new_rows.append(new_row)
    
        # Write to output file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)
    
    print(f"Saved to {output_file}")
    print(f"Rows processed: {len(new_rows)}\n")

def process_ma_ms(input_file, output_file):
    """
    Process MA_MS_edited.csv: Extract ID in square brackets from end of column 3
    and place it in a new column at index 4
    """
    print(f"Processing {input_file}...")
    
    # Read the CSV file as raw rows
    import csv
    import re
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Process each row
    new_rows = []
    for row in rows:
        if len(row) > 2:
            col3_content = row[2]
            
            # Look for content in square brackets at the end
            match = re.search(r'\s*\[([^\]]+)\]\s*$', col3_content)
            
            if match:
                # Extract the ID (content inside brackets)
                id_text = match.group(1)
                # Remove the bracketed text from column 3
                cleaned_text = col3_content[:match.start()].strip()
                
                # Build new row: columns 0-3, then new column with ID, then rest
                new_row = row[:2] + [cleaned_text] + [id_text] + row[3:]
            else:
                # No brackets found, insert blank column at index 4
                new_row = row[:3] + [''] + row[3:]
        else:
            # Row doesn't have column 3, just add blank at index 4
            new_row = row[:3] + [''] + row[3:]
        
        new_rows.append(new_row)
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)
    
    print(f"Saved to {output_file}")
    print(f"Rows processed: {len(new_rows)}\n")


def generate_summary(folder):
    """
    Generate a summary CSV file with filename, column count, and row count
    for all CSV files in the folder
    """
    print("=" * 60)
    print("Generating summary file...")
    print("=" * 60 + "\n")
    
    import csv
    import glob
    
    # Get all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder, "*.csv"))
    
    summary_data = []
    
    for filepath in sorted(csv_files):
        filename = os.path.basename(filepath)
        
        # Skip the summary file itself if it already exists
        if filename == "col-row-count.csv":
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                num_rows = len(rows)
                num_cols = len(rows[0]) if rows else 0
                
                summary_data.append([filename, num_cols, num_rows])
                print(f"{filename}: {num_cols} columns, {num_rows} rows")
        
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            summary_data.append([filename, "Error", "Error"])
    
    # Write summary file
    summary_path = os.path.join(folder, "col-row-count.csv")
    with open(summary_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "Number of Columns", "Number of Rows"])
        writer.writerows(summary_data)
    
    print(f"\nSummary saved to {summary_path}")
    print("=" * 60 + "\n")



def main():
    """
    Main function to process special case CSV files
    """
    print("=" * 60)
    print("CSV File Processor - Special Cases")
    print("=" * 60 + "\n")
    
    # Define special case files and their processing functions
    special_cases = [
        ("KY_MS_edited.csv", "KY_MS_00.csv", process_ky_ms),
        ("MN_MS_edited.csv", "MN_MS_00.csv", process_mn_ms),
        ("OH_MS_edited.csv", "OH_MS_00.csv", process_oh_ms),
        ("AL_MS_edited.csv", "AL_MS_00.csv", process_al),
        ("HI_MS_edited.csv", "HI_MS_00.csv", process_hi),
        ("MO_MS_edited.csv", "MO_MS_00.csv", process_mo),
         ("MA_MS_edited.csv", "MA_MS_00.csv", process_ma_ms)
    ]
    
    # Process each special case
    for input_filename, output_filename, process_func in special_cases:
        input_path = os.path.join(data_folder, input_filename)
        output_path = os.path.join(data_folder, output_filename)
        
        # Check if input file exists
        if os.path.exists(input_path):
            try:
                process_func(input_path, output_path)
            except Exception as e:
                print(f"Error processing {input_filename}: {e}\n")
        else:
            print(f"Warning: {input_filename} not found in {data_folder}\n")
    
    print("=" * 60)
    print("Processing complete!")
    print("=" * 60)


    # Generate summary file
    generate_summary(data_folder)

if __name__ == "__main__":
    main()