import sys
import Parse
'''
run state machine
Start ---> MF ---> RT ---> DT ---> Text ---> Dot ---> End
            ^       ^   |             ^   |        |
            |       +---+             +---+        |
            |                                      |
            +--------------------------------------+
'''
def main():

	#allowed state transitions
	#each state has a dictionary of <cmd> : <new state>

	#EOF: END was added int the DOT because I oringially threw an error if it gave an icomplete mail message
	#kept the above still part of the dictionary in case for future use
    allowed = {
        'START': {'MAIL': 'MF'},
        'MF': {'RCPT': 'RT'},
        'RT': {'RCPT': 'RT', 'DATA': 'DT'},
        'DT': {'*': 'Text'},
        'Text': {'*': 'Text', '.': 'DOT'},
        'DOT': {'MAIL': 'MF', 'EOF': 'END'}
    }

    state = 'START'

    mailfrom = ''

    #empy lists to hold recipients and the email message to be able to write to file later on
    recipients = []
    data_message = []

    for line in sys.stdin:

        print line

        #text is the only thing that doesn't need to be validated or stopped untl the end line
        #if text, assign that a cmd; if not, parse line to find out what cmd it has

        if '*' in allowed[state].keys():
            cmd = '.' if line.rstrip() == '.' else '*'
        else:
        	'''
        	parse_command returns what type of command it is
        	if none, the command was unrecognizable (500)
        	then check in dictionary to see if cmd is allowed in particular state
        	'''

            cmd = Parse.parse_command(line)
            if cmd is None:
                print "500 Syntax error: command unrecognized"
                continue

        if cmd not in allowed[state].keys():
            print "503 Bad sequence of commands"
            continue


        #checks to see if the parameters are valid

        if cmd == 'MAIL' or cmd == 'RCPT':
            if not Parse.parse_line(line, cmd):
                print "501 Syntax error in parameters or arguments"
                continue

        #transitioning into a new state

        new_state = allowed[state][cmd]

        if new_state == 'DT':
            print "354 Start mail input; end with <CLRF>.<CLRF>"
        elif new_state == 'DOT':
            print "250 OK"
            write_to_files(recipients, data_message, mailfrom)
            recipients = []
            data_message = []
        elif new_state == 'Text':
            data_message.append(line)
        elif new_state == 'RT':
            print "250 OK"
            recipients.append(line)
        elif new_state == 'MF':
            print "250 OK"
            mailfrom = line

        state = new_state


#append to file: loops through recipients and data_message
def write_to_files(recipients, data_message, mailfrom):

    for address in recipients:
        filename = "forward/" + mailbox(address)

        with open(filename, "a+") as f:

            f.write("From: " + mailbox(mailfrom) + "\n")

            for line in recipients:
                f.write("To: " + mailbox(line) + "\n")

            for line in data_message:
                f.write(line)


#gets only the mailbox out of a line of text
def mailbox(line):

    ind = 0;

    while not line[ind] == "<":
        ind += 1

    startind = ind

    while not line[ind] == ">":
        ind += 1

    return line[startind+1:ind]

main()


