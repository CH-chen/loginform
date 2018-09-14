import re


# r = re.compile(r'^1[3|4|5|6|7|8|9][0-9]{9}$')
r = re.compile(r'^1[3-9][0-9]{9}$')
print(r.match("122222222222222"))
print(r.match("185aaaaaaaaa"))
print(r.match("18599999999"))
print(r.match("1a536303630"))
print(r.match("12536303630"))
print(r.match("185363036300"))