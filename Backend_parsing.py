import json
from urllib2 import urlopen
from re import match

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
        eighteenth_Century = []
        nineteenth_Century = []
        twentieth_Century = []
        twentyfirst_Century = []
        
        json = """{
                        "name":"NEO",
                        "children"[
                                {"""

        #century size i.e. es = eighteenth centruy small
        es = ""
        em = ""
        el = ""
        eu = ""
        ns = ""
        nm = ""
        nl = ""
        nu = ""
        ts = ""
        tm = ""
        tl = ""
        tu = ""
        fs = ""
        fm = ""
        fl = ""
        fu = ""
        

        for element in the_Data:
            if match("^17[0-9]{2}",element["first_obs"]) != None:
                if element["diameter"] == "":
                    eu += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                elif element["diameter"] >100:
                    el += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                elif element["diameter"] > 15:
                    em += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                else:
                    es += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
            elif match("^18[0-9]{2}",element["first_obs"]) != None:
                if element["diameter"] == "":
                    nu += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                elif element["diameter"] >100:
                    nl += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                elif element["diameter"] > 15:
                    nm += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                else:
                    ns += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
            elif match("^19[0-9]{2}",element["first_obs"]) != None:
                if element["diameter"] == "":
                    tu += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                elif element["diameter"] >100:
                    tl += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                elif element["diameter"] > 15:
                    tm += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                else:
                    ts += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
            elif match("^20[0-9]{2}",element["first_obs"]) != None:
                if element["diameter"] == "":
                    fu += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                elif element["diameter"] >100:
                    fl += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                elif element["diameter"] > 15:
                    fm += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
                else:
                    fs += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])




if __name__ == "__main__":
    Parser()

