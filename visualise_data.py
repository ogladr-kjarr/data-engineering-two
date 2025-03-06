import polars as pl
from polars import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt


def random_attempts(d: DataFrame):
    all = slice(None)
    subset_t01_1 = d.loc[('T01', 1, all)]
    subset_t01_2 = d.loc[('T01', 2, all)]
    # subset_t01 = d.loc[('T01', [1,2], all)]

    fig, ax = plt.subplots()
    subset_t01_1.plot(y='DRYTMP', use_index=True)
    subset_t01_2.plot(y='DRYTMP', use_index=True)
    # subset_t01.plot(y='DRYTMP', use_index=False)
    ax.plot()
    
    # subset_t01.loc[:, 'DRYTMP'].plot()  
    # met_data = pd.read_csv(Path('full_data.csv'))

if __name__ == '__main__':

    d = pl.read_csv('/home/ogladr-kjarr/data/ceh_ecn/wide_file.csv', try_parse_dates=True)
    random_attempts(d)

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