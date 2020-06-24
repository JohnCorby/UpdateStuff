SERVER_DIR = 'server'

from SiteUtil import spigot, bukkit, jenkins, auto


def manual_download():
    """this is where you put the code to download the things"""
    auto('https://www.spigotmc.org/resources/screamingbedwars-1-9-1-15.63714')
    spigot('https://www.spigotmc.org/resources/commandspy.18498')
    spigot('https://www.spigotmc.org/resources/coreprotect.8631')
    spigot('https://www.spigotmc.org/resources/f3nperm.46461')
    bukkit('https://dev.bukkit.org/projects/grief-prevention')
    jenkins('https://ci.lucko.me/job/LuckPerms/lastSuccessfulBuild/artifact/bukkit/build/libs')
    bukkit('https://dev.bukkit.org/projects/luma')
    jenkins('https://papermc.io/ci/job/mcMMO')
    bukkit('https://dev.bukkit.org/projects/multiverse-core')
    bukkit('https://dev.bukkit.org/projects/multiverse-netherportals')
    bukkit('https://dev.bukkit.org/projects/multiverse-portals')
    spigot('https://www.spigotmc.org/resources/per-world-inventory.4482')
    bukkit('https://dev.bukkit.org/projects/plugman')
    # todo ultimatetimber
    spigot('https://www.spigotmc.org/resources/vault.34315')
    spigot('https://www.spigotmc.org/resources/voidgenerator.25391')
    bukkit('https://dev.bukkit.org/projects/worldedit')
    bukkit('https://dev.bukkit.org/projects/worldguard')
