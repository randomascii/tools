def flu_sum(filename):
  total = 0
  for line in open(filename).readlines()[1:]:
    total += sum(int(x) for x in line.strip().split(',')[3:])
  return total

print(flu_sum('FluView_StackedColumnChart_Data.csv'))
print(flu_sum('FluView_StackedColumnChart_Data (1).csv'))
