import requests, json

class TinyPyBot:
	def __init__(self, token):
		self.BOT_TOKEN = token
		self.TELEGRAM_API_URL = "https://api.telegram.org/bot"
		self.offset = 0
		self.message = None
		self.message_list = []

	def request(self, query, params={}):
		r = requests.get(self.TELEGRAM_API_URL+self.BOT_TOKEN+'/'+query, params=params)
		response = r.json()

		if r.status_code != 200:
			print "ERROR "+ str(response["error_code"])+": "+ response["description"]
			return False

		if response["ok"] and response["result"] == []:
			return True

		return response["result"]

	def getMessages(self, limit=100):
		while len(self.message_list) > 0:
			self.message = self.message_list.pop(0)
			self.offset = self.message["update_id"]+1
			return True

		updates = self.request("getUpdates", {"offset": self.offset, "limit": limit})
		
		if isinstance(updates, bool):
			self.message = None
			return updates

		self.message_list = updates
		self.message = self.message_list.pop(0)
		self.offset = self.message["update_id"]+1
		return True

	def whoSends(self, message):
		firstName = message["from"]["first_name"] if "first_name" in message["from"] else ""
		lastName  = " "+message["from"]["last_name"] if "last_name" in message["from"] else ""
		userName  = " [@"+message["from"]["username"]+"]" if "username" in message["from"] else ""
		return firstName+lastName+userName

	def sendMessage(self, text, chat_id, params={}):
		params.update({'chat_id': chat_id, 'text': text})
		return self.request("sendMessage", params)

	def editMessageText(self, text, chat_id, message_id, params={}):
		params.update({'chat_id': chat_id, 'message_id': message_id, 'text': text})
		return self.request("editMessageText", params)

	def forceReply(self, selective=0, params={}):
		params.update({"force_reply": True})
		if selective != 0: params.update({"selective": selective})
		return json.dumps(params)

	class inlineKeyboard:
		def __init__(self):
			self.tojson = {"inline_keyboard": []}

		def addButton(self, text, params={}):
			params.update({"text": text})
			self.tojson["inline_keyboard"].append([params, ])

		def getJson(self):
			return json.dumps(self.tojson)