from prometheus_client.parser import text_string_to_metric_families
import sys

metrics = text_string_to_metric_families(sys.stdin.read())
for family in metrics:
  for sample in family.samples:
    print('{0} ({1}): {2}'.format(*sample))