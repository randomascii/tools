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
This script randomly selects a 5-star photo from the user's pictures folder or
the public pictures folder.

This script uses PIL/Pillow to scan the images and extract rating tags. It
caches the results in a text file that holds the path, last-modified time, and
rating (tab separated). It can either update the database occasionally (every
now and then) or it can get the file list and update the database whenever the
count changes.

A list of the photos that have been displayed is kept. This list could be used
to avoid repetition, but given a sufficiently large number of photos there
shouldn't be a problem with repetition so this has not been implemented. Instead
the list of displayed photos is simply retained so that the user can find out
what pictures have been shown.

This can be set as a scheduled task that runs every five minutes or so. In this
context it is important to run it using pythonw.exe so that no console window
pops up.
"""

import ctypes
import datetime
import os
# To make this available you need to install Pillow with this command:
# pip3 install pillow
from PIL import Image, ExifTags
import random
import sys
import time

# Use the documents directory or localappdata (shadow version) to store the
# database of files and their attributes, and other status files.

# This is not, apparently, a completely robust way to get the user's documents
# directory, but the alternatives are much messier and not worth it to me.
database_dir = os.path.expanduser(r'~\Documents')

# Note that Python reads/writes from a shadow version of localappdata due to
# managed app restrictions, which makes the database and the recent files
# difficult to view.
#database_dir = os.environ['localappdata']

def GetPictures(directories):
  """
  Scan the specified directories for .jpg files and return a list of file paths.
  """
  result = []
  for directory in directories:
    for root, dirs, files in os.walk(directory, topdown=False):
      for name in files:
        ext = os.path.splitext(name)[1].lower()
        if ext.lower() in ['.jpg']:
          result.append(os.path.join(root, name))
  return result

def main():
  verbose = True
  start = time.time()
  database = os.path.join(database_dir, 'WallpaperPhotoDatabase.txt')
  try:
    lines = open(database, 'rb').read().decode('utf-16').splitlines()
  except:
    # If the database doesn't exist then create an empty one.
    lines = []

  old_database = {}
  for line in lines:
    path, mtime, rating = line.split('\t')
    old_database[path] = (float(mtime), int(rating))

  mypictures = os.path.expanduser(r'~\Pictures')
  publicpictures = os.path.normpath(os.path.expanduser(r'~\..\public\Pictures'))
  # Set this to the list of directories to be scanned.
  directories = [mypictures, publicpictures]

  # Scanning the entire picture directory is fast if it is cached, and gives a
  # quite reliable way to detect when new pictures appear. But it is not free,
  # especially on slow hard drives. Set detect_changes to True to get update
  # whenever the file count changes.
  detect_changes = True
  if detect_changes:
    picture_list = GetPictures(directories)

  # Recreate the database if it doesn't exist, and every now and then.
  if not old_database or (detect_changes and len(picture_list) != len(old_database)):
    if verbose:
      print('Updating database from %d to %d pictures.' % (len(old_database), len(picture_list)))

    if not detect_changes:
      picture_list = GetPictures(directories)
    # Set a larger decompression bomb level. Could set this to None to disable
    # compression bomb warnings entirely.
    Image.MAX_IMAGE_PIXELS = 300000000

    rating_tag = 18246

    new_database = {}
    count = 0
    updated = 0
    for path in picture_list:
      count += 1
      if int(count % 5000) == 0:
        print('%d out of %d, %s.' % (count, len(picture_list), path))
      mtime = os.path.getmtime(path)
      if path in old_database and old_database[path][0] == mtime:
        new_database[path] = old_database[path]
      else:
        updated += 1
        with Image.open(path) as img:
          img_exif = img.getexif()
          rating = img_exif.get(rating_tag, 0)
        new_database[path] = (mtime, rating)
    if updated > 0:
      print('Updated %d entries.' % updated)
    if new_database != old_database:
      print('Writing updated database.')
      output_list = []
      for key, value in new_database.items():
        output_list.append('%s\t%f\t%d' % (key, value[0], value[1]))
      output_string = '\n'.join(output_list)
      with open(database, 'wb') as f:
        f.write(output_string.encode('utf-16'))
  else:
    new_database = old_database
  # Make sure we don't reference old_database anymore
  del old_database

  # Filter to just the 5-star photos.
  filtered = [key for key in new_database.keys() if new_database[key][1] == 5]
  if verbose:
    print('Filtered from %d to %d pictures.' % (len(new_database), len(filtered)))

  while True:
    # Select a random line.
    path = random.choice(filtered)
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
  history = os.path.join(database_dir, 'WallpaperPhotoHistory.txt')
  with open(history, 'a') as f:
    f.write('%s\t%f\t%d\n' % (path, new_database[path][0], new_database[path][1]))
  elapsed = time.time() - start
  if verbose:
    print('%f s to do work.' % elapsed)


if __name__ == '__main__':
  try:
    sys.exit(main())
  except Exception as e:
    with open(os.path.join(database_dir, 'WallpaperError.txt'), 'a') as f:
      date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      message = 'Exception caught at %s: %s\n' % (date_time, e)
      f.write(message)
      print(message)
