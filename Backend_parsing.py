import json
from urllib2 import urlopen
from re import match
import sqlite3

class Data_Grabber:
    def __init__ (self):
        self.data = None

    def Read_file(self):
        with open("qlt5pn3.txt", "r") as fp:
            json_Data = json.load(fp)
            return json_Data

    def Request_json(self, request, url="http://www.asterank.com/api/asterank?query="):
        query = "{"
        request_Elements = request.replace(" ", "").split(",")
        for element in request_Elements:
            if element == "" :
                break
            elif ">=" in element:
                variable, value = element.split(">=")
                if query != "{":
                    query += ','
                query += '"' + variable + '":' + """{"$gte":""" + str(value) + "}"
            elif ">" in element:
                variable, value = element.split(">")
                if query != "{":
                    query += ','
                query += '"' + variable + '":' + """{"$gt":""" + str(value) + "}"
            elif "<=" in element:
                variable, value = element.split("<=")
                if query != "{":
                    query += ','
                query += '"' + variable + '":' + """{"$lte":""" + str(value) + "}"
            elif "<" in element:
                variable, value = element.split("<")
                if query != "{":
                    query += ','
                query += '"' + variable + '":' + """{"$lt":""" + str(value) + "}"
            elif "=" in element:
                variable, value = element.split("=")
                if query != "{":
                    query += ','
                query += '"' + variable + '":' + """{"$e":""" + str(value) + "}"
        query += "}"
        get_Request = url + query + "&limit=1000"
        json_Data = json.load(urlopen(get_Request))
        return json_Data






class Parser:
    def __init__(self):
        self.Grab_data()

    def Grab_data(self):
        #the_Data = Data_Grabber().Request_json("q>=1")
        the_Data = Data_Grabber().Read_file()
        """average_Q = 0
        for element in the_Data:
            average_Q += element["q"]
        average_Q /= len(the_Data)
        print average_Q"""
        self.config_Output(the_Data)

    def config_Output(self, the_Data):
        total_Q = 0
        
        database = sqlite3.connect("Asteroid.db")
        database.text_factory = str
        operator = database.cursor()
        operator.execute("CREATE TABLE IF NOT EXISTS NEO(CENTURY, SPEC, AU, SIZE, NAME UNIQUE)")
        
        for element in the_Data:
            if match("^17[0-9]{2}",element["first_obs"]) != None:
                the_Century = 1700
            elif match("^18[0-9]{2}",element["first_obs"]) != None:
                the_Century = 1800
            elif match("^19[0-9]{2}",element["first_obs"]) != None:
                the_Century = 1900
            elif match("^20[0-9]{2}",element["first_obs"]) != None:
                the_Century = 2000
    
            if element["diameter"] == "":
                the_Size = "unknown"
            elif element["diameter"] > 100:
                the_Size = "large"
            elif element["diameter"] > 15:
                the_Size = "medium"
            else:
                the_Size = "small"
                    
            sql = "INSERT OR REPLACE INTO NEO VALUES (%d, '%s', %s, '%s','%s')"% (the_Century, element["spec"], element["q"], the_Size, element["full_name"])
            operator.execute(sql)

        operator.execute("SELECT * FROM NEO")
        string = operator.fetchall()
        print string

        operator.close()
        database.close()

if __name__ == "__main__":
    Parser()

