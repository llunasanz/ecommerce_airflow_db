import requests
import json

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
def get_most_relevant_items_from_category(category: str):
    url = f"https://api.mercadolibre.com/sites/MLA/search?category={category}#json"
    response = requests.get(url).text
    response_json = json.loads(response)
    data = response_json["results"]

    # Create a list of new JSON objects with only the required fields
    new_json_list = [
        dict(map(lambda k: (k, get_value_from_item_key(item, k)), keys_to_extract.keys()))
        for item in data
    ]

    new_json_str = json.dumps(new_json_list, indent=4)

    print(new_json_str)

