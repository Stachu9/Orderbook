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
    action: ActionType
    price: float
    quantity: int

    def __init__(self, orderId, orderType, action, price, quantity):
        self.orderId = orderId
        self.orderType = orderType
        self.action = action
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return {
            "Id": self.orderId,
            "Order": self.orderType,
            "Type": self.action,
            "Price": self.price,
            "Quantity": self.quantity
        }
    
    def printAction(self):
        orderType = "Buy" if self.orderType == OrderType.BUY else "Sell"
        actionType = "Add" if self.action == ActionType.ADD else "Remove"

        return "Id: {}  Order: {}  Type: {}  Price: {}$  Quantity: {}".format(self.orderId, orderType, actionType, self.price, self.quantity)
    
    def printOrder(self):
        orderType = "Buy" if self.orderType == OrderType.BUY else "Sell"
        actionType = "Add" if self.action == ActionType.ADD else "Remove"

        return "Id: {}  Order: {}   Price: {}$  Quantity: {}".format(self.orderId, orderType, self.price, self.quantity)
    
    @staticmethod
    def createActionObject(action):
        orderType = OrderType.BUY if action["Order"] == "Buy" else OrderType.SELL
        actionType = ActionType.ADD if action["Type"] == "Add" else ActionType.REMOVE

        return Action(action["Id"], orderType, actionType, action["Price"], action["Quantity"])

# create orderbook of summed up orders from list
def createOrderBook(orders):
    orderBook = []

    # creates list of different Id's in orders
    IdList = []
    for element in orders:
        if not element.orderId in IdList:
            IdList.append(element.orderId)

    for Id in IdList:

        orderWithSpecificId = next((item for item in orderBook if item["id"] == Id), 0)

        # creates temporary list of orders with the same Id
        for element in orders:

            if element.orderId == Id:
                if not orderWithSpecificId:
                    orderWithSpecificId = {"id": element.orderId, "order": element.orderType, "price": element.price, "quantity": element.quantity}
                    orderBook.append(orderWithSpecificId)
                else:
                    if element.action == ActionType.ADD:
                        orderWithSpecificId["quantity"] += element.quantity
                    else:
                        orderWithSpecificId["quantity"] -= element.quantity

                        if orderWithSpecificId["quantity"] == 0:
                            orderBook.remove(orderWithSpecificId)
        
    return orderBook
        
# finds best price and quantity of shares in this price        
def findBestPrice(orderBook, orderType):
    
    # creates temporary list of orders of the same type (buy / sell)
    tempList = []
    for element in orderBook:
        if element["order"] == orderType:
            tempList.append(element)
    
    # if there is no order of this type returns False
    if len(tempList) == 0:
        return False
    
    bestPrice = {"price": tempList[0]["price"], "quantity": tempList[0]["quantity"]}
    
    # if there is only 1 order of this type - function returns it as best price
    if len(tempList) == 1:
        return bestPrice
    
    # looks for the best price and sums quantity of shares in this price
    if orderType == OrderType.BUY:
        for i in range(1, len(tempList)):
            if bestPrice["price"] == tempList[i]["price"]:
                bestPrice["quantity"] += tempList[i]["quantity"]
            elif bestPrice["price"] < tempList[i]["price"]:
                bestPrice["price"] = tempList[i]["price"]
                bestPrice["quantity"] = tempList[i]["quantity"]
    else:
        for i in range(1, len(tempList)):
            if bestPrice["price"] == tempList[i]["price"]:
                bestPrice["quantity"] += tempList[i]["quantity"]
            elif bestPrice["price"] > tempList[i]["price"]:
                bestPrice["price"] = tempList[i]["price"]
                bestPrice["quantity"] = tempList[i]["quantity"]
    
    return bestPrice


def main():
    
    # list of active, proceeded orders
    listOfOrders = []
    
    print("No active orders.")
    i = 0
    
    for i in range(len(givenOrders)):
        print()
        # input used only to stop program and ask for user reaction
        input("To add order to the list press enter.")
        print()
        print()
        print("---------------------------------")
        
        # if there is another order in given list - adds to list of orders - else quits program
        listOfOrders.append(Action.createActionObject(givenOrders[i]))
        
        orderBook = createOrderBook(listOfOrders)
        bestSharesToBuy = findBestPrice(orderBook, OrderType.SELL)
        bestSharesToSell = findBestPrice(orderBook, OrderType.BUY)
        
        print("Order added in this step from the given list:")
        print(listOfOrders[i].printAction())
        print()
        print("Actual orderbook:")
        for element in orderBook:
            print("Id: {}  Order: {}   Price: {}$  Quantity: {}".format(element["id"], element["order"], element["price"], element["quantity"]))
        
        print()
        # checks if there is any best buy or sell oportunity and prints it.
        if bestSharesToBuy:
            print("The best you can buy is " + str(bestSharesToBuy["quantity"]) + " shares at price " + str(bestSharesToBuy["price"]) + "$")
        else:
            print("The best you can buy is - no SELL offers in orderbook")        
        
        if bestSharesToSell:
            print("The best you can sell is " + str(bestSharesToSell["quantity"]) + " shares at price " + str(bestSharesToSell["price"]) + "$")
        else:
            print("The best you can buy is - no SELL offers in orderbook")
        
        i += 1
    print("No more given orders.")

main()