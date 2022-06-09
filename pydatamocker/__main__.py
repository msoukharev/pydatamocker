import os
import argparse
import json
from pydatamocker import Schema, Table
import re


def form_table(fname: str) -> Table:
    with open(fname, 'rt') as f:
        content = json.load(f)
        bname = os.path.splitext(os.path.basename(fname))[0]
        table = Table(bname, content['size'])
        for field in content['fields']:
            table.field(field['name'], field['value'])
    return table


def create(insrc: str, outsrc: str):
    sch = Schema()

    if os.path.isdir(insrc):
        for fname in os.listdir(insrc):
            if os.path.isfile(os.path.basename(fname)[0]) and re.fullmatch('^*.json$', fname):
                sch.add(form_table(fname))
    elif os.path.isfile(insrc):
        sch.add(form_table(insrc))
    else:
        raise ValueError(f'Invalid input path path {insrc}')

    sch.sample()

    if os.path.exists(outsrc):
        if not os.path.isdir(outsrc):
            raise ValueError(f'Path {outsrc} is not a directory')
    else:
        os.mkdir(outsrc)

    for table in sch.tables.values():
        with open(os.path.join(outsrc, table._name + '.csv'), 'wt+') as f:
            table._data.to_csv(f, index=False)


def main():
    ap = argparse.ArgumentParser(description="Create mock data tables with configuration files")
    ap.add_argument(
        '--in',
        help='Table build file or directory containing table build files',
        dest='insrc',
        required=True
    )
    ap.add_argument(
        '--out',
        help='Destination directory for the result data',
        required=False,
        default=os.pardir,
        dest='outsrc'
    )
    args = ap.parse_args()
    create(args.insrc, args.outsrc)


main()
