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

# create orderbook of summed up orders from list
def createOrderBook(actions):
    orderBook: list[Order] = []

    # creates list of different Id's in orders
    idList = []
    for action in actions:
        if not action.orderId in idList:
            idList.append(action.orderId)

    for id in idList:

        orderWithSpecificId = next((item for item in orderBook if item.getId() == id), 0)

        # creates temporary list of orders with the same Id
        for action in actions:

            if action.orderId == id:
                if not orderWithSpecificId:
                    orderWithSpecificId = Order(action)
                    orderBook.append(orderWithSpecificId)
                else:
                    orderWithSpecificId.addAction(action)
    
    return orderBook
        
# finds best price and quantity of shares in this price        
def findBestPrice(orderBook, orderType):
    
    # creates temporary list of orders of the same type (buy / sell)
    tempList = []
    for element in orderBook:

        if element.getOrderType() == orderType:
            tempList.append(element)
    
    # if there is no order of this type returns False
    if len(tempList) == 0:
        return False
    
    bestPrice = {"price": tempList[0].getPrice(), "quantity": tempList[0].getQuantity()}
    
    # if there is only 1 order of this type - function returns it as best price
    if len(tempList) == 1:
        return bestPrice
    
    # looks for the best price and sums quantity of shares in this price
    if orderType == OrderType.BUY:
        for i in range(1, len(tempList)):
            if bestPrice["price"] == tempList[i].getPrice():
                bestPrice["quantity"] += tempList[i].getQuantity()
            elif bestPrice["price"] < tempList[i].getPrice():
                bestPrice["price"] = tempList[i].getPrice()
                bestPrice["quantity"] = tempList[i].getQuantity()
    else:
        for i in range(1, len(tempList)):
            if bestPrice["price"] == tempList[i].getPrice():
                bestPrice["quantity"] += tempList[i].getQuantity()
            elif bestPrice["price"] > tempList[i].getPrice():
                bestPrice["price"] = tempList[i].getPrice()
                bestPrice["quantity"] = tempList[i].getQuantity()
    
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
        print(listOfOrders[i])
        print()
        print("Actual orderbook:")
        for order in orderBook:
            print("Id: {}  Order: {}   Price: {}$  Quantity: {}".format(order.getId(), order.getOrderType(), order.getPrice(), order.getQuantity()))
        
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