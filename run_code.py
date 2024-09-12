import zipfile
import os
import re
import csv
from xml.etree import ElementTree as ET

# Path to the zipped KMZ file
zip_file_path = 'Power_Capacity_34.5kV.kmz.zip'

# Path to extract the contents of the zip file
kmz_extracted_dir = 'kmz_extracted/'

# Directory to extract the KMZ contents
kmz_file_name = 'Power_Capacity_34.5kV.kmz'
kmz_file_path = os.path.join(kmz_extracted_dir, kmz_file_name)
extract_dir = 'extracted_kmz/'

# Step 1: Unzip the .zip file to extract the KMZ file
print("Extracting the .kmz file from the .zip archive...")

# Create the extraction directory for KMZ if it doesn't exist
os.makedirs(kmz_extracted_dir, exist_ok=True)

# Extract the KMZ from the zip archive
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(kmz_extracted_dir)

# Check if the KMZ file exists after extraction
if os.path.exists(kmz_file_path):
    print(f"KMZ file extracted to {kmz_file_path}")
    
    # Step 2: Unzip the KMZ file
    print("Extracting the contents of the KMZ file...")
    
    # Create the extraction directory for KMZ contents if it doesn't exist
    os.makedirs(extract_dir, exist_ok=True)

    # Unzip the KMZ file
    with zipfile.ZipFile(kmz_file_path, 'r') as kmz:
        kmz.extractall(extract_dir)

    # Step 3: Find the KML file in the extracted contents
    kml_file_path = None
    for file in os.listdir(extract_dir):
        if file.endswith('.kml'):
            kml_file_path = os.path.join(extract_dir, file)
            break

    # Step 4: Read and Parse the KML file
    if kml_file_path:
        print(f"KML file found at: {kml_file_path}")
        
        # Parse the KML file
        tree = ET.parse(kml_file_path)
        root = tree.getroot()

        # Namespace for KML
        namespace = '{http://www.opengis.net/kml/2.2}'

        # Define the path for the output CSV file
        csv_file_path = 'power_capacity_data.csv'

        # Open CSV file for writing
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write the CSV header
            csvwriter.writerow(['Name', 'GIS ID', 'OH_UG', 'Capacity_Range_KW', 'Capacity_Status', 'Voltage_Class', 'Coordinates'])

            # Iterate through each Placemark in the KML file
            for placemark in root.findall(f'.//{namespace}Placemark'):
                name = placemark.find(f'{namespace}name').text
                
                # Extract data from the HTML-like description field using regular expressions
                description = placemark.find(f'{namespace}description').text
                gis_id = re.search(r'<td>GIS ID</td>\s*<td>(.*?)</td>', description).group(1)
                oh_ug = re.search(r'<td>OH_UG</td>\s*<td>(.*?)</td>', description).group(1)
                capacity_range_kw = re.search(r'<td>Capacity_Range_KW</td>\s*<td>(.*?)</td>', description).group(1)
                capacity_status = re.search(r'<td>Capacity_Status</td>\s*<td>(.*?)</td>', description).group(1)
                voltage_class = re.search(r'<td>Voltage_Class</td>\s*<td>(.*?)</td>', description).group(1)
                
                # Extract coordinates
                coordinates = placemark.find(f'.//{namespace}coordinates').text.strip()

                # Write the row to the CSV file
                csvwriter.writerow([name, gis_id, oh_ug, capacity_range_kw, capacity_status, voltage_class, coordinates])

        print(f"Data has been written to {csv_file_path}")
    else:
        print("KML file not found in the extracted contents.")
else:
    print("KMZ file was not found after extracting the .zip archive.")
