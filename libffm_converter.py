import argparse, sys
import csv
from utils import hashstr

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', dest='bins', default=int(1e+6), type=int)
    parser.add_argument('csvfile')
    parser.add_argument('ffmfile')
    args = vars(parser.parse_args())

    return args

args = parse_args()

with open(args['ffmfile'], 'w') as f:
    for row in csv.DictReader(open(args['csvfile'])):
        # row is dict
        row_to_write = [row['label'], ]
        field = 0
        for feat in row.keys():
            if feat == 'label':
                continue
            items = str(row[feat]).split(" ")
            for item in items:
                row_to_write.append(":".join([str(field), hashstr(str(field)+'='+item, args['bins']), '1']))
            field += 1
        row_to_write = " ".join(row_to_write)
        f.write(row_to_write + '\n')