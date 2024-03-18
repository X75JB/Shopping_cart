# Jackson Blackman
# 251344173
# Jblackm8
# 2023-12-08
# This file will create a purchasing system simular to that of online web-stores

class Product:
    def __init__(self, name, price, category):
        # Initialize product attributes
        self._name = name
        self._price = price
        self._category = category

    # Define how products are classified
    def __eq__(self, other):
        if isinstance(other, Product):
            if (self._name == other._name and self._price == other._price) and (self._category == other._category):
                return True
            else:
                return False
        else:
            return False

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_category(self):
        return self._category

    # Implement string representation
    def __repr__(self):
        rep = 'Product(' + self._name + ',' + str(self._price) + ',' + self._category + ')'
        return rep


class Inventory:
    # Create an empty dict to store product info
    def __init__(self):
        self.inventory_data = {}

    # Used to add a new product to the inventory
    def add_to_productInventory(self, productName, productPrice, productQuantity):
        self.inventory_data[productName] = {'price': productPrice, 'quantity': productQuantity}

    # Used to add a specified quantity to a product located in the inventory
    def add_productQuantity(self, nameProduct, addQuantity):
        self.inventory_data[nameProduct]['quantity'] += addQuantity

    # Used to remove a specified quantity from a product located within the inventory
    def remove_productQuantity(self, nameProduct, removeQuantity):
        self.inventory_data[nameProduct]['quantity'] -= removeQuantity

    # Used to get the price of a product
    def get_productPrice(self, nameProduct):
        return self.inventory_data[nameProduct]['price']

    # Used to get the quantity of a product
    def get_productQuantity(self, nameProduct):
        return self.inventory_data[nameProduct]['quantity']

    # Used to display the inventory
    def display_Inventory(self):
        for product, details in self.inventory_data.items():
            print(f"{product}, {details['price']}, {details['quantity']}")


class ShoppingCart:
    # Creates a shopping cart with buyer name and inventory
    def __init__(self, buyerName, inventory):
        self.buyer_name = buyerName
        # Dict to store given items in the cart
        self.cart_data = {}
        self.inventory = inventory

    # Used to add items to the cart while updating the inventory respectively
    def add_to_cart(self, nameProduct, requestedQuantity):
        # Product is within the cart, update the quantity
        if nameProduct in self.cart_data:
            self.cart_data[nameProduct] += requestedQuantity
        # If product is not in cart, add it to the cart
        else:
            self.cart_data[nameProduct] = requestedQuantity

        # Used to check if the inventory has enough quantity to fill the cart
        if self.inventory.get_productQuantity(nameProduct) < requestedQuantity:
            return "Can not fill the order"
        # Updating the inventory quantity
        else:
            self.inventory.remove_productQuantity(nameProduct, requestedQuantity)
            return "Filled the order"

    # Used to remove a product from the cart and update the inventory
    def remove_from_cart(self, nameProduct, requestedQuantity):
        # If product is already in the users cart, update the quantity
        if nameProduct not in self.cart_data:
            return "Product not in the cart"

        if self.cart_data[nameProduct] < requestedQuantity:
            return "The requested quantity to be removed from cart exceeds what is in the cart"

        # Update the cart quantity
        self.cart_data[nameProduct] -= requestedQuantity

        # Update the inventory quantity
        self.inventory.add_productQuantity(nameProduct, requestedQuantity)

        return "Successful"

    # Used to display the contents of the shopping cart, total, and buyers name
    def view_cart(self):
        total_price = 0
        for product, quantity in self.cart_data.items():
            price = self.inventory.get_productPrice(product)
            total_price += price * quantity
            print(f"{product} {quantity}")
        print(f"Total: {total_price}")
        print(f"Buyer Name: {self.buyer_name}")


class ProductCatalog:
    # Create a product catalog
    def __init__(self):
        self.catalog_data = []
        self.low_prices = set()
        self.medium_prices = set()
        self.high_prices = set()

    # Adds a new product to the catalog
    def addProduct(self, product):
        self.catalog_data.append(product)

    # Places products within price categories then displays the information
    def price_category(self):
        for product in self.catalog_data:
            price = product.get_price()

            if 0 <= price <= 99:
                self.low_prices.add(product.get_name())
            elif 100 <= price <= 499:
                self.medium_prices.add(product.get_name())
            elif price >= 500:
                self.high_prices.add(product.get_name())

        print(f"Number of low price items: {len(self.low_prices)}")
        print(f"Number of medium price items: {len(self.medium_prices)}")
        print(f"Number of high price items: {len(self.high_prices)}")

    # Displays the catalog
    def display_catalog(self):
        for product in self.catalog_data:
            print(f"Product: {product.get_name()} Price: {product.get_price()} Category: {product.get_category()}")


def populate_inventory(filename):
    try:
        # Attempt to read file
        with open(filename, 'r') as file:
            # Instantiate the inventory object
            inventory = Inventory()

            # Iterate over the lines in the file
            for line in file:
                fields = line.strip().split(',')

                # Extract the data
                productName, productPrice, productQuantity, productCategory = fields

                # Convert the price and quantity to their respective integers
                productPrice = int(productPrice)
                productQuantity = int(productQuantity)

                # Add product to the inventory
                inventory.add_to_productInventory(productName, productPrice, productQuantity)

            # Return the populated Inventory object
            return inventory

    except FileNotFoundError:
        print(f"Could not read file: {filename}")
        return None


def populate_catalog(filename):
    try:
        # Attempt to read file
        with open(filename, 'r') as file:
            # Instantiate the catalog object
            product_catalog = ProductCatalog()

            for line in file:
                fields = line.strip().split(',')

                # Extract the data
                productName, productPrice, _, productCategory = fields

                # Convert price to integer
                productPrice = int(productPrice)

                # Instantiate a product object
                product = Product(productName, productPrice, productCategory)

                # Add the product to the catalog
                product_catalog.addProduct(product)

            # Return the now populated catalog
            return product_catalog

    except FileNotFoundError:
        print(f"Could not read file: {filename}")
        return None
