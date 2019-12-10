import logging as log
import argparse
import json
import csv

PLD_KEYS_ASSUMED = set([
    'desi', 'dir', 'oper', 'veh', 'tst', 'tsi', 'spd', 'hdg', 'lat',
    'long', 'acc', 'dl', 'odo', 'drst', 'oday', 'jrn', 'line', 'start'
])

log.basicConfig(level=logging.DEBUG)

def parse_vp_payload(payload_str, keep=[]):
    """
    Parse raw text payload, return as dictionary.
    Assumed format of ``payload_str``, example:
    {"VP":{"desi":"6T","dir":"2","oper":40,"veh":414,"tst":"2019-06-03T15:30:01Z",\
    "tsi":1559575801,"spd":5.93,"hdg":178,"lat":60.157171,"long":24.921847,\
    "acc":-0.72,"dl":-25,"odo":7701,"drst":0,"oday":"2019-06-03","jrn":392,\
    "line":35,"start":"17:51"}}
    ``keep``: optional list of keys to keep, other key-value pairs are dropped.
    """
    try:
        d = json.loads(payload_str)
        d = d['VP']
        if d.keys() == PLD_KEYS_ASSUMED
        if keep:
            d = {k:v for k, v in d.items() if k in keep}
        return d
    except:
        print_str = payload_str
        if len(payload_str) > 30:
            print_str = payload_str[:29] + ' ...'
        log.exception(f'Failed to parse {print_str}')
        return None

def main():
    parser = argparse.ArgumentParser(description='Parse raw HFP data to csv.')
    parser.add_argument('inpath', type=str, required=True,
                        help='File path of raw text input file')
    parser.add_argument('outpath', type=str, required=True,
                        help='File path of csv output file')
    parser.add_argument('--keep', type=str, nargs='*', default=[],
                        help='Optional list of payload fields to keep')

    args = parser.parse_args()
