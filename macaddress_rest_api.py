import boto3
import base64
from botocore.exceptions import ClientError
import requests
import json
import sys


def api_key_extractor():
    secret_name = "CiscoTask"
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)

    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return json.loads(secret)["api_key"]


api_url = "https://api.macaddress.io/v1?"
api_key = api_key_extractor()

#mac_address = "44:38:39:ff:ef:57"
#mac_address = str(sys.argv[1])
mac_address = str(raw_input("prompt"))

payload = {'apiKey': api_key , 'output': 'json','search':mac_address}

print "MAC Address Entered = " +str(mac_address)
for key,value in payload.items():
    api_url+=str(key)+"="+str(value)+"&"

api_url= api_url[:-1]
r= requests.get(api_url)

api_response = json.loads(r.text)

if api_response['vendorDetails']['companyName']=="":
    Company = "None"
    print "The MAC address does not belong to any registered block."
else :
    Company = api_response['vendorDetails']['companyName']
print "Company = " +str(Company)
