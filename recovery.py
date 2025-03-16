import os
import csv

# Ask the user for a directory
directory = input("Please paste the directory path: ")
directory = os.path.normpath(directory)

# Construct the path to rename.csv
csv_path = os.path.join(directory, 'rename.csv')

# Check if rename.csv exists
if not os.path.isfile(csv_path):
	print(f"rename.csv not found in {directory}")
else:
	# Open rename.csv and process each row
	with open(csv_path, mode='r', newline='') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			if len(row) != 2:
				print(f"Skipping invalid row: {row}")
				continue
			new_name, old_name = row
			old_path = os.path.join(directory, old_name)
			new_path = os.path.join(directory, new_name)
			if os.path.isfile(old_path):
				os.rename(old_path, new_path)
				print(f"Renamed {old_name} to {new_name}")
			else:
				print(f"File {old_name} not found in {directory}")