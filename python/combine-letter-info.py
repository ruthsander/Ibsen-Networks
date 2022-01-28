import os, glob
import pandas as pd

path = "./"

all_files = sorted(glob.glob(os.path.join(path, "letter_information_18*.csv")))
df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
df_merged = pd.concat(df_from_each_file, ignore_index=True)
df_merged.to_csv("merged_letter_info.csv")



#
# with open('original.csv', 'r') as f1:
#     original = f1.read()
#
# with open('all.csv', 'a') as f2:
#     f2.write('\n')
#     f2.write(original)