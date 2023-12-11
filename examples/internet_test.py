import urllib.request

def connect(host="https://google.com"):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

print( "connected" if connect() else "No internet")
