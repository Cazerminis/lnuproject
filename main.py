from network import WLAN
import urequests as requests
import machine
import time
import keys #import the keys file
import urequests #for some reason I have to do this one as well or things won't work

#Read hardware
adc = machine.ADC()
apin = adc.channel(pin='P16')


#Ubidots
TOKEN = keys.Ubidots
DELAY = 60  # Delay in seconds

wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.INT_ANT)
wlan.connect(ssid=keys.WIFI_NAME, auth=(WLAN.WPA2, keys.WIFI_PASS)) 
while not wlan.isconnected ():
    machine.idle()
print("Connected to Wifi\n")


#Builds the json to send the request
def build_json(variable1, value1):
    try:
        data = {variable1: {"value": value1}}
        return data
    except:
        return None

#Sends the request to ubidots to store data
def post_var(device,value1):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        data = build_json("Grader", value1)
        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
            pass
    except:
        pass

#Send IFTTT notification on phone
def send_warning(grader):
        try:  
            tempUrl="https://maker.ifttt.com/trigger/{triggerword}/with/key/{webhookskey}"      # remove "{}"
            if(grader>9):
                print("high temp")
                res = urequests.post(url=tempUrl, json={"value1": grader})         
                return res.json(),c      
            else:
                pass
        except:
            pass

while True:
    millivolts = apin.voltage()
    celsius = (millivolts - 500.0) / 10.0
    post_var("pycom",celsius)
    send_warning(celsius)
    time.sleep (DELAY)
