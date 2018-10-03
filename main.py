import json
import time
import urllib.request
# from win10toast import ToastNotifier
import webbrowser
import onesignal as onesignal_sdk

pageUrl = "https://www.roblox.com/catalog/json?Category=2&Subcategory=2&SortType=3&Direction=2&PageHash" \
          "=0e4ba52b8fb2ab17f924d1fdc696e22d "

knownItems = []
currentNotify = None

onesignal_client = onesignal_sdk.Client(user_auth_key="ZTgwMzI1MjUtNjM5Yi00MTdkLWE4ODgtYjRlMWY4MGU2NTlj",
                                        app={"app_auth_key": "ODMyYjcxYmEtMjI3Yi00NTNmLTllODctNjYwNjg2NTcyMjBh",
                                             "app_id": "0c25cbfd-3b76-4d31-bb5e-0febcef8a3b2"})


def getLimiteds():
    page = urllib.request.urlopen(pageUrl).read()
    data = json.loads(page)

    # with open('catalog.json') as f:
    #     data = json.load(f)

    limiteds = []
    for x in data:
        if x["Remaining"] == "":
            continue
        remaining = int(x["Remaining"])
        if remaining > 0:
            limiteds.append(x)

    return limiteds


def click():
    webbrowser.open_new(currentNotify["AbsoluteUrl"])


def main():
    items = getLimiteds()

    for x in items:
        known = False
        for y in knownItems:
            if x["Name"] == y["Name"]:
                known = True
                break
        if not known:
            knownItems.append(x)
            print(x["Name"])

            global currentNotify
            currentNotify = x

            new_notification = onesignal_sdk.Notification(contents={"en": x["Name"]})
            new_notification.set_parameter("headings", {"en": "New "+x["LimitedAltText"]})

            new_notification.set_included_segments(["Active Users"])

            onesignal_response = onesignal_client.send_notification(new_notification)
            # ToastNotifier().show_toast(x["Name"], "New Limited!", icon_path=None, duration=5, threaded=True,
            #                           callback_on_click=click)

    return


while True:
    time.sleep(2)
    main()
