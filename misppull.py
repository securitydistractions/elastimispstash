import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pymemcache.client.base import Client
import json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


## The following settings are for your memcached installation.
## Update them to fit your installation.
MEMCACHED_HOST = '127.0.0.1'
MEMCACHED_PORT = 11211

## The following settings are for your MISP installation.
## Update them to fit your installation
MISP_URL = 'https://****INSERTYOURMISPADDRESSHERE****/attributes/restSearch'
MISP_API_KEY = '****INSERTYOURMISPAPIKEYHERE****'

client = Client((MEMCACHED_HOST, MEMCACHED_PORT))

def misppull(dataType):
  headers={'Authorization':MISP_API_KEY,'Accept':'application/json','Content-type':'application/json'}
  data=json.dumps({"returnFormat":"json","type":dataType,"tags":"Feed-%","to_ids":"yes","includeEventTags":"yes","includeContext":"yes"})
  response = requests.post(MISP_URL,headers=headers,data=data,verify=False)
  return response


if __name__ == '__main__':
  dataTypes={'domain', 'ip-%', 'md5', 'sha1','sha256'}
  for dt in dataTypes:
    response = misppull(dt)
    data=response.json()
    if 'response' in data:
      for item in data["response"]["Attribute"]:
        tagList=[]
        for tag in item['Tag']:
          for k,v in tag.items():
            if(k=='name' and 'Feed-' in tag['name']):
              tagList.append(str(v))
        client.set(str(item['type'] + '-' + item['value']), tagList, 130)
