class OrderManager:
    def __init__(self):
        print("Create OrderManager")

    def getLatestOrder(self):
        return {
            'user': 'Thijs',
            'name': 'Bacardi Cola',
            'price': 7,
            'drink': {
                "name": "Bacardi Cola",
                "ingredients": [
                    {
                        'name': 'Bacardi',
                        'type': 'liquor',
                        'amount': 2,
                        'position': 2
                    },
                    {
                        'name': 'Cola',
                        'type': 'soda',
                        'amount': 200,
                        'position': 0
                    }
                ]
            }
        }
