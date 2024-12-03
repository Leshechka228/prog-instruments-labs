import csv
import re
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