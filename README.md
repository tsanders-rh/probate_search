This utility allows for multi-county probate records searching (Estate and Marriage) for South Carolina.

```console
Usage: probate_search_cli.py <options>

Search South Carolina Probate Data Records.  The results are output to a .csv
file.

Options:
  -h, --help            show this help message and exit
  -c COUNTY, --county=COUNTY
                        Specify a county for the search. Optionally, you can
                        specify multiple ("i.e. -c Aiken -c Charleston") or
                        "ALL" to search all counties.
  -t TYPE, --type=TYPE  Specify the type of records to be searched.  Valid
                        values are "Estate" (Default) or "Marriage".
  -l LASTNAME, --lastname=LASTNAME
                        Specify the last or business name for the search. You
                        can use "%" to wildcard.
  -f FIRSTNAME, --firstname=FIRSTNAME
                        Specify the first name for the search. You can use "%"
                        to wildcard.
  -m MIDDLENAME, --middlename=MIDDLENAME
                        Specify the middle name for the search. You can use
                        "%" to wildcard.
```
