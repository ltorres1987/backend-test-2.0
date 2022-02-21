import requests


def main():

    res = requests.put('http://delivery-service:8000/status_change_tracking')
    if res:
        print('Response OK')
    else:
        print('Response Failed')

    print(res.status_code)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
