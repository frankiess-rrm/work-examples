emodict = {}


def openfile(filename):
    so = open(filename, 'r', encoding="utf8")
    imported = so.readlines()
    so.close()
    statusdump(imported)


def statusdump(statusfile_list):
    packname_list = []
    packname_dict = {}
    depends_list = []
    depends_dict = {}
    descr_list = []
    descr_dict = {}

    for line in statusfile_list:
        if line.startswith('Package:', 0, 8):
            packname_list = line.strip('\n').split(': ', 1)
            packname_dict = {packname_list[0]: packname_list[1]}
            emodict.update({packname_list[1]: packname_dict})
        if line.startswith('Depends:', 0, 8):
            depends_list = line.strip('\n').split(': ', 1)
            depends_dict = {depends_list[0]: depends_list[1]}
            emodict[packname_list[1]][depends_list[0]] = depends_list[1]
        if line.startswith('Description:', 0, 12):
            descr_list = line.strip('\n').split(': ', 1)
        if line.startswith(' ', 0, 1) and not line.startswith(' /', 0, 2):
            descr2 = line.strip('\n')
            descr_list[1] = descr_list[1] + str(descr2)
            descr_dict = {descr_list[0]: descr_list[1]}
            emodict[packname_list[1]][descr_list[0]] = descr_list[1]

    return emodict


def rdependencies(emodict):
    pass


def writetohtml(fileoutput):
#needs packages list from other file
    f = open('indexhtml.txt', 'a')

    packagesstr = ''
    for x in range(len(packages)):
        packagesstr = '<a href="' + packages[x] + '.html">' + packages[x] + '</a>\n'
        f.write(packagesstr)
    f.close()


def subpages(emodict2):
    pass


openfile('status')

for key in emodict:
    print(key, ' : ', emodict[key])