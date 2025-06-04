import pandas as pd
import sys
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)


def find_scrip_codes_by_keyword_and_type(
    csv_path,
    keyword,
    exchange_type_filter,
    exchange,
    name_column='FullName',
    scrip_code_column='ScripCode',
    exchange_column='Exch',
    exchange_type_column='ExchType'
):
    # Load the CSV
    df = pd.read_csv(csv_path)

    # Filter by keyword in Full Name (case-insensitive)
    name_matches = df[df[name_column].str.contains(keyword, case=False, na=False)]

    # Further filter by Exchange Type (exact match)
    filtered1 = name_matches[name_matches[exchange_type_column] == exchange_type_filter]

    filtered = filtered1[filtered1[exchange_column]== exchange]

    if filtered.empty:
        print(f"No matches found for keyword: '{keyword}' and Exchange Type: '{exchange_type_filter}'")
        return None

    # Select only relevant columns to return
    result = filtered[[scrip_code_column, exchange_column, exchange_type_column, name_column]]

    print(f"Found {len(result)} matches:")

    return result

# Example usage
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "scrip_master.csv")

keyword = sys.argv[1]
exchange_type = sys.argv[2]  
exchange = sys.argv[3]

results = find_scrip_codes_by_keyword_and_type(csv_path, keyword, exchange_type, exchange)

if results is not None:
    print(results)
