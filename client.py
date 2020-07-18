import socket
import time
import operator

class ClientError(Exception):
	pass

class Client:

	_Client__connection = 0

	def __init__(self, host, port, timeout = None):
		self.host = host
		self.port = port
		self.timeout = timeout
		Client._Client__connection = socket.create_connection((self.host,self.port),timeout=self.timeout)

	#method for getting metrics from server
	def get(self, metric_name):
		request = f"get {metric_name}\n"
		data_recv = ""
		try:
			Client._Client__connection.sendall(request.encode("utf8"))
			data_recv = Client._Client__connection.recv(1024).decode("utf8")


			data_list = data_recv.split('\n')

			if len(data_list[1].split()) != 3 and data_recv != "ok\n\n":
				raise ClientError 
		except ClientError as err:
			print("ClientError: wrong request...\n")

			raise ClientError

		if data_list[0] == 'ok' and len(data_list[1].split()) == 3:
			return Client.pasre_data_request(data_list)
		else :
			return {}		#if request "ok\n\n" - no key


	#method for parse information and make dict of information
	def pasre_data_request(data_list):
		index = 1

		_dict = dict()
		while index < len(data_list):
			if(data_list[index] == ''):
				break
			item = data_list[index].split()
			if item[0] in _dict:
				_dict[item[0]] += [(int(item[2]),float(item[1]))]
			else:
				_dict[item[0]] = [(int(item[2]),float(item[1]))]
			index += 1

		for key,value in _dict.items():
			_dict[key] = sorted(value) 
		return _dict



	#method for saving new metrics in server
	def put(self, metric_name, metric_value, timestamp = None):
		if timestamp is None:
			timestamp = int(time.time()) 

		request = f"put {metric_name} {metric_value} {timestamp}\n"
		try:
			Client._Client__connection.sendall(request.encode("utf8"))
			_recv = Client._Client__connection.recv(1024).decode("utf8").split('\n')
			if _recv[0] != "ok":
				raise ClientError
		except ClientError as err:
			print("ClientError: wrong request...\n")
			raise ClientError