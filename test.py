import requests

response = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=University%20of%20UCLA&inputtype=textquery&fields=name,geometry&key=AIzaSyDW2jyW0oHvmMnobFbSNeTlLMVaYSUVpBw')
print(response)
print(response.json())

