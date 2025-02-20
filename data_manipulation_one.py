from pathlib import Path
from pandas import DataFrame
import pandas as pd

def get_csv_file_list(folder: str) -> list:
    p = Path(folder)
    generator = p.glob('*.csv')
    file_list = list(generator)
    return file_list

def load_csv_and_concatenate(files: list) -> DataFrame:
    result = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    return result

def write_csv(folder: str, df: DataFrame):
    p = Path(folder + "/full_data.csv")
    df.to_csv(p, index=False)

if __name__ == "__main__":
    data_location = '/home/ogladr-kjarr/data/ceh_ecn'
    file_location_list = get_csv_file_list(data_location)
    x = load_csv_and_concatenate(file_location_list)
    write_csv(data_location, x)