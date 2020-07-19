import asyncio

"""
Global server storage.
"""
storage = dict()

"""
Class wich manipulate with request and data.
"""
class Server:

	def __init__(self):
		pass

	"""
	Method save request to storage of server.
	"""
	def save_request(key, value, timestamp):
		if key not in storage:
			storage[key] = [(float(value),int(timestamp))]
		else:
			_values = dict(storage.get(key))

			print(_values)

			_values = {v:k for k, v in _values.items()}

			print(_values)
			_dict = dict()

			if timestamp in _values.keys():  # If timestamp is in storage - update data.
				print(timestamp,"is chande")
				_values[timestamp] = value
				for k,v in _values.items():
					if k not in _dict:
						_dict[float(v)] = int(k)
					else:
						_dict[float(v)] += int(k)
				storage[key] = tuple(_dict.items())
			else:
				_dict[float(value)] = int(timestamp)
				storage[key] += tuple(_dict.items())
					

	"""
	Method get data from storage by correct request.
	"""
	def get_data(request_key):
		_data = ''

		if request_key in storage.keys():
			values = storage.get(request_key)
			for item in values:
				_data += f'{request_key} {item[0]} {item[1]}\n'

		if request_key == '*':
			for key,value in storage.items():
				for item in value:
					_data += f'{key} {item[0]} {item[1]}\n'

		return f'ok\n{_data}\n'

	"""
	Method for return request to client.
	"""
	def make_request(key):
		_data = ''

		for key,value in storage.items():
			for item in value:
				_data += f'{key} {item[0]} {item[1]}\n'

		request = Server.qet_data()
		return request

	def _is_digit(string):
		if string.isdigit():
			return True
		else:
			try:
				float(string)
				return True
			except ValueError:
				return False

	"""
	Method check request for valid structure.
	"""
	def check_request(self,data_recv):
		_recv_list = data_recv.split()

		if len(_recv_list) == 4 or len(_recv_list) == 2:
			if (_recv_list[0] == 'put' 
				and Server._is_digit(_recv_list[3]) 
				and Server._is_digit(_recv_list[2])):

				Server.save_request(
					_recv_list[1], 
					float(_recv_list[2]), 
					int(_recv_list[3])
				)

				return 'ok\n\n'

			elif _recv_list[0] == 'get' and len(_recv_list) == 2:
				return Server.get_data(_recv_list[1])
			else:
				return 'error\nwrong command\n\n'
		else:
			return 'error\nwrong command\n\n'


# Class which make connection between
# client and server and make request
# between them.
class ClientServerProtocol(asyncio.Protocol):

	def __init__(self):
		pass

	"""
	Make connection between server and client.
	"""
	def connection_made(self, transport):
		self.server = Server()
		self.transport = transport
		peername = transport.get_extra_info('peername')
		print('Connection from {}'.format(peername))
		

	"""
	Method for receive data between server and client.
	"""
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