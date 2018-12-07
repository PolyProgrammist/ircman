# Import some necessary libraries.
import socket, re, subprocess, os, time, threading, sys

# Some basic variables used to configure the bot
from download_file import download
from google_worker import images_links
from jpg2ascii import ascii_from_image

file_name = 'res/temp.jpg'

server = "irc.ubuntu.com"  # Server
channel = "#arseni"  # Channel
botnick = "Pupa"  # Your bots nick
password = ""

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))  # Here we connect to the server using the port 6667

auth_str = "USER " + botnick + " " + botnick + " " + botnick + " " + botnick + "\n"
nick_str = "NICK " + botnick + "\n"
iden_str = "nickserv identify " + password + "\r\n"

ircsock.send(auth_str.encode())  # user authentication
ircsock.send(nick_str.encode())  # assign the nick to the bot
ircsock.send(iden_str.encode())


def ping():  # respond to server Pings.
    ircsock.send(("PONG :pingis\n").encode())


def sendmsg(msg):  # sends messages to the channel.
    ircsock.send(("PRIVMSG " + channel + " :" + msg + "\n").encode())


def joinchan(chan):  # join channel(s).
    ircsock.send(("JOIN " + chan + "\n").encode())


def spli_msg(s):
    name = s.split('!', 1)[0][1:]
    message = s.split('PRIVMSG', 1)[1].split(':', 1)[1]
    return name, message


# main functions of the bot
def main():
    # start by joining the channel. --TO DO: allow joining list of channels
    joinchan(channel)

    # open the chat log file if it exists and delete it to start fresh.
    # with open("ircchat.log", "w") as temp:
    #     temp.write("")

    # start infinite loop to continually check for and receive new info from server
    while 1:
        # clear ircmsg value every time
        ircmsg = ""

        # set ircmsg to new data received from server
        ircmsg = ircsock.recv(2048).decode('utf-8')

        # remove any line breaks
        ircmsg = ircmsg.strip('\n\r')

        # print received message to stdout (mostly for debugging).
        if ircmsg.find(f'PRIVMSG {channel}') != -1:
            print(ircmsg)
            print()

        # repsond to pings so server doesn't think we've disconnected
        if ircmsg.find('PING :') != -1:
            ping()

        # look for PRIVMSG lines as these are messages in the channel or sent to the bot
        # sendmsg("Или тебе норм?")
        if ircmsg.find(f'PRIVMSG {channel}') != -1:
            name, message = spli_msg(ircmsg)

            if message.find('Лупа, покажи мне ') != -1:
                req = message.split('покажи мне ', 1)[1]

                urls = images_links(req)
                url = urls[1]

                download(url, file_name)
                ascii_image = ascii_from_image(file_name, 100, '\'.-/ilnmoILO')
                print(ascii_image)
                lines = ascii_image.split(sep='\n')

                current_line = 1
                while True:
                    ircmsg = ircsock.recv(2048).decode('utf-8')

                    if ircmsg.find('PING :') != -1:
                        ping()

                    if ircmsg.find(f'PRIVMSG {channel}') != -1:
                        name, msg = spli_msg(ircmsg)
                        print(name, msg)
                        if name == 'Lupa':
                            time.sleep(0.5)
                            print(current_line)
                            sendmsg(lines[current_line])
                            print("sended")

                            current_line += 2

                            if current_line >= len(lines) - 2:
                                print("Pupa end")
                                break
            else:
                print(message)
            print("-"*100)

            # sendmsg(f'{name} siad "{message}", bit he is stupid, don`t  listen him')

main()
