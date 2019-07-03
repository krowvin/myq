from myq import MYQ
myq = MYQ()
myq.login('email@gmail.com', 'password')

myq.open()
while(myq.get_state()!='open'):
    print(myq.get_state())
    time.sleep(5)
print(myq.get_state())
myq.close()
while(myq.get_state()!='closed'):
    print(myq.get_state())
    time.sleep(5)
