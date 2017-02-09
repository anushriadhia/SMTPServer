
#parse_line function makes sure the whole line is valid.
#takes in cmd_id to know whether to pass as MAIL FROM or RCPT TO
def parse_line(line, cmd_id):

    if cmd_id == "MAIL":
        parse_mail_from_command(line)
    elif cmd_id == "RCPT":
        parse_rcpt_to_command(line)

    if not path(line):
        return False

    if not crlf(line[index]):
        if char(line[index]) or line[index].isspace() or special(line[index]):
            return False
        else:
            exit()

    return True

#Solely finds out whether the command can be recognized
def parse_command(line):
    if parse_mail_from_command(line):
        return "MAIL"
    elif parse_rcpt_to_command(line):
        return "RCPT"
    elif data_command_parse(line):
        return "DATA"

    return None

#makes sure the DATA command is valid
def data_command_parse(line):
    global index
    index = 0

    if line[:4] == "DATA":
        index += 4
    else:
        return False

    whitespace(line)

    return crlf(line)



#checks validity of MAIL FROM command
def parse_mail_from_command(line):
    global index
    index = 0

    if line[:4] == "MAIL":
        index += 4
    else:
        return False

    startind = index

    whitespace(line)

    if startind == index:
        return False

    if line[index:index+5] == "FROM:":
        index += 5
    else:
        return False

    whitespace(line)

    return True



#checks validity of RCPT TO command in the same exact manner as the MAIL FROM
def parse_rcpt_to_command(line):
    global index
    index = 0

    if line[:4] == "RCPT":
        index += 4
    else:
        return False

    startind = index
    whitespace(line)
    if startind == index:
        return False

    if line[index:index+3] == "TO:":
        index += 3
    else:
        return False

    whitespace(line)

    return True



#increments index in places where any amount of whitespace is allowed
def whitespace(line):
    global index

    while index < len(line) and line[index].isspace():
        index += 1



#all of the followng methods are part of the original recursive descent parsing
#return False if not valid parameter
def path(line):
    global index

    if line[index] == "<":
        index += 1
    else:
        return False

    if not mailbox(line):
        return False

    if line[index] == ">":
        index += 1
        return True
    else:
        return False


def mailbox(line):
    global index

    if not is_string(line, 0):
        return False

    if line[index] == "@":
        index += 1
    else:
        return False

    if not domain(line):
        return False

    return True


def domain(line):
    global index

    if not name(line):
        return False
    else:
        if line[index] == ".":
            index += 1
            return domain(line)
        else:
            return True


def name(line):
    global index

    if not (line[index]).isalpha():
        return False
    index += 1
    if not let_dig_str(line, 0):
        return False

    return True


def let_dig_str(line, count):
    global index

    if line[index + count].isalpha() | unicode(line[index + count]).isnumeric():
        count += 1
        return let_dig_str(line, count)

    else:
        index += count
        if count > 0:
            return True
        else:
            return False


def is_string(line, count):
    global index

    if char(line[index + count]):
        count += 1
        return is_string(line, count)
    else:
        index += count
        return count > 0


def char(character):
    return not (special(character) or character.isspace())


def crlf(line):
    return "\n" in line or "\r" in line


def special(character):
    valid = set('<>()[]\.,;:@"')
    return set(character).issubset(valid)


