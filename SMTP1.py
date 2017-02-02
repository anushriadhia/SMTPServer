import sys
import Parse


def main():

    mail_messages()

# do we have to keep stdin open after the period?? for another message?
# how do we know the client is done sending?
        #check for end of file; but keep on recieving until then (control + D)
# if something throws an error, should we just leave the entire thing?
        #don't exit, either wait for current command or start message all over, either way program should be ready to read input
# how to check if something is out of order
        #call a universal parse command that checks what it is and have it differentiate
        #for data, mail from, rcpt to commands
# how to just get mailbox



def mail_messages():

    mail_from = sys.stdin.readline()
    if not Parse.parse_mail_from_command(mail_from):
        return False

    recipients = []
    counter = 0

    while True:
        read_line = sys.stdin.readline()

        if read_line == "DATA":
            print "354 Start mail input; end with <CLRF>.<CLRF>"
            break

        if not Parse.parse_rcpt_to_command(read_line):
            return False

        recipients[counter] = read_line
        counter += 1

    data_message = []
    counter = 0

    while True:
        read_line = sys.stdin.readline()
        print read_line

        if end_line(read_line):
            print "250 OK"
            break

        data_message[counter] = read_line
        counter += 1

    write_to_files(recipients,  data_message)


def end_line(line):
    return Parse.crlf(line[0]) and line[1] == "." and Parse.crlf(line[2])


def write_to_files(recipients, data_message):

    for address in recipients:
        filename = "forward/" + address

        with open(filename) as f:
            for line in data_message:
                f.write(line)
