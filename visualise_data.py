import polars as pl
from polars import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt


def direct_matplot_lib(d: DataFrame):

    d_filtered = d.filter(pl.col("SITECODE") == "T12")

    fig, ax = plt.subplots()
    ax.scatter(
        x=d_filtered["TIMESTAMP"],
        y=d_filtered["DRYTMP"],
        c=d_filtered["AWSNO"]
    )

    ax.set_title('Dry Temperature at Cairngorms')
    ax.set_xlabel('Year')
    ax.set_ylabel('Temperature / Celcius')


def direct_seaborn_lib(d: DataFrame):
    d_filtered = d.filter(pl.col("SITECODE") == "T12")

    fig, ax = plt.subplots()
    sns.scatterplot(
        d_filtered,
        x="TIMESTAMP",
        y="DRYTMP",
        hue="AWSNO",
        ax=ax,
    )
    ax.set_title('Dry Temperature at Cairngorms')
    ax.set_xlabel('Year')
    ax.set_ylabel('Temperature / Celcius')


def summarized_single_site(d: DataFrame):
    d_filtered = d.filter(pl.col("SITECODE") == "T12")
    ts = d_filtered.select(pl.col('TIMESTAMP'), pl.col('DRYTMP'))
    sorted_ts = ts.sort('TIMESTAMP')
    average_ts = sorted_ts.group_by_dynamic(
        "TIMESTAMP", every="1mo").agg(pl.col("DRYTMP").mean())

    sns.relplot(data=average_ts, kind='line', x='TIMESTAMP', y='DRYTMP')


def summarized_multiple_sites(d: DataFrame):
    ts_for_group = d.with_columns(
        pl.col('TIMESTAMP').dt.year().alias('YEAR'),
        pl.col('TIMESTAMP').dt.month().alias('MONTH')
    )

    ts_grouped = ts_for_group.group_by(
        ['SITECODE', 'YEAR', 'MONTH']
    ).agg(
        pl.col('DRYTMP').mean().alias('MEANDRYTMP')
    ).with_columns(
        pl.datetime(
            pl.col('YEAR'),
            pl.col('MONTH'),
            pl.lit('01')
        ).alias('TIMESTAMP')
    ).select(
        pl.col('TIMESTAMP'),
        pl.col('SITECODE'),
        pl.col('MEANDRYTMP')
    ).sort('TIMESTAMP')

    g = sns.FacetGrid(ts_grouped, col="SITECODE", col_wrap=2, height=6)
    g.map(sns.pointplot, "TIMESTAMP", "MEANDRYTMP")


if __name__ == '__main__':

    d = pl.read_csv('/home/ogladr-kjarr/data/ceh_ecn/wide_file.csv',
                    try_parse_dates=True)
    direct_matplot_lib(d)
    direct_seaborn_lib(d)
    summarized_single_site(d)
    summarized_multiple_sites(d)
