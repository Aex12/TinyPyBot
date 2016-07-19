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

	def sendMessage(self, text, chat_id, params={}):
		params.update({'chat_id': chat_id, 'text': text})
		return self.request("sendMessage", params)

	def sendMessageReply(self, text, message, params={}):
		if "message" in message:
			params.update({'chat_id': message["message"]["chat"]["id"], 'text': text, 'reply_to_message_id': message["message"]['message_id']})
			return self.request("sendMessage", params)

	def editMessageText(self, text, chat_id, message_id, params={}):
		params.update({'chat_id': chat_id, 'message_id': message_id, 'text': text})
		return self.request("editMessageText", params)


class reply_markup:
	class inlineKeyboard:
		def __init__(self):
			self.tojson = {"inline_keyboard": []}
			self.line = []

		def addButton(self, text, params={}):
			params.update({"text": text})
			self.line.append(params)
			return self

		def newLine(self):
			self.tojson["inline_keyboard"].append(self.line)
			self.line = []
			return self

		def getJson(self):
			return json.dumps(self.tojson)

	def forceReply(self, selective=0, params={}):
		params.update({"force_reply": True})
		if selective != 0: params.update({"selective": selective})
		return json.dumps(params)


class parse_message:
	def __init__(self, message):
		self.data = message

	@property
	def is_message(self):
		if "message" in self.data:
			return True
		else:
			return False

	@property
	def is_callback_query(self):
		if "callback_query" in self.data:
			return True
		else:
			return False

	@property
	def message_id(self):
		if not self.is_message: return False
		return self.data["message"]["message_id"]

	@property
	def text(self):
		if not self.is_message: return None
		return self.data["message"]["text"]

	@property
	def chat_id(self):
		if not self.is_message: return False
		return self.data["message"]["chat"]["id"]	
	
	@property
	def has_entities(self):
		if not self.is_message: return False
		if "entities" in self.data["message"]:
			return True
		else:
			return False

	@property
	def has_commands(self):
		if not self.has_entities: return False
		for entity in self.data["message"]["entities"]:
			if entity["type"] == "bot_command": return True
		return False

	@property
	def has_text(self):
		if not self.is_message: return False
		if "text" in self.data["message"]:
			return True
		else:
			return False
	

	@property
	def is_command(self):
		if not self.has_entities: return False
		if "bot_command" != self.data["message"]["entities"][0]["type"]: return False
		if  0 == self.data["message"]["entities"][0]["offset"]:
			return True
		else:
			return False

	@property
	def is_forwarded(self):
		if not self.is_message: return False
		if "forward_from_chat" in self.data["message"]:
			return True
		else:
			return False
	

	@property
	def command(self):
		if not self.is_command: return False
		return self.data["message"]["text"][1:]

	@property
	def from_id(self):
		if self.is_message:
			return self.data["message"]["from"]["id"]
		elif self.is_callback_query:
			return self.data["callback_query"]["from"]["id"]

	@property
	def whoSends(self):
		if not self.is_message: return None
		firstName = self.data["message"]["from"]["first_name"] if "first_name" in self.data["message"]["from"] else ""
		lastName  = " "+self.data["message"]["from"]["last_name"] if "last_name" in self.data["message"]["from"] else ""
		userName  = " [@"+self.data["message"]["from"]["username"]+"]" if "username" in self.data["message"]["from"] else ""
		return firstName+lastName+userName

	def forward_from_chat(self, key):
		if not self.is_forwarded: return None
		if key in self.data["message"]["forward_from_chat"]:
			return self.data["message"]["forward_from_chat"][key]
		else:
			return None

	def logIt(self):
		if self.has_text:
			print self.whoSends + ": " + self.text