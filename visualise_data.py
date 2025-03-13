import polars as pl
from polars import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def direct_matplot_lib(d: DataFrame):

    d_filtered = d.filter(pl.col("SITECODE") == "T09")

    fig, ax = plt.subplots()
    ax.scatter(
        x=d_filtered["TIMESTAMP"],
        y=d_filtered["DRYTMP"],
        c=d_filtered["AWSNO"]
    )

    ax.set_title('Dry Temperature at Alice Holt')
    ax.set_xlabel('Year')
    ax.set_ylabel('Temperature / Celcius')


def direct_seaborn_lib(d: DataFrame):
    d_filtered = d.filter(pl.col("SITECODE") == "T09")

    fig, ax = plt.subplots()
    sns.scatterplot(
        d_filtered,
        x="TIMESTAMP",
        y="DRYTMP",
        hue="AWSNO",
        ax=ax,
    )
    ax.set_title('Dry Temperature at Alice Holt')
    ax.set_xlabel('Year')
    ax.set_ylabel('Temperature / Celcius')


def summarized_single_site(d: DataFrame):
    d_filtered = d.filter(pl.col("SITECODE") == "T09")
    ts = d_filtered.select(pl.col('TIMESTAMP'), pl.col('DRYTMP'))
    sorted_ts = ts.sort('TIMESTAMP')
    average_ts = sorted_ts.group_by_dynamic(
        "TIMESTAMP", every="1mo").agg(pl.col("DRYTMP").mean())

    fig, ax = plt.subplots()
    sns.lineplot(
        data=average_ts,
        x='TIMESTAMP',
        y='DRYTMP',
        ax=ax)

    ax.set_title('Monthly Dry Temperature at Alice Holt')
    ax.set_xlabel('Year')
    ax.set_ylabel('Temperature / Celcius')


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
        pl.col('YEAR'),
        pl.col('SITECODE'),
        pl.col('MEANDRYTMP')
    ).sort('TIMESTAMP')

    order = ts_grouped.select(pl.col('SITECODE')).to_series().to_list()
    site_order = sorted(list(set(order)))

    g = sns.FacetGrid(
        ts_grouped,
        col="SITECODE",
        col_wrap=2,
        height=6,
        col_order=site_order)

    g.map(sns.pointplot, "TIMESTAMP", "MEANDRYTMP")
    g.set_xlabels('Year')
    g.set_ylabels('Temperature / Celcius')
    g.set_titles('Dry Temp at site {col_name}')


def one_year_one_site(d: DataFrame):

    one_year = d.with_columns(
        pl.col('TIMESTAMP').dt.year().alias('YEAR'),
        pl.col('TIMESTAMP').dt.month().alias('MONTH')
    ).filter((pl.col('YEAR') == 2015) & (pl.col('SITECODE') == 'T09'))

    fig, ax = plt.subplots()
    sns.kdeplot(
        data=one_year, x="DRYTMP", hue="MONTH", palette="crest", ax=ax
    )

    ax.set_title('Dry Temperature at Alice Holt in 2015')
    ax.set_xlabel('Year')
    ax.set_ylabel('Temperature / Celcius')


def ridge(d: DataFrame):

    # sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

    # Create the data
    ts_ridge = d.with_columns(
        pl.col('TIMESTAMP').dt.year().alias('YEAR'),
        pl.col('TIMESTAMP').dt.month().alias('MONTH')
    ).filter(
            (pl.col('SITECODE') == 'T09') &
            (pl.col('YEAR') == 2000)
    ).select(['MONTH', 'DRYTMP'])

    x = ts_ridge.select(pl.col('DRYTMP')).to_series().to_list()
    g = ts_ridge.select(pl.col('MONTH')).to_series().to_list()
    df = pd.DataFrame(dict(x=x, g=g))
    
    # Initialize the FacetGrid object
    pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
    g = sns.FacetGrid(df, row="g", hue="g", aspect=15, height=.5, palette=pal)

    # Draw the densities in a few steps
    g.map(sns.kdeplot, "x",
        bw_adjust=.5, clip_on=False,
        fill=True, alpha=1, linewidth=1.5)
    g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw_adjust=.5)

    # passing color=None to refline() uses the hue mapping
    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)


    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)


    g.map(label, "x")

    # Set the subplots to overlap
    g.figure.subplots_adjust(hspace=-.25)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.despine(bottom=True, left=True)
    g.fig.suptitle('Dry Temperatures at Alice Holt in 2000 by Month')
    g.set_axis_labels('Temperature / Celcius')


if __name__ == '__main__':

    d = pl.read_csv('/home/ogladr-kjarr/data/ceh_ecn/wide_file.csv',
                    try_parse_dates=True)
    direct_matplot_lib(d)
    direct_seaborn_lib(d)
    summarized_single_site(d)
    summarized_multiple_sites(d)
    one_year_one_site(d)
    ridge(d)
