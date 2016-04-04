import random

def getLines(fpath, C):
  buffer = []

  f = open(fpath, 'r')
  keys = next(f)
  buffer.append(keys)

  for line_num, line in enumerate(f):
    n = line_num + 1.0
    r = random.random()
    if n <= C:
      buffer.append(line.strip())
    elif r < C/n:
      loc = random.randint(1, C-1)
      buffer[loc] = line.strip()

  return buffer


# if __name__ == "__main__":
#   main(sys.argv[1], sys.argv[2])

# From: http://stackoverflow.com/a/10821480/965352
