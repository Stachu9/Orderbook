from enum import Enum


# list of all given orders
givenOrders = [
    {"Id": 1, "Order": "Buy", "Type": "Add", "Price": 20.0, "Quantity": 100},
    {"Id": 2, "Order": "Sell", "Type": "Add", "Price": 25.0, "Quantity": 200},
    {"Id": 3, "Order": "Buy", "Type": "Add", "Price": 23.0, "Quantity": 50},
    {"Id": 4, "Order": "Buy", "Type": "Add", "Price": 23.0, "Quantity": 70},
    {"Id": 3, "Order": "Buy", "Type": "Remove", "Price": 23.0, "Quantity": 50},
    {"Id": 5, "Order": "Sell", "Type": "Add", "Price": 28.0, "Quantity": 100}
    ]

class OrderType(Enum):
    BUY = 0
    SELL = 1

class ActionType(Enum):
    ADD = 0
    REMOVE = 1

class Action(object):

    orderId: int
    orderType: OrderType
    actionType: ActionType
    price: float
    quantity: int

    def __init__(self, orderId, orderType, actionType, price, quantity):
        self.orderId = orderId
        self.orderType = orderType
        self.actionType = actionType
        self.price = price
        self.quantity = quantity

    def __str__(self):

        orderType = "Buy" if self.orderType == OrderType.BUY else "Sell"
        actionType = "Add" if self.actionType == ActionType.ADD else "Remove"

        return "Id: {}  Order: {}  Type: {}  Price: {}$  Quantity: {}".format(self.orderId, orderType, actionType, self.price, self.quantity)
    
    @staticmethod
    def createActionObject(action):
        orderType = OrderType.BUY if action["Order"] == "Buy" else OrderType.SELL
        actionType = ActionType.ADD if action["Type"] == "Add" else ActionType.REMOVE

        return Action(action["Id"], orderType, actionType, action["Price"], action["Quantity"])

class Order(object):

    def __init__(self, action):
        self.actions: list[Action] = []
        self.actions.append(action)

    def __str__(self):
        orderType = "Buy" if self.getOrderType() == OrderType.BUY else "Sell"
        return "Id: {}  Order type: {}  Price: {}$  Quantity: {}".format(self.getId(), orderType, self.getPrice(), self.getQuantity())

    def getId(self):
        return self.actions[0].orderId

    def getOrderType(self):
        return self.actions[0].orderType
    
    def getPrice(self):
        return self.actions[0].price
    
    def getQuantity(self):
        quantity = 0
        for action in self.actions:
            if action.actionType == ActionType.ADD:
                quantity += action.quantity
            else:
                quantity -= action.quantity
        
        return quantity
    
    def addAction(self, action):
        if not ((self.actions[0].orderId == action.orderId) and (self.actions[0].orderType == action.orderType) and (self.actions[0].price == action.price)):
            raise ValueError("Action id doesn't match")
        elif not (self.actions[0].orderType == action.orderType):
            raise ValueError("Action order type doesn't match")
        elif not (self.actions[0].price == action.price):
            raise ValueError("Action price doesn't match")
        self.actions.append(action)

class OrderBook(object):
    
    def __init__(self):
        self.orders = {}

    def addAction(self, action):

        if action.orderId in self.orders:
            self.orders[action.orderId].addAction(action)       
        else:
            self.orders[action.orderId] = Order(action)

    def findBestOfferToBuy(self):

        bestOfferToBuy = {}

        for order in self.orders.values():
            if order.getOrderType() == OrderType.SELL:
                if bestOfferToBuy:
                    if bestOfferToBuy["price"] == order.getPrice():
                        bestOfferToBuy["quantity"] += order.getQuantity()
                    elif bestOfferToBuy["price"] > order.getPrice():
                        bestOfferToBuy["price"] = order.getPrice()
                        bestOfferToBuy["quantity"] = order.getQuantity()
                else:
                    bestOfferToBuy["price"] = order.getPrice()
                    bestOfferToBuy["quantity"] = order.getQuantity()
        
        return bestOfferToBuy
    
    def findBestOfferToSell(self):

        bestOfferToSell = {}

        for order in self.orders.values():
            if order.getOrderType() == OrderType.BUY:
                if bestOfferToSell:
                    if bestOfferToSell["price"] == order.getPrice():
                        bestOfferToSell["quantity"] += order.getQuantity()
                    elif bestOfferToSell["price"] < order.getPrice():
                        bestOfferToSell["price"] = order.getPrice()
                        bestOfferToSell["quantity"] = order.getQuantity()
                else:
                    bestOfferToSell["price"] = order.getPrice()
                    bestOfferToSell["quantity"] = order.getQuantity()
        
        return bestOfferToSell

def main():
    
    orderBook = OrderBook()

    # list of active, proceeded orders
    listOfOrders = []
    
    print("No active orders.")
    
    for i in range(len(givenOrders)):
        print()
        # input used only to stop program and ask for user reaction
        input("To add order to the list press enter.")
        print()
        print()
        print("---------------------------------")
        
        # if there is another order in given list - adds to list of orders - else quits program

        action = Action.createActionObject(givenOrders[i])
        orderBook.addAction(action)
        
        bestSharesToBuy = orderBook.findBestOfferToBuy()
        bestSharesToSell = orderBook.findBestOfferToSell()
        
        print("Order added in this step from the given list:")
        print(action)
        print()
        print("Actual orderbook:")
        for order in orderBook.orders.values():
            print(order)
        
        print()
        # checks if there is any best buy or sell oportunity and prints it.
        if bestSharesToBuy:
            print("The best you can buy is " + str(bestSharesToBuy["quantity"]) + " shares at price " + str(bestSharesToBuy["price"]) + "$")
        else:
            print("The best you can buy is - no SELL offers in orderbook")        
        
        if bestSharesToSell:
            print("The best you can sell is " + str(bestSharesToSell["quantity"]) + " shares at price " + str(bestSharesToSell["price"]) + "$")
        else:
            print("The best you can sell is - no BUY offers in orderbook")
        
    print("No more given orders.")

main()