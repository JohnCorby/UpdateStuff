SERVER_DIR = 'server'

from SiteUtil import spigot, bukkit, jenkins, auto


def manual_download():
    """this is where you put the code to download the things"""
    auto('https://www.spigotmc.org/resources/screamingbedwars-1-9-1-15.63714')
    auto('https://www.spigotmc.org/resources/commandspy.18498')
    auto('https://www.spigotmc.org/resources/coreprotect.8631')
    auto('https://www.spigotmc.org/resources/f3nperm.46461')
    auto('https://dev.bukkit.org/projects/grief-prevention')
    auto('https://ci.lucko.me/job/LuckPerms/lastSuccessfulBuild/artifact/bukkit/build/libs')
    auto('https://dev.bukkit.org/projects/luma')
    auto('https://papermc.io/ci/job/mcMMO')
    auto('https://dev.bukkit.org/projects/multiverse-core')
    auto('https://dev.bukkit.org/projects/multiverse-netherportals')
    auto('https://dev.bukkit.org/projects/multiverse-portals')
    auto('https://www.spigotmc.org/resources/per-world-inventory.4482')
    auto('https://dev.bukkit.org/projects/plugman')
    # todo ultimatetimber
    auto('https://www.spigotmc.org/resources/vault.34315')
    auto('https://www.spigotmc.org/resources/voidgenerator.25391')
    auto('https://dev.bukkit.org/projects/worldedit')
    auto('https://dev.bukkit.org/projects/worldguard')
