import cherrypy
import json
from operator import itemgetter
import math

f=open('jfile.json',mode='r')
my_data=json.load(f)
f.close()
R = 6371000

class USER_ID(object):

    # default function 
    @cherrypy.expose 
    def index(self): 
        return 'Hello! how are you ?'

    # sorted data by price
    @cherrypy.expose
    def getsorteddata(self,reverse=True, criteria='price'):
        new_data=sorted(my_data,key=itemgetter(criteria),reverse=reverse)
        jdata = json.dumps(new_data)
        return jdata

    # Id - getitem?id=AAsm & Location - getitem?location=AAsm
    #location NOT WORKING
    @cherrypy.expose
    def getitem(self,id=None,location=None):
        data_id = []
        data_loc = []
        for i in my_data:   
            for key in i:          
                if(location == None):
                    if(i[key] == id):
                        data_id.append(i)                        
                else:
                    if(i[key] == location):
                        data_loc.append(i)
        j_id = json.dumps(data_id)
        j_loc = json.dumps(data_loc)
        return j_id,j_loc
  
    # Status - getitemslist?status=AAsm & getitemslist?userid=AAsm
    @cherrypy.expose
    def getitemlist(self,status=None,userid=None):
        data_status = []
        data_uid = []
        for i in my_data:   
            for key in i:
                if(status == None):
                    if(i[key] == userid):
                        data_uid.append(i)
                else:
                    if(i[key] == status):
                        data_status.append(i)
        j_uid = json.dumps(data_uid)
        j_status = json.dumps(data_status)
        return j_status,j_uid

    # get_items_in_radius?radius=xy&latitude=xx&longitude=yy
    @cherrypy.expose
    def get_items_in_xy(self, xy=10, lat1=37.37657636848912, long1=-121.92350465218554):
        distance_data = []
        for lst in my_data:
            
            latlong = lst['loc']
            lat2 = latlong[0]
            long2 = latlong[1] 
            phi1 = math.radians(lat1)
            phi2 = math.radians(lat2)

            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(long1 - long2)

            a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2

            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

            meters = R * c
            km = meters / 1000.0

            if(km <= xy):
                distance_data.append(lst)
            jdata_km = json.dumps(distance_data)
        return jdata_km


if __name__ == "__main__":
    cherrypy.quickstart(USER_ID())