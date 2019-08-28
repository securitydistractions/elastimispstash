import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pymemcache.client.base import Client
import json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

client = Client(('127.0.0.1', 11211)) #assumes local memcached application, if needed change this to suit your installation

def misppull(dataType):
  headers={'Authorization':'****INSERTYOURMISPAPIKEYHERE****','Accept':'application/json','Content-type':'application/json'}
  data=json.dumps({"returnFormat":"json","type":dataType,"tags":"Feed-%","to_ids":"yes","includeEventTags":"yes","includeContext":"yes"})
  response = requests.post('https://****INSERTYOURMISPADDRESSHERE****/attributes/restSearch',headers=headers,data=data,verify=False)
  return response


if __name__ == '__main__':
  dataTypes={'domain', 'ip-%', 'md5', 'sha1','sha256'}
  for dt in dataTypes:
    response = misppull(dt)
    data=response.json()
    if data:
      for item in data["response"]["Attribute"]:
        tagList=[]
        for tag in item['Tag']:
            for k,v in tag.items():
                if(k=='name' and 'Feed-' in tag['name']):
                     tagList.append(str(v))
            client.set(str(item['type'] + '-' + item['value']), tagList, 130)
