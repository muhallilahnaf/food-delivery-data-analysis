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


def delete_nested_keys(data):
    temp = dict()
    allowed = ['int', 'str', 'bool', 'NoneType', 'float']
    for k, v in data.items():
        if type(v).__name__ in allowed:
            temp[k] = v
    return temp


def add_new_fields(gdata, index, newdata):
    old = gdata[index]
    old_keys = set(old.keys())
    new_keys = set(newdata.keys())
    keys_absent_in_old = new_keys - old_keys
    if len(keys_absent_in_old) > 0:
        for k in keys_absent_in_old:
            gdata[index][k] = newdata[k]
    return gdata


def print_diff(gdata, index, newdata, code):
    old = gdata[index]
    for k, v in old.items():
        if newdata[k] and v != newdata[k]:
            print(f'value difference in code={code} key={k} old={v} new={newdata[k]}')


def update_variations(code, food_id, var_data):
    global variations
    for variation in var_data:
        id = variation['id']
        # delete id key
        del variation['id']
        # delete nested keys
        variation = delete_nested_keys(variation)
        # add food id and rest code
        variation['food_id'] = food_id
        variation['rest_code'] = code
        if id in variations:
            # if new fields found, add them
            variations = add_new_fields(gdata=variations, index=id, newdata=variation)
            # if change in value, print
            print_diff(gdata=variations, index=id, newdata=variation, code=code)
        else:
            # add food item to menu
            variations[id] = variation


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
            var_data = food['product_variations']
            # delete id key
            del food['id']
            # delete nested keys
            food = delete_nested_keys(food)
            # add category and rest code
            food['category'] = cat_name
            food['rest_code'] = code
            if id in menu:
                # if new fields found, add them
                menu = add_new_fields(gdata=menu, index=id, newdata=food)
                # if change in value, print
                print_diff(gdata=menu, index=id, newdata=food, code=code)
            else:
                # add food item to menu
                menu[id] = food
            # update variations
            update_variations(code, id, var_data)


def read_and_update_data(data):
    global rest
    for code, val in data.items():
        val = val["data"]
        # add nested keys to top level
        chain = val['chain']
        for k, v in chain.items():
            val[f'chain_{k}'] = v
        val['city_name'] = val['city']['name']

        rest_cuisines = val['cuisines']
        rest_menus = val['menus']
        
        # delete nested keys
        val = delete_nested_keys(val)
        if code in rest:
            # if new fields found, add them
            rest = add_new_fields(gdata=rest, index=code, newdata=val)
            # if change in value, print
            print_diff(gdata=rest, index=code, newdata=val, code=code)
        else:
            # add info to rest
            rest[code] = val                
        # update cuisines data
        update_cuisines(code, rest_cuisines)
        # update menu data
        update_menu(code, rest_menus)


def read(fname, index_col=False, cols=False):
    global ROOT_DIR
    file_path = os.path.join(ROOT_DIR, 'data', fname)
    if index_col:
        temp = dict()
        try:
            df = pd.read_csv(file_path, index_col=index_col)
            for index, row in df.iterrows():
                temp[str(index)] = row.to_dict()
        except Exception as e:
            print(e)
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