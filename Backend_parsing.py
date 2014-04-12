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
        
        """
        for element in the_Data:
            if match("^17[0-9]{2}",element["first_obs"]) != None:
                if element["spec"] in eighteenth_Century:
                    eighteenth_Century[element["spec"]].append(element)
                else:
                    eighteenth_Century[element["spec"]] = []
                    eighteenth_Century[element["spec"]].append(element)
            elif match("^18[0-9]{2}",element["first_obs"]) != None:
                if element["spec"] in nineteenth_Century:
                    nineteenth_Century[element["spec"]].append(element)
                else:
                    nineteenth_Century[element["spec"]] = []
                    nineteenth_Century[element["spec"]].append(element)
            elif match("^19[0-9]{2}",element["first_obs"]) != None:
                if element["spec"] in twentieth_Century:
                    twentieth_Century[element["spec"]].append(element)
                else:
                    twentieth_Century[element["spec"]] = []
                    twentieth_Century[element["spec"]].append(element)
            elif match("^20[0-9]{2}",element["first_obs"]) != None:
                if element["spec"] in twentyfirst_Century:
                    twentyfirst_Century[element["spec"]].append(element)
                else:
                    twentyfirst_Century[element["spec"]] = []
                    twentyfirst_Century[element["spec"]].append(element)"""


        for element in the_Data:
            if match("^17[0-9]{2}",element["first_obs"]) != None:
                eighteenth_Century.append(element)
            elif match("^18[0-9]{2}",element["first_obs"]) != None:
                nineteenth_Century.append(element)
            elif match("^19[0-9]{2}",element["first_obs"]) != None:
                twentieth_Century.append(element)
            elif match("^20[0-9]{2}",element["first_obs"]) != None:
                twentyfirst_Century.append(element)



        json += """"name":"18th Century",
            "children":["""
        for element in eighteenth_Century:
        #json += """{"name":""" + '"' + element["name"] + '"' + ""","Perihelion":""" + '"' + element["q"]  + '"' """}"""
            json += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
        json += ']}'
        json += """"name":"19th Century",
            "children":["""
        for element in nineteenth_Century:
            json += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
        json += ']}'
        json += """"name":"20th Century",
            "children":["""
        for element in twentieth_Century:
            json += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
        json += ']}'
        json += """"name":"21st Century",
            "children":["""
        for element in twentyfirst_Century:
            json += """{"name":"%s","Perihelion":"%s"}"""% (element["name"], element["q"])
        json += ']}]}}'

        print json






if __name__ == "__main__":
    Parser()

