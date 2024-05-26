# Numadic Data test - Vehicle Asset Report Generation

Built an API to generate the Asset Report using Flask.

The API takes start time and end time in epoch format as input parameters. Below is a screenshot of the web page developed using Flask, HTML and CSS.

![WhatsApp Image 2024-05-26 at 04 30 01_ff94d064](https://github.com/manoj24vvr/Numadic_Data_test/assets/75264791/9c6d567b-1bb0-4876-a64e-dd64acd7e10f)
![WhatsApp Image 2024-05-26 at 04 30 17_aa496608](https://github.com/manoj24vvr/Numadic_Data_test/assets/75264791/7836670f-222e-43ef-a9e0-27d920bba901)

Inserted a button at the end of the web page to download the final asset report.

## Output :

The file [asset_report_sample_output.xlsx](https://github.com/manoj24vvr/Numadic_Data_test/blob/main/asset_report_sample_output.xlsx) contains a sample output in the specified format of 15 Vehicle Trails data from the EOP-Dump.

Following is the list of fields/columns in the final output:
#### Required Columns:
1) License plate number
2) Distance
3) Number of Trips Completed
4) Average Speed
5) Transporter Name
6) Number of Speed Violations

#### Additional Columns:
7) Total Quantity
8) Number of Harsh Accelarations
9) Number of Harsh Braking
10) Percentage of Overspeeding

> If you want make the API call:
> clone this repo/download the [asset_report_app.py](https://github.com/manoj24vvr/Numadic_Data_test/blob/main/asset_report_app.py)
> Change paths to Trip-Info.csv file and EOP-dump folder
> Run 'python asset_report_app.py' in the terminal.
