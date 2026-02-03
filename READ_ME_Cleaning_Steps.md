# Initial Cleaning 
## Step 1: Download file from Google Sheets

### 1.A Compare to parameters file
- do the file names match the names of the tabs on the sheet?
- are the cleaning parameters correctly indicated?

# Step 2: Convert Excel file to individual CSV files for each state

`excel_to_csv.py`
- converts excel file to separate CSV files for each state
- drops rows 2-4, keeping State name row and column headings

Outcome: individual files for each state with appropriate suffix (_ms or _hs)


## Step 2: Reshape the data and Initial Data Clean up
- update file names and folder names as necessary
- run the `process_states_cleaner.py` script
	-uses params csv to know which operations to perform on each spreadsheet

### How `process_states_cleaner.py` works:

2a. Fill blanks in first column (Keyword)
	actions:
		if there is data in the rows except for the first column, fill in the first cell with the keyword in the cell immediately above it.
		if the entire row is blank, skip it.

2b. Transpose rows so that each standard is one row
	if indicated in transpose column of the parameters spreadsheet:
	actions:
		move each cell after the 4th column to a new row, copying the contents of the first four columns

2c. Separate indicator numbers from text
	actions:
		- moves indicator number to its own column

2d. Counts the number of columns in the resulting file and produces the 'ms_column_counts.csv' file	



*current issues*
- not all indicator numbers get recognized
	- esp. if they start with a a phrase
	


# Secondary Cleaning:

## To prepare for secondary cleaning
- Review cleaned files to identify additional steps needed
	- concatenate additional columns
	- convert grade columns
	- what else?
	

## Other Things to Do

- create unique indicators for each standard
- standard list of courses?


Last steps at the end of cleaning (for now)
- add the state column at the beginning of every row
- remove empty rows
-