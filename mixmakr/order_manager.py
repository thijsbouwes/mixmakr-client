import requests
import os
from time import sleep

class OrderManager:
    url = ''
    headers = {}
    orders = []
    updates = []
    order = {}

    def __init__(self):
        self.setup()

    def setup(self):
        print("Create OrderManager")

        self.url = os.getenv("API_URL")
        self.headers = {
            'Authorization': 'Bearer ' + os.getenv("API_TOKEN"),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def run(self):
        while True:
            # process updates
            updates = self.updates
            self.updates = []

            for update in updates:
                self.updateOrder(update['message'], update['status'], update['order-id'])

            # fetch latest orders
            self.getOrders()

            sleep(1)

    def getOrders(self):
        r = requests.get(self.url + '/orders', headers=self.headers)

        if r.status_code == requests.codes.ok:
            self.orders = r.json()
            print("ORDERS: " + str(len(self.orders)))

    def queueUpdateOrder(self, message, status = False):
        if bool(self.order):
            self.updates.append({'message': message, 'status': status, 'order-id': self.order['id']})
        else:
            print("NO order, status: " + message)

    def updateOrder(self, message, status, order_id):
        data = {
            'message': message
        }

        if status != False:
            data['status'] = status

        r = requests.post(self.url + '/orders/' + str(order_id), headers=self.headers, json=data)

    def getLatestOrder(self):
        if self.order:
            self.order = {}

        if self.orders:
            self.order = self.orders.pop()

        return self.order
