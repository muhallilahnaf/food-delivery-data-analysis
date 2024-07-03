import os
import json
import pandas as pd


# global
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
cuisines = dict()
rest = dict()
menu = dict()
variations = dict()
cuisines_rest = []


def update_variations(code, food_id, var_data):
    global variations
    for variation in var_data:
        id = variation['id']
        temp = {
            'var_name': None,
            'price': None,
            'food_id': food_id,
            'rest_code': code
        }
        if 'name' in variation:
            temp['var_name'] = variation['name']
        if 'price' in variation:
            # if available, use price before discount as the price
            disc_price = 'price_before_discount'
            if disc_price in variation and variation[disc_price] > 0:
                temp['price'] = variation[disc_price]
            else:
                temp['price'] = variation['price']
        # add variation
        variations[id] = temp


def update_cuisines(code, rest_cui):
    global cuisines
    global cuisines_rest
    for cui in rest_cui:
        cui_name = {'name': cui['name']} 
        cui_id = str(cui['id'])
        # update cuisines fact table
        if cui_id not in cuisines:
            cuisines[cui_id] = cui_name
        # update cuisine-rest dim table
        cui_tup = (cui_id, code)
        if cui_tup not in cuisines_rest:
            cuisines_rest.append(cui_tup)


def update_menu(code, rest_menu):
    global menu
    if type(rest_menu) is not list:
        print(code, 'menu is not list')
        return
    categories = rest_menu[0]["menu_categories"]
    if type(categories) is not list:
        print(code, 'menu categories is not list')
        return
    # loop through categories
    for cat in categories:
        cat_name = cat['name']
        # loop through food items
        for food in cat['products']:
            id = food['id']
            temp = {
                'food_name': None,
                'master_category_id': None,
                'is_express_item': None,
                'category_name': cat_name,
                'rest_code': code
            }
            if 'name' in food:
                temp['food_name'] = food['name']
            if 'master_category_id' in food:
                temp['master_category_id'] = food['master_category_id']
            if 'is_express_item' in food:
                temp['is_express_item'] = food['is_express_item']
            menu[id] = temp                
            # update variations
            if 'product_variations' in food:
                update_variations(code, id, food['product_variations'])


def update_rest(code, val):
    global rest
    temp = {
        'budget': None,
        'is_vat_included': None,
        'is_voucher_enabled': None,
        'is_super_vendor': None,
        'vertical_segnment': None,
        'customer_type': None,
        'latitude': None,
        'longitude': None,
        # 'area': None,
        'post_code': None,
        'primary_cuisine_id': None,
        'rating': None,
        'review_number': None,
        'chain_main_vendor_code': None,
    }
    for k in temp.keys():
        try:
            temp[k] = val[k]
        except:
            continue
    try:
        temp['chain_main_vendor_code'] = val['chain']['main_vendor_code']
    except:
        pass
    rest[code] = temp


def read_and_update_data(data):
    global rest
    for code, val in data.items():
        val = val["data"]
        # update restaurant data
        update_rest(code, val)
        # update cuisines data
        if 'cuisines' in val:
            update_cuisines(code, val['cuisines'])
        # update menu data
        if 'menus' in val:
            update_menu(code, val['menus'])


def read(fname, index_col=False, cols=False):
    global ROOT_DIR
    file_path = os.path.join(ROOT_DIR, 'data', fname)
    if index_col:
        temp = dict()
        try:
            df = pd.read_csv(file_path, index_col=index_col)
            for index, row in df.iterrows():
                temp[str(index)] = row.to_dict()
        except:
            pass
        return temp
    if cols:
        temp = list()
        try:
            df = pd.read_csv(file_path)
            for i, row in df.iterrows():
                tup1 = row[cols[0]]
                tup2 = row[cols[1]]
                temp.append((tup1, tup2))
        except Exception as e:
            print(e)
        return temp
    

def save(name, data, table_type, cols=[], index_label=''):
    # convert to df
    if table_type == 'dim':
        df = pd.DataFrame(data, columns=cols)
    if table_type == 'fact':
        df = pd.DataFrame.from_dict(data, orient='index')
    # check NA
    na_cols = df.isna().sum()
    print(f'---{name}---')
    print(na_cols)
    # save as csv
    global ROOT_DIR
    if 'cuisine' not in name:
        name = name + '_clean'
    file_path = os.path.join(ROOT_DIR, 'data', f'{name}.csv')
    if table_type == 'dim':
        df.to_csv(file_path, index=False)
    if table_type == 'fact':
        df.to_csv(file_path, index_label=index_label)


def main():
    global cuisines
    global rest
    global menu
    global variations
    global cuisines_rest

    # file names, index label, col names
    cuisines_name = 'cuisines'
    cuisines_type = 'fact'
    cuisines_index_label = 'cui_id'
    
    rest_name = 'rest'
    rest_type = 'fact'
    rest_index_label = 'rest_code'

    menu_name = 'menu'
    menu_type = 'fact'
    menu_index_label = 'food_id'

    variations_name = 'variations'
    variations_type = 'fact'
    variations_index_label = 'var_id'

    cuisines_rest_name = 'cuisines_rest'
    cuisines_rest_type = 'dim'
    cuisines_rest_cols = ['cui_id', 'rest_code']

    # read csv
    cuisines = read(
        fname=f'{cuisines_name}.csv', 
        index_col=cuisines_index_label
    )
    rest = read(
        fname=f'{rest_name}.csv', 
        index_col=rest_index_label
    )
    menu = read(
        fname=f'{menu_name}.csv', 
        index_col=menu_index_label
    )
    variations = read(
        fname=f'{variations_name}.csv', 
        index_col=variations_index_label
    )
    cuisines_rest = read(
        fname=f'{cuisines_rest_name}.csv', 
        cols=cuisines_rest_cols
    )
    
    # loop through files and read
    global ROOT_DIR
    file_path = os.path.join(ROOT_DIR, 'data', 'restaurant_data.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
        # read and update data
        read_and_update_data(data)
    # save data
    save(cuisines_name, cuisines, cuisines_type, index_label=cuisines_index_label)
    save(rest_name, rest, rest_type, index_label=rest_index_label)
    save(menu_name, menu, menu_type, index_label=menu_index_label)
    save(variations_name, variations, variations_type, index_label=variations_index_label)
    save(cuisines_rest_name, cuisines_rest, cuisines_rest_type, cols=cuisines_rest_cols)


main()