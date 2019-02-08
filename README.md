# CSV-Report-Processing
## Check `Task description.md` for more details about the task for this script

Loads csv file and process the data using pandas and pycountry modules. It checks whether csv file is encoded with UTF-8, or UTF-16 and opens it with proper encoding mode. At the end it creates new csv file with processed data and encoded in UTF-8.

### Modules and packages

Pandas:
```
pip install pandas
```
Pycountry:
```
pip install pycountry
```
### Getting started
```
import pandas as pd
import pycountry
import sys
```
### Running script
```
generate_csv('your_file.csv')
```
Running this will generate You new csv file with name of `output - your_file.csv`

### Thanks!
