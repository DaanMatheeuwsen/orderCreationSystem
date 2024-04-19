import mysql.connector

# Connect to your database
connection = mysql.connector.connect(
    host="localhost",
    user="admin_rsg-ocs",
    password="pe61BcRXSu",
    database="admin_rsg-ocs"
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Define the data to be inserted
data_to_insert = [
    ("Company1", 1, "BookingNumber1", "AgreedTariff1", "InvoiceReference1", "ContactPerson1", "EmailAddress1", "PhoneNumber1", "NameLoading1", "StreetHousenumberLoading1", "CountryCodeLoading1", "PostalcodeLoading1", "CityLoading1", "RequestedLoadingDateFrom1", "RequestedLoadingTime1", "RequestedLoadingTimeUntil1", "RequestedLoadingDateUntil1", "SlotbookingRequiredLoading1", "LoadingReference1", "NameUnloading1", "StreetHousenumberUnloading1", "CountryCodeUnloading1", "PostalcodeUnloading1", "CityUnloading1", "RequestedUnloadingDateFrom1", "RequestedUnloadingTime1", "RequestedUnloadingDateUntil1", "RequestedUnloadingTimeUntil1", "SlotbookingRequiredUnloading1", "NeutralUnloadingRequired1", "NeutralLoadingRequired1", "UnloadingReference1", "Quantity1", "ShipUnit1", "WeightPerShipUnit1", "TotalWeight1", "Length1", "Height1", "Stackable1", "Description1", "Palletexchange1", "ADR1", "ADRCode1", "ASignWasteRegistration1", "Temperature1", "MinTemp1", "MaxTemp1", "TrailerType1", "LoadUnloadingInfomration1", "LicenseplateRequired1", "Remark1"),
    # Add more data rows as needed
]

# Define the SQL query to insert data into the table
insert_query = """
INSERT INTO your_table_name (companyName, companyId, BookingNumber, AgreedTariff, InvoiceReference, ContactPerson, EmailAddress, PhoneNumber, NameLoading, StreetHousenumberLoading, CountryCodeLoading, PostalcodeLoading, CityLoading, RequestedLoadingDateFrom, RequestedLoadingTime, RequestedLoadingTimeUntil, RequestedLoadingDateUntil, SlotbookingRequiredLoading, LoadingReference, NameUnloading, StreetHousenumberUnloading, CountryCodeUnloading, PostalcodeUnloading, CityUnloading, RequestedUnloadingDateFrom, RequestedUnloadingTime, RequestedUnloadingDateUntil, RequestedUnloadingTimeUntil, SlotbookingRequiredUnloading, NeutralUnloadingRequired, NeutralLoadingRequired, UnloadingReference, Quantity, ShipUnit, WeightPerShipUnit, TotalWeight, Length, Height, Stackable, Description, Palletexchange, ADR, ADRCode, ASignWasteRegistration, Temperature, MinTemp, MaxTemp, TrailerType, LoadUnloadingInfomration, LicenseplateRequired, Remark)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Execute the SQL query to insert data
cursor.executemany(insert_query, data_to_insert)

# Commit the transaction
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
