import json
import boto3
from pprint import pprint
from urllib.request import urlopen


url = 'https://api.spacexdata.com/v3/launches'

json_url = urlopen(url)
text = json.loads(json_url.read())

dynamo_list = []
i = 0
while i < len(text):
    for item in text:
        main_dc = {}
        main_dc['Mission Name'] = text[i]['mission_name']
        main_dc['Launch Year'] = text[i]['launch_year']
        main_dc['Country'] = text[i]['rocket']['second_stage']['payloads'][0]['nationality']
        main_dc['Device'] = text[i]['rocket']['second_stage']['payloads'][0]['payload_type']
        main_dc['Customers'] = text[i]['rocket']['second_stage']['payloads'][0]['customers']
        main_dc['Launch_Success'] = text[i]['launch_success']
        if text[i]['launch_success'] == False:
            main_dc['Failure Reason'] = text[i]['launch_failure_details']['reason']
        dynamo_list.append(main_dc)
        i += 1

print(dynamo_list)

dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
table = dynamodb.Table('space_x')
for i in range(0,len(dynamo_list)):
    table.put_item(Item=dynamo_list[i])
