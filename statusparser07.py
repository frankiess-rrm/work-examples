#  This program takes a Debian status file and outputs an html-file and directory structure with relevant package
#  information.
#  Index file will have list of all packages in status file, all packages are links to pages with further information.
#  Package pages have package name, description, dependencies and reverse dependencies, with links to other packages
#  when available.
#  Dependencies are available in the status file, and reverse dependencies are calculated by this program.
#
#  My first real program, applying for Reaktor in 2020.
#  Jay Pitkanen

import re  # This could probably be done without regex.
import os


# The dictgenerator function turns the status file into a dictionary with all necessary data nested as their own
# dictionaries under the package name key.

def dictgenerator(statusfile_list):

    current_pack = ''
    basedict = {}
    descr_list = []  # for basedict
    packagelist = []

    for line in statusfile_list:
        if line.startswith('Package:', 0, 8):  # We look for lines with Package and create the first level of basedict.
            linep = line.strip('\n')
            list1 = linep.split('ackage: ', 1)
            current_pack = list1[1].strip()
            packagelist.append(current_pack)
            basedict[current_pack] = {}
        elif line.startswith('Depends:', 0, 8):  # We look for lines with Depends and add to the Package key.
            linede = line.strip('\n')
            linede_list = linede.split('epends: ', 1)
            del linede_list[0]
            depends_list = linede_list[0].split(', ')
            basedict[current_pack]['Depends'] = depends_list

        # For Description, we add the separate lines as list elements for later formatting purposes.

        elif line.startswith('Description:', 0, 12):
            linedscr = line.strip('\n')
            descr_list = linedscr.split('escription: ', 1)
            del descr_list[0]

        # We want to look for lines necessarily correlate to Description and nothing else.

        elif line.startswith(' ', 0, 2) and not line.startswith(' /', 0, 3):
            descr_list.append(line.strip('\n'))
            basedict[current_pack]['Description'] = descr_list
    return basedict, packagelist


# The packdeplistgen function uses the basedict-dictionary to create a new nested list "packdeplist", with the first
# index holding a package name in the first subindex and all its dependencies in the following subindexes. We will use
# this list to create reverse dependencies.

def packdeplistgen(statusfile_list):  # outputs combined package name and dependency list

    packdeplist = []  # list package name index[0] and index[1:-1] is packages it needs

    for line in statusfile_list:
        if line.startswith('Package:', 0, 8):
            linep = line.strip('\n')
            packname_list = linep.split('ackage: ', 1)
            packdeplist.insert(0, [(packname_list[1].strip())])
        elif line.startswith('Depends:', 0, 8):
            line = line.strip('\n').lstrip('Depends:')
            linedep = re.sub(r'\([^()]*\)', '', line)  # Using Regex to delete everything within parentheses.
            deplist = linedep.split(', ')
            for i in deplist:
                line = i.strip()
                if ('|') in line:
                    alt_check = line.split(' | ')
                    packdeplist[0].append(alt_check[0].strip())
                else:
                    packdeplist[0].append(line)
    return packdeplist


# The reversedependency function uses the packdeplist-list to find reverse dependencies for packages. We will use this
# to create the Rdepends key:value in basedict.

def reversedependency(pdlist, rddict):  # function for rdepends key
    xdict = {}
    for level0 in pdlist:  # This loop compares all list indexes in nested lists to the [0] list index.
        for level1 in range(1, len(level0)):
            key = level0[level1]
            xdict.setdefault(key, [])
            xdict[key].append(level0[0])  # Then appends the found values to a new dictionary.

    for key, value in xdict.items():
        try:
            rddict[key]['Rdepends'] = value  # Not all packages have reverse dependencies, we try if it exists.
        except:
            print('Package is not installed or provided through another package.')

    for a, b in rddict.items():
        print('\nPackage Name:', a)
        for key in b:
            print(key + ':', b[key])

    return rddict





# The pagecreator function takes the basedict-dictionary (now with all data available) and turns it into HTML.
# Pagecreator creates the index.html in the root, the directory structure for packages and all HTML pages for every
# package. HTML pages will include name, description, dependency and reverse dependency neatly formatted.

def pagecreator(basedict, testmatchlist):
    parent_dir = "Projects/"  # Just a random project directory

    try:  # If paths exist, don't freak out
        os.makedirs(parent_dir, exist_ok=True)
        os.remove(parent_dir + 'index.html')
    except OSError:
        print(f'Directory {parent_dir} can not be created')

    indexpage = open(parent_dir + 'index.html', 'a', encoding="utf-8")
    indexcontent = '''<!DOCTYPE html><html><head><style>div {margin: 25px 50px 75px; font-family:"consolas"}</style></head><body><div><h1>Status File Parser</h1><p>This program takes the Linux status-file and parses out relevant data about installed packages.</p><p>Below you'll find a list of packages in the status-file. Please click on a package to see:</p><p><ul><li>Package name</li><li>Package description</li><li>Package dependencies</li><li>Package reverse dependencies</li></ul><hr>'''
    indexcontentend = '</div></body></html>'
    indexpage.write(indexcontent)

    for directory, value in basedict.items():  # Begin for-loop to work with second level of the basedict-dictionary.

        path = os.path.join(parent_dir, directory)
        try:
            os.makedirs(path, exist_ok=True)
        except OSError:
            print(f'Directory {path} can not be created')

        htmldesc = ''  # Variable to hold the description data to be used in the page HTML
        for dkey in value:
            if dkey == 'Description':
                htmldesc += value[dkey][0]
                htmldesc = htmldesc.capitalize() + '.<br><br>'
                for i in range(1, len(value[dkey])):
                    htmldesc = htmldesc + value[dkey][i]
                    htmldesc = re.sub('\s\.', "", htmldesc)

        # The htmldepnd-variable holds the dependency data for the page HTML.
        # It does a few things. A dependency (or alternative dependency) that refers to a package that's not installed
        # will show up as regular text. A dependency with an existing install will show up as a link to that package.
        # Uses conditional statements to compare dependencies without version data to installed package list.

        htmldepnd = ''
        for dkey in value:
            if dkey == 'Depends':
                for i in value[dkey]:
                    if '|' not in i:
                        if i.partition(' ')[0] in testmatchlist:
                            htmldepnd += '<li><a href="https://ratracemaverick.com/parse/' + parent_dir + i.partition(' ')[0] + '/' + i.partition(' ')[0] + '.html">' + i + '</a></li>'
                        else:
                            htmldepnd += '<li>' + i + '</li>'
                    elif '|' in i and ')' not in i:
                        split1 = i.split(' | ')
                        strx = ''
                        for j in split1:
                            if j.strip() in testmatchlist:
                                strx += '<a href="https://ratracemaverick.com/parse/' + parent_dir + j + '/' + j + '.html">' + j + '</a> | '
                            else:
                                strx += j + ' | '
                        htmldepnd += '<li>' + strx.rstrip(' | ') + '</li>'
                    else:
                        split2 = i.split(' | ')
                        stry = ''
                        for k in split2:
                            if k.partition(' ')[0] in testmatchlist:
                                stry += '<a href="https://ratracemaverick.com/parse/' + parent_dir + k.partition(' ')[0] + '/' + k.partition(' ')[0] + '.html">' + k + '</a> | '
                            else:
                                stry += k + ' | '
                        htmldepnd += '<li>' + stry.rstrip(' | ') + '</li>'

        if len(htmldepnd) <= 2:  # If there are no package dependencies
            htmldepnd = 'No current package dependencies.'

        htmlrdepnd = ''  # Variable to hold the reverse dependency data to be used in the page HTML, all URL
        for dkey in value:
            if dkey == 'Rdepends':
                for i in value[dkey]:
                    htmlrdepnd += '<li><a href="https://ratracemaverick.com/parse/' + parent_dir + i + '/' + i + '.html">' + i + '</a></li>'
        if len(htmlrdepnd) <= 2:
            htmlrdepnd = 'No current reverse dependencies.'

        # Write the index page using the package name data from basedict dictionary

        htmlpackage = '<a href="https://ratracemaverick.com/parse/' + parent_dir + directory + '/' + directory + '.html">' + directory + '</a><br>'
        indexpage.write(htmlpackage)

        # Write the package page html into the subdirectories using the variables above.

        packpage = open(parent_dir + directory + '/' + directory + '.html', 'w', encoding="utf-8")
        packagescontent = '<!DOCTYPE html><html><head><style>div {margin: 25px 50px 75px; font-family:"consolas"}</style></head><div><h1>Package: ' + directory + '</h1><h3>Description:</h3><p> ' + htmldesc + '</p><h3>Dependencies:</h3><ul>' + htmldepnd + '</ul><h3>Reverse Dependencies:</h3><ul>' + htmlrdepnd + '</ul><hr></div></body></html>'
        packpage.write(packagescontent)
        packpage.close()
    indexpage.write(indexcontentend)
    indexpage.close()


# Runtime, opens status-file and moves program run logic along.

if __name__ == '__main__':
    file = 'status'
    so = open(file, 'r', encoding="utf8")
    statusread = so.readlines()
    so.close()
    firstdict, packageslist = dictgenerator(statusread)
    plist = packdeplistgen(statusread)
    emodict = reversedependency(plist, firstdict)
    pagecreator(emodict, packageslist)
