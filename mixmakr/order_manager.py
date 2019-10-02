import requests
import os

class OrderManager:
    url = ''
    headers = {}
    orders = []
    order = {}

    def setup(self):
        print("Create OrderManager")

        self.url = os.getenv("API_URL")
        self.headers = {
            'Authorization': 'Bearer ' + os.getenv("API_TOKEN"),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        self.getOrders()

    def getOrders(self):
        r = requests.get(self.url + '/orders', headers=self.headers)

        if r.status_code == requests.codes.ok:
            self.orders = r.json()

    def updateOrder(self, message, status = False):
        if bool(self.order) == False:
            return

        data = {
            'message': message
        }

        if status != False:
            data['status'] = status

        r = requests.post(self.url + '/orders/' + str(self.order['id']), headers=self.headers, json=data)

    def getLatestOrder(self):
        self.order = {}

        if self.orders:
            self.order = self.orders.pop()

        return self.order
