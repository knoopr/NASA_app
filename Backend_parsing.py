import json

class Data_Grabber:
    def __init__ (self):
        self.data = None

    def Read_file(self):
        with open("qlt5pn3.txt", "r") as fp:
            json_Data = json.load(fp)
            return json_Data

    def Request_json(self):
        print "json request"




class Parser:
    def __init__(self):
        self.Grab_data()

    def Grab_data(self):
        the_Data = Data_Grabber().Read_file()
        average_Q = 0
        for element in the_Data:
            average_Q += element["q"]
        average_Q /= len(the_Data)-1
        print average_Q



if __name__ == "__main__":
    Parser()

