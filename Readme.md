# Introduction

This project was created to practise working with CSV files, with the PostgreSQL Docker image, and data visualization libraries.

The data was taken from the CEH [ECN data site](https://catalogue.ceh.ac.uk/datastore/eidchub/fc9bcd1c-e3fc-4c5a-b569-2fe62d40f2f5/), specifically the [meterological section](https://catalogue.ceh.ac.uk/datastore/eidchub/fc9bcd1c-e3fc-4c5a-b569-2fe62d40f2f5/).


# Data Wrangling

## DataFrame Library

Initially I started using Pandas, as that looks to be the standard. But I also looked at Polars and found it to be much more intuitive to use. This was especially so when I was pivoting the DataFrame to a wide format and having to deal with the hierarchical indexes. I found these indexes to be a bit convoluted, whereas with Polars the DataFrame behaves as I expect it to when doing a pivot, much the same was as dplyr in R.

## CSV sizes

Initially I loaded and concatenated all the files into one long format data frame, before creating the timestamp, removing the duplicates, and finally manipulating into a wide format file.  This worked fine on one computer as it had 8GB of RAM, but the laptop I use when I'm out only has 4GB of RAM and 4GB of swap. It had no way of doing the operations in the same way as my larger RAM computer, and after loading a few files Fedora would close VSCode with a memory warning.

I noticed that after writing both the long format and the wide format files, the wide format file was much much smaller in size. This makes sense as it's not duplicating the same fields barring value around fourteen times for each point in time. With that in mind I restructured the code in the loading loop to carry out the manipulations on each file just after loading, then converted to a wide format, and concatenated all the wide format DataFrames together. This worked perfectly and didn't come close to using all the RAM or swap.

The only change I had to make was in the way I concatenated the DataFrames together. Originally I used the 'vertical' setting for the 'how' parameter, but as some of the wide format DataFrames had columns others did not, it threw an error. Changing the how setting to 'diagonal_relaxed' allowed it to happily add more columns as it found them.

# Plots

The plots here are just the most basic to get a quick look at the data. Using a faceted plot to show all the sites I decided to focus on just one site, T09 - Alice Holt. This was because it's one of the few that have a continuous reading with one group of sensors, many other sites have combinations of sensor groups. This was found using the following code, where AWSNO 2 represents the use of another set of sensors as opposed to just AWSNO 1. I then sorted the dataframe to show all the sitecodes that have AWSNO 2 readings.

```python
    d_f = d.filter(pl.col('AWSNO') == 2)
    d_u = d_f.select(
            'SITECODE'
        ).unique(
            'SITECODE'
        ).sort('SITECODE')
```
Ridge plot was very fragile, in the end I used the code from this [example]() and after having no success trying to tailor it to my data, I tailored my data to the existing structure and it worked.  The only annoying thing is that if the theme isn't set, the plot doesn't display properly. But when running in an interactive window on VSCode this setting on subsequent re-runs affects the theme on all the other plots, which isn't desired.

was happy getting the facetgrid for each site to display the site code in the facet windows.

The only thing I couldn't do, even with trying Google, existing Stack Overflow questions, and ChatGPT, was to get the x-axis tick marks on the facetgrid for each site to work. At the moment it's a horrible bar of overlapping text, nothing I tried worked and I'm still unsure of how it should be done, especially as ChatGPT was so sure of its numerous examples and attempts.

# Software installed

todo: create a pip requirements file and create a venv

pip install types-seaborn