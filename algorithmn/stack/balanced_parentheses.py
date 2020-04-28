class Stack(object):
	def _init_(self, limit = 10):
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


def balanced_parentheses(parentheses):
	if len(parentheses) % 2 != 0:
		return False

	stack = Stack(len(parentheses))

	for parenthesis in parentheses:
		if parenthesis == '(':
			stack.push(parenthesis)
		else:
			if parenthesis == ')':
				if !

