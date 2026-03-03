import pandas as pd
import os
from pathlib import Path

def process_csv_files(data_folder, params_file):
    """
    Process CSV files according to parameters file specifications.
    
    Args:
        data_folder: Path to the folder containing CSV files (ms_2026)
        params_file: Path to the parameters CSV file
    """
    # Read parameters file
    print(f"Reading parameters file: {params_file}")
    params_df = pd.read_csv(params_file, encoding = 'utf-8')
    
    # Fill NaN values in skip and concat columns with 0
    params_df['skip'] = params_df['skip'].fillna(0).astype(int)
    params_df['concat'] = params_df['concat'].fillna(0).astype(int)
    
    print(f"\nProcessing files in: {data_folder}")
    print(f"Found {len(params_df)} entries in parameters file\n")
    
    data_path = Path(data_folder)
    processed_count = 0
    skipped_count = 0
    column_counts = []
    
    # Iterate through each row in the parameters file
    for idx, row in params_df.iterrows():
        state_name = row['state']
        skip_flag = row['skip']
        concat_flag = row['concat']
        
        # Construct the _00.csv filename
        csv_filename = f"{state_name}_00.csv"
        csv_file = data_path / csv_filename
        
        print(f"Processing: {csv_filename}")
        
        # Check if skip flag is set
        if skip_flag == 1:
            print(f"  ⊗ Skip flag = 1, skipping this file")
            skipped_count += 1
            print()
            continue
        
        # Check if file exists
        if not csv_file.exists():
            print(f"  Warning: File not found, skipping...")
            continue
        
        # Read the CSV file
        try:
            df = pd.read_csv(csv_file, header=None, encoding = 'utf-8')
        except Exception as e:
            print(f"  Error reading file: {e}")
            continue
        
        # STEP 1: Replace empty, NA, or N/A in column index 1 with "no_content"
        if len(df.columns) > 1:
            # Get column at index 1
            col_name = df.columns[1]
            
            # Replace empty strings, NA, N/A with "no_content"
            df[col_name] = df[col_name].fillna("no_content")
            df[col_name] = df[col_name].replace(['', 'NA', 'N/A', 'na', 'n/a'], "no_content")
            
            # Save the modified file back to _00.csv
            df.to_csv(csv_file, index=False)
            print(f"  ✓ Replaced empty/NA values in column index 1")
        
        # STEP 2: Check if concat is needed
        if concat_flag == 1:
            print(f"  Concat flag = 1, processing concatenation...")
            
            # Check if there are more than 5 columns
            if len(df.columns) > 5:
                # Get column at index 4
                col_index_4 = df.columns[4]
                
                # Get all columns from index 5 onwards
                cols_to_concat = df.columns[5:]
                
                # Concatenate columns index 4 and beyond
                def concat_row(row):
                    values = [str(row[col_index_4])]
                    for col in cols_to_concat:
                        values.append(str(row[col]))
                    # Filter out 'nan' strings from the concatenation
                    values = [v for v in values if v != 'nan']
                    return ' +++ '.join(values)
                
                df[col_index_4] = df.apply(concat_row, axis=1)
                
                # Drop columns from index 5 onwards
                df = df.drop(columns=cols_to_concat)
                
                print(f"  ✓ Concatenated {len(cols_to_concat) + 1} columns into column index 4")
            else:
                print(f"  File has {len(df.columns)} columns (≤5), no concatenation needed")
            
            # Save as _done.csv
            done_file = csv_file.parent / csv_file.name.replace('_00.csv', '_done.csv')
            df.to_csv(done_file, index=False, encoding= 'utf-8')
            print(f"  ✓ Saved as: {done_file.name}")
            
        else:
            # concat_flag = 0, just rename _00.csv to _done.csv
            print(f"  Concat flag = 0, renaming file...")
            done_file = csv_file.parent / csv_file.name.replace('_00.csv', '_done.csv')
            df.to_csv(done_file, index=False)
            print(f"  ✓ Saved as: {done_file.name}")
        
        # Track column count for the _done.csv file
        num_columns = len(df.columns)
        column_counts.append({
            'file': done_file.name,
            'columns': num_columns
        })

        processed_count += 1
        print()
    
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"Successfully processed {processed_count} files")
    print(f"Skipped {skipped_count} files (skip flag = 1)")
    print(f"{'='*60}")

     # Display column count summary
    if column_counts:
        print(f"\n{'='*60}")
        print(f"COLUMN COUNT SUMMARY (_done.csv files)")
        print(f"{'='*60}")
        for info in column_counts:
            print(f"{info['file']}: {info['columns']} columns")
        print(f"{'='*60}")

if __name__ == "__main__":
    # Set up paths
    # Assuming the script is run from the parent directory of ms_2026
    data_folder = "ms_2026"
    params_file = "ms_params.csv"  # In the parent folder
    
    # Check if paths exist
    if not os.path.exists(data_folder):
        print(f"Error: Data folder '{data_folder}' not found!")
        print(f"Current directory: {os.getcwd()}")
        exit(1)
    
    if not os.path.exists(params_file):
        print(f"Error: Parameters file '{params_file}' not found!")
        print(f"Current directory: {os.getcwd()}")
        exit(1)
    
    # Process the files
    process_csv_files(data_folder, params_file)