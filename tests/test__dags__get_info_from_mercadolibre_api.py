import unittest
from unittest.mock import patch, Mock
import json
import sys
import os

# Add the `dags` directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dags')))

import get_info_from_mercadolibre_api

class TestMercadolibreAPI(unittest.TestCase):

    def test_get_value_from_item_key(self):
        item = {'id': '12345', 'title': 'Sample Item', 'price': 100.0}
        
        # Test existing keys
        self.assertEqual(get_info_from_mercadolibre_api.get_value_from_item_key(item, 'id'), '12345')
        self.assertEqual(get_info_from_mercadolibre_api.get_value_from_item_key(item, 'title'), 'Sample Item')
        self.assertEqual(get_info_from_mercadolibre_api.get_value_from_item_key(item, 'price'), 100.0)
        
        # Test non-existing key
        self.assertIsNone(get_info_from_mercadolibre_api.get_value_from_item_key(item, 'sold_quantity'))

    @patch('get_info_from_mercadolibre_api.requests.get')
    def test_get_most_relevant_items_from_category(self, mock_get):
        mock_response = Mock()
        expected_response = {
            "results": [
                {
                    "id": "MLA123456",
                    "title": "Item 1",
                    "price": 1000,
                    "sold_quantity": 10,
                    "thumbnail": "http://example.com/image1.jpg"
                },
                {
                    "id": "MLA654321",
                    "title": "Item 2",
                    "price": 2000,
                    "sold_quantity": 5,
                    "thumbnail": "http://example.com/image2.jpg"
                }
            ]
        }
        mock_response.text = json.dumps(expected_response)
        mock_get.return_value = mock_response

        # Expected new JSON structure
        expected_new_json = [
            {
                "id": "MLA123456",
                "title": "Item 1",
                "price": 1000,
                "sold_quantity": 10,
                "thumbnail": "http://example.com/image1.jpg"
            },
            {
                "id": "MLA654321",
                "title": "Item 2",
                "price": 2000,
                "sold_quantity": 5,
                "thumbnail": "http://example.com/image2.jpg"
            }
        ]

        with patch('builtins.print') as mock_print:
            get_info_from_mercadolibre_api.get_most_relevant_items_from_category('MLA1577')
            mock_print.assert_called_once()
            args, _ = mock_print.call_args
            result = json.loads(args[0])
            self.assertEqual(result, expected_new_json)

if __name__ == '__main__':
    unittest.main()
