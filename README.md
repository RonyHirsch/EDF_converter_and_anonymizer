# EDF_converter_and_anonymizer
A Python-based module for both converting Eyelink Data Files (EDFs) and removing any PHI data from them.
- This is a convenient Python script which both converts EDFs to ASCII files (using SR Research's EDF2ASC), and in addition - removes the dateline (containing information about the folderpaths, dates and times) - all in one simple run. 
- The only parameter it takes is the folder path where all the EDFs are. Note that it doesn't override anything, just adds the anonymized ASCII files to the same folder. 
- As this is based on SR Research product, to run this script successfully you'll need it to be in the same folder where you have the "edf2asc.exe" and "edfapi.dll" (provided by SR Research for those with license, see more at https://download.sr-support.com/dispdoc/page25.html ) 
