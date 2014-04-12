class Data_Grabber:
    def __init__ (self):
        self.data = None

    def Read_file(self):
        print "file"

    def Request_json(self):
        print "online"


class Parser:
    def __init__(self):
        self.Grab_data()

    def Grab_data(self):
        print "grab"


if __name__ == "__main__":
    Parser()

