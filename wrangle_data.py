from pathlib import Path
import polars as pl
from polars import DataFrame


def get_csv_file_list(folder: str) -> list:
    p = Path(folder)
    generator = p.glob('*.csv')
    file_list = list(generator)
    return file_list


def load_csv_mutate_concatenate(files: list) -> DataFrame | None:
    result = None

    for f in files:
        long = pl.read_csv(f)
        stamped = transform_timestamp(long)
        de_duped = remove_duplicates(stamped)
        wide = long_to_wide(de_duped)

        if result is None:
            result = wide
        else:
            result = pl.concat([result, wide], how="diagonal_relaxed")

    return result


def transform_timestamp(d: DataFrame) -> DataFrame:
    d = d.with_columns(pl.col('SHOUR').replace(24, 0))
    d = d.with_columns(
        pl.concat_str(
            [
                pl.col("SDATE"),
                pl.lit(" "),
                pl.col("SHOUR"),
                pl.lit(":00:00")
                ]
        ).str.to_datetime("%d-%B-%y %H:%M:%S").alias("TIMESTAMP")
    )
    return d


def remove_duplicates(d: DataFrame) -> DataFrame:
    duplicate = d.select(
        pl.col('SITECODE'),
        pl.col("AWSNO"),
        pl.col("TIMESTAMP"),
        pl.col("FIELDNAME")).is_duplicated()
    d = d.filter(~duplicate)
    return d


def write_wide_csv(folder: str, file: str, d: DataFrame):
    p = Path(folder + file)
    d.write_csv(p)


def long_to_wide(d: DataFrame) -> DataFrame:
    d = d.pivot('FIELDNAME',
                index=['SITECODE', 'AWSNO', 'TIMESTAMP'],
                values='VALUE')
    return d


def read_wide_format(folder: str, file: str) -> DataFrame:
    d = pl.read_csv(folder + file, try_parse_dates=True)
    return d


def wrangle_to_wide_format(folder: str):
    file_location_list = get_csv_file_list(folder)
    d = load_csv_mutate_concatenate(file_location_list)
    if d is None:
        raise IOError("No files loaded")
    else:
        write_wide_csv(folder, 'wide_file.csv', d)


def wrangle_to_postgres(folder: str):
    pass


if __name__ == '__main__':
    wrangle_to_wide_format('/home/ogladr-kjarr/data/ceh_ecn/')
