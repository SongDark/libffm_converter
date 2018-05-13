import argparse, sys
from utils import delete, cat, split_csv, parallel_convert


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', dest='nr_thread', default=16, type=int)
    parser.add_argument('converter')
    parser.add_argument('source')
    parser.add_argument('destination')
    args = vars(parser.parse_args())

    return args

def main():

    args = parse_args()

    split_csv(args['source'], args['nr_thread'], True)

    parallel_convert(args['converter'], [args['source'], args['destination']], args['nr_thread'])

    cat(args['destination'], args['nr_thread'])

    delete(args['source'], args['nr_thread'])

    delete(args['destination'], args['nr_thread'])

main()