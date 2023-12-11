import requests
import json

class WooCommerceManager:

    def __init__(self, api_url, consumer_key, consumer_secret):
        self.api_url = api_url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def get_orders(self):
        response = requests.get(
            f"{self.api_url}/wp-json/wc/v3/orders",
            auth=(self.consumer_key, self.consumer_secret)
        )
        return json.loads(response.text)
