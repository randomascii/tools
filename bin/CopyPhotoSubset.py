# Copyright 2021 Bruce Dawson. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""
This script uses photo information from ~\Documents\PhotoDatabase.txt (which is
populated by a separate photo-scanning tool) to select photos that contain a
specified sub-string to a flash drive. Sample usage:

  python3.exe CopyPhotoSubset.py "Bruce Dawson" d:\photos

This will find all photos with "Bruce Dawson" in the database (presumably from
face tags, but it could be a directory name) into d:\photos. The copying
preserves the directory structure except that the first three levels of the
directory structure are removed, so "C:\Users\Public\Pictures\2013\2013_10"
becomes just "2013\2013_10"
"""

import argparse
import os
import shutil


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--text', help='Text to search for.',
                      required=True)
  parser.add_argument('--dest', help='Destination directory.',
                      required=True)
  args = parser.parse_args()
  needle = args.text
  dest = args.dest

  print('Copying all files containing "%s" to %s.' % (needle, dest))

  database_dir = os.path.expanduser(r'~\Documents')
  database_path = os.path.join(database_dir, 'PhotoDatabase.txt')
  with open(database_path, 'rb') as f:
    lines = f.read().decode('utf-16').splitlines()
  print('Read %s lines.' % len(lines))
  for line in lines:
    if line.count(needle) > 0:
      parts = line.split('\t')
      path = parts[0]
      sub_path = '\\'.join(path.split('\\')[4:])
      output_path = os.path.join(dest, sub_path)
      if not os.path.exists(output_path):
        print('Copying from %s to %s' % (path, output_path))
        dir = os.path.split(output_path)[0]
        os.makedirs(dir, exist_ok=True)
        shutil.copy2(path, output_path)

if __name__ == '__main__':
  main()
