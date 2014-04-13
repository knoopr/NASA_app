import json
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
from re import match
import sqlite3

class Data_Grabber:
    def __init__ (self):
        self.data = None

    def Read_file(self):
        # TODO Fix, this is lazy. Now it's super-lazy due to panicked last-minute integration
        try:
            # Path on heroku
            with open("neovi/sunburst/static/sunburst/json/qlt5pn3.txt", "r") as fp:
                json_Data = json.load(fp)
        except IOError:
            try:
                # Path on localhost loaded in django context
                with open("sunburst/static/sunburst/json/qlt5pn3.txt", "r") as fp:
                    json_Data = json.load(fp)
            except IOError:
                # Path when executing main method
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
    def __init__(self, heirJson=None):
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
        json = """{"name":"Near Earth Objects", "children":["""
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
            
            if element["q"] < .0025:
                the_Distance = "0 < .0025"
            elif element["q"] < .005:
                the_Distance = ".0025 < .005"
            elif element["q"] < .0075:
                the_Distance = ".005 < .0075"
            elif element["q"] < .01:
                the_Distance = ".0075 < .01"
            elif element["q"] > .01:
                the_Distance = ".01 > "
            
                    
            sql = "INSERT OR REPLACE INTO NEO VALUES (%d, '%s', '%s', '%s','%s')"% (the_Century, element["spec"], the_Distance, the_Size, element["full_name"])
            operator.execute(sql)
        
        
        centuries = database.cursor()
        spectrometer = database.cursor()
        asteroid_Sizes = database.cursor()
        for century in centuries.execute("SELECT DISTINCT CENTURY FROM NEO"):
            json+= """\n{"name":"%s's", "feature":"discovery", "children":["""%century[0]
            for spec in spectrometer.execute("SELECT DISTINCT SPEC FROM NEO WHERE CENTURY=%d" %century[0]):
                json += """\n{"name":"%s-type", "feature":"spectra", "children":["""%spec[0]
                for size in asteroid_Sizes.execute("SELECT DISTINCT SIZE FROM NEO WHERE CENTURY=%d AND SPEC='%s'" %(century[0], spec[0])):
                    json += """\n{"name":"%s", "feature":"size", "children":[\n"""%size[0]
                    for asteroid in operator.execute("SELECT AU, COUNT(*) FROM NEO WHERE CENTURY=%d AND SPEC='%s' AND SIZE='%s'" %(century[0], spec[0], size[0])):
                        json += """{"name":"%s", "feature":"distance", "number":%s},\n"""%(asteroid[0], asteroid[1])
                    json = json[:-2]
                    json += "\n]},"
                json = json[:-1]
                json += "\n]},"
            json = json[:-1]
            json += "\n]},"
        json = json[:-1]
        json += "\n]}"
        
        print (json)
        self.hierJson = json

        operator.close()
        database.close()

if __name__ == "__main__":
    Parser()

