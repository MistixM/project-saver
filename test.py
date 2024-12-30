import requests
import sys

def main():
    a = 2
    b = 3

    print(a + b)

if __name__ == "__main__":
    url = 'https://mistixm.pythonanywhere.com/request_access'
    request = requests.post(url, json={"api": "gfgfgs"}).status_code

    if not request == 200:
        sys.exit("Not allowed. Contact with mdev: https://mdev.uk.to")

    main()