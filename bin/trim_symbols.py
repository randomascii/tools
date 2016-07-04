# Copyright 2016 Bruce Dawson. All Rights Reserved.
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
This script looks in the symbol cache directory (defaulting to c:\symbols, but
you can specify a directory) and for each sub-directory deletes all but the
most recent symbols or PE files. This can free up large amounts of space.

The idea is that the old symbols are unlikely to be needed again, and if they
are needed then they will be downloaded from their original symbol server.

It would also be safe to delete everything from the symbol cache directory,
but that would be inefficient because it would require some still-useful symbols
to be downloaded again.

Because this script is doing a partial rmdir /s it can be dangerous - it can
blast away most of the files in a directory if you pass it the wrong path.
However it contains some basic sanity checks. In particular, it will only delete
files if the file names match the grandparent directory, and if there is just
one file in the directory.
"""

import os
import sys

def main():
  symbol_cache_dir = r'c:\symbols'
  if len(sys.argv) > 1:
    symbol_cache_dir = sys.argv[1]

  if not os.path.isdir(symbol_cache_dir):
    print '"%s" is not a directory.' % symbol_cache_dir
    return 1

  deleted_count = 0
  deleted_size = 0
  for symbol in os.listdir(symbol_cache_dir):
    ext = os.path.splitext(symbol)[1]
    if ext.lower() in ['.pdb', '.exe', 'dll']:
      # eg.: c:\symbols\chrome.dll.pdb
      outer_symbol_path = os.path.join(symbol_cache_dir, symbol)
      # eg.: c:\symbols\chrome.dll.pdb\A982846B8C61458C9C4C3E33C6FA8F511
      inner_symbol_dirs = []
      for inner_symbol_dir in os.listdir(outer_symbol_path):
        mtime = os.path.getmtime(os.path.join(outer_symbol_path, inner_symbol_dir))
        inner_symbol_dirs.append((mtime, inner_symbol_dir))
      # Sort by date
      inner_symbol_dirs.sort()
      # Iterate over all but the most recent entries
      # Retain the last two because there may be 32-bit/64-bit binaries with the
      # same name but different symbols, or development/stable versions.
      for x in inner_symbol_dirs[:-2]:
        inner_symbol_path = os.path.join(outer_symbol_path, x[1])
        files = os.listdir(inner_symbol_path)
        # If there are extra files or if the file name doesn't match the parent
        # directory then maybe this isn't a symbol cache?
        if len(files) == 1 and files[0] == symbol:
          file_path = os.path.join(inner_symbol_path, files[0])
          print 'removing %s' % file_path
          deleted_size += os.path.getsize(file_path)
          deleted_count += 1
          os.remove(file_path)
          print 'removing %s' % inner_symbol_path
          os.rmdir(inner_symbol_path)
        else:
          print 'Leaving %s, just in case.' % inner_symbol_path
  print 'Deleted %d files totaling %d bytes' % (deleted_count, deleted_size)


if __name__ == '__main__':
  sys.exit(main())
