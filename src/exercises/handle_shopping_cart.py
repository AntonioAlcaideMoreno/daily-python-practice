def handle_shopping_cart(orders):
    # Create an empty dictionary for the shopping cart
    shopping_cart={}
    # Process each order in the list
    for order in orders:
        try:
            # Divide the order into item and quantity and add to shopping cart
            item,quantity=order.split(":")
            quantity=int(quantity)
            if quantity<0:
                print(f"Negative quantity not allowed: {order}")
                continue
            if item in shopping_cart.keys():
                shopping_cart[item]+=quantity
            else:
                shopping_cart[item]=quantity
        # Manage specific errors
        except ValueError:
            # Manage value errors
            if ":" not in order:
                print(f"Invalid format: {order}")
            elif not isinstance(quantity,int):
                print(f"Invalid quantity: {order}")
        except Exception as e:
            # Manage unexpected errors
                print("Unexpected error ocurred!")
    # Return completed shopping cart
    return shopping_cart