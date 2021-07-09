import requests
import re
import json
import uuid


def main():
    headerList = {
        'User-Agent': 'PostmanRuntime/7.26.8',
        'Connection': 'close',
        'Accept': 'gzip, deflate',
        'Postman-Token': str(uuid.uuid4())

    }
    instaName = 'shengkaitest'
    url = 'https://www.instagram.com/' + instaName

    result = getRespond(url, headerList)
    # result = verifyContent(result)
    # result = captureJsonString(result)
    # result = toJson(result)
    # edges = result['entry_data']['ProfilePage'][0]['graphql']['user']['edge_felix_video_timeline']['edges']
    # for i in edges:
    #     print(i['node']['shortcode'])
    print(result)
    return 0


def getRespond(url, headerList):
    result = requests.get(url, headers=headerList)
    # result = re.findall(r"window\._sharedData =.*;", result.text)
    return result.text


def verifyContent(data):
    return data[0] if len(data) > 0 else "Failed"


def captureJsonString(data):
    return data.split("= ")[1][:-1]


def toJson(data):
    return json.loads(data)


if __name__ == "__main__":
    main()