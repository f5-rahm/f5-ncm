# F5-NCM
A python module for working with the BIG-IP Next Central Manager API

Getting Started:

```
from next import Next
b = Next('ip/fqdn', 'username', 'password', session_verify=False)
irules = b.load('/api/v1/spaces/default/irules')
```

Method mapping:

| HTTP Method | F5-NCM Method |
| --- |---------------|
| GET | load          |
| POST | create        |
| PUT | update        |
| PATCH | modify |
| DELETE | delete |

This is lightweight session management and the onus is on the user to know the API calls needed. 

For common tasks, utility functions will be added such as:

```angular2html
from next import Next
from utils.devices import get_devices
b = Next('172.16.2.105', 'username', 'password', session_verify=False)
devices = get_devices(b)
for device in devices:
    print(f"Host: {device.get('hostname')}, Addr: {device.get('address')}, ID: {device.get('id')}")
    
Host: next-vmp-1, Addr: 172.16.2.161, ID: a4148c93-5306-4605-b8bb-92d6b1f78c26
Host: next-vmp-2, Addr: 172.16.2.162, ID: 73504686-3ea1-4593-a76f-1ab8f567f152
```