# native imports
import urllib.request
import urllib.error

# third-party imports
import requests

# custom imports


def checkConnectivity():
    '''
    check for internet connectivity, in order to be able to request API data
    '''
    try:
        urllib.request.urlopen("http://www.google.com", timeout=1)
        return True
    except urllib.error.URLError:
        return False

def requestAPI(path):
    response = requests.get("https://engineering-task.elancoapps.com/api/"+path)
    
    if (response.status_code == 200):
        return response.json()
    else:
        return False