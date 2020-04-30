class Stack(object):
	def __init__(self, limit = 10):
		self.stack = []
		self.limit = limit

	def push(self, data):
		if len(self.stack) >= self.limit:
			raise IndexError("Index Overhead")
		self.stack.append(data)

	def pop(self):
		if self.stack:
			return self.stack.pop()
		else:
			raise IndexError("Stack has been empty")

	def is_empty(self):
		return not bool(self.stack)

def balanced_parentheses(parentheses):
	print(len(parentheses))
	if len(parentheses) % 2 != 0:
		return False
	# odd number must be not balanced
	stack = Stack(len(parentheses))

	for item in parentheses:
		if item == '(':
			stack.push('(')
		else:
			if stack.is_empty():
				return False
			else:
				stack.pop()

	return True
if __name__ == '__main__':
	examples = ['(((())))', '(((()))', '((())))']

	for exam in examples:
		print("exmales is balanced_parentheses?: ", balanced_parentheses(exam))
