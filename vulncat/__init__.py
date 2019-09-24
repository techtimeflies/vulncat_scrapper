import argparse

parser = argparse.ArgumentParser()

parser.add_argument('category')

args = parser.parse_args()

if(args.category):
    print('category running')