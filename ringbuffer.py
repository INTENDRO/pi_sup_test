"""
TO DO:

"""

class RingbufferFullException(Exception):
	pass

class RingbufferEmptyException(Exception):
	pass

class RingbufferTypeException(Exception):
	pass

class Ringbuffer:
	def __init__(self, maxlen=0, fixed_type = None):
		self.__maxlen = maxlen
		self.__buffer = []
		self.__fixed_type = fixed_type
		# self.count = 0


	@property
	def count(self):
		# return self.count
		return len(self.__buffer)


	@property
	def is_full(self):
		# only check if buffer is full if a maximum length has been set
		if self.__maxlen:
			# return self.count == self.maxlen
			return (len(self.__buffer) == self.__maxlen)
		else:
			return False


	@property
	def is_empty(self):
		# return self.count == 0
		return (len(self.__buffer) == 0)


	def append(self, item):
		if self.is_full:
			raise RingbufferFullException("Cannot append an item to a full ringbuffer!")

		if self.__fixed_type:
			if type(item) != self.__fixed_type:
				raise RingbufferTypeException("Cannot append an item of type {}!".format(type(item)))

		self.__buffer.append(item)


	def extend(self, seq):
		if self.__maxlen:
			if (self.__maxlen - len(self.__buffer)) < len(seq):
				raise RingbufferFullException("Cannot append the sequence. The buffer does not have enough memory left!")

		if self.__fixed_type:
			if not all(isinstance(x,self.__fixed_type) for x in seq):
				raise RingbufferTypeException("Cannot append the sequence because at least one type does not match!")

		self.__buffer.extend(seq)


	def remove(self):
		if self.is_empty:
			raise RingbufferEmptyException("Cannot remove item from an empty ringbuffer!")

		return self.__buffer.pop(0)


	def peak(self):
		return self.__buffer[:]


	def count_item(self, item):
		return self.__buffer.count(item)


	def remove_until_item(self, item):
		try:
			idx = self.__buffer.index(item)
			ret_list = self.__buffer[:idx+1]
			self.__buffer = self.__buffer[idx+1:]
			return ret_list
		except ValueError:
			return []

	def clear(self):
		self.__buffer = []