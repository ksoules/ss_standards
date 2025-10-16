import csv
from pathlib import Path

def process_csv(input_filename: str, transpose: bool) -> None:
    """
    Process a CSV file according to specified rules and create an edited output file.
    
    Args:
        input_filename: Name of the input CSV file
        transpose: Boolean flag indicating whether to transpose extra columns
    """
    print(f"\nProcessing file: {input_filename}")
    print(f"Transpose mode: {transpose}")
    
    # Generate output filename in same directory as input file
    input_path = Path(input_filename)
    output_filename = input_path.parent / f"{input_path.stem}_edited{input_path.suffix}"
    print(f"Output will be written to: {output_filename}")
    
    # Store processed rows
    output_rows = []
    found_keyword = False
    prev_first_col = ""
    row_count = 0
    
    print("\nReading input file...")
    # Read input file
    with open(input_filename, 'r', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile)
        
        # Skip the header row entirely
        try:
            next(reader)
            print("Skipped header row")
        except StopIteration:
            print("Error: File is empty")
            return
        
        # Process remaining rows
        for row in reader:
            row_count += 1
            #print(f"\nProcessing row {row_count}: {row}")
            
            # Check for keyword row
            if not found_keyword:
                if row and row[0] == "Keyword":
                    found_keyword = True
                    output_rows.append(row)
                    print("Found 'Keyword' row - will begin processing subsequent rows")
                else:
                    pass
                    #print("Skipping row (before 'Keyword' row)")
                continue
            
            # Handle blank rows
            if not any(row):
               # print("Found blank row - preserving as-is")
                output_rows.append(row)
                continue
            
            # Fill blank first column
            if not row[0]:
                row[0] = prev_first_col
               # print(f"Filled blank first column with: {prev_first_col}")
            prev_first_col = row[0]
            
            # If transpose is False, just add the row and continue
            if not transpose:
                output_rows.append(row)
                #print("Transpose=False, adding row as-is")
                continue
            
            # Handle transposition for rows with more than 4 columns
            if len(row) > 4:
                #print(f"Row has {len(row)} columns - will create additional rows for columns beyond 4")
                # Add the base row with first 4 columns
                base_row = row[:4]
                output_rows.append(base_row)
                #print(f"Added base row: {base_row}")
                
                # Create new rows for extra columns
                for i, extra_col in enumerate(row[4:], start=1):
                    if extra_col.strip():  # Only create new row if extra column has content
                        new_row = row[:3] + [extra_col]
                        output_rows.append(new_row)
                        #print(f"Created new row for column {i+4}: {new_row}")
            else:
                output_rows.append(row)
                #print("Row has 4 or fewer columns - adding as-is")
    
    print(f"\nProcessed {row_count} rows total") 
    print(f"Writing {len(output_rows)} rows to output file")
    
    # Write output file
    with open(output_filename, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(output_rows)
    
    print(f"Processing complete. Output written to {output_filename}")

def main():
    """
    Main function with hardcoded parameters for testing.
    """
    # Hardcoded parameters for testing
    input_filename = input ('type a state name  : ')
    dir_path = r"C:\Users\kates\Dropbox\Academics\Research Projects\State Standards\ss_standards\for_testing"
    input_filename = f"{dir_path}\\{input_filename}_MS.csv"
    
    #input_filename = r"C:\Users\kates\Dropbox\Academics\Research Projects\State Standards\New York_MS.csv"  # Replace with your input filename
    transpose = input('Transpose? y/n')              # Set to False to test without transposition
    transpose = True if transpose == 'y' else False

    try:
        process_csv(input_filename, transpose)
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()