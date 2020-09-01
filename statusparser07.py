import re
import os


def dictgenerator(statusfile_list):  # outputs basedict

    current_pack = ''
    basedict = {}
    descr_list = []  # for basedict

    for line in statusfile_list:
        if line.startswith('Package:', 0, 8):
            linep = line.strip('\n')
            list1 = linep.split('ackage: ', 1)
            current_pack = list1[1].strip()
            basedict[current_pack] = {}
        elif line.startswith('Depends:', 0, 8):
            linede = line.strip('\n')
            linede_list = linede.split('epends: ', 1)
            del linede_list[0]
            depends_list = linede_list[0].split(', ')
            basedict[current_pack]['Depends'] = depends_list
        elif line.startswith('Description:', 0, 12):
            linedscr = line.strip('\n')
            descr_list = linedscr.split('escription: ', 1)
            del descr_list[0]
        elif line.startswith(' ', 0, 2) and not line.startswith(' /', 0, 3):
            descr_list.append(line.strip('\n'))
            basedict[current_pack]['Description'] = descr_list
    return basedict


def packdeplistgen(statusfile_list):  # outputs package name and dependency list

    packdeplist = []  # list package name index[0] and index[1:-1] is packages it needs

    for line in statusfile_list:
        if line.startswith('Package:', 0, 8):
            linep = line.strip('\n')
            packname_list = linep.split('ackage: ', 1)
            packdeplist.insert(0, [(packname_list[1].strip())])
        elif line.startswith('Depends:', 0, 8):
            line = line.strip('\n').lstrip('Depends:')
            linedep = re.sub(r'\([^()]*\)', '', line)
            deplist = linedep.split(', ')
            for i in deplist:
                line = i.strip()
                if ('|') in line:
                    alt_check = line.split(' | ')
                    packdeplist[0].append(alt_check[0].strip())
                else:
                    packdeplist[0].append(line)
    return packdeplist


def reversedependency(packdeplist, rddict):  # function for rdepends key
    xdict = {}
    for level0 in packdeplist:
        for level1 in range(1, len(level0)):
            # print(level0[0], level0[level1])
            key = level0[level1]
            xdict.setdefault(key, [])
            xdict[key].append(level0[0])

    for key, value in xdict.items():
        try:
            rddict[key]['Rdepends'] = value
        except:
            print('Package is not installed or provided through another package.')

    for a, b in rddict.items():
        print('\nPackage Name:', a)
        for key in b:
            print(key + ':', b[key])

    return rddict


def pagecreator(basedict):
    parent_dir = "Projects/01/"
    testmatchlist = []

    try:
        os.makedirs(parent_dir, exist_ok=True)
    except OSError:
        print(f'Directory {parent_dir} can not be created')

    indexpage = open(parent_dir + 'index.html', 'a', encoding="utf-8")
    indexcontent = '''<!DOCTYPE html><html><head><style>div {margin: 25px 50px 75px; font-family:"consolas"}</style></head><body><div><h1>Status File Parser</h1><p>This program takes the Linux status-file and parses out relevant data about installed packages.</p><p>Below you'll find a list of packages in the status-file. Please click on a package to see:</p><p><ul><li>Package name</li><li>Package description</li><li>Package dependencies</li><li>Package reverse dependencies</li></ul><hr>'''
    indexcontentend = '</div></body></html>'
    indexpage.write(indexcontent)

    for directory, value in basedict.items():

        testmatchlist.append(directory)

        path = os.path.join(parent_dir, directory)
        try:
            os.makedirs(path, exist_ok=True)
        except OSError:
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
                    if i in testmatchlist:
                        htmldepnd += '<li><a href="https://ratracemaverick.com/parse/' + parent_dir + i + '/' + i + '.html">' + i + '</a></li>'
                    elif (' (' in i) and not ('|' in i):
                        split1 = i.split(' (', 1)
                        x = split1[0].strip()
                        if x in testmatchlist:
                            htmldepnd += '<li><a href="https://ratracemaverick.com/parse/' + parent_dir + x + '/' + x + '.html">' + split1[0] + ' (' + split1[1] + '</a></li>'
                        elif x not in testmatchlist:
                            htmldepnd += '<li>' + split1[0] + ' (' + split1[1] + '</li>'
                    elif (' (' not in i) and ('|' not in i) and not (i in testmatchlist):
                        htmldepnd += '<li>' + i + '</li>'
                    elif ('|' in i) and (' (' not in i):
                        split2 = i.split(' | ')
                        strx = ''
                        for x in split2:
                            x = x.strip()
                            if x in testmatchlist:
                                strx += '<a href="https://ratracemaverick.com/parse/' + parent_dir + x + '/' + x + '.html">' + x + '</a> | '
                            elif x not in testmatchlist:
                                strx += x + ' | '
                        htmldepnd += '<li>' + strx.rstrip(' | ') + '</li>'
                    elif ('|' in i) and (' (' in i):
                        split3 = i.split(' | ')
                        strxy = ''
                        for x in split3:
                            split4 = x.split(' (', 1)
                            i = split4[0].strip()
                            if i in testmatchlist:
                                try:
                                    strxy += '<li><a href="https://ratracemaverick.com/parse/' + parent_dir + i + '/' + i + '.html">' + split4[0] + ' (' + split4[1] + '</a></li> | '
                                except:
                                    strxy += '<li><a href="https://ratracemaverick.com/parse/' + parent_dir + i + '/' + i + '.html">' + split4[0] + '</a></li> | '
                            elif i not in testmatchlist:
                                try:
                                    strxy += split4[0] + ' (' + split4[1] + ' | '
                                except:
                                    strxy += split4[0] + ' | '
                        htmldepnd = '<li>' + strxy.rstrip(' | ') + '</li>'


        if len(htmldepnd) <= 2:
            htmldepnd = 'No current package dependencies.'

        htmlrdepnd = ''
        for dkey in value:
            if dkey == 'Rdepends':
                for i in value[dkey]:
                    htmlrdepnd += '<li><a href="https://ratracemaverick.com/parse/' + parent_dir + i + '/' + i + '.html">' + i + '</a></li>'
        if len(htmlrdepnd) <= 2:
            htmlrdepnd = 'No current reverse dependencies.'

        htmlpackage = '<a href="https://ratracemaverick.com/parse/' + parent_dir + directory + '/' + directory + '.html">' + directory + '</a><br>'
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
    plist = packdeplistgen(statusread)
    emodict = reversedependency(plist, firstdict)
    pagecreator(emodict)
