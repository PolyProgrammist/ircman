# Import some necessary libraries.
import random
import socket, re, subprocess, os, time, threading, sys

# Some basic variables used to configure the bot
from download_file import download
from google_worker import images_links
from image_getter import get_correct_image_url
from jpg2ascii import ascii_from_image

botnick = sys.argv[1][2:]
command_ask = 'Lupa and Pupa, do some magic'
command_set_color = 'set color'
command_set_weight = 'set weight'
weight = 100

time_sleep = 0.2
help = [
    'I need somebody!',
    'Not just anybody!',
    'You know I need someone!!!',
    f' Запрос на рисование: {command_ask} что-нибудь',
    f' Установить новый цвет: {command_set_color} \'.-/ilnmoILO',
    f' Установить ширину картинки: {command_set_weight} 100',
    'Послушать битлов и получить справку: Help!'
]

assert botnick == 'Pupa' or botnick == 'Lupa'
brother = 'Lupa' if botnick == 'Pupa' else 'Pupa'

file_name = 'res/' + botnick + 'temp'

server = "irc.ubuntu.com"  # Server
channel = '#test-bot'
# channel = "#2448"  # Channel
botnick = botnick  # Your bots nick
password = ""

print('Starting ' + botnick)
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))  # Here we connect to the server using the port 6667
print('Connected ' + botnick)

auth_str = "USER " + botnick + " " + botnick + " " + botnick + " " + botnick + "\n"
nick_str = "NICK " + botnick + "\n"
iden_str = "nickserv identify " + password + "\r\n"

ircsock.sendall(auth_str.encode())  # user authentication
print('Authentication sent ' + botnick)
ircsock.sendall(nick_str.encode())  # assign the nick to the bot
print('Nick sent ' + botnick)
ircsock.sendall(iden_str.encode())
print('Identification sent ' + botnick)

request = 'Апельсин'
color_theme = '\'.-/ilnmoILO'
current_line = 0
lines = []
state = 0
help_counter = 0


# 0 - ожидание запроса
# 1 - Лупа качает, Пупа ждёт ссылку


def ping():  # respond to server Pings.
    ircsock.sendall(("PONG :pingis\n").encode())


def sendmsg(msg):  # sends messages to the channel.
    message = "PRIVMSG " + channel + " :" + msg + "\n"
    encoded = message.encode()
    ircsock.sendall(encoded)


def joinchan(chan):  # join channel(s).
    ircsock.sendall(("JOIN " + chan + "\n").encode())


def split_msg(s):
    name = s.split('!', 1)[0][1:]
    message = s.split('PRIVMSG', 1)[1].split(':', 1)[1]
    return name, message


# main functions of the bot
def main():
    # start by joining the channel. --TO DO: allow joining list of channels
    global state, request, current_line, lines, help_counter, color_theme, weight
    joinchan(channel)

    # open the chat log file if it exists and delete it to start fresh.
    # with open("ircchat.log", "w") as temp:
    #     temp.write("")

    # start infinite loop to continually check for and receive new info from server
    while True:
        # clear ircmsg value every time
        ircmsg = ""

        # set ircmsg to new data received from server
        ircmsg = ircsock.recv(2048).decode('utf-8')

        # remove any line breaks
        ircmsg = ircmsg.strip('\n\r')

        # print received message to stdout (mostly for debugging).
        # if ircmsg.find(f'PRIVMSG {channel}') != -1:
        #     print(ircmsg)
        #     print()

        # repsond to pings so server doesn't think we've disconnected
        if ircmsg.find('PING :') != -1:
            ping()

        if ircmsg.find(f'PRIVMSG {channel}') != -1:
            name, message = split_msg(ircmsg)
            if message == 'Стоямба!':
                print('Стоп')
                time.sleep(time_sleep)
                state = 0
                if botnick == 'Lupa':
                    sendmsg('Понял')
                else:
                    sendmsg('Принял')

        if state == 3:
            if ircmsg.find(f'PRIVMSG {channel}') != -1:
                name, message = split_msg(ircmsg)
                print("$$$" + message)
                if name == brother:
                    if message == 'Я всё':
                        state = 0
                        sendmsg('Мы сделали это, бро')
                    else:
                        if current_line == len(lines) - 1:
                            time.sleep(time_sleep)
                            state = 0
                            sendmsg('Я всё')
                        elif current_line < len(lines):
                            time.sleep(time_sleep)
                            sendmsg(lines[current_line])
                            current_line += 2

        if state == 2:
            # print(botnick*10)
            if ircmsg.find(f'PRIVMSG {channel}') != -1:
                name, message = split_msg(ircmsg)
                if name == 'Pupa' and message.find('Пойдёт') != -1:
                    print('Lupa begin drawing')
                    time.sleep(time_sleep)
                    state = 3
                    current_line = 0
                    sendmsg(lines[current_line])
                    current_line = 2
                    continue

        if state == 1:
            if botnick == 'Lupa':
                print('Lupa load urls')
                urls = images_links(request)
                url = get_correct_image_url(urls, f'{botnick}-lalala.jpg')
                download(url, f'{file_name}-{botnick}.jpg')
                lines = ascii_from_image(f'{file_name}-{botnick}.jpg', weight, color_theme).split(sep='\n')

                sendmsg(f'Пупа, как тебе эта {url}?')
                state = 2
                continue

            else:
                if ircmsg.find(f'PRIVMSG {channel}') != -1:
                    name, message = split_msg(ircmsg)
                    if name == 'Lupa' and message.find('эта ') != -1:
                        print('Pupa get url from Lupa')

                        url = message.split('эта ')[1][:-1]
                        download(url, f'{file_name}-{botnick}.jpg')
                        lines = ascii_from_image(f'{file_name}-{botnick}.jpg', weight, color_theme).split(sep='\n')
                        time.sleep(time_sleep)

                        print('Пупа принял ссылку', len(lines))
                        time.sleep(time_sleep)
                        sendmsg(f'Пойдёт')
                        state = 3
                        current_line = 1
                        continue

        if state == 0:
            if ircmsg.find(f'PRIVMSG {channel}') != -1:
                name, message = split_msg(ircmsg)

                if message.find(command_ask) != -1 and name != brother:
                    request = message.split(command_ask, 1)[1]
                    if request == '':
                        request = 'Мэрлин Монро'

                    if botnick == 'Lupa':
                        sendmsg('Понял')
                        state = 1
                        continue
                    else:
                        sendmsg('Принял')
                        time.sleep(time_sleep)
                        state = 1
                        continue

        if ircmsg.find(f'PRIVMSG {channel}') != -1:
            name, message = split_msg(ircmsg)
            if message.find(command_set_weight) != -1 and name != brother:
                weight = int(message.split(command_set_weight)[1][1:])
                if botnick == 'Lupa':
                    sendmsg('Понял')
                else:
                    sendmsg('Принял')

        if ircmsg.find(f'PRIVMSG {channel}') != -1:
            name, message = split_msg(ircmsg)
            if message == 'Help!' and name != brother:
                if botnick == 'Lupa' and help_counter % 2 == 0:
                    sendmsg(help[help_counter % len(help)])
                if botnick == 'Pupa' and help_counter % 2 == 1:
                    sendmsg(help[help_counter % len(help)])
                help_counter += 1

        if ircmsg.find(f'PRIVMSG {channel}') != -1:
            name, message = split_msg(ircmsg)
            if message.find(command_set_color) != -1 and name != brother:
                print(message.split(command_set_color)[1][1:])
                color_theme = message.split(command_set_color)[1][1:]
                if botnick == 'Lupa':
                    sendmsg('Понял')
                else:
                    sendmsg('Принял')

main()
