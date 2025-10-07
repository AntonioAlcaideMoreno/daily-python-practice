# Fibonacci sequence calculator
def fibonacci(n):
	"""Calculate the nth Fibonacci number.

	Args:
		n: The position in the Fibonacci sequence (1-indexed)
		
	Returns:
		The Fibonacci number at position n
		
	Raises:
		ValueError: If n is negative
		ValueError: If n is not an integer
	"""
	if type(n) != int:
		raise ValueError("Value should be an integer value > 0")
	elif n < 0:
		raise ValueError("Value should be > 0")
	elif n <= 2:
		return n - 1
	else:
		return fibonacci(n - 1) + fibonacci(n - 2)

def main():
	# Main entry point - calls the function fibonacci and prints result.
	print("Fibonacci sequence:")
	for i in range(1, 11):
		print(f"Fibonacci({i}) = {fibonacci(i)}")  

if __name__ == "__main__":
	main()