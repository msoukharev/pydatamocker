# Pydatamocker

Create lots of rich mock data.

## About

Pydatamocker can generate tabular data of various data types and distributions using random generation and sampling. It is also possible to create a lookups from one table to another. Sampling is very fast even when generating 1'000'000s of records with ~10 fields. Tables are hold their data in DataFrame [see: pandas](https://pandas.pydata.org).

### Datasets

The package bundles a few datasets in `.pkl` files. They can be sampled by specifying `dataset`.

| Dataset | Description | Count |
|:-------:|:-----------:|:-----:|
| first_name | Collection of given names | ~ 20'000 |
| last_name | Collection of family names | ~ 20'000 |

### Code example

```python
import pydatamocker as pdm

users = pdm.createEmpty('Users')

users.field(name='FirstName', dataset='first_name')
users.field(name='LastName', dataset='last_name')
users.field(name='SpouseLastName', dataset='last_name')
users.field(name='Age', datatype='integer', distr='binomial', n=40, p=0.7)
users.field(name='SpouseAge', datatype='integer', distr='normal', mean=40, std=10)
users.field(name='Status', datatype='enum', values=['Active', 'Inactive', 'Pending confirmation'], \
    weights=[23, 69, 3], distr='shuffled')
users.field(name='Bucket', datatype='enum', values=['1', '2', '3', '4', '5', '6'], distr='ordered')
users.field(name='Grade', datatype='enum', values=[1.5, 2.7, 3.3, 4], distr='shuffled')
users.field(name='DateRegistered', datatype='date', distr='range', start='2010-02-13', end='2021-10-30')
users.field(name='LastLogin', datatype='datetime', distr='range', start='2015-02-13T8:10:30', end='2021-10-30T19:30:43')

df = users.sample(1_000_000)
```
