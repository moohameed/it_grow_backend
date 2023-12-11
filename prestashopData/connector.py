import requests
import xml.etree.ElementTree as ET

class PrestaShopManager:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def get_orders(self):
        response = requests.get(self.api_url + "/orders", auth=(self.api_key, ''))
        response.raise_for_status()  # Cela lèvera une exception si la requête échoue.
        root = ET.fromstring(response.content)  # Parse XML content
        
        orders = []
        for order in root.findall('.//order'):  # Find all order elements
            orders.append(order.attrib)  # Add each order's attributes to the list
        
        return orders
