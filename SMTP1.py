import sys
import Parse

# do we have to keep stdin open after the period?? for another message?
# how do we know the client is done sending?
# check for end of file; but keep on receiving until then (control + D)
# if something throws an error, should we just leave the entire thing?
# don't exit, either wait for current command or start message all over, be ready to read input
# priority of errors: syntax, out of order, the arguments
# what is null space? after data can there be white space?
# use a list to check everything with the list--> while loop, and everything


def mail_messages():

    allowed = ["MF"]
    RTcount = 0
    recipients = []
    DTcount = 0
    mailfrom = ""

    for line in sys.stdin.readlines():
        print line
        code=Parse.parse_command(line)

        if code == "500":
            print "500 Syntax error: command unrecognized"
            return False
        elif code not in allowed:
            print "503 Bad sequence of commands"
            return False

        if not Parse.parse_line(line, code):
            print "501 Syntax error in parameters or arguments"
            return False

        if code == "RT":
            recipients[RTcount] = line
            RTcount += 1

        if allowed == ["MF"]:
            mailfrom = line
            allowed = ["RT"]
        elif allowed == ["RT"]:
            allowed = ["RT", "DT"]
        elif code == "DT":
            allowed = []


# how do i change state???/ how do i change the allowed depending on what it was before?
# how to check for data messages ??





    mail= sys.stdin.readlines()

    mfcode = Parse.parse_command(mail[0])

    if mfcode == "500":
        print "500 Syntax error: command unrecognized"
        return False
    elif mfcode == "MF":
        print "250 OK"
    else:
        print "503 Bad sequence of commands"

    recipients = []
    counter = 0
    index = 1

    while True:
        rcptcode = Parse.parse_command(mail[index])

        if rcptcode == "500":
            print "500 Syntax error: command unrecognized"
            return False
        elif rcptcode == "DT":
            if counter == 0:
                print "503 Bad sequence of commands"
                return False
            else:
                index += 1
                break
        elif rcptcode == "MF":
            print "503 Bad sequence of commands"
            return False

        if not Parse.parse_line(mail[index], rcptcode):
            print "501 Syntax error in parameters or arguments"
            return False

        print "250 OK"
        recipients[counter] = mail[index]
        counter += 1
        index += 1

    data_message = []
    counter = 0

    while True:

        if end_line(mail[index]):
            print mail[index]
            print "250 OK"
            break

        data_message[counter] = mail[index]
        counter += 1
        index += 1

    write_to_files(recipients,  data_message, mail[0])
    return True


def end_line(line):
    return Parse.crlf(line[0]) and line[1] == "." and Parse.crlf(line[2])


def write_to_files(recipients, data_message, mailfrom):

    for address in recipients:
        filename = "forward/" + mailbox(address)

        with open(filename) as f:

            f.write("From: " + mailbox(mailfrom))

            for line in recipients:
                f.write("To: " + mailbox(line))

            for line in data_message:
                f.write(line)


def mailbox(line):

    ind = 0;

    while not line[ind] == "<":
        ind += 1

    startind = ind

    while not line[ind] == ">":
        ind += 1

    return line[startind+1:ind]



