"""
TO DO:
raise exception instead of returning integers!

"""


class Sup:
	def __init__(self):
		pass


	def crc8(self, data_list):
		"""Calculate the CRC8 byte for a MAC address.

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


	def package(self, data_type, data_list):
		packet = [((data_type&0x03)<<6) | (len(data_list)&0x3F)]
		packet.extend(data_list)
		packet.append(self.crc8(packet))

		return packet


	def unpackage(self, data_list):
		if self.crc8(data_list) != 0:
			return -1

		if (data_list[0]&0x3F)+2 != len(data_list):
			return -2

		data_type = (data_list[0]>>6)&0x03

		return (data_type, data_list[1:-1])

	# other possibilities: with numbers (like uC), with a list (insert method)

	def stuff_packet3(self, data_list):
		data_bit_counter = 0
		data_byte_counter = 0
		stuff_bit_counter = 0
		stuff_byte_counter = 0
		consecutiveOnes = 0
		stuffCount = 0
		stuffed_list = [0]

		for i in range(len(data_list)*8):
			if data_list[data_byte_counter] & (0x80 >> data_bit_counter):
				stuffed_list[stuff_byte_counter] |= (0x80 >> stuff_bit_counter)
				consecutiveOnes += 1
				stuff_bit_counter += 1
				if(stuff_bit_counter == 8):
					stuff_bit_counter = 0
					stuff_byte_counter += 1
					stuffed_list.append(0)

				if consecutiveOnes == 5:
					consecutiveOnes = 0
					stuffed_list[stuff_byte_counter] &= ~(0x80 >> stuff_bit_counter)
					stuff_bit_counter += 1
					if(stuff_bit_counter == 8):
						stuff_bit_counter = 0
						stuff_byte_counter += 1
						stuffed_list.append(0)

			else:
				consecutiveOnes = 0
				stuffed_list[stuff_byte_counter] &= ~(0x80 >> stuff_bit_counter)
				stuff_bit_counter += 1
				if(stuff_bit_counter == 8):
					stuff_bit_counter = 0
					stuff_byte_counter += 1
					stuffed_list.append(0)

			data_bit_counter += 1
			if(data_bit_counter == 8):
				data_bit_counter = 0
				data_byte_counter += 1

		stuffed_list.insert(0,0x7E)
		stuffed_list.append(0x7E)

		return stuffed_list


	def stuff_packet2(self, data_list):
		temp_list = []

		for item in data_list:
			temp_list.extend(list("{:08b}".format(item&0xFF)))

		bitCounter = 0
		consecutiveOnes = 0
		stuffCount = 0

		while bitCounter < len(temp_list):
			if temp_list[bitCounter] == "1":
				consecutiveOnes += 1

				if consecutiveOnes == 5:
					consecutiveOnes = 0
					bitCounter += 1
					temp_list.insert(bitCounter,"0")
					# data_str = data_str[:bitCounter] + "0" + data_str[bitCounter:]
					
			else:
				consecutiveOnes = 0

			bitCounter += 1

		temp = bitCounter % 8
		if temp:
			temp_list.extend(["0"]*(8-temp))
			bitCounter += (8-temp)

		stuffed_list = []
		for i in range(0,bitCounter,8):
			stuffed_list.append(int("".join(temp_list[i:i+8]),2))

		stuffed_list.insert(0,0x7E)
		stuffed_list.append(0x7E)
		
		return stuffed_list


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
			return -1

		if data_list[0] == 0x7E:
			data_list.pop(0)

			if not data_list:
				return -1

		if data_list[-1] == 0x7E:
			data_list.pop()

			if not data_list:
				return -1

		data_str = "".join(["{:08b}".format(x & 0xFF) for x in data_list])

		bitCounter = 0
		consecutiveOnes = 0
		stuffCount = 0

		while bitCounter < len(data_str):
			if data_str[bitCounter] == "1":
				consecutiveOnes += 1

				if consecutiveOnes == 5:
					consecutiveOnes = 0
					# bitCounter += 1

					if data_str[bitCounter+1] == "1":
						return -2

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


	def send(self, data_type, data_list):
		packet_list = self.package(data_type, data_list)
		stuffed_list = self.stuff(packet_list)

		return stuffed_list


	def receive(self, data_list):
		unstuffed_list = self.unstuff(data_list)
		if type(unstuffed_list) is int:
			return -1

		package_tuple = self.unpackage(unstuffed_list)
		if type(package_tuple) is int:
			return -2

		return package_tuple


	def print_list_hex_byte(self, data_list):
		print("[",end="")
		print(", ".join(["0x{:02X}".format(x & 0xFF) for x in data_list]),end="")
		print("]")