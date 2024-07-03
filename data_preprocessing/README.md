**Navigation:**

[1. Data collection (scraping)](../data_collection)\
[2. Data preprocessing]()\
[3. Data integration](../data_integration)\
[4. Data analysis](../data_analysis)

## 2. Data Preprocessing

In this process, we convert the data into a structured format, remove unnecessary or redundant information, and perform any data cleaning (type checking, handling missing values) if necessary.

1. `restaurant_data_to_csv.py`

Using this script, we inspect the data at a higher-level to convert the semi-structured JSON data into a structured tabular (CSV) format.

There are two key observations:
1. Most of the nested keys contain redundant/unnecessary data.
2. The data of a restaurant can be divided into 4 parts:
    - restaurant (restaurant details)
	- cuisine (every restaurant serves one or more cuisine)
	- menu (each restaurant serves multiple food items)
	- variations (each food item has multiple variations based on price, portion, toppings, etc.)

The script performs the following steps:
1. loads data from the `restaurant_data.json` file
2. divides the data into the above-mentioned 4 parts
3. extracts the required nested key-values and flatten them (using the parent key as a prefix to the nested key)
4. generates the CSV files

After execution, the state of the data is as follows:

| file name | table type | description |
| --- | --- | --- |
| cuisines.csv | fact table | cuisine ID and name |
| rest.csv | fact table | restaurant code and details |
| menu.csv | fact table | food id and details |
| variations.csv | fact table | variation ID, food price and details |
| cuisines\_rest.csv | dimension table | connects restaurants and cuisines |

Next, we check the data at a lower-level to further filter out reduntant columns.

2. `data_check_*.ipynb`

The Python notebooks are used to check the data and only keep necessary/useful data. Using Pandas, we do the following steps:

- check value counts to determine unique values and their counts
- check missing or N/A values
- drop columns
- remove/anonymize personal information
- add new columns based on existing columns

The following changes are made:
1. **restaurant:**
    - dropped all columns except *rest_code, budget, is_vat_included, is_voucher_enabled, is_super_vendor, vertical_segment, customer_type, latitude, area, longitude, post_code, primary_cuisine_id, rating, review_number, chain_main_vendor_code*
    - export as `rest_clean.csv`
2. **menu:**
    - dropped all columns except *food_id, food_name, master_category_id, is_express_item, category_name, rest_code*
    - export as `menu_clean.csv`
3. **variations:**
    - if there is a discount on the price, we take the `price_before_discount` value as the `price`
    - dropped all columns except *var_id, var_name, price, food_id, rest_code*
    - export as `variations_clean.csv`

Now we have the following data files: 
`rest_clean.csv`, `menu_clean.csv`, `variations_clean.csv`, `cuisines.csv`, `cuisines_rest.csv`.

3. `restaurant_data_to_csv_clean.py`

This script performs the job of both `restaurant_data_to_csv.py` and `data_check_*.ipynb` i.e. it divides the JSON data into tabular CSV files and also cleans up the data to only store the required columns.

Once we know which columns to keep and how to preprocess the data, we can skip steps 1 and 2 and run this script directly to obtain the following data files:
`rest_clean.csv`, `menu_clean.csv`, `variations_clean.csv`, `cuisines.csv`, `cuisines_rest.csv`.


**NB:**
- *All the scripts are written such that we can re-run the scripts to continue the process, should any error occur or we run out of retries while scraping. At each step, data is not overwritten, rather missing data is added and differences are shown in console.*
- *After performing data preprocessing once, we know which columns/values we want to keep. So we can simplify the process for future by calling the API and only save the required key-values instead of saving all of them and then filtering.*
