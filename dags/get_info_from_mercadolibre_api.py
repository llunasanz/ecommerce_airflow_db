# dags/fetch_data.py
from datetime import datetime
import requests
import json
import csv
import argparse

# Keys to extract and their default values
keys_to_extract = {
    'id': None,
    'title': None,
    'price': 0,
    'sold_quantity': 0, 
    'thumbnail': None
}

def get_value_from_item_key(item, key):
    return item.get(key, None)

# Category format: MLA0123 (string)
def get_most_relevant_items_from_category(category: str, output_file_path = '/opt/airflow/output.tsv'):
    url = f"https://api.mercadolibre.com/sites/MLA/search?category={category}#json"
    response = requests.get(url).text
    response_json = json.loads(response)
    data = response_json["results"]

    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create a list of new JSON objects with only the required fields
    new_json_list = [
        {**dict(map(lambda k: (k, get_value_from_item_key(item, k)), keys_to_extract.keys())), 'created_date': current_datetime}
        for item in data
    ]

    new_json_str = json.dumps(new_json_list, indent=4)

    fieldnames = list(keys_to_extract.keys()) + ['created_date']

    with open(output_file_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter='\t')
        dict_writer.writeheader()
        dict_writer.writerows(new_json_list)

    print(new_json_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch most relevant items from MercadoLibre category.')
    parser.add_argument('--category', type=str, default='MLA1577', help='Category ID to fetch items from')
    parser.add_argument('--output_file', type=str, default='/opt/airflow/output.tsv', help='Output file path for TSV')

    args = parser.parse_args()

    get_most_relevant_items_from_category(args.category, args.output_file)
