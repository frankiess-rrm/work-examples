import re
emodict = {}

so = open('status', 'r', encoding="utf8")
statusfile_list = so.readlines()
so.close()

packname_list = []      # for emodict
depends_list = []       # for emodict
descr_list = []         # for emodict
packdeplist = []        # list package name index[0] and index[1:-1] is packages it needs

# outputs emodict
for line in statusfile_list:
    if line.startswith('Package:', 0, 8):
        linep = line.strip('\n')
        packname_list = linep.split('ackage: ', 1)
        emodict[packname_list[1]] = {}
    if line.startswith('Depends:', 0, 8):
        linede = line.strip('\n')
        depends_list = linede.split('epends: ', 1)
        emodict[packname_list[1]]['Depends'] = depends_list[1]
    if line.startswith('Description:', 0, 12):
        linedscr = line.strip('\n')
        descr_list = linedscr.split('escription: ', 1)
    if line.startswith(' ', 0, 2) and not line.startswith(' /', 0, 3):
        linedscr2 = line.strip('\n')
        descr_list[1] += str(linedscr2)
        emodict[packname_list[1]]['Description'] = descr_list[1]



# outputs packdeplist
for line in statusfile_list:
    if line.startswith('Package:', 0, 8):
        linep = line.strip('\n')
        packname_list = linep.split('ackage: ', 1)
        packdeplist.insert(0, [packname_list[1]])
    if line.startswith('Depends:', 0, 8):
        line = line.strip('\n').lstrip('Depends:')
        linedep = re.sub(r'\([^)]*\)', '', line)
        deplist = linedep.split(', ')
        for i in deplist:
            line = i.strip()
            if line.find('|') != -1:
                alt_check = line.split(' | ')
                packdeplist[0].append(alt_check[0].strip())
            else:
                packdeplist[0].append(line)
#for i in packdeplist:
#    print(i)


#function for rdepends key
xdict = {}
for level0 in packdeplist:
    for level1 in range(1, len(level0)):
        #print(level0[0], level0[level1])
        key = level0[level1]
        xdict.setdefault(key, [])
        xdict[key].append(level0[0])

for key, value in xdict.items():
    try:
        emodict[key]['Rdepends'] = value
    except:
        print('Package is not installed or provided through another package.')

for a, b in emodict.items():
    print('\nPackage Name:', a)
    for key in b:
        print(key + ':', b[key])








