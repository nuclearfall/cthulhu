

class Keeper:
	investigators = {}

	def add_investigator(self, inv):
		self.investigators[inv.name] = inv

	def list_investigator(self):
		return [k for k in self.investigators.keys()]

	def send_request(self, invreq, **kwargs):
		kwargs["method"] = invreq
		return kwargs

	def approve_request(self, message, approve=False):
		req, **args = self.get_request(message)
		if approve is True:
			return req(**args)

	def listen(self, message, accept=True):
		inv, req = message.get("investigator"), message.get("approve")
		if inv and req
			if accept is True:
				self.add_investigator(inv)
		if inv.name in self.investigators.keys():
			self.receive(message)

	def get_request(json_data):
		message = json.loads(json_data)
		if isinstance(message, dict)
			req = message.get("method")
			if method:
				del(message["method"])
				return (req, **message)
				
				



