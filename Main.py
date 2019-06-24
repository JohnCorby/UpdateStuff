import os
from re import compile

from Util import *

SERVER_DIR = '..'

# clear out plugins dir of jars
for fp in os.listdir(PLUGIN_DIR):
    if fp.endswith('.jar'):
        fp = join(PLUGIN_DIR, fp)
        os.remove(fp)
        print('removed', fp)

# paper
download(
    get('https://papermc.io/ci/job/Paper-1.14/lastSuccessfulBuild/artifact/paperclip.jar'),
    SERVER_DIR, 'server.jar'
)

# plugman
download(get('https://dev.bukkit.org/projects/plugman/files/latest'), PLUGIN_DIR)
# multiverse
jenkins(
    'https://ci.onarandombox.com/job/Multiverse-Core',
    compile(r'Multiverse-Core-[\d.]+(-SNAPSHOT)?\.jar')
)
jenkins(
    'https://ci.onarandombox.com/job/Multiverse-NetherPortals',
    compile(r'Multiverse-NetherPortals-[\d.]+(-SNAPSHOT)?\.jar')
)
# essentials
jenkins(
    'https://ci.ender.zone/job/EssentialsX',
    compile(r'EssentialsX-[\d.]+\.jar'),
    compile(r'EssentialsXChat-[\d.]+\.jar'),
    compile(r'EssentialsXSpawn-[\d.]+\.jar')
)
# coreprotect
spigot('https://www.spigotmc.org/resources/coreprotect.8631')
# perworldinventory
spigot('https://www.spigotmc.org/resources/per-world-inventory.4482')

# worldedit
print('getting worldedit')
url = 'http://builds.enginehub.org/job/worldedit/last-successful'

d = PyQuery(get(url).content)

file_url = d('.panel-body .list-unstyled a[href$=".jar"]')
file_url = map(lambda e: e.attrib['href'], file_url)
# NOTE: this will always be the right href
# alphabetical order means worldedit-bukkit comes first
file_url = list(file_url)[0]

download(get(file_url), PLUGIN_DIR)
