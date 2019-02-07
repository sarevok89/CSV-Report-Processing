import pandas as pd
import pycountry
import sys


def get_country_code(subdivision_name):
    """
    Function using pycountry lookup method. It looks for subdivision's country code, which is given as two letters and then
    by looking for country with such country code it gets it's alpha_3 value, which is a three letters country code.

    :param subdivision_name: country subdivision name i.e. 'Fāryāb' is a subdivision of Afghanistan
    :return: returns either three letter country code, or 'XXX' if a country with this name doesn't exist
    """

    try:
        two_letters = pycountry.subdivisions.lookup(subdivision_name).country_code
        three_letters = pycountry.countries.lookup(two_letters).alpha_3
        return three_letters

    except LookupError:
        return "XXX"

    except Exception as e:
        print("\nError occured:")
        print(e, file=sys.stderr)


def generate_csv(csv_file):

    output_csv = 'output - ' + csv_file

    try:
        df = pd.read_csv(csv_file, names=['date', 'state name', 'number of impressions', 'CTR percentage'], encoding="utf_8")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file, names=['date', 'state name', 'number of impressions', 'CTR percentage'], encoding="utf_16")
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

    try:

        # Adding new column with 3 letter country code for each city

        df['three letter country code'] = df.apply(lambda x: get_country_code(x['state name']), axis=1)

        # Dropping 'state name' column as we don't need it anymore

        df.drop('state name', axis=1, inplace=True)

        # Reordering the dataframe

        df = df[['date', 'three letter country code', 'number of impressions', 'CTR percentage']]

        # Changing 'date' format to desired

        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y/%m/%d')

        # Stripping 'CTR percentage' cells off '%' sign and changing them to 'float' type

        df['CTR percentage'] = df['CTR percentage'].map(lambda x: x.strip("%"))
        df['CTR percentage'] = df['CTR percentage'].apply(lambda x: float(x)/100)

        # Calculating actual clicks on each view, rounding them up and getting rid of 'CTR percentage' column

        df['actual clicks'] = df['number of impressions'] * df['CTR percentage']
        df['actual clicks'] = df['actual clicks'].round()
        df['actual clicks'] = df['actual clicks'].astype(int)
        df.drop('CTR percentage', axis=1, inplace=True)

        # Grouping items by 'date' and 'three letter country code' columns and rounding up 'actual clicks' column

        df = df.groupby(['date', 'three letter country code']).aggregate(sum)

        # Creating csv file without column names

        df.to_csv(output_csv, header=False, encoding="UTF-8", line_terminator="\n")
        print(f"Successfully created '{output_csv}' file.")

    except Exception as e:
        print(e, file=sys.stderr)
        print("\nCouldn't create an output file")


if __name__ == "__main__":
    csv_file = input("Please enter name of your csv file followed by '.csv'.\n"
                     "It should be placed in the same directory as this script file. \n")
    generate_csv(csv_file)
