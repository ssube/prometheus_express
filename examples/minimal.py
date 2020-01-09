from prometheus_express import Counter

import time

def main():
  ctr = Counter('foo', 'some foos')

  while True:
    ctr.inc(1)
    time.sleep(1)
    print(ctr.render('esp32'))

main()
