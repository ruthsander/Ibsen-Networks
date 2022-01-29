import os, glob
import pandas as pd

# THIS SCRIPT MERGES THE CONTENT OF ALL FILES NAMED 'letter_information_18' INTO A NEW CSV FILE

# SPECIFY THE LOCATION OF THE CSV FILES TO BE MERGED
path = "./"

all_files = sorted(glob.glob(os.path.join(path, "letter_information_18*.csv")))
df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
df_merged = pd.concat(df_from_each_file, ignore_index=True)
df_merged.to_csv("merged_letter_info.csv")

