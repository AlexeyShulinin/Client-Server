import asyncio

#global server storage
_storage = dict()

#class wich manipulate with request and data
class Server:

	def __init__(self):
		pass

	#method save request to storage of server
	def save_request(key, value, timestamp):
		if key not in _storage:
			_storage[key] = [(float(value),int(timestamp))]
		else:
			values = dict(_storage.get(key))

			print(values)

			values = {v:k for k, v in values.items()}

			print(values)
			_dict = dict()

			#if timestamp is in storage - update data
			if timestamp in values.keys():
				print(timestamp,"is chande")
				values[timestamp] = value
				for k,v in values.items():
					if k not in _dict:
						_dict[float(v)] = int(k)
					else:
						_dict[float(v)] += int(k)
				_storage[key] = tuple(_dict.items())
			else:
				_dict[float(value)] = int(timestamp)
				_storage[key] += tuple(_dict.items())
					

	#method get data from storage by correct request
	def get_data(request_key):
		data = ''
		if request_key in _storage.keys():
			values = _storage.get(request_key)
			for item in values:
				data += f'{request_key} {item[0]} {item[1]}\n'
		if request_key == '*':
			for key,value in _storage.items():
				for item in value:
					data += f'{key} {item[0]} {item[1]}\n'
		return f'ok\n{data}\n'

	#method for return request to client
	def make_request(key):
		index = 1
		data = ''

		for key,value in _storage.items():
			for item in value:
				data += f'{key} {item[0]} {item[1]}\n'

		request = Server.qet_data()
		return request

	def is_digit(string):
		if string.isdigit():
			return True
		else:
			try:
				float(string)
				return True
			except ValueError:
				return False


	#nethod checking request for valid structure 
	def check_request(self,data_recv):
		recv_list = data_recv.split()
		print(len(recv_list))
		if len(recv_list) == 4 or len(recv_list) == 2:
			if recv_list[0] == 'put' and Server.is_digit(recv_list[3]) and Server.is_digit(recv_list[2]):
				Server.save_request(recv_list[1], float(recv_list[2]), int(recv_list[3]))
				print(_storage)
				return 'ok\n\n'
			elif recv_list[0] == 'get' and len(recv_list) == 2:
				return Server.get_data(recv_list[1])
			else:
				return 'error\nwrong command\n\n'
		else:
			return 'error\nwrong command\n\n'

class ClientServerProtocol(asyncio.Protocol):


	def __init__(self):
		pass

	#make connection between server and client
	def connection_made(self, transport):
		#object of connection
		self.server = Server()
		self.transport = transport
		peername = transport.get_extra_info('peername')
		print('Connection from {}'.format(peername))
		
	#method for receive data between server and client
	def data_received(self, data):
		resp = data.decode("utf8")
		print(resp)
		request = self.server.check_request(resp)
		print(request)
		self.transport.write(request.encode("utf8"))


def run_server(host, port):
	loop = asyncio.get_event_loop()
	coro = loop.create_server(
		ClientServerProtocol,
		host, port
	)

	server = loop.run_until_complete(coro)

	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass

	server.close()
	loop.run_until_complete(server.wait_closed())
	loop.close()

if __name__ == "__main__":
	run_server("127.0.0.1", 8181)