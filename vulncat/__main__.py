import argparse
import vulncat
import logging
import os

loglevel='DEBUG'
logpath=f'{os.getcwd()}/logs'

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
parser.add_argument('-l', '--list', action='store_true', help='list all the categories of vulnerabilities')

args = parser.parse_args()

if args.list:
    vulncat.parse_categories()