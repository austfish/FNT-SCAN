from config import settings

yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'


def banner():
    message = white + '{' + red + settings.version + ' #dev' + white + '}'

    FntScan_banner = f"""{yellow}
███████ ███    ██ ████████    ███████  ██████  █████  ███    ██ {green}
██      ████   ██    ██       ██      ██      ██   ██ ████   ██ 
█████   ██ ██  ██    ██ █████ ███████ ██      ███████ ██ ██  ██ {blue}
██      ██  ██ ██    ██            ██ ██      ██   ██ ██  ██ ██ 
██      ██   ████    ██       ███████  ██████ ██   ██ ██   ████ {message}   
                              
{white}FntScan is a powerful Crawler and passive scanner integration tool!{end}
"""
    print(FntScan_banner)
