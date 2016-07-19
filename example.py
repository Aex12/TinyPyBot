#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TinyPyBot import TinyPyBot, parse_message


token  = "xxxxxxxxxxxxxxxxxxxxxxxxx" #your bot token
bot = TinyPyBot(token)


while bot.getMessages():
	if bot.message is None: continue

	message = parse_message(bot.message)
	message.logIt()

	if message.is_command:
		if message.command.lower().startswith("ping"):
			bot.sendMessage("pong", message["chat"]["id"])
		if message.command.lower().startswith("pong"):
			bot.sendMessage("ping", message["chat"]["id"])
		continue

	if "hello" in message.text:
		bot.sendMessageReply("Hi!", message.data)