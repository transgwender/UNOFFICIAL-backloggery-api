from urllib import request, parse
import json

if __name__ == '__main__':
    data = { 'type': "load_user_library", 'username': "Drumble" }
    data = json.dumps(data)
    data = str(data)
    data = data.encode('utf-8')
    req =  request.Request("https://backloggery.com/api/fetch_library.php", data=data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    req.add_header('User-Agent', 'UnofficialAPI/0.0.1 (dev[at]gwenkornak.ca)')
    req.add_header('If-Modified-Since', 'Thu, 05 Jun 2025 04:14:34 GMT')
    resp = request.urlopen(req)
    result = json.loads(resp.read().decode('utf-8'))
    pass
