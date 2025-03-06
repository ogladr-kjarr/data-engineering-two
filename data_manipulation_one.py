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
    d = d.pivot('FIELDNAME', index=['SITECODE', 'AWSNO','TIMESTAMP'], values='VALUE')
    return d

def read_wide_format(folder: str, file: str) -> DataFrame:
    d = pl.read_csv(folder + file, try_parse_dates=True)
    return d

def wrangle_files(folder: str):
    file_location_list = get_csv_file_list(folder)
    d = load_csv_mutate_concatenate(file_location_list)
    if d is None:
        raise IOError("No files loaded")
    else: 
        write_wide_csv(folder, 'wide_file.csv', d)


def random_attempts():
    # all = slice(None)
    # subset_t01_1 = wide_df.loc[('T01', 1, all)]
    # subset_t01_2 = wide_df.loc[('T01', 2, all)]
    # subset_t01 = wide_df.loc[('T01', [1,2], all)]

    # fig, ax = plt.subplots()
    # subset_t01_1.plot(y='DRYTMP', use_index=True)
    # subset_t01_2.plot(y='DRYTMP', use_index=True)
    # subset_t01.plot(y='DRYTMP', use_index=False)
    # ax.plot()
    
    # subset_t01.loc[:, 'DRYTMP'].plot()  
    # met_data = pd.read_csv(Path('full_data.csv'))
    pass

if __name__ == '__main__':
    wrangle_files('/home/ogladr-kjarr/data/ceh_ecn/')

# df = pl.read_csv('./wide_file.csv', try_parse_dates=True)

# ts = df.select(pl.col('TIMESTAMP'), pl.col('SITECODE'), pl.col('DRYTMP'))
# sorted_ts = ts.sort('TIMESTAMP')
# average_ts = sorted_ts.group_by_dynamic("TIMESTAMP", every="1mo").agg(pl.col("DRYTMP").mean())
# sns.relplot(data=average_ts,kind='line',x='TIMESTAMP',y='DRYTMP')

# ts_for_group = df.with_columns(
#     pl.col('TIMESTAMP').dt.year().alias('YEAR'),
#     pl.col('TIMESTAMP').dt.month().alias('MONTH'),
#     pl.col('TIMESTAMP').dt.day().alias('DAY')
# )

# ts_grouped = ts_for_group.group_by(
#     ['SITECODE','YEAR','MONTH']
# ).agg(
#     pl.col('DRYTMP').mean().alias('MEANDRYTMP')
# ).with_columns(
#     pl.datetime(
#         pl.col('YEAR'),
#         pl.col('MONTH'),
#         pl.col('DAY')
#     ).alias('TIMESTAMP')
# ).select(
#     pl.col('TIMESTAMP'),
#     pl.col('SITECODE'),
#     pl.col('MEANDRYTMP')
# ).sort('TIMESTAMP')




# average_ts = sorted_ts.group_by_dynamic(["TIMESTAMP","SITECODE"], every="1mo").agg(pl.col("DRYTMP").mean())
# sns.relplot(data=ts_grouped,kind='line',x='TIMESTAMP',y='MEANDRYTMP', hue='SITECODE')


# g = sns.FacetGrid(ts_grouped, col="SITECODE", col_wrap=2, height=6)
# g.map(sns.pointplot, "TIMESTAMP", "MEANDRYTMP")