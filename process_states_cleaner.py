import csv
import os
from pathlib import Path
from typing import Dict, List, Tuple
import shutil


def read_params_file(params_path: str) -> Dict[str, Dict[str, bool]]:
    """
    Read the parameters file and return a dictionary of file parameters.
    """
    params = {}
    print(f"\nReading parameters from {params_path}")
    
    try:
        with open(params_path, 'r', encoding = 'utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                state = row['state']
                params[state] = {
                    'skip': row['skip'] == '1',
                    'rearrange': row['rearrange'].lower() == '1',
                    'split': row['split'].lower() == '1',
                    'review': row['review'].lower() == '1'
                }
        
        print(f"Loaded parameters for {len(params)} files")
        return params
    except PermissionError:
        print(f"Error: No permission to read {params_path}")
        raise
    except FileNotFoundError:
        print(f"Error: Parameters file not found at {params_path}")
        raise

def check_flag_status(filepath: Path) -> bool:
    """
    Check if a file already has the _FLAG suffix.
    """
    return filepath.stem.endswith('_FLAG')

def safe_write_file(input_path: Path, output_path: Path, write_function) -> Path:
    """
    Safely write to a new file using a temporary file.
    """
    # Create a temporary file path
    temp_path = output_path.parent / f"temp_{output_path.name}"
    
    try:
        # Write to temporary file first
        write_function(input_path, temp_path)
        
        # If the output file already exists, try to remove it
        if output_path.exists():
            try:
                output_path.unlink()
            except PermissionError:
                print(f"Error: Cannot overwrite existing file {output_path.name} - permission denied")
                if temp_path.exists():
                    temp_path.unlink()
                raise
        
        # Rename temporary file to final output file
        temp_path.rename(output_path)
        return output_path
    
    except Exception as e:
        # Clean up temporary file if something goes wrong
        if temp_path.exists():
            temp_path.unlink()
        raise e

def fill_empty_cells(rows: List[List[str]]) -> List[List[str]]:
    """
    Fill empty cells in the first column with values from previous rows.
    Preserves completely blank rows.
    """
    output_rows = []
    found_keyword = False
    prev_first_col = ""
    
    for row in rows:
        if not found_keyword:
            if row and row[0] == "Keyword":
                found_keyword = True
            output_rows.append(row)
            continue
        
        # If row is completely empty, preserve it
        if not any(row):
            output_rows.append(row)
            prev_first_col = ""
            continue
        
        # Fill empty first column with previous value
        if not row[0]:
            row[0] = prev_first_col
        prev_first_col = row[0]
        output_rows.append(row)
    
    return output_rows

def transpose_columns(rows: List[List[str]]) -> List[List[str]]:
    """
    Transpose data from columns after the 4th column into new rows,
    copying the first three columns' content.
    """
    output_rows = []
    
    for row in rows:
        if len(row) <= 4:
            output_rows.append(row)
            continue
        
        # Write the base row with first 4 columns
        output_rows.append(row[:4])
        
        # Create new rows for additional columns
        for extra_col in row[4:]:
            if extra_col.strip():
                new_row = row[:3] + [extra_col]
                output_rows.append(new_row)
    
    return output_rows

def process_split_indicators(rows: List[List[str]], was_rearranged: bool) -> List[List[str]]:
    """
    Split the fourth column based on specific rules.
    """
    output_rows = []
    start_processing = was_rearranged  # Start immediately if file was rearranged
    
    for row in rows:
        # Look for "Keyword" row if file wasn't rearranged
        if not start_processing:
            if row and row[0] == "Keyword":
                start_processing = True
            continue
        
        if len(row) < 4:
            continue
        
        text = row[3].strip()
        code = ""
        description = text
        
        # Handle special prefixes
        if text.startswith(('Theme ', 'Era ', 'SS ')):
            parts = text.split(' ', 2)
            if len(parts) >= 3:
                code = f"{parts[0]} {parts[1]}"
                description = parts[2]
        elif text.startswith(('The ', 'Students ')):
            code = ""
            description = text
        else:
            parts = text.split(' ', 1)
            if len(parts) == 2:
                code = parts[0]
                description = parts[1]
            else:
                code = text
                description = ""
        
        new_row = row[:3] + [code, description]
        output_rows.append(new_row)
    
    return output_rows

def process_file(input_path: Path, file_params: Dict[str, bool]) -> None:
    """
    Process a single file with all required operations and save to a single output file.
    """
    # Read input file
    with open(input_path, 'r', encoding='utf-8', newline='') as infile:
        rows = list(csv.reader(infile))
    
    # Apply operations
    if not file_params['skip']:
        # Fill empty cells for all non-skipped files
        rows = fill_empty_cells(rows)
        print(f"Completed filling cells in {input_path.name}")
        
        # Apply transpose operation if rearrange is true
        if file_params['rearrange']:
            rows = transpose_columns(rows)
            print(f"Completed transposing columns in {input_path.name}")
        
        # Apply split operation
        if file_params['split']:
            rows = process_split_indicators(rows, file_params['rearrange'])
            print(f"Completed splitting indicators in {input_path.name}")
        
        # Write final output file
        output_path = input_path.parent / f"{input_path.stem}_edited{input_path.suffix}"
        try:
            # Create a temporary file path
            temp_path = output_path.parent / f"temp_{output_path.name}"
            
            try:
                # Write to temporary file first
                with open(temp_path, 'w', encoding='utf-8', newline='') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerows(rows)
                
                # If the output file already exists, try to remove it
                if output_path.exists():
                    try:
                        output_path.unlink()
                    except PermissionError:
                        print(f"Error: Cannot overwrite existing file {output_path.name} - permission denied")
                        if temp_path.exists():
                            temp_path.unlink()
                        raise
                
                # Rename temporary file to final output file
                temp_path.rename(output_path)
                print(f"Saved processed file as {output_path.name}")
                
            except Exception as e:
                # Clean up temporary file if something goes wrong
                if temp_path.exists():
                    temp_path.unlink()
                raise e
                
        except Exception as e:
            print(f"Error saving processed file: {str(e)}")
            raise
    else:
        # Handle skipped files
        if not check_flag_status(input_path):
            try:
                flagged_path = input_path.parent / f"{input_path.stem}_FLAG{input_path.suffix}"
                shutil.copy2(input_path, flagged_path)
                print(f"Added FLAG suffix to {input_path.name}")
            except PermissionError:
                print(f"Error: Cannot create flagged file {flagged_path.name}")
                raise

def process_files(folder_path: str, params_file: str) -> None:
    """
    Main function to process all files according to their parameters.
    """
    try:
        folder_path = Path(folder_path)
        if not folder_path.exists():
            print(f"Error: Folder not found at {folder_path}")
            return
        
        params = read_params_file(params_file)
        
        stats = {
            'skip': [],
            'fill': [],
            'rearrange': [],
            'split': [],
            'review': []
        }
        
        print("\nBeginning file processing...")
        
        for state, file_params in params.items():
            input_file = folder_path / f"{state}"
            
            if not input_file.exists():
                print(f"\nWarning: File not found: {input_file.name}")
                continue
            
            print(f"\nProcessing {input_file.name}")
            
            try:
                # Process the file
                process_file(input_file, file_params)
                
                # Update statistics
                if file_params['skip']:
                    stats['skip'].append(state)
                else:
                    stats['fill'].append(state)
                    if file_params['rearrange']:
                        stats['rearrange'].append(state)
                    if file_params['split']:
                        stats['split'].append(state)
                    if file_params['review']:
                        stats['review'].append(state)
                        print(f"Marking {state} for review")
                
            except Exception as e:
                print(f"Error processing {input_file.name}: {str(e)}")
                continue
        
        print("\n=== Processing Summary ===")
        for param, files in stats.items():
            print(f"\n{param.capitalize()} parameter:")
            print(f"Number of files: {len(files)}")
            if files:
                print("Files:")
                for file in files:
                    print(f"- {file}")
    
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise

def main():
    
    #Main entry point of the script.
    
    try:
        folder_path = r'C:\Users\kates\Dropbox\Academics\Research Projects\State Standards\ss_standards\for_testing'
        params_file = r'C:\Users\kates\Dropbox\Academics\Research Projects\State Standards\ss_standards\MS_testing_params.csv'
        
        process_files(folder_path, params_file)
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease check that:")
        print("1. You have permission to read and write in the specified folder")
        print("2. The paths you entered are correct")
        print("3. The MS_params.csv file is not open in another program")
        print("4. You have sufficient disk space")

if __name__ == "__main__":
    main()