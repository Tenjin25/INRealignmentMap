import csv

input_file = 'data/AllOfficeResults.csv'
output_file = 'data/AllOfficeResults_clean.csv'

# Read CSV normally and write without quotes
with open(input_file, 'r', encoding='utf-8') as infile:
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        
        for row in reader:
            writer.writerow(row)

print(f"Created {output_file} with minimal quotation marks")
