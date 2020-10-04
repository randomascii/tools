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
Sum data from the clipboard. This script reads lines of data from the clipboard,
converts each line to a python float (double) and sums them, also printing other
statistics.

This is useful for summing columns of WPA (Windows Performance Analyzer) data
from ETW traces. Just select all data, control-clicking as needed to deselect
particular rows, then right-click in the column-> Copy Other-> Copy Column
Selection. Then run this tool. This tool assumes that commas can be discarded
and will fail in many non-English locales.
"""

from __future__ import print_function

import sys
import win32clipboard

def main():
  win32clipboard.OpenClipboard()
  data = win32clipboard.GetClipboardData()
  win32clipboard.CloseClipboard()

  sum = 0
  min = 1e100
  max = 0
  count = 0
  missed_count = 0
  for line in data.splitlines():
    try:
      val = float(line.replace(',', '').replace('%', ''))
      count += 1
      sum += val
      if val < min:
        min = val
      if val > max:
        max = val
    except:
      missed_count += 1

  if count > 0:
    print("Found %d values, sum is %1.3f, min %1.3f, avg %1.3f, max %1.3f." % (count, sum, min, sum / count, max))
  if missed_count > 0:
    print("Found %d non-numeric values" % missed_count)


if __name__ == '__main__':
    sys.exit(main())
