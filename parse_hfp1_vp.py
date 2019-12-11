from datetime import datetime
import logging as log
import argparse
import json
import sys
import csv

PLD_KEYS_ASSUMED = set([
    'desi', 'dir', 'oper', 'veh', 'tst', 'tsi', 'spd', 'hdg', 'lat',
    'long', 'acc', 'dl', 'odo', 'drst', 'oday', 'jrn', 'line', 'start'
])

log.basicConfig(level=log.DEBUG)

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
        d = json.loads(payload_str.strip())
        d = d['VP']
        if d.keys() != PLD_KEYS_ASSUMED:
            raise Exception('Keys different than assumed')
        if keep:
            d = {k:v for k, v in d.items() if k in keep}
        return d
    except:
        print_str = payload_str
        if len(payload_str) > 30:
            print_str = payload_str[:29] + ' ...'
        log.exception(f'Failed to parse {print_str}')
        sys.exit()
        return ''

def main():
    parser = argparse.ArgumentParser(description='Parse raw HFP data to csv.')
    parser.add_argument('inpath', type=str,
                        help='File path of raw text input file')
    parser.add_argument('outpath', type=str,
                        help='File path of csv output file')
    parser.add_argument('--keep', type=str, nargs='*', default=[],
                        help='Optional list of payload fields to keep')
    parser.add_argument('--debug', action='store_true',
                        help='Debug prints?')

    args = parser.parse_args()
    dbg = args.debug

    fields = args.keep or PLD_KEYS_ASSUMED
    i = 0
    n_success = 0
    stime = datetime.now()
    with open(args.inpath, 'r') as fobj_in:
        with open(args.outpath, 'w') as fobj_out:
            writer = csv.DictWriter(fobj_out, fieldnames=fields)
            writer.writeheader()
            for l in fobj_in:
                i += 1
                if dbg:
                    print(f'Line {i}', end='\r', flush=True)
                # Assuming that line has both topic and payload;
                # payload starts from a curly bracket so we pick a substring
                # from that position onwards
                pl = l[l.find('{'):]
                d = parse_vp_payload(payload_str=pl, keep=args.keep)
                if d:
                    writer.writerow(d)
                    n_success += 1
    etime = datetime.now()
    if dbg:
        log.info(f'Finished in {etime-stime}, {n_success}/{i} lines')

if __name__ == '__main__':
    main()
