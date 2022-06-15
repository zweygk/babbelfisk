import requests

def main():
    
    sentence = "What's up, doc?"

    http_request_url = 'http://127.0.0.1:5002/'
    data = {
        'sentence': sentence
    }
    header = {'Content-Type': 'application/json'}

    r = requests.post(http_request_url, json=data, headers=header)

    print(r.json())


if __name__ == "__main__":
    main()
