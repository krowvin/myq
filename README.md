# myq
Python wrapper for Chamberlain MYQ API

## Dependencies
* requests
```python -m pip install requests```

## How Tos
### Login
```python
from myq import MYQ
myq = MYQ()
myq.login('myemail@gmail.com', 'mypassword')
```
### Open / Close
```python
myq.close()
myq.open()
```
### Toggle!
```python
myq.toggle()
```

### Full Example
```python
from myq import MYQ
import time
myq = MYQ()
# Change these to your MYQ Login
myq.login('email@gmail.com', 'password')
print(myq.get_state())
# Open the door
myq.open()
# Print the state until it is considered open, this could make an infinite loop - it's for example use only
while(myq.get_state()!='open'):
    print(myq.get_state())
    time.sleep(5)
print(myq.get_state())
myq.close()
while(myq.get_state()!='closed'):
    print(myq.get_state())
    time.sleep(5)
```

## Door States
```python
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
```
## Complete List of Methods
method(args) -> returntype
* login(username:str, password:str) -> None
* get_details() -> list
* is_logged_in() -> bool
* open() -> list
* close() -> list
* toggle() -> list
* update_garage_details() -> None
* get_state() -> str

## Future additions
* Code for checking if a token has expired - It's possible if the user keeps the myq object alive long ehough the token would expire and a request could fail. One thought is to assign a timestamp with the token and if the current date is beyond the limit, login again with a new timestamp
## Credits
Special thanks to Arraylabs, I borrowed the API calls and state numbers from their code. Saved me a bunch of legwork with WireShark. 
Checkout the pymyq here: https://github.com/arraylabs/pymyq
