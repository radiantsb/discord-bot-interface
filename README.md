# discord-bot-interface
a python program to interact with discord

you will need to edit config.json to include your bots token, optionally you can create shortcuts, useful for channel and user id's

uses py-cord library which requires an alternative audioop package such as `audioop-lts` as it has been removed from the standard library

commands:
help - show this list
dm [userid] [message] - send a dm to a user
read [userid] print dm history with a user
send [channelid] [message] - send a message to a channel
reply [channelid] [messageid] [message] reply to a message
delete [channelid] [messageid] - delete a message
edit [channelid] [messageid] [message] - edit a message
image [name] save the image in your clipboard with a name
dm+ [userid] [image] [message] - dm a user, including an image
reply+ [channelid] [messageid] [image] [message] - reply to a message, including an image
send+ [channelid] [image] [message] - send a message to a channel, including an image

tips:
config.json allows you to specify shortcuts for channel ids and user ids
your most recent command is saved, typing an invalid command will reuse it with a new last argument
eg.

\> send [channel] message1

\> message2
