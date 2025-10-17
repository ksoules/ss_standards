# Step 1: Convert Excel file to individual CSV files for each state

excel_to_csv.py
- converts excel file to separate CSV files for each state
- drops rows 2-4, keeping State name row and column headings

Outcome: individual files for each state with appropriate suffix (_ms or _hs)


# Step 2: Reshape the data and Initial Data Clean up


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
		{- updates parameters spreadsheet to whether or not the state has indicators} not yet


script: process_states_cleaner.py
- uses params csv to know which operations to perform on each spreadsheet
- does each of the steps above

*current issues*
- not all indicator numbers get recognized
	- esp. if they start with a a phrase
	



# Step 3 (maybe): 
- create unique indicators for each standard
- standard list of courses?


Last steps at the end of cleaning (for now)
- add the state column at the beginning of every row
- remove empty rows
-