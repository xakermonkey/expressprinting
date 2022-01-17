import cups

def set_pswd(promt):
    return "print"


def set_connection_cups():
    cups.setServer("cupsd")
    cups.setPort(631)
    cups.setEncryption(cups.HTTP_ENCRYPT_IF_REQUESTED)
    cups.setUser("print")
    cups.setPasswordCB(set_pswd)
    con = cups.Connection()
    return con