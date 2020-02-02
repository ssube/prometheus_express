def parse_file(name, open=open):
  with open(name, 'r') as source:
    return parse_str(source.readlines())

def parse_str(lines):
  data = {}
  for rline in lines:
    line = rline.strip()
    if len(line) == 0 or line[0] == '#':
      continue

    parts = line.split(':')
    if len(parts) < 2:
      continue

    value = ''.join(parts[1:]).strip()
    if len(value) == 0:
      continue

    data[parts[0]] = value

  return data
