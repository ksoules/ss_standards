# Step 1: Convert Excel file to individual CSV files for each state

excel_to_csv.py
- converts excel file to separate CSV files for each state
- drops rows 2-4, keeping State name row and column headings

Outcome: individual files for each state with appropriate suffix (_ms or _hs)


# Step 2: Reshape the data


2a. Fill blanks in first column (Keyword)
	actions:
		if there is data in the rows except for the first column, fill in the first cell with the keyword in the cell immediately above it.
		if the entire row is blank, skip it.

2b. Transpose rows so that each standard is one row
	if indicated in transpose column of the parameters spreadsheet:
	actions:
		move each cell after the 4th column to a new row, copying the contents of the first four columns



# Step 3: Clean Up the Data

3a. separate indicator numbers from text
	actions:
		- moves indicator number to its own column
		- updates parameters spreadsheet to whether or not the state has indicators



process_states.py
- ??

fill_and_transpose.py
- ??

transpose_rows.py
- ??

split_indicators.py
- ??

multi_function_script.py
- looks like an initial attempt to run all of the scripts at once across all of the CSV files


# Step 3 (maybe): 
- create unique indicators for each standard
- standard list of courses?


Last steps at the end of cleaning (for now)
- add the state column at the beginning of every row
- remove empty rows
-