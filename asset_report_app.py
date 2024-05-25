from flask import Flask, request, jsonify, render_template_string, send_file
import pandas as pd
import os
from datetime import datetime
from math import radians, cos, sin, sqrt, atan2

app = Flask(__name__)

# path to the 'Trip-Info.csv' file
trip_info = pd.read_csv("D:\\Manoj-1\\Manoj\\Offcampus Assign\\Numadac\\Data test\\Trip-Info.csv")

# path to the 'EOL-dump' folder containing all vehicles trail data
path_to_EOL_dump = "D:\\Manoj-1\\Manoj\\Offcampus Assign\\Numadac\\Data test\\EOL-dump"
vehicle_trail_files = os.listdir(path_to_EOL_dump)

# function - to filter only required data based on start and end time
def filter_data(df, start_time, end_time):
    df['tis'] = pd.to_datetime(df['tis'], unit='s')
    return df[(df['tis'] >= start_time) & (df['tis'] <= end_time)]

# function - to calculate distance based on latitude and longitude values using haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# function - to iterate over all vehicle trail files, calculate and return required fields
def retrieve_calculated_data(path_to_EOL_dump,vehicle_trail_files, start_time, end_time):
    # list - to append one record for each vehicle trail data in each iteration
    data_records = []
    count = 0
    for file in vehicle_trail_files:
        count = count + 1
        file_path = os.path.join(path_to_EOL_dump, file)
        vehicle_df = pd.read_csv(file_path)
        filtered_data = filter_data(vehicle_df, start_time, end_time)
        if not filtered_data.empty:
            # Required columns
            distance = sum(haversine(filtered_data['lat'].iloc[i], filtered_data['lon'].iloc[i], 
                                     filtered_data['lat'].iloc[i+1], filtered_data['lon'].iloc[i+1])
                           for i in range(len(filtered_data)-1))
            avg_speed = filtered_data['spd'].mean()
            speed_violations = filtered_data['osf'].sum()
            lic_plate_no = filtered_data['lic_plate_no'].iloc[0]
            transporter_name = trip_info[trip_info['vehicle_number'] == lic_plate_no]['transporter_name'].iloc[0]
            num_trips = trip_info[trip_info['vehicle_number'] == lic_plate_no]['trip_id'].nunique()

            # Additional columns
            total_duration = (filtered_data['tis'].iloc[-1] - filtered_data['tis'].iloc[0]).total_seconds()
            average_duration = total_duration / num_trips
            total_quantity = trip_info[trip_info['vehicle_number'] == lic_plate_no]['quantity'].sum()
            num_harsh_accelerations = filtered_data['harsh_acceleration'].sum()
            num_harsh_brakes = filtered_data['hbk'].sum()
            percentage_overspeeding = (speed_violations / num_trips) * 100 if num_trips > 0 else 0

            data_records.append([
                lic_plate_no, distance, num_trips, avg_speed, transporter_name, speed_violations,
                total_quantity, num_harsh_accelerations, num_harsh_brakes, percentage_overspeeding
            ])
        if count > 15:
            break
    return data_records

# Created API using Flask and developed a simple frontend using HTML and CSS
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            start_time = int(request.form['start_time'])
            end_time = int(request.form['end_time'])
            start_time = datetime.utcfromtimestamp(start_time)
            end_time = datetime.utcfromtimestamp(end_time)

            metrics = retrieve_calculated_data(path_to_EOL_dump,vehicle_trail_files, start_time, end_time)

            if not metrics:
                return render_template_string("""
                    <h1>No data available for the specified time period</h1>
                """)

            report_df = pd.DataFrame(metrics, columns=[
                'License plate number', 'Distance', 'Number of Trips Completed', 'Average Speed', 'Transporter Name', 'Number of Speed Violations',
                'Total Quantity', 'Number of Harsh Accelarations', 'Number of Harsh Braking','Percentage of Overspeeding'
            ])

            report_html = report_df.to_html(index=False, classes="table table-striped table-bordered")
            
            # Optionally, save the report as an Excel file
            report_path = 'asset_report.xlsx'
            report_df.to_excel(report_path, index=False)

            return render_template_string("""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Asset Report</title>
                    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
                    <style>
                        body { background-color: #f8f9fa; }
                        .container { margin-top: 50px; }
                        .table { margin-top: 20px; }
                        h1 { color: #007bff; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Asset Report</h1>
                        <form method="post">
                            <div class="form-group">
                                <label for="start_time">Start Time:</label>
                                <input type="text" class="form-control" id="start_time" name="start_time" placeholder="Enter start time (epoch)">
                            </div>
                            <div class="form-group">
                                <label for="end_time">End Time:</label>
                                <input type="text" class="form-control" id="end_time" name="end_time" placeholder="Enter end time (epoch)">
                            </div>
                            <button type="submit" class="btn btn-primary">Submit</button>
                        </form>
                        <div>{{ report_html|safe }}</div>
                        <p class="mt-3">Download the report as an Excel file: <a href="/download_report" class="btn btn-primary">Download</a></p>
                    </div>
                </body>
                </html>
            """, report_html=report_html)

        except Exception as e:
            return render_template_string("""
                <h1>Error: {{ error }}</h1>
            """, error=str(e))

    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Asset Report</title>
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { background-color: #f8f9fa; }
                .container { margin-top: 50px; }
                .table { margin-top: 20px; }
                h1 { color: #007bff; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Asset Report</h1>
                <form method="post">
                    <div class="form-group">
                        <label for="start_time">Start Time:</label>
                        <input type="text" class="form-control" id="start_time" name="start_time" placeholder="Enter start time (epoch)">
                    </div>
                    <div class="form-group">
                        <label for="end_time">End Time:</label>
                        <input type="text" class="form-control" id="end_time" name="end_time" placeholder="Enter end time (epoch)">
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </body>
        </html>
    """)

# to download the final asset report in the excel format upon clicking on the Download button
@app.route('/download_report')
def download_report():
    report_path = 'asset_report.xlsx'
    return send_file(report_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
