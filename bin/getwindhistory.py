'''
Helper script for summarizing two-day log of wind data from Jericho.

The too-wide header for the data in its 205-column glory looks like this:
                  Temp     Hi    Low   Out    Dew  Wind  Wind   Wind    Hi    Hi   Wind   Heat    THW                Rain    Heat    Cool    In     In    In     In     In   In Air  Wind  Wind    ISS   Arc.
  Date    Time     Out   Temp   Temp   Hum    Pt. Speed   Dir    Run Speed   Dir  Chill  Index  Index   Bar    Rain  Rate    D-D     D-D    Temp   Hum    Dew   Heat    EMC Density  Samp   Tx   Recept  Int.

The summarizing is simply a matter of grabbing specific column ranges.
'''

from urllib.request import urlopen
content = urlopen('https://jsca.bc.ca/main/downld02.txt').read()
content = content.decode('utf-8').replace('\r\n', '\n')

lines = content.split('\n')
# Trim the usual blank line from the bottom.
if not len(lines[-1]):
  lines = lines[:-1]

speeds = []
max_speed = 1.0
for line in lines[3:]:
  speed = float(line[50:55])
  if speed > max_speed:
    max_speed = speed
  speeds.append(speed)

# Put the headers at the bottom also.
lines = lines + [lines[2]] + lines[:2]

# Print everything.
for line in lines:
  # First 16 columns gives us date/time.
  # Columns 50:61 gives us wind speed and direction.
  print('%s%s' % (line[:16], line[50:61]))

# Now print an ASCII art graph of wind speeds:
v_scale = 1
print()

num_rows = int(max_speed * v_scale + 0.5) + 1
rows = []
for row_num in range(num_rows):
  rows.append([' '] * len(speeds))

for index, speed in enumerate(speeds):
  y = int(speed * v_scale + 0.5)
  rows[y][index] = 'x'

for index, row in enumerate(reversed(rows)):
  print('%2d: %s' % (len(rows) - index - 1, ''.join(row)))
print('-' * (len(rows[0]) + 4))
