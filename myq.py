import requests
# Written By: Krowvin
# Dated: 7/3/2019
# Rev: 0.1
# Tons of help from this
# https://github.com/arraylabs/pymyq/blob/master/pymyq
# This is essentially a dumbed down version of the pymyq library so that I could understand it and to
# remove ASYNC for use with QT


class MYQ:
    def __init__(self):
        # Default APPID For all chamberlain devices
        self.app_id = 'NWknvuBd7LoFHfXmKNMBcgajXtZEgKUh4V7WNzMidrpUUluDpVYVZx+xT4PCM5Kx'
        self.email = None
        self.passw = None
        self.device_id = None
        self.user_agent = "Chamberlain/3.73"
        self.domain = 'https://myqexternal.myqdevice.com'
        self.login_endpoint = "api/v4/User/Validate"
        self.device_list_endpoint = "api/v4/UserDeviceDetails/Get"
        self.device_status_endpoint = "api/v4/DeviceAttribute/getDeviceAttribute"
        self.device_set_endpoint = "api/v4/DeviceAttribute/PutDeviceAttribute"
        self.state = 'unknown'
        self.state_names = {
            1: 'open',
            2: 'closed',
            3: 'stopped',
            4: 'opening',
            5: 'closing',
            6: 'unknown',
            7: 'unknown',
            8: 'transition',
            9: 'open',
            0: 'unknown'
        }
        # Security Token for access to API - acquired through login()
        self.token = None

    def login(self, username, password):
        headers = {
            'MyQApplicationId': self.app_id,
            'User-Agent'      : self.user_agent
            }
        # Post to get sec token
        credentials = {
            'username': username,
            'password': password
            }

        r = requests.post(self.domain + '/' + self.login_endpoint, headers=headers, json=credentials)
        status = r.status_code
        if status == 200:
            self.token = r.json()['SecurityToken']
            print("Token Acquired:", self.token)
            print("Login Successful!")
        else:
            print("Failed to get Token:")
            print(r.text)
            print("Status:", status)

    def get_details(self):
        if self.is_logged_in():
            headers = {
                'MyQApplicationId': self.app_id,
                'User-Agent'      : self.user_agent,
                'securityToken'   : self.token
                }
            r = requests.get(self.domain + '/' + self.device_list_endpoint, headers=headers)
            status = r.status_code
            if status == 200:
                #print(status)
                #print(r.json())
                print("Detail Retrieved")
            else:
                print("Failed to fetch details - Status Code:", status)
            return r.json()

    def is_logged_in(self):
        if self.token:
            return True
        else:
            print("You must call login(username, password) before accessing details")
            print("Example:")
            print("myq=MYQ()")
            print('myq.login("mysuperemail@gmail.com", "secretpassword69")')
            print('myq.open()')
            return False

    def open(self):
        if self.device_id:
            headers = {
                'MyQApplicationId': self.app_id,
                'User-Agent'      : self.user_agent,
                'securityToken'   : self.token
                }
            json = {
                'attributeName' : 'desireddoorstate',
                'myQDeviceId'   : self.device_id,
                'AttributeValue': 1,
                }
            r = requests.put(self.domain + '/' + self.device_set_endpoint, json=json, headers=headers)
            status = r.status_code
            if status == 200:
                print(status)
                print(r.text)
                print(r.json())
            else:
                print("Failed to fetch details - Status Code:", status)
            return r.json()
        else:
            print("No Device ID Found!")
            self.update_garage_details()
            self.open()

    def close(self):
        if self.device_id:
            headers = {
                'MyQApplicationId': self.app_id,
                'User-Agent'      : self.user_agent,
                'securityToken'   : self.token
                }
            json = {
                'attributeName' : 'desireddoorstate',
                'myQDeviceId'   : self.device_id,
                'AttributeValue': 0,
                }
            r = requests.put(self.domain + '/' + self.device_set_endpoint, json=json, headers=headers)
            status = r.status_code
            if status == 200:
                print(status)
                print(r.text)
                print(r.json())
            else:
                print("Failed to fetch details - Status Code:", status)
            return r.json()
        else:
            print("No Device ID Found!")
            self.update_garage_details()

    def toggle(self):
        # Return JSON of open or close request

        # Update device ID and device state
        self.update_garage_details()
        if self.state == 'closed':
            return self.open()
        elif self.state == 'open':
            return self.close()
        else:
            print("State is", self.state)
            print("Could not toggle the door.")
            return None

    def update_garage_details(self):
        details = self.get_details()
        devices = details['Devices']
        door_count = 0
        for device in devices:
            if device['MyQDeviceTypeName'] == 'GarageDoorOpener':
                # Update device ID
                self.device_id = device['MyQDeviceId']
                for attr in device['Attributes']:
                    # Update the door state
                    if attr['AttributeDisplayName'] == 'desc':
                        print("Description:", attr['Value'])
                    if attr['AttributeDisplayName'] == 'doorstate':
                        print("Door State:", self.state_names[int(attr['Value'])])
                        self.state = self.state_names[int(attr['Value'])]
                print("GarageDoorOpener ID Acquired: ", self.device_id)
                door_count += 1
        if door_count > 1:
            print("I discovered more than one garage door opener, i'll save the last one in the data set")

    def get_state(self):
        self.update_garage_details()
        return self.state
