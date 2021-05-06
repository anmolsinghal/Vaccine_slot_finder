import requests
from datetime import date,datetime,timedelta
import os
import smtplib
from time import time,ctime,sleep
import pdb

def parse_json(result):
    output = []
    centers = result['centers']
    for center in centers:
        sessions = center['sessions']
        for session in sessions:
            if session['available_capacity'] > 0:
                res = { 'name': center['name'], 'block_name':center['block_name'],'age_limit':session['min_age_limit'], 'vaccine_type':session['vaccine'] , 'date':session['date'],'available_capacity':session['available_capacity'] }
                output.append(res)
    return output
def call_api(district,date):
    
    d1 = date.strftime("%d/%m/%Y")

    date = str(d1).replace("/","-")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + str(district)+ "&date="+ date
    print(api)
    response = requests.get(api,headers = headers)
    

    if response.status_code == 200:
        result = response.json()
        output = parse_json(result)
        result_str = ""
        if len(output) > 0:
            for center in output:
            
                if center['age_limit'] <=23 and center['available_capacity'] > 0:
                    result_str = result_str + "Available at\n"
                    result_str = result_str + center['name'] + "\n"
                    result_str = result_str + "block:"+center['block_name'] + "\n"
                    result_str = result_str + "vaccine count:"+str(center['available_capacity']) + "\n"
                    result_str = result_str + "vaccine type:"+ center['vaccine_type'] + "\n"
                    result_str = result_str + center['date'] + "\n"
                    result_str = result_str + "age_limit:"+str(center['age_limit'])+"\n"
                    result_str = result_str + "-----------------------------------------------------\n"

        return result_str
    else:
        return -1

def run():
    print(ctime(time()))
    result_str = ""
    for district in [108, 187,496]:
        for date in [datetime.today() + timedelta(days=x) for x in range(1,7)]:
            #print('Checking for '+str(district)+' on '+str(date))
            ret= call_api(district,date)
            result_str = result_str+str(ret)
    if '"Available at'in result_str:
    	a = 0
    	while a<10:
    	    a = a+1
    	    os.system('spd-say "Vaccine found"')
    else:
        os.system('spd-say "Vaccine not found"')
    print(result_str)

t = datetime.now()    
minutes= 5
if __name__=="__main__":
    run()
    while True:
        delta = datetime.now()-t
        if delta.seconds >= minutes * 60:
            run()
            t = datetime.now()
