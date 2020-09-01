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
            depends_list = linede.split('epends: ', 1)
            emodict[packname_list[1]]['Depends'] = depends_list[1]
        if line.startswith('Description:', 0, 12):
            linedscr = line.strip('\n')
            descr_list = linedscr.split('escription: ', 1)
        if line.startswith(' ', 0, 2) and not line.startswith(' /', 0, 3):
            linedscr2 = line.strip('\n')
            descr_list[1] += str(linedscr2)
            emodict[packname_list[1]]['Description'] = descr_list[1]
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


def reversedependency(packdeplist,emodict): # function for rdepends key
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
    parent_dir = "D:/Python Projects/Statusparser/"
    for directory in basedict.keys():
        parent_dir = "D:/Python Projects/Statusparser/"
        path = os.path.join(parent_dir, directory)
        try:
            os.makedirs(path, exist_ok=True)
            print("Directory '%s' created successfully" % directory)
        except OSError as error:
            print("Directory '%s' can not be created" % directory)
        print("Directory '% s' created" % directory)

        packpage = open(parent_dir + '/' + directory + '/' + directory + '.html', 'a')
        packagescontent = '''<!DOCTYPE html>
            <html>
            <head>
            <style>
            div {margin: 25px 50px 75px;}
            </style>
            </head>
            <body>
                        	
            <div><h1>Package:''' + directory + '''</h1><h3 class="">Description</h3><p>''' + description + '''</p><h3 
            class="">Dependencies (what packages it needs to function)</h3><ul><li>''' + dependlist + '''</li><li>List 2</li>
            </ul><h3 class="">''' + rdependlist + '''(what packages rely on this package to function)</h3><ul><li>
            Rdependency list</li><li>List 2</li></ul>
                        
            <hr>
            </div></body></html>'''
        packpage.write(packagescontent)
        packpage.close()

    indexpage = open(parent_dir + '/' + 'index.html', 'a')
    packagescontent = '''
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        div {
          margin: 25px 50px 75px;
        }
        </style>
        </head>
        <body>

        <div><h1>Status File Parser</h1><p>This program takes the Linux status-file and parses out relevant information 
        about installed packages.</p><p>Below you'll find a list of packages in the status-file. Please click on a package 
        to see:</p><p><ul><li>Package name</li><li>Package description</li><li>Package dependencies</li><li>Package reverse 
        dependencies</li></ul>

        <hr>
        '''
    packagesstr = ''
    packagescontentend = '</div></body></html>'
    indexpage.write(packagescontent)
    for y in basedict.keys():
        packagesstr = '<a href="' + parent_dir + '/' + y + '/' + y + '.html">' + y + '</a>\n<br>'
        indexpage.write(packagesstr)
    indexpage.write(packagescontentend)
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