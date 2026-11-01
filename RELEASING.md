# Releasing the GramAdapt clld app

Install from source on github:
```shell
git clone --branch v1.2.1 --depth 1 https://github.com/cldf-datasets/gramadapt gramadapt-cldf
git clone https://github.com/clld/gramadapt
cd gramadapt
pip install -e .[test]
```

Recreate the database:
```shell
clld initdb development.ini --cldf ../gramadapt-cldf/cldf/StructureDataset-metadata.json
```

Run the tests:
```shell
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO --compress gzip:9 gramadapt > gramadapt.sql.gz
```

