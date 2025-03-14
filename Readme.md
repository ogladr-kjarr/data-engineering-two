# Introduction

This project was created to practise working with CSV files and data visualization libraries.

The data was taken from the CEH [ECN data site](https://catalogue.ceh.ac.uk/datastore/eidchub/fc9bcd1c-e3fc-4c5a-b569-2fe62d40f2f5/), specifically the [meterological section](https://catalogue.ceh.ac.uk/datastore/eidchub/fc9bcd1c-e3fc-4c5a-b569-2fe62d40f2f5/).


# Data Wrangling

## DataFrame Library

Initially I started using Pandas, as that looks to be the standard. But I also looked at Polars and found it to be much more intuitive to use. This was especially so when I was pivoting the DataFrame to a wide format and having to deal with the hierarchical indexes. I found these indexes to be a bit convoluted, whereas with Polars the DataFrame behaves as I expect it to when doing a pivot, much the same was as dplyr in R.

## CSV sizes

Initially I loaded and concatenated all the files into one long format DataFrame, before creating the timestamp, removing the duplicates, and finally manipulating into a wide format file.  This worked fine on one computer as it had 8GB of RAM, but the laptop I use when I'm out only has 4GB of RAM and 4GB of swap. It had no way of doing the operations in the same way as my larger RAM computer, and after loading a few files Fedora would close VSCode with a memory warning.

I noticed that after writing both the long format and the wide format files, the wide format file was much much smaller in size. This makes sense as it's not duplicating the same numerous fields around fourteen times for each sensor at each point in time. With that in mind I restructured the code in the loading loop to carry out the manipulations on each file just after loading, then converted to a wide format, and concatenated all the wide format DataFrames together. This worked perfectly and didn't come close to using all the RAM or swap.

The only change I had to make was in the way I concatenated the DataFrames together. Originally I used the 'vertical' setting for the 'how' parameter, but as some of the wide format DataFrames had columns others did not, it threw an error. Changing the how setting to 'diagonal_relaxed' allowed it to happily add more columns as it found them.

## Data Modifications

The first thing to do was create the list of files to be read. The files were downloaded manually and saved into a single folder. The function below lists all the CSV files.

```python
def get_csv_file_list(folder: str) -> list:
    p = Path(folder)
    generator = p.glob('*.csv')
    file_list = list(generator)
    return file_list
```

Next was loading each individual file and passing it through a number of wrangling functions. This controller function read each csv, called on the mutations, then saved them all into one single dataframe.

```python
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
```

The first mutation was to create the timestamp column from the date and hour columns. The columns were amended with literals to create a date time format that could be parsed by the to_datetime function.

```python
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
```

The next step was to remove duplicates. The site code, timestamp, and sensor make the main attributes to be checked for duplicates, however AWSNO is used to differentiate between sensor groups as far as I can tell, and so it also needs to be checked for duplicates. Once a list is created, the DataFrame is filtered to remove the duplicate rows.

```python
def remove_duplicates(d: DataFrame) -> DataFrame:
    duplicate = d.select(
        pl.col('SITECODE'),
        pl.col("AWSNO"),
        pl.col("TIMESTAMP"),
        pl.col("FIELDNAME")).is_duplicated()
    d = d.filter(~duplicate)
    return d
```

The last mutation is to transform the DataFrame from a long format to a wide format. We keep the three main identifying columns as the index, create new columns based on the values in fieldname, and give them the values from the value column.

```python
def long_to_wide(d: DataFrame) -> DataFrame:
    d = d.pivot('FIELDNAME',
                index=['SITECODE', 'AWSNO', 'TIMESTAMP'],
                values='VALUE')
    return d
```

Lastly the file is written to disk as a CSV file.

# Plots

The plots here are just the most basic to have a quick look at part of the data. I decided to use the dry temperature sensor to focus on, as it provides the most pleasing and intuitive data, that of a hourly temperature reading over a number of years. I decided to focus on one side, T09 - Alice Holt.

First though, to see the above, I created a FacetGrid plot of all sites dry temperature values, as shown below. I was happy getting the plot to show the site code in each facets title, but I was unhappy at the way the xticks aren't shown properly. Using the documention, Stack Overflow, ChatGPT, and Claude Sonnet, I could not find a working solution. I even tried using a pandas DataFrame in case there was some difference between their date time representation interpretation by the graph, but that didn't work either.

![All Sites FacetGrid Plot](plots/facet-grid-seaborn.png)

Next I created two scatter plots, the first using Matplotlib directly, the second using Seaborn. There are basic plots to see the distribution of points. Below is the Matplotlib plot.

![Basic Matplot Scatter Plot](plots/basic-matplotlib.png)

And below is the Seaborn plot.

![Basic Seaborn Scatter Plot](plots/basic-seaborn.png)

Next is a summarized plot, with the data aggregated to months.

![Monthly Summarized Line Plot](plots/monthly-summary-seaborn.png)

The last two plots are density plots for Alice Holt, covering the year of 2000. The first is quite a busy and unreadable plot, which I include just to be able to compare to the ridge plot that follows.

![One Site One Year Density Plot](plots/one-site-monthly-seaborn.png)

The ridge plot was very fragile, in the end I used the code from this [example]() and after having no success trying to tailor it to my data, I tailored my data to the existing structure and it worked. 

TODO: Change the month integers to the month names.

![One Site One Year Ridge Plot](plots/one-site-monthly-ridge-seaborn.png)
\]

# Software installed

todo: create a pip requirements file and create a venv

pip install types-seaborn