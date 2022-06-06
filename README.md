# Pydatamocker

Create lots of rich mock data.

## About

Pydatamocker can generate relational data with values of various data types and distributions using random generation and sampling.

### Datasets

The package bundles a few datasets in `.pkl` files. They can be sampled by specifying `dataset`.

| Dataset | Description | Count |
|:-------:|:-----------:|:-----:|
| first_name | Collection of given names | ~ 20'000 |
| last_name | Collection of family names | ~ 20'000 |

### Code example

```python
from pydatamocker import Table, Schema

sch = Schema()

users = sch.add(Table('Users', 1_000))

users.field('FirstName', { 'dataset': { 'name': 'first_name' } })
users.field('LastName', { 'dataset': {
    'name': 'last_name',
    'restrict': 3
}})
users.field('Age', { 'binomial': { 'n': 40, 'p': 0.7 } })
users.field('SpouseAge', { 'normal': { 'mean': 40, 'std': 10 } })
users.field('Status', { 'enum': { 'values': ['Active', 'Inactive', 'Pending confirmation'],
    'counts': [23, 69, 3], 'shuffle': True } })
users.field('Bucket', { 'enum': { 'values': ['1', '2', '3', '4', '5', '6'], 'shuffle': False } })
users.field('Grade', { 'enum': { 'values': [1.5, 2.7, 3.3, 4], 'shuffle': True } })
users.field('LastLogin', { 'uniform': { 'min': '2015-02-13T8:10:30', 'max': '2021-10-30T19:30:43' } })
users.field('RegisteredDate', { 'uniform': { 'min': '2015-02-13', 'max': '2021-10-30', 'format': 'date' } })
users.field('ConstField', { 'const': 10, 'filters': [
    {
        'multiply': {
            'const': 20
        }
    },
    {
        'subtract': {
            'normal': {
                'mean': 40,
                'std': 10
            }
        }
    },
    {
        'floor': 10
    },
    {
        'round': 1
    },
    {
        'multiply': {
            'ref': (users._name, 'Grade')
        }
    }
]})



sch.sample()

df = users.getData()
df.head(5)

```
