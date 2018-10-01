"""
TO DO:
raise exception instead of returning integers!
no magic numbers! eg. max data length
crc8 -> crc16

"""


class SupDataLengthException(Exception):
	pass

class SupCRCError(Exception):
	pass

class SupStuffError(Exception):
	pass

class Sup:
	def __init__(self):
		pass


	def crc8(self, data_list):
		"""Calculate the CRC8 for a given data list.

		Parameters:
		self
		data_list: data to calculate the CRC8 [list of int(0-255)]

		Return value:
		int: CRC8 value 8bit unsigned (0-255)

		Exceptions:
		TypeError - parameter has the wrong type
		ValueError - parameter has the correct type but is out of range
		"""

		# CHECK INPUT
		if type(data_list) is not list:
			raise TypeError("data_list needs to be a list!")
		else:
			for i in data_list:
				if type(i) is not int:
					raise TypeError("List element needs to be an integer!")
				elif i<0 or i>255:
					raise ValueError("Integer needs to be between 0 and 255!")
					
		# ACTUAL FUNCTION
		crc = 0
		for in_byte in data_list:
			for i in range(8):
				temp = (crc ^ in_byte) & 0x80
				crc <<= 1
				if temp:
					crc ^= 0x07
				in_byte <<= 1

		crc &= 0xFF

		return crc


	def crc16(self, data_list):
		"""Calculate the CRC16 for a given data list.

		Parameters:
		self
		data_list: data to calculate the CRC16 [list of int(0-255)]

		Return value:
		int: CRC16 value 16bit unsigned

		Exceptions:
		TypeError - parameter has the wrong type
		ValueError - parameter has the correct type but is out of range
		"""

		# CHECK INPUT
		if type(data_list) is not list:
			raise TypeError("data_list needs to be a list!")
		else:
			for i in data_list:
				if type(i) is not int:
					raise TypeError("List element needs to be an integer!")
				elif i<0 or i>255:
					raise ValueError("Integer needs to be between 0 and 255!")
					
		# ACTUAL FUNCTION
		crc = 0xFFFF
		for in_byte in data_list:
			for i in range(8):
				temp = (crc ^ in_byte) & 0x0001
				crc >>= 1
				if temp:
					crc ^= 0x8408
				in_byte >>= 1

		crc &= 0xFFFF

		return crc


	def package(self, data_list):
		data_length = len(data_list)
		if not(0 < data_length < 257):
			raise SupDataLengthException("Data list length is not valid! (Length: {})".format(data_length))

		packet = [data_length-1]
		packet.extend(data_list)
		crc16 = self.crc16(packet)
		packet.append(crc16 & 0xFF)
		packet.append((crc16>>8) & 0xFF)

		return packet


	def unpackage(self, data_list):
		if self.crc16(data_list) != 0:
			raise SupCRCError("CRC incorrect!")

		if (data_list[0]+4) != len(data_list):
			raise SupDataLengthException("Packet length does not match the length byte in the packet! (Packet: {}  Length byte: {})".format(len(data_length-2),data_list[0]+1))

		return data_list[1:-2]


	def stuff(self, data_list):
		data_str = "".join(["{:08b}".format(x & 0xFF) for x in data_list])

		bitCounter = 0
		consecutiveOnes = 0
		stuffCount = 0

		while bitCounter < len(data_str):
			if data_str[bitCounter] == "1":
				consecutiveOnes += 1

				if consecutiveOnes == 5:
					consecutiveOnes = 0
					bitCounter += 1
					data_str = data_str[:bitCounter] + "0" + data_str[bitCounter:]
					
			else:
				consecutiveOnes = 0

			bitCounter += 1

		temp = bitCounter % 8
		if temp:
			data_str = data_str + "0"*(8-temp)
			bitCounter += (8-temp)

		stuffed_list = []
		for i in range(0,bitCounter,8):
			stuffed_list.append(int(data_str[i:i+8],2))

		stuffed_list.insert(0,0x7E)
		stuffed_list.append(0x7E)
		
		return stuffed_list


	def unstuff(self, data_list):
		if not data_list:
			raise SupDataLengthException("Data list does not contain any data (empty after removing flag bytes)!")

		if data_list[0] == 0x7E:
			data_list.pop(0)

			if not data_list:
				raise SupDataLengthException("Data list does not contain any data (empty after removing flag bytes)!")

		if data_list[-1] == 0x7E:
			data_list.pop()

			if not data_list:
				raise SupDataLengthException("Data list does not contain any data (empty after removing flag bytes)!")

		data_str = "".join(["{:08b}".format(x & 0xFF) for x in data_list])

		bitCounter = 0
		consecutiveOnes = 0
		stuffCount = 0

		while bitCounter < len(data_str):
			if data_str[bitCounter] == "1":
				consecutiveOnes += 1

				if consecutiveOnes == 5:
					consecutiveOnes = 0

					if data_str[bitCounter+1] == "1":
						raise SupStuffError("More than five consecutive ones in the data!")

					data_str = data_str[:bitCounter+1] + data_str[bitCounter+2:]
					stuffCount += 1
			else:
				consecutiveOnes = 0

			bitCounter += 1

		data_length = (bitCounter//8)*8 # get amount of data 

		unstuffed_list = []
		for i in range(0,data_length,8):
			unstuffed_list.append(int(data_str[i:i+8],2))

		return unstuffed_list


	def send(self, data_list):
		packet_list = self.package(data_list)
		stuffed_list = self.stuff(packet_list)

		return stuffed_list


	def receive(self, data_list):
		unstuffed_list = self.unstuff(data_list)
		package_list = self.unpackage(unstuffed_list)

		return package_list


	def print_list_hex_byte(self, data_list):
		print("[",end="")
		print(", ".join(["0x{:02X}".format(x & 0xFF) for x in data_list]),end="")
		print("]")