F5-NCM

This is a python module to assist in interacting with the BIG-IP Next Central Manager API

Initial Usage:

```
from next import NEXT
b = NEXT('ip/fqdn', 'username', 'password', session_verify=False)
irules = b.load('/api/v1/spaces/default/irules')
```