from peewee import * 
import json
import cherrypy
import math

f=open('jfile.json',mode='r')
my_data=json.load(f)
f.close()
R = 6371000

db = SqliteDatabase('details.db')

class Detail(Model):
    id = TextField()
    loc = TextField()
    userId = TextField()
    description = TextField(null=True)
    price = IntegerField()
    status = TextField()

    class Meta:
        database = db


db.connect()
db.create_tables([Detail])

insert_query1 = Detail.insert(my_data).execute()


# for i in Detail.select().dicts():
#     lat2=Detail.loc[0]
#     print(lat2)
    

# for i in Detail.select().dicts():
    # print(i)      #to print every data in dictionary 
 
# for detail in Detail.select():
#     print(detail.loc)    #to print a specific data field 

# for i in Detail.select().order_by(Detail.price.desc()).dicts():
#     print(i)              #tp print desc sorted data by price

class USER_ID(object):
    @cherrypy.expose
    def index(self):
        return 'Hey There!'

    #Sorted Data
    @cherrypy.expose
    def getsorteddata(self,criteria='price'):
        sort=[]
        for i in Detail.select().order_by(criteria).dicts():
            sort.append(i)
        return json.dumps(sort)

    #for location and id search
    @cherrypy.expose
    def getitem(self,id=None,location=None):
        data_id =[]
        data_loc =[]
        for i in Detail.select().where(Detail.id == id).dicts():   
            data_id.append(i)   
        for j in Detail.select().where(Detail.loc == location).dicts():
            data_loc.append(j)
                        
        j_id = json.dumps(data_id)
        j_loc = json.dumps(data_loc)
        return j_id,j_loc

    # for status and userid search
    @cherrypy.expose
    def getitemlist(self,status=None,userid=None):
        data_status=[]
        data_userid=[]
        for i in Detail.select().where(Detail.status == status).dicts():
            data_status.append(i)
        for j in Detail.select().where(Detail.userId == userid).dicts():
            data_userid.append(j)
        j_status = json.dumps(data_status)
        j_userid = json.dumps(data_userid)
        return j_status,j_userid
 
    @cherrypy.expose
    def get_items_is_xy(self,xy=10,lat1=None, long1=None):
        distance_data=[]
        for i in Detail.select():
            lat2=Detail.loc[0]  #giving expression not a real number
            long2=Detail.loc[1]  #giving expression not a real number
            phi1 = math.radians(lat1)
            phi2 = math.radians(lat2)

            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(long1 - long2)

            a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2

            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

            meters = R * c
            km = meters / 1000.0

            for i in Detail.select().where(km <= xy).dicts():
                distance_data.append(i)
            jdata_km=json.dumps(distance_data)
        return jdata_km

if __name__ == "__main__":
    cherrypy.quickstart(USER_ID())




