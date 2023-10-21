import csv
from datetime import datetime, timedelta

global payment_timestamp


def receivedPayments(csvFile, colNumbers, searchWord):
    searchWord1 = 'INDBNK'  # Search for "INDBNK" in column 3 (index 2)
    colNumber1 = 2

    searchWord2 = 'credited'  # Search for "credited" in column 5 (index 4)
    colNumber2 = 4

    # Define the time range for comparison (10 minutes before and after the current time)
    current_time = datetime.now()
    time_range_start = current_time - timedelta(minutes=10)
    time_range_end = current_time + timedelta(minutes=10)

    # Format time_range_start and time_range_end to display milliseconds
    formatted_time_range_start = time_range_start.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    formatted_time_range_end = time_range_end.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    try:
        with open(csvFile, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)

            for row_number, row in enumerate(reader, start=1):
                if len(row) > colNumber1 and len(row) > colNumber2:
                    if searchWord1 in row[colNumber1] and searchWord2 in row[colNumber2]:
                        row_data_col2 = row[colNumber1].split()
                        row_data_col4 = row[colNumber2].split()
                        # print(row_data_col2[1])
                        # print(row_data_col4)
                        date_time = row[1]
                        try:
                            data_12 = row_data_col2[12]
                        except IndexError:
                            data_12 = "N/A"

                        amount = row_data_col4[0].split("Rs.")
                        # print(amount)
                        if float(amount[1]) >= 1:
                            print(date_time, row_data_col2[0], data_12, row_data_col4[0],
                                  row_data_col4[1])
                            # return True
                            print("True")

    except FileNotFoundError:
        print(f"The file '{csvFile}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Define the path to your CSV file
csv_file_path = 'C:\Ozeki\All SMS Record\\report_2309.csv'

# Define the column numbers you want to print (0-based indices)
column_numbers = [2, 4]  # Replace with the column indices you want to print

receivedPayments(csv_file_path, column_numbers, searchWord="credited")
