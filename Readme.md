# Introduction

This project was created to practise working with CSV files, with the PostgreSQL Docker image, and data visualization libraries.


# Data Wrangling

## DataFrame Library

Initially I started using Pandas, as that looks to be the standard. But I also looked at Polars and found it to be much more intuitive to use. This was especially so when I was pivoting the DataFrame to a wide format and having to deal with the hierarchical indexes. I found these indexes to be a bit convoluted, whereas with Polars the DataFrame behaves as I expect it to when doing a pivot, much the same was as dplyr in R.

## CSV sizes

Initially I loaded and concatenated all the files into one long format data frame, before creating the timestamp, removing the duplicates, and finally manipulating into a wide format file.  This worked fine on one computer as it had 8GB of RAM, but the laptop I use when I'm out only has 4GB of RAM and 4GB of swap. It had no way of doing the operations in the same way as my larger RAM computer, and after loading a few files Fedora would close VS studio with a memory warning.

I noticed that after writing both the long format and the wide format files, the wide format file was much much smaller in size. This makes sense as it's not duplicating the same fields barring value around fourteen times for each point in time. With that in mind I restructured the code in the loading loop to carry out the manipulations on each file just after loading, then converted to a wide format, and concatenated all the wide format DataFrames together. This worked perfectly and didn't come close to using all the RAM or swap.

The only change I had to make was in the way I concatenated the DataFrames together. Originally I used the 'vertical' setting for the 'how' parameter, but as some of the wide format DataFrames had columns others did not, it threw an error. Changing the how setting to 'diagonal_relaxed' allowed it to happily add more columns as it found them.

# Plots

I do miss ggplot2, but Seaborn looks interesting. The plots here are just the most basic, trying out example code.

# Software installed

todo: create a pip requirements file and create a venv

pip install types-seaborn