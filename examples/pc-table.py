#! /usr/bin/env python3

from argparse import ArgumentParser
from prometheus_client.parser import text_string_to_metric_families
import requests


parser = ArgumentParser(description='prometheus metrics collector')
parser.add_argument('endpoint', type=str)


def main():
    args = parser.parse_args()
    r = requests.get(args.endpoint)
    for family in text_string_to_metric_families(r.text):
            print('Metrics: {} ({})'.format(family.name, family.documentation))
            for sample in family.samples:
                print('Sample: {} ({})'.format(sample.value, sample.labels))


if __name__ == '__main__':
    main()
