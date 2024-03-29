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
Summarize Catan roll information from colonist.io roll history. The expected use
is to select-all/copy the roll history then run catan_rolls.bat which uses
fromclip.exe (not yet released) to pipe the clipboard data to this Python
script.
"""

from __future__ import print_function

import fileinput

# Zero-based is for C/C++, one-based is for Fortran, but two-based is for dice
# games. Subtract two when storing data, add two when retrieving it.
histograms = [0] * 11

sevens = {}

for line in fileinput.input():
  if line.count("rolled") > 0:
    person, rolled, dice1, dice2 = line.split()
    # Strip off the noisy 'Guest' prefix for cleaner output.
    if person.startswith('Guest'):
      person = person[len('Guest'):]
    # Strip off the #nnnn suffix for cleaner output.
    person = person.split('#')[0]
    roll = int(dice1[-1]) + int(dice2[-1])
    print('%2d rolled by %s' % (roll, person))
    histograms[roll-2] += 1
    if roll == 7:
      sevens[person] = sevens.get(person, 0) + 1

print()
print('Rolls histogram:')
for i in range(len(histograms)):
  print('%2d %s' % (i + 2, 'x' * histograms[i]))

print('')
for name in sevens.keys():
  print('%2d sevens rolled by %s' % (sevens[name], name))
