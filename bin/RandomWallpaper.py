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

"""
This script randomly selects a photo from a list of files.

The list of files has a heading line and subsequent lines have tab-separated
columns where the first column is the file name and the third column is a rating
that goes from 0 to 5 stars. This script only selects from photos that are
five-star rated.

A list of selected photos is retained, which could be used to avoid repetition,
but given a sufficiently large number of photos this shouldn't be a problem.

This can be set as a scheduled task. In this context it is important to run it
using pythonw.exe so that no console window pops up.
"""

import ctypes
import os
import random
import sys

def main():
  # This is not, apparently, a completely robust way to get the user's documents
  # directory, but the alternatives are much messier and not worth it to me.
  documents = os.path.expanduser(r'~\Documents')
  database = os.path.join(documents, 'PhotoDatabase.txt')
  lines = open(database, 'rb').read().decode('utf-16').splitlines()
  # Filter to just the 5-star photos. This also removes the heading line.
  filtered = [line for line in lines if line.split('\t')[2] == '5']

  while True:
    # Select a random line.
    line = random.choice(filtered)
    path = line.split('\t')[0]
    # Try again if the photo doesn't exist for some reason.
    if not os.path.exists(path):
      continue
    # Try again if the file is a video.
    extension = os.path.splitext(path)[1].lower()
    if extension in ['.mp4', '.mov', '.wmv']:
      continue

    # Magic incantation to set the wallpaper.
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 2)
    break

  # Record information about the displayed photo.
  history = os.path.join(documents, 'PhotoWallpaperHistory.txt')
  with open(history, 'a') as f:
    f.write('%s\n' % line)


if __name__ == '__main__':
    sys.exit(main())
