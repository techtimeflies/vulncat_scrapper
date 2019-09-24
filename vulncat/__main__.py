import argparse
import vulncat
import logging
import os

loglevel='DEBUG'
logpath=f'{os.getcwd()}/log'

# create the log directory if it does not exist
if os.path.exists(logpath) == False: os.mkdir(logpath)

logging.basicConfig(
    level=loglevel,
    filename=f'{logpath}/app.log', 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%a, %d %b %Y %H:%M:%S'
    )


parser = argparse.ArgumentParser(description='Vulncat web parser cli')

#parser.add_argument('-h', "--help", help='cli helper')
parser.add_argument('-category', action='store_true', help='list all the categories of vulnerabilities')
parser.add_argument('-kingdom', action='store_true', help='list all the kingdoms')
parser.add_argument('-language', action='store_true', help='list all the languages')

args = parser.parse_args()

if args.category:
    vulncat.scrape_filters('category')

if args.kingdom:
    vulncat.scrape_filters('kingdom')

if args.language:
    vulncat.scrape_filters('codelang')