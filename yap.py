import argparse
import os
import sys
from yapf.yapflib.yapf_api import FormatFile

my_parser = argparse.ArgumentParser(description='List the content of a folder')
my_parser.add_argument('Path',
                       metavar='path',
                       type=str,
                       help='the path to list')

args = my_parser.parse_args()
input_path = args.Path


_, _, filenames = next(os.walk(input_path))
print(*filenames)
for file in filenames:
    if os.path.splitext(file)[1] == "py":
        FormatFile(os.path.join(input_path, file), in_place=True)
            