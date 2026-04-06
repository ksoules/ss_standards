# Step 1
- copy all _done.csv files to new folder
-identify which do not have the right number of columns
    - AL - 4
    - CO - 6
    - CT - 9
    - DE - 7
    - HI - 6
    - KS - 7
    - OH - 6
    - OK - 6
    - OR - 9
    - WI - 6

## Desired structure for all files
Keyword	Grade/Area	Course	Indicator	Standard

- in the merge process: ADD STATE ID

## Manually Fix states with the wrong number of columns

### Problems
- AL: not spliting the indicators correctly
    - added an empty indicator column
- CO: one secondary standard isn't merging correctly
    - manual merge
- CT: extra column appears blank
    - delete all contents of extra column
- DE: Extra 2 columns appear blank
    - delete all contents of extra columns
- HI: extra column appears blank
    - delete all contents of extra column
- KS: Extra 2 columns appear blank
    - delete all contents of extra columns
- OH:  Extra 2 columns appear blank
    - delete all contents of extra column
- OK:  Extra 2 columns appear blank
    - delete all contents of extra column
- OR:  Extra 4 columns appear blank
    - delete all contents of extra column
- WI: extra column appears blank
    - delete all contents of extra column

# Step 2: Merge all of the data