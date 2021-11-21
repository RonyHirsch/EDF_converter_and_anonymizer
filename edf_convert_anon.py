import os
import subprocess
import argparse

"""
This module operates on a single folder containing EDF (Eyelink Data Format) files. For each EDF file, the module:
1. Saves this file in ASCII format: Using SR-research's EDF2ASC conversion
2. Edits the ASCII-format file s.t it will be anonymized - removes all lines which contain date time or identifier from
the ascii-file.
Results are printed to shell, but everything is saved in-place in the folder the user inputs. The method does NOT 
override the original EDFs.
@author: RonyHirsch
"""

EDF = ".edf"
ASC = ".asc"
EDF_TO_ASC = "edf2asc.exe"
CONV_FROM = "CONVERTED FROM"
DATE_TIME = "DATE"


def asc_anonymize(path_to_ascii):
    """
    Remove conversion line and date+time line from ASCII eye-tracking data file.
    :param path_to_ascii: path to a single ascii-format eye-tracking data file
    :return: nothing, saves the same file w/o the date+time data (in-place)
    """
    ascii_name = os.path.split(path_to_ascii)[-1]
    with open(path_to_ascii, 'r') as et_f:
        et = et_f.read().splitlines(True)
    with open(path_to_ascii, 'w') as et_f_conv:
        for line in et:
            if CONV_FROM not in line and DATE_TIME not in line:
                et_f_conv.write(line)
    print(f"DATE AND TIME REMOVED FROM FILE {ascii_name}")
    return


def edf_to_ascii(file_path):
    """
    This method takes an edf (Eyelink Data Format) file and converts it to ascii format using SR Research's EDF2ASC.
    IMPORTANT: for this to run the script should be located in the same folder as the edfapi.dll and edf2asc.exe
    :param file_path: path to a single edf file.
    :return: nothing. the function just adds an ascii file where the edf file resides. DOES NOT OVERRIDE THE EDFs
    """
    path, file_name = os.path.split(file_path)
    file_stripped = file_name.split(".")[0] + ASC  # name w/o the ".edf" suffix
    # get where we're at. ASSUMPTION : THE EDF2ASC DLL AND EXE ARE IN THE SAME FOLDER THIS SCRIPT RUNS IN
    conversion_folder = os.path.dirname(os.path.realpath(__file__))
    cmd = os.path.join(conversion_folder, EDF_TO_ASC)
    if not os.path.isfile(os.path.join(path, file_stripped)):
        subprocess.run([cmd, "-p", path, file_path], shell=True)
    else:
        print(f"FILE {file_stripped} already exists in {path}")
    return


def convert_edf(folderpath):
    """
    Goes over all edf files in folder and:
    (1) converts them to ASCII using SR Research's EDF2ASC and then
    (2) removes conversion line and date+time line from the ascii file, saves it.
    :param folderpath: path to where all edf files are located
    :return: nothing. saves everything in folderpath
    """
    edf_files = [f for f in os.listdir(folderpath) if f.endswith(EDF)]
    for edf_file in edf_files:
        print(f"Converting file {edf_file}: ")
        edf_to_ascii(os.path.join(folderpath, edf_file))
    print(f"ALL EDF FILES IN FOLDER {folderpath} HAVE BEEN CONVERTED TO ASCII")
    ascii_files = [f for f in os.listdir(folderpath) if f.endswith(ASC)]
    for asc_file in ascii_files:
        asc_anonymize(os.path.join(folderpath, asc_file))
    print(f"ALL ASCII FILES IN FOLDER {folderpath} HAVE BEEN ANONYMIZED")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folderpath', type=str, required=True)
    args = parser.parse_args()
    convert_edf(folderpath=args.folderpath)


if __name__ == "__main__":
    main()

