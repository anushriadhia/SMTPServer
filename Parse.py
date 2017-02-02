
def parse_mail_from_command(line):
    global index

    index = 0

    if line[:4] == "MAIL":
        index += 4

    else:
        print("500 Syntax error: command unrecognized")
        return False

    startind = index

    whitespace(line)              #allows for as much whitespace and updates the index

    if startind==index:


    if line[index:index+4] == "FROM:":
        index += 5

    else:
        print("500 Syntax error: command unrecognized")
        return False

    whitespace(line)

    if not path(line):                         #once it recieves any error,
        return False

    if not crlf(line[index]):
        if char(line[index]) or sp(line[index]) or special(line[index]):            #makes sure there aren't any other characters after the path
            print "500 Syntax error: command unrecognized"
            return False

        else:
            exit()                      #indicates the end of file, so exit code

    print "250 OK"                   #passes everything
    return True


def parse_rcpt_to_command(line):
    global index

    index = 0

    if line[:4] == "RCPT":
        index += 4

    else:
        print("500 Syntax error: command unrecognized")
        return False

    whitespace(line)              #allows for as much whitespace and updates the index

    if line[index:index+4] == "TO:":
        index += 3

    else:
        print("500 Syntax error: command unrecognized")
        return False

    whitespace(line)

    if not path(line):                         #once it recieves any error,
        return False

    if not crlf(line[index]):
        if char(line[index]) or sp(line[index]) or special(line[index]):            #makes sure there aren't any other characters after the path
            print "500 Syntax error: command unrecognized"
            return False

        else:
            exit()                      #indicates the end of file, so exit code

    print "250 OK"                   #passes everything
    return True


def whitespace(line):

    global index

    while line[index].isspace():
        index += 1


def path(line):
    global index
    global address
    global startind
    global endind

    if line[index] == "<":
        index += 1
    else:
        print "501 Syntax error in parameters or arguments"
        return False

    startind=index

    if not mailbox(line):
        return False

    endind=index

    if line[index] == ">":
        index += 1
        return True
    else:
        print "501 Syntax error in parameters or arguments"
        return False


def mailbox(line):
    global index

    if not local_part(line):
        return False

    if line[index] == "@":
        index += 1
    else:
        print "501 Syntax error in parameters or arguments"
        return False

    if not domain(line):
        return False

    return True


def domain(line):
    global index
    #check to see if there is element
    #if not, check if .
        #if there is period, call domain
        #if not, check how many times it has recurse, if at least once return true else return false

    if not name(line):
        print "501 Syntax error in parameters or arguments"
        return False
    else:
        if line[index] == ".":
            index += 1
            return domain(line)
        else:
            return True


def local_part(line):

    if not is_string(line, 0):
        print "501 Syntax error in parameters or arguments"
        return False
    else:
        return True


def name(line):
    global index
    #has to start with a letter
    #then go to letter digit string

    if not a(line[index]):
        return False
    index += 1
    if not let_dig_str(line, 0):
        return False

    return True


def let_dig_str(line, count):
    global index
    #check for let-dig
        #if not there, check how many times it has recursed:
            #if more than one, return true, else return false
    #if there, increment index and call let-dig-str again

    if let_dig(line[index + count]):
        count += 1
        return let_dig_str(line, count)

    else:
        index += count
        if count > 0:
            return True
        else:
            return False


def let_dig(character):
    global index

    if a(character) | d(character):
        return True
    else:
        return False


def is_string(line, count):
    global index
    #check for character
        #if there, increment count , call isString function again
        #if not, check to see count
            #if count is > 0, return true
            #else return false

    if char(line[index + count]):
        count += 1
        return is_string(line, count)
    else:
        index += count
        return count > 0


def char(character):
    return not special(character) and not sp(character)


def crlf(line):
    return "\n" in line or "\r" in line


def sp(character):
    return character.isspace()


def a(character):
    return character.isalpha()


def d(character):
    return unicode(character).isnumeric()


def special(character):
    valid = set('<>()[]\.,;:@"')
    return set(character).issubset(valid)


