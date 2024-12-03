import csv
import re
import json
import chardet
from checksum import calculate_checksum


validation_patterns = [
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',  # email
    r'^\d+(\.\d{1,2})?$',                                # height
    r'^\d{10,15}$',                                     # inn
    r'^\d{2} \d{2} \d{6}$',                             # passport
    r'^[А-Яа-яЁё\s]+$',                                 # occupation
    r'^[+-]?([1-9]\d*(\.\d+)?|0(\.\d+)?|\.\d+)$',       # latitude
    r'^#[0-9A-Fa-f]{6}$',                              # hex_color
    r'^\d{4}-\d{4}$',                                   # issn
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$',  # uuid
    r'^\d{2}:\d{2}:\d{2}\.\d{6}$'                      # time
]


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10001)) 
    return result['encoding']


def is_valid_row(row):
    return all(re.match(pattern, field) for pattern, field in zip(validation_patterns, row))


def process_csv(file_path):
    invalid_rows = []
    encoding = detect_encoding(file_path)

    with open(file_path, mode='r', encoding=encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)
        for row_number, row in enumerate(csv_reader, start=2):
            if not is_valid_row(row):
                invalid_rows.append(row_number)

    return invalid_rows
