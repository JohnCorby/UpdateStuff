SERVER_DIR = 'server'
PLUGIN_DIR = f'{SERVER_DIR}/plugins'

from SiteUtil import spigot, bukkit, server


def download_all():
    """this is where you put the code to download the things"""
    # server test
    server()

    # bukkit test
    bukkit('https://dev.bukkit.org/projects/plugman/')

    # spigot test
    spigot('https://www.spigotmc.org/resources/coreprotect.8631/')
