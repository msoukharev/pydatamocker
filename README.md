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
users = pdm.createEmpty('Users')

users.field('FirstName', { 'type': 'dataset', 'dataset': {
    'name': 'first_name',
    }
})
users.field('LastName', { 'type': 'dataset', 'dataset': {
    'name': 'last_name',
    'restrict': 3
    }
})
users.field('Age', { 'type': 'number', 'distr': { 'name': 'binomial', 'n': 40, 'p': 0.7 } })
users.field('SpouseAge', { 'type': 'number', 'distr': { 'name': 'normal', 'mean': 40, 'std': 10 } })
users.field('Status', { 'type': 'enum', 'distr': { 'values': ['Active', 'Inactive', 'Pending confirmation'],
    'weights': [23, 69, 3], 'name': 'shuffled' } })
users.field('Bucket', { 'type': 'enum', 'distr': { 'values': ['1', '2', '3', '4', '5', '6'], 'name': 'ordered' } })
users.field('Grade', { 'type': 'enum', 'distr': { 'values': [1.5, 2.7, 3.3, 4], 'name': 'shuffled' }})
users.field('LastLogin', { 'type': 'datetime', 'distr': { 'name': 'range', 'start': '2015-02-13T8:10:30', 'end': '2021-10-30T19:30:43' }})
users.field('RegisteredDate', { 'type': 'datetime', 'distr': { 'name': 'range', 'start': '2015-02-13', 'end': '2021-10-30' }, 'format': 'date'})
users.field('ConstField', { 'type': 'number', 'const': 10 , 'filters': [
    {
        'operator': 'add',
        'argument': {
            'type': 'number',
            'const': 20
        }
    },
    {
        'operator': 'subtract',
        'argument': {
            'type': 'number',
            'distr': {
                'name': 'normal',
                'std': 20,
                'mean': 30
            }
        }
    },
    {
        'operator': 'floor',
        'argument': {
            'type': 'number',
            'const': 0
        }
    },
    {
        'operator': 'round',
        'argument': {
            'type': 'number',
            'const': 0
        }
    }
]})

df = users.sample(300_000)
df.head(10)
```
