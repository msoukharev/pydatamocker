from asyncio import run
import os
import argparse
from pydatamocker import Schema, from_json
import re


async def create(insrc: str, outsrc: str):
    sch = Schema()
    fpaths = []
    if os.path.isdir(insrc):
        for fname in os.listdir(insrc):
            fpath = os.path.join(insrc, fname)
            if os.path.isfile(fpath) and re.fullmatch(r'^.+\.json$', fname):
                fpaths.append(fpath)
    elif os.path.isfile(insrc):
        fpaths.append(insrc)
    else:
        raise ValueError(f'Invalid input path path {insrc}')

    sch = await from_json(fpaths)
    sch.sample()

    if os.path.exists(outsrc):
        if not os.path.isdir(outsrc):
            raise ValueError(f'Path {outsrc} is not a directory')
    else:
        os.mkdir(outsrc)

    for table in sch.tables.values():
        with open(os.path.join(outsrc, table._name + '.csv'), 'wt+') as f:
            table._data.to_csv(f, index=False)


async def main():
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
    await create(args.insrc, args.outsrc)

run(main())
