#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TinyPyBot import TinyPyBot


token  = "xxxxxxxxxxxxxxxxxxxxxxxxx" #your bot token
bot = TinyPyBot(token)


while bot.getMessages():
	if bot.message is None: continue
	
	if "message" in bot.message:
		message = bot.message["message"]
		
		if "text" in message:
			print bot.whoSends(message) + ": " + message["text"]
				
		if "entities" in message:
			if "bot_command" == message["entities"][0]["type"] and 0 == message["entities"][0]["offset"]:
				if message["text"][1:].startswith("ping"):
					bot.sendMessage("pong", message["chat"]["id"])
				if message["text"][1:].startswith("pong"):
					bot.sendMessage("ping", message["chat"]["id"])
		if "text" in message:
			if "hello" in message["text"]:
				bot.sendMessageReply("Hi!", message)