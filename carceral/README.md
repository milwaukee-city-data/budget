# Retrieve population trends from Wisconsin DOC

## Install dependencies

```bash
$ python -m pip install -r requirements.txt
```

You will also need to make sure a Java executable is in your environment's
`$PATH`.

## To use

```bash
$ python -m get_doc_trends  # scrape DOC trends into a JSON file
$ python -m unpack_doc_trends  # plot trends and write to a CSV file
```
