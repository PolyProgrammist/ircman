import socket
from time import sleep
import filecmp

logging_file = 'logging.txt'
with open(logging_file, 'w') as fout:
    pass

def test_first():
    botnick = 'tester_lupa_pupa'
    server = "irc.ubuntu.com"  # Server
    channel = '#test-bot'
    password = ""

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

    file_name = 'res/tmp.txt'
    with open('kek.txt', 'w') as fout:
        pass

    def joinchan(chan):  # join channel(s).
        ircsock.sendall(("JOIN " + chan + "\n").encode())

    sleep(10)

    def send_message(msg):
        message = "PRIVMSG " + channel + " :" + msg + "\n"
        with open(file_name, 'a') as fout:
            fout.write(message)
        encoded = message.encode()
        ircsock.sendall(encoded)

    def receive_message():
        ircmsg = ircsock.recv(2048).decode('utf-8')
        with open(logging_file, 'a') as fout:
            fout.write(ircmsg)

        if ircmsg[1:5] in ['Pupa', 'Lupa']:
            with open(file_name, 'a') as fout:
                name = ircmsg[1:5]
                ircmsg = name + ' ' + ircmsg[ircmsg.find('PRIVMSG'):]
                fout.write(ircmsg)
        return 'Мы сделали это, бро' in ircmsg

    joinchan(channel)
    send_message('Lupa and Pupa, do some magic Мэрилин Монро')
    while not receive_message():
        print('receiving')

    return filecmp.cmp('tests/merilin.txt', file_name)


assert test_first()
