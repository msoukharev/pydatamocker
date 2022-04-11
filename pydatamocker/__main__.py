import argparse
from pydatamocker import createFromJSON

def create_table(**kwargs):
    table = createFromJSON(kwargs['config'])
    res = table.sample()
    res.to_csv(kwargs.get('destination') or table.config['title'], index=False)

def main():
    ap = argparse.ArgumentParser(description="Create mock data tables with configuration files")
    ap.add_argument('--config', help='Config file(s) path', required=True)
    ap.add_argument('--dest', help='Schema file(s) destination', required=False)
    args = ap.parse_args()
    create_table(**{
        'config': args.config,
        'destination': args.dest,
    })
    pass

main()
