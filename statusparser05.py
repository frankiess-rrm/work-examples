import re
import os


def dictgenerator(statusfile_list):  # outputs emodict

    emodict = {}
    packname_list = []  # for emodict
    depends_list = []  # for emodict
    descr_list = []  # for emodict

    for line in statusfile_list:
        if line.startswith('Package:', 0, 8):
            linep = line.strip('\n')
            packname_list = linep.split('ackage: ', 1)
            emodict[packname_list[1]] = {}
        if line.startswith('Depends:', 0, 8):
            linede = line.strip('\n')
            linede_list = linede.split('epends: ', 1)
            del linede_list[0]
            depends_list = linede_list[0].split(', ')
            emodict[packname_list[1]]['Depends'] = depends_list
        if line.startswith('Description:', 0, 12):
            linedscr = line.strip('\n')
            descr_list = linedscr.split('escription: ', 1)
            del descr_list[0]
        if line.startswith(' ', 0, 2) and not line.startswith(' /', 0, 3):
            descr_list.append(line.strip('\n'))
            emodict[packname_list[1]]['Description'] = descr_list
    return emodict


def packdeplistgen(statusfile_list):  # outputs package name and dependency list

    packname_list = []
    packdeplist = []  # list package name index[0] and index[1:-1] is packages it needs

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
    return packdeplist


def reversedependency(packdeplist, emodict):  # function for rdepends key
    xdict = {}
    for level0 in packdeplist:
        for level1 in range(1, len(level0)):
            # print(level0[0], level0[level1])
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

    return emodict


def pagecreator(basedict):
    parent_dir = "Projects/01/"
    try:
        os.makedirs(parent_dir, exist_ok=True)
    except OSError as error:
        print(f'Directory {parent_dir} can not be created')
    indexpage = open(parent_dir + 'index.html', 'a', encoding="utf-8")
    indexcontent = '''<!DOCTYPE html><html><head><style>div {margin: 25px 50px 75px; font-family:"consolas"}</style></head><body><div><h1>Status File Parser</h1><p>This program takes the Linux status-file and parses out relevant data about installed packages.</p><p>Below you'll find a list of packages in the status-file. Please click on a package to see:</p><p><ul><li>Package name</li><li>Package description</li><li>Package dependencies</li><li>Package reverse dependencies</li></ul><hr>'''
    indexcontentend = '</div></body></html>'
    indexpage.write(indexcontent)
    htmlpackage = ''

    for directory, value in basedict.items():
        path = os.path.join(parent_dir, directory)
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as error:
            print(f'Directory {path} can not be created')

        htmldesc = ''
        for dkey in value:
            if dkey == 'Description':
                htmldesc += value[dkey][0]
                htmldesc = htmldesc.capitalize() + '.<br><br>'
                for i in range(1, len(value[dkey])):
                    htmldesc = htmldesc + value[dkey][i]
                    htmldesc = re.sub('\s\.', "", htmldesc)

        htmldepnd = ''
        for dkey in value:
            if dkey == 'Depends':
                for i in value[dkey]:
                    htmldepnd = htmldepnd + '<li>' + i + '</li>'
        if len(htmldepnd) <= 2:
            htmldepnd = 'No current package dependencies.'

        htmlrdepnd = ''
        for dkey in value:
            if dkey == 'Rdepends':
                for i in value[dkey]:
                    htmlrdepnd = htmlrdepnd + '<li>' + i + '</li>'
        if len(htmlrdepnd) <= 2:
            htmlrdepnd = 'No current reverse dependencies.'


        htmlpackage = '<a href="https://ratracemaverick.com/parse/' + parent_dir + directory + '/' + directory + '.html">' + directory + '</a>\n<br>'
        indexpage.write(htmlpackage)

        packpage = open(parent_dir + directory + '/' + directory + '.html', 'w', encoding="utf-8")
        packagescontent = '<!DOCTYPE html><html><head><style>div {margin: 25px 50px 75px; font-family:"consolas"}</style></head><div><h1>Package: ' + directory + '</h1><h3>Description:</h3><p> ' + htmldesc + '</p><h3>Dependencies:</h3><ul>' + htmldepnd + '</ul><h3>Reverse Dependencies:</h3><ul>' + htmlrdepnd + '</ul><hr></div></body></html>'
        packpage.write(packagescontent)
        packpage.close()
    indexpage.write(indexcontentend)
    indexpage.close()


if __name__ == '__main__':
    file = 'status'
    so = open(file, 'r', encoding="utf8")
    statusread = so.readlines()
    so.close()
    firstdict = dictgenerator(statusread)
    packdeplist = packdeplistgen(statusread)
    emodict = reversedependency(packdeplist, firstdict)
    pagecreator(emodict)