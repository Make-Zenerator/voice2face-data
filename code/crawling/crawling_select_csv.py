import os
import pandas as pd
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()

    # Conventional args
    parser.add_argument('--csv_file', type=str, default='output_test.csv')
    parser.add_argument('--data_path', type=str, default='origin/video')
    parser.add_argument('--save_csv', type=str, default='new_output.csv')

    args = parser.parse_args()

    return args


def list_files_and_folders(data_path):
    if os.path.isdir(data_path):
        items = os.listdir(data_path)
        return items
    else:
        return None

def main(csv_file, data_path, save_csv):

    csv_data = pd.read_csv(csv_file, header=None)
    youtube_ids = list_files_and_folders(data_path)

    for youtube_id in youtube_ids:
        filtered_df = csv_data[csv_data[0].astype(str).str.contains(youtube_id)]
        first_row = filtered_df.iloc[0:1]
        file_name = list_files_and_folders(os.path.join(data_path, youtube_id))[0]
        file_name_list = file_name.split("_")
        first_row[4] =  file_name_list[0]
        first_row[5] =  file_name_list[1]
        first_row.to_csv(save_csv, mode="a", index=False, header=False)


if __name__ == '__main__':
    args = parse_args()
    main(**args.__dict__)