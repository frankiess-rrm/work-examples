
a = {'x': {'package': 'x', 'description': 'y'}, 'c': {'package2': 'c', 'description': 'd'}}

# gets package names
# so = open('status', 'r', encoding="utf8")
# solist = so.readlines()
# for line in solist:
#     packagelist = []
#     if line.find('Package:') != -1:
#         packagelist.append(line.rstrip('\n'))
# so.close()
# turn packages into links
# add this to index.html
# with a welcome message

'''
how to insert rdependencies line into list:
go to (Package 1 dependency package) and add rdependency Package 1

create loop that grabs package name for url name for html file
grabs name, description, dependencies, rdependencies information
as well, adds into html file
'''

# so = open('status', 'r', encoding="utf8")
# solist = so.readlines()
# for line in solist:
#     packagelist = []
#     if line.find('Package:') != -1:
#         packagelist.append(line.rstrip('\n'))
# so.close()
#
# so = open('status', 'r', encoding="utf8")
# sostring = so.read()
# so.close()
# sostring2 = sostring.replace('Package:', 'xyzxyzyz43Package:')
# solist = sostring2.split('xyzxyzyz43')

so = open('status', 'r', encoding="utf8")
sostring = so.readlines

'''
if line [0] == 'Package:'
    add new key to dict
    add others under this key

if not line[0] == ' '
if the first char is not a space

'''