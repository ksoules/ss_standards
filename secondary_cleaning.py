import pandas as pd
import os
from pathlib import Path

# State abbreviation mapping
STATE_ABBREV = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'Washington DC': 'DC',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

def extract_state_name(filename):
    """Extract state name from filename (e.g., 'Alabama_MS_edited.csv' -> 'Alabama')"""
    return filename.replace('_MS_edited.csv', '').replace('_', ' ')

def should_concatenate(filename, params_df):
    """Check if file should have columns concatenated based on params file"""
    match = params_df[params_df['state'] == filename]
    if not match.empty:
        concat_val = match.iloc[0]['Concat']
        # Treat 1 as True, everything else (0, NaN, empty) as False
        return concat_val == 1
    return False

def is_row_empty(row):
    """Check if row is completely empty (all NaN or empty strings)"""
    return row.isna().all() or (row.astype(str).str.strip() == '').all()

def process_csv(input_path, output_path, state_abbrev, concatenate):
    """Process a single CSV file"""
    # Read CSV
    df = pd.read_csv(input_path, dtype=str, keep_default_na=False)
    
    # Replace empty strings with NaN for easier processing
    df = df.replace('', pd.NA)
    
    # Step 1: Drop completely empty rows
    df = df[~df.apply(is_row_empty, axis=1)]
    
    # Step 2: If only column 0 has data, write "NA" in column 1
    if len(df.columns) >= 2:
        mask = df.iloc[:, 0].notna() & df.iloc[:, 1:].isna().all(axis=1)
        df.loc[mask, df.columns[1]] = "NA"
    
    # Step 3: Concatenate columns 5+ if needed (before adding state column)
    if concatenate and len(df.columns) > 5:
        # Concatenate columns from index 5 onwards
        cols_to_concat = df.columns[5:]
        
        # Create concatenated column (replace NaN with empty string for concat)
        df[df.columns[4]] = df[cols_to_concat].fillna('').apply(
            lambda row: '::'.join([str(val) for val in row if val != '']), 
            axis=1
        )
        
        # If concatenation resulted in empty string, replace with original col 5 value
        df.loc[df[df.columns[4]] == '', df.columns[4]] = pd.NA
        
        # Drop the extra columns
        df = df.drop(columns=cols_to_concat)
    
    # Step 4: Add state abbreviation column at the beginning
    df.insert(0, 'State', state_abbrev)
    
    # Replace NaN back with empty strings for output
    df = df.fillna('')
    
    # Save processed file
    df.to_csv(output_path, index=False)
    print(f"Processed: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")

def main():
    # Setup paths
    input_folder = 'ms_raw'
    params_file = 'ms_params_2.csv'
    
    # Read parameters file
    params_df = pd.read_csv(params_file, dtype={'state': str, 'Concat': float})
    params_df['Concat'] = params_df['Concat'].fillna(0)
    
    # Get all _edited.csv files
    input_path = Path(input_folder)
    edited_files = list(input_path.glob('*_edited.csv'))
    
    print(f"Found {len(edited_files)} files to process\n")
    
    # Process each file
    for file_path in edited_files:
        filename = file_path.name
        
        # Extract state name and get abbreviation
        state_name = extract_state_name(filename)
        state_abbrev = STATE_ABBREV.get(state_name, 'XX')  # 'XX' as fallback
        
        # Check if concatenation is needed
        concatenate = should_concatenate(filename, params_df)
        
        # Create output filename
        output_filename = filename.replace('_edited.csv', '_2.csv')
        output_path = input_path / output_filename
        
        # Process the file
        process_csv(file_path, output_path, state_abbrev, concatenate)
    
    print(f"\nProcessing complete! All files saved in {input_folder}/")

if __name__ == "__main__":
    main()