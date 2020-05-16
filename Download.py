SERVER_DIR = 'server'
PLUGIN_DIR = f'{SERVER_DIR}/plugins'

from SiteUtil import spigot, bukkit, server, plugin


def download_all():
    """this is where you put the code to download the things"""
    # server test
    server()

    # plugin test
    plugin('https://papermc.io/ci/view/all/job/mcMMO/lastSuccessfulBuild/artifact/target/mcMMO.jar')

    # bukkit test
    bukkit('https://dev.bukkit.org/projects/plugman/')

    # spigot test
    spigot('https://www.spigotmc.org/resources/coreprotect.8631/')
