import pandas as pd
import os
import unicodedata


def clean_text(text):
    """
    Clean text by removing or replacing problematic characters.
    Returns ASCII-compatible text.
    """
    if pd.isna(text):  # Handle NaN/None values
        return text
    
    # Convert to string if not already
    text = str(text)
    
    # Normalize Unicode characters
    normalized = unicodedata.normalize('NFKD', text)
    
    # Replace or remove problematic characters
    # Keep only ASCII characters, replace others with closest equivalent
    cleaned = ''.join(char if ord(char) < 128 else ' ' for char in normalized)
    
    # Remove multiple spaces
    cleaned = ' '.join(cleaned.split())
    
    return cleaned

def convert_excel_sheets_to_csv():
    # Define the file path
    excel_file = r"C:\Users\kates\Dropbox\Academics\Research Projects\State Standards\ss_standards\testing_data.xlsx"
    
    # Get the directory path for saving CSV files
    base_dir = os.path.dirname(excel_file)

    # Get the directory path for saving CSV files
    output_dir = os.path.dirname(excel_file)

    # Create output folder name (change this as needed)
    output_folder = "for_testing"
    output_dir = os.path.join(base_dir, output_folder)

  
    try:
        # Read all sheets from the Excel file
        excel = pd.ExcelFile(excel_file)
        
        # Get list of sheet names
        sheet_names = excel.sheet_names
        
        # Process each sheet
        for sheet in sheet_names:
            # Read the sheet into a DataFrame with header=None to avoid treating first row as header
            df = pd.read_excel(excel_file, sheet_name=sheet, header=None)
            
            # Delete the first 5 rows
            df = df.drop([1,2,3]).reset_index(drop=True)
            
            
            # Clean all string columns
            for column in df.columns:
                if df[column].dtype == 'object':  # Only clean string/object columns
                    df[column] = df[column].apply(clean_text)
            
            # Create output filename
            # CHANGE SUFFIX AS NEEDED
            csv_filename = f"{sheet}_MS.csv"
            csv_path = os.path.join(output_dir, csv_filename)
            
            # Save to CSV with UTF-8-sig encoding
            df.to_csv(csv_path, index=False, header=False, encoding='utf-8-sig')
            print(f"Created: {csv_filename}")
            
        print(f"\nSuccessfully processed {len(sheet_names)} sheets.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    convert_excel_sheets_to_csv()