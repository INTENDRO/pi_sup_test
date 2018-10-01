import sup
import ringbuffer
import serial
import time
import timeit
import statistics

uart_port = serial.Serial(
			"/dev/ttyAMA0",
			baudrate=115200,  # THIS BAUDRATE IS OPTIMAL FOR RESET PULSES
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=3.0
		)

uart_port.reset_input_buffer()
uart_port.reset_output_buffer()




##############################################################################
# mySup = sup.Sup()
# mySup.print_list_hex_byte(mySup.package([0x7D,0xBF]))
# mySup.print_list_hex_byte(mySup.package([0xFF]))
# mySup.print_list_hex_byte(mySup.package([0x12,0x34,0x56]))

# mySup.print_list_hex_byte(mySup.send([0x7D,0xBF]))
# mySup.print_list_hex_byte(mySup.send([0xFF]))
# mySup.print_list_hex_byte(mySup.send([0x12,0x34,0x56]))


##############################################################################

# mySup = sup.Sup()
# mySup.stuff_packet2([0x12,0x34])
# mySup.print_list_hex_byte(mySup.stuff_packet ([0x7D,0xBF]))
# mySup.print_list_hex_byte(mySup.stuff_packet2([0x7D,0xBF]))
# mySup.print_list_hex_byte(mySup.stuff_packet3([0x7D,0xBF]))

##############################################################################

# times = timeit.repeat(setup = "import sup; mySup = sup.Sup()", stmt ="mySup.stuff_packet([0x7D,0xBF])",repeat = 5, number = 10000)
# print("stuff_packet:")
# print("min: {:.3f}  max: {:.3f}  avg: {:.3f}".format(min(times),max(times),statistics.mean(times)))
# print()
# times = timeit.repeat(setup = "import sup; mySup = sup.Sup()", stmt ="mySup.stuff_packet2([0x7D,0xBF])",repeat = 5, number = 10000)
# print("stuff_packet2:")
# print("min: {:.3f}  max: {:.3f}  avg: {:.3f}".format(min(times),max(times),statistics.mean(times)))
# print()
# times = timeit.repeat(setup = "import sup; mySup = sup.Sup()", stmt ="mySup.stuff_packet3([0x7D,0xBF])",repeat = 5, number = 10000)
# print("stuff_packet3:")
# print("min: {:.3f}  max: {:.3f}  avg: {:.3f}".format(min(times),max(times),statistics.mean(times)))
# print()

##############################################################################

# mySup = sup.Sup()
# mySup.unstuff([0x7E,0x12,0x7E])
# mySup.unstuff([0x34,0x7E])
# mySup.unstuff([0x7E,0x56])
# mySup.unstuff([0x78])
# mySup.unstuff([0x12,0x34,0x56])
# print(mySup.unstuff([0x7E,0x7E]))

##############################################################################

# mySup = sup.Sup()
# mySup.print_list_hex_byte(mySup.stuff_packet([0xFF]))
# mySup.print_list_hex_byte(mySup.unstuff([0x7E,0xFB,0x80,0x7E]))

##############################################################################

# mySup = sup.Sup()
# mySup.print_list_hex_byte(mySup.get_packet(0, [0x12,0x34]))

##############################################################################

# mySup = sup.Sup()
# data_type, data_list = mySup.receive([0x7E, 0x02, 0x7C, 0xDF, 0x6A, 0x40, 0x7E])
# print(data_type)
# mySup.print_list_hex_byte(data_list)
# data_type, data_list = mySup.receive([0x7E, 0x40, 0xC7, 0x7E])
# print(data_type)
# mySup.print_list_hex_byte(data_list)
# data_type, data_list = mySup.receive([0x7E, 0x83, 0x12, 0x34, 0x56, 0x77, 0x7E])
# print(data_type)
# mySup.print_list_hex_byte(data_list)

##############################################################################

# data_buffer = []

# try:
# 	while True:
# 		temp = uart_port.in_waiting
# 		if temp:
# 			data_buffer.extend(list(uart_port.read(temp)))
# 			print("temp: ",str(data_buffer))
# 		time.sleep(1)

# except KeyboardInterrupt:
# 	pass

##############################################################################

# myRingbuffer = ringbuffer.Ringbuffer(2,str)
# print(myRingbuffer.is_empty)
# print(myRingbuffer.is_full)
# print(myRingbuffer.count)
# myRingbuffer.append("Hello")
# print(myRingbuffer.is_empty)
# print(myRingbuffer.is_full)
# print(myRingbuffer.count)
# myRingbuffer.append("World!")
# print(myRingbuffer.is_empty)
# print(myRingbuffer.is_full)
# print(myRingbuffer.count)

# print()

# print(myRingbuffer.remove())
# print(myRingbuffer.is_empty)
# print(myRingbuffer.is_full)
# print(myRingbuffer.count)
# print(myRingbuffer.remove())
# print(myRingbuffer.is_empty)
# print(myRingbuffer.is_full)
# print(myRingbuffer.count)

# print()

# myRingbuffer.extend(["Hoi","du"])
# print(myRingbuffer.is_empty)
# print(myRingbuffer.is_full)
# print(myRingbuffer.count)
# myRingbuffer.clear()
# print(myRingbuffer.is_empty)
# print(myRingbuffer.is_full)
# print(myRingbuffer.count)

# print()

# myRingbuffer.extend(["Hoi","du"])
# print(myRingbuffer.is_empty)
# print(myRingbuffer.is_full)
# print(myRingbuffer.count)

# print()

# print(myRingbuffer.peak())
# print(myRingbuffer.count_item("Hoi"))
# print(myRingbuffer.remove_until_item("ich"))
# print(myRingbuffer.peak())

##############################################################################

# ringbuff = ringbuffer.Ringbuffer()
# mySup = sup.Sup()

# data = 0

# oldtime = time.time()

# try:
# 	while True:
# 		temp = time.time()
# 		if (temp - oldtime) >= 1:
# 			oldtime = temp
# 			# uart_port.write(mySup.send(0, [data]))
# 			mySup.print_list_hex_byte(mySup.send(0, [data]))
# 			data += 1
# 			if data == 256:
# 				data = 0


# except KeyboardInterrupt:
# 	pass


##############################################################################


ringbuff = ringbuffer.Ringbuffer()
mySup = sup.Sup()


data = 0
wait_for_return = False

oldtime = time.time()

error_list = []

try:
	while True:
		temp = time.time()
		if (temp - oldtime) >= 0.01:
			oldtime = temp

			if wait_for_return:
				error_list.append(data)

			data += 1
			if data == 256:
				data = 0
			
			print("Send: 0x{:02x}".format(data))
			# mySup.print_list_hex_byte(mySup.send([data]))
			uart_port.write(mySup.send([data]))
			wait_for_return = True
			
			
		temp = uart_port.in_waiting
		if temp:
			ringbuff.extend(list(uart_port.read(temp)))

		if ringbuff.count_item(0x7E):
			temp = ringbuff.remove_until_item(0x7E)
			
			try:
				temp = mySup.receive(temp)
				if (len(temp) == 1) and (temp[0] == data):
					wait_for_return = False
					print("time diff: {:.6f}".format(time.time()-oldtime))
			except (sup.SupDataLengthException, sup.SupCRCError, sup.SupStuffError):
				pass


except KeyboardInterrupt:
	print("Stopping the test...")

print("error_list: ")
mySup.print_list_hex_byte(error_list)

##############################################################################

# mySup = sup.Sup()

# mySup.print_list_hex_byte(mySup.send(0,[0x00]))
# print(mySup.receive([0x7E, 0x01, 0x00, 0x15, 0x7E]))
# print()

# mySup.print_list_hex_byte(mySup.send(0,[0xff]))
# print(mySup.receive([0x7E, 0x01, 0xF7, 0xD9, 0x80, 0x7E]))


# print()
# mySup.print_list_hex_byte(mySup.unstuff([0x7E, 0x01, 0x00, 0x15, 0x7E]))
# print()
# mySup.print_list_hex_byte(mySup.unstuff([0x7E, 0x01, 0xF7, 0xD9, 0x80, 0x7E]))
# print()
# mySup.print_list_hex_byte(mySup.stuff([0x1F]))
##############################################################################

# mySup = sup.Sup()

# packet = mySup.package([0x3f,0x89])
# mySup.print_list_hex_byte(packet)
# mySup.print_list_hex_byte(mySup.unpackage(packet))

##############################################################################

uart_port.close()