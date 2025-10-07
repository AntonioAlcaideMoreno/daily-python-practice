def sum_nested_list(nested_list):
    """ This function takes a nested list of integers and returns the sum of all integers.
    For example, sum_nested([1, 2, [3, 4], 5]) should return 15."""
    """ This exercise consists of writing a recursive function (a function that calls itself) to solve such a problem."""
    total = 0   # Initialize total to 0
    for element in nested_list:  # We iterate over all elements in the list
        if isinstance(element, list): 
            total += sum_nested_list(element)  # If the element is a list, then we call again the function to subdivide the list in smaller parts
        else:
            total += element    # If the element is an integer, then we add it to the total, already stored from previous iterations
    return total

def main():
    # Main entry point - calls the function sum nested and prints result.
    print(sum_nested_list([1, 2, [3, 4], 5]))

if __name__ == "__main__":
    main()