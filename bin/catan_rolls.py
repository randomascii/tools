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

import fileinput

for line in fileinput.input():
  if line.count("rolled") > 0:
    person, rolled, dice1, dice2 = line.split()
    if person.startswith('Guest'):
      person = person[len('Guest'):]
    person = person.split('#')[0]
    roll = ord(dice1[-1]) - ord('0') + ord(dice2[-1]) - ord('0')
    print('%2d rolled by %s' % (roll, person))
