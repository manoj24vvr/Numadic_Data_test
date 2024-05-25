# Numadic Data test - Vehicle Asset Report Generation

Built an API to generate the Asset Report using Flask.

The API takes start time and end time in epoch format as input parameters. Below is a screenshot of the web page developed using Flask, HTML and CSS.

![WhatsApp Image 2024-05-26 at 04 30 01_ff94d064](https://github.com/manoj24vvr/Numadic_Data_test/assets/75264791/9c6d567b-1bb0-4876-a64e-dd64acd7e10f)

The file [asset_report_sample_output.xlsx](https://github.com/manoj24vvr/Numadic_Data_test/blob/main/asset_report_sample_output.xlsx) contains a sample output run on 15 Vehicle Trails data from the EOP-Dump.

## Dataset :

The data required for this project is taken from the below website.
> http://snap.stanford.edu/data/web-Amazon-links.html

It contains user reviews (numerical rating and textual comment) towards amazon products on 24 product categories(e.g., cell phones, clothing, beauty, etc.), and there is an independent dataset for each product category. We will select 5 product categories in this project i.e., Arts.txt.gz, Cell_Phones_&_Accessories.txt.gz, Jewelry.txt.gz, Musical_Instruments.txt.gz, Watches.txt.gz. On choosing the category of product, recommendations are displayed based on user based similarity .

## Pipeline :
After we select a dataset to work on, this project will mainly consist three steps:

1) Data Processing
2) Perform EDA
3) create the training and testing datasets
4) Conduct rating prediction and make evaluation
5) Conduct Top-N Recommendation

