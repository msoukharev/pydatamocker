# Pydatamocker

Create rich mock data for testing, learning and proofs of concepts!

## About

Pydatamocker can generate tabular data of various data types and distributions using random generation and sampling. It is also possible to create a lookups from one table to another. Sampling is very fast even when generating 1'000'000s of records with ~10 fields. The tables are presented in the form of [pandas](https://pandas.pydata.org) DataFrames.

The API for writing the tables to files is easy to use. Just specify the file path and the formatting is inferred from the file extension, be it csv, tsv, json or a simple text file.

### Datasets

Some datasets are included with the package. They can be sampled for fields. Datasets included are:

* ~ 20'000 names of various origins
* ~ 20'000 surnames of various origins

## Get started

### Production

Install the prod version by running
```sh
python3 -m pip install pydatamocker
```

### Testing

Install the latest testing version by running
```sh
python3 -m pip install --index-url https://test.pypi.org/simple/ pydatamocker
```

### Code example

You can generate mock tables with

```python
# Create data table
acc = MockTable('Accounts')
# Create an integer field with binomial(10, 0.4) distribution
acc.add_field('YearsOfExperience', 'integer', distr='binomial', n=10, p=0.4)
# Field with real randomized first names
acc.add_field('FirstName', 'first_name')
# Field with real randomized surnames
acc.add_field('LastName', 'last_name')
# Date field
acc.add_field('DateHired', 'date', distr='uniform', start='2016-10-25', end='2020-02-10')
# Integer field
acc.add_field('Id', 'integer', distr='range', start=100000, end=90000000)

# Create sample
acc.sample(100_000)

# Create another table
audit = MockTable('Audits')
# Add a lookup
audit.add_lookup(acc, ['Id'])
# Add an enum field
audit.add_field('Subject', 'enum', values=['PPI Access', 'Administrative Reconfiguration', 'Phone contact'], weights=[5, 1, 2])
audit.add_field('ContactedAt', 'datetime', distr='range', start='2016-10-25', end='2019-03-15')

audit.sample(1_000_000)

# Get pandas dataframe
acc_df = acc.get_dataframe()
audit_df = audit.get_dataframe()

# Dump into csv (other formats also supported)
acc.dump('accounts.csv')
audit.dump('audits.csv')
```
