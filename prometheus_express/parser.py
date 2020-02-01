def count_indent(line):
  return len(line) - len(line.lstrip(' '))

def count_next_indent(lines):
  if len(lines) > 0:
    return count_indent(lines[0])
  else:
    return -1

def parse_file(name):
  with open(name, 'r') as source:
    return parse_str(source.readlines())

def parse_str(lines):
  data = {}
  for rline in lines:
    line = rline.strip()
    if len(line) == 0:
      continue

    parts = line.split(':')
    if len(parts) < 2:
      continue

    data[parts[0]] = parts[1].strip()

  return data
