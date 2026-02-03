# ss_standards
Social Studies Standards research project

# Data Processing Goal
- normalize the data so that all states are in the same format

## Transpose
- rearrange data so that each entry is on its own line in the spreadsheet

### Fill and Transpose
- rerranges the data, but then also fills in blank cells with duplicate information, such as grade, course, keyword, etc


**Desired Components**
- key word
- grade
- course name
- standard text
- standard ID (if it exists)

IDEAL DATA FORM

| ID  | State | Grade | Course  | Text                | (other details) | Keyword  |
| --- | ----- | ----- | ------- | ------------------- | --------- | -------- |
| xdy | AA    | 8     | US-hist | Sample text         | NA        | Keyword1 |
| xdy | AA    | 8     | US-hist | Sample text         | NA        | Keyword3 |
| xdy | AA    | 8     | US-hist | Sample text         | NA        | Keyword4 |
| sdf | MS    | 6     | US-hist | another sample text | NA        | Keyword1 |



*will need to determine*
- if/how to create unique identifiers
    - if we want to create a single file that can be queried instead of having to query each
    state independently
    - some states have systems and others do not
- what to do with additional info
    - theme/concept/time period

**Other issues**
~~ remove unwanted line breaks~~
~~ deal with unusual characters~~
- revise grade column so it is all numerical

# Secondary Cleaning
1. Drop completely empty rows - implemented

2. If there is only data in column 1, write NA column 2. implemented
- need to normalize NA strings

2. Add a state abbreviation column at the beginning of each each file - implemented

3. Concatenate the contents of columns 5 - not yet working
3. grades: words to numbers - not implemented


# Data Processing Part 2
- clean up keyword list
    - variations on terms (e.g. Jew, Judaism, Jewish)
    - categories of terms (religious traditions, places, concepts, people)

# DO BEFORE PROCESSING ALL STATES
i.e. after everything is working on the selection of test states
1. update/review parameters spreadsheet
1. download new data from Alaska, etc


# KNOWN ISSUES
- when viewing the files in excel, some grade ranges, such as 6-8 or 7/8, might get autoformated as dates. 
    - to prevent this, view in another application (R studio, etc)