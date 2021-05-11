from twilio.rest import Client
from datetime import datetime
import requests 
import json
def get_covid_vacination_alert(event=None, context=None):

    account_sid = '' 
    auth_token = '' 
    client = Client(account_sid, auth_token) 

    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    tdate = datetime.today().strftime('%d-%m-%Y')
    complete_message = ""

    pincodes = [416405]


    for pincode in pincodes:
        url_report = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}'.format(pincode, tdate)

        response = requests.get(url_report,headers=headers)
        if response.status_code !=200:
            print(response.text)
        report = json.loads(response.text.encode('utf8'))
        for centers in report["centers"]:
            message = "*Center Name:* " + centers["name"] + "\n"
            message = message+ "*Center Address:* "+ centers["address"] + "\n"

            sessionInfo = ""
            for session in centers["sessions"]:
                capacity = session["available_capacity"]
                if(capacity > 0):
                    sessionInfo = sessionInfo + "*Session Date:* "+ session["date"]+ "\n"
                    sessionInfo = sessionInfo+ "*Vaccine:* "+ session["vaccine"]+"\n"
                    sessionInfo = sessionInfo+ "*Min Age Limit:* "+ str(session["min_age_limit"])+"\n"
                    sessionInfo = sessionInfo+ "*Available Capacity:* "+ str(session["available_capacity"])+"\n"
                    slots = ""
                    for slot in session["slots"]:
                        slots = slots + slot+", "
                    sessionInfo = sessionInfo+ "*Slots:* "+slots +"\n\n\n"
            
            if sessionInfo:
                complete_message = complete_message + message + sessionInfo
                
    if complete_message:
        mobileNos = ['+918087574229' ]
        for mobileNo in mobileNos:
            client.messages.create( 
                                from_='whatsapp:+14155238886',  
                                body=complete_message,      
                                to='whatsapp:'+ mobileNo
                            )

if __name__ == "__main__":
    get_covid_vacination_alert()