import pyrebase
from datetime import datetime
import json
import pandas as pd

config={
"apiKey": "AIzaSyCDAGglBwh-7NEU4lAFTS7f5tbGacUXdMA",
  "authDomain": "kvh-proj.firebaseapp.com",
  "projectId": "kvh-proj",
  "storageBucket": "kvh-proj.appspot.com",
  "messagingSenderId": "348476571342",
  "appId": "1:348476571342:web:9aa8f6c522c33a2f171a9f",
  "measurementId": "G-FW36366BN7",
  "databaseURL": "https://kvh-proj-default-rtdb.firebaseio.com"
}
db=pyrebase.initialize_app(config)
rl_db=db.database()
im_db=db.storage()

#Setting Values to Table in Database

inc_time=datetime.now()
inc_time=inc_time.strftime("%H:%M:%S")
key=str(rl_db.generate_key())
img_url=key[1:]+".jpg"
rl_db.child("incidents").child(key).set({'incident_type':'abuse','incident_time':inc_time,'img_url':img_url,'cam_id':"x2"})


#HTML Read Database Table entry and Display it as Table
'''
vals=rl_db.child("incidents").get().val()
loc_vals=rl_db.child("location").get().val()
tmp={}
tmp['IncidentId']=[]
tmp['IncidentType']=[]
tmp['CamId']=[]
tmp['District']=[]
tmp['Latitude']=[]
tmp['Longitude']=[]
tmp['Time']=[]
for i in vals:
    #print(i)
    #print(vals[i])
    #print(loc_vals[vals[i]['cam_id']])
    tmp["IncidentId"].append(i)
    tmp["IncidentType"].append(vals[i]["incident_type"])
    tmp["CamId"].append(vals[i]['cam_id'])
    tmp["Time"].append(vals[i]['incident_time'])
    tmp["District"].append(loc_vals[vals[i]['cam_id']]['district'])
    tmp["Latitude"].append(loc_vals[vals[i]['cam_id']]['latitude'])
    tmp["Longitude"].append(loc_vals[vals[i]['cam_id']]['longitude'])
df=pd.DataFrame(tmp)
json_recs=df.reset_index().to_json(orient='IncidentId')
data=json.loads(json_recs)
print(df)'''

##Images from Database

#store images using
'''im_db.child("images/"+inc_id+".jpg").put(path.local)'''
#Extracting images From Database

'''
image_name="NRI4kuLIRgmnvrOpGeU1.jpg"
link=f"https://firebasestorage.googleapis.com/v0/b/kvh-proj.appspot.com/o/images%2F"+image_name+"?alt=media&token=2f5b7de6-16bc-47fd-9695-a5865840eebf"
print(link)
'''