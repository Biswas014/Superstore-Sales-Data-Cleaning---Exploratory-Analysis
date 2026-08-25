import pandas as pd
import numpy as np


## for showing the full dataset in the terminal
pd.set_option('display.max_columns',None)
pd.set_option('display.width',None)
pd.set_option('display.max_colwidth',None)

## load the file and take it inside a dataframe
df = pd.read_csv("E:\Projects\Portfolio_Projects\Python\Superstore sales analytics\Raw_Superstore_dt.csv")

## Data Exploration

# print(df.shape)  #rows - 52212,clm- 22

#print(df.head(10)) 

# print(df.columns)
# print(df.dtypes)
# print(df.info())

# print(df['Unnamed: 0'])

## drop unnecessary columns 
  
  # one way (just drop it)
# df.drop(columns= ['Unnamed: 0'],inplace= True)
  
  # or drop all columns follows the same pattern
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# print(df)

## creating a user defined function for checking whether records of a column follows a specified pattern, if yes remove those
 
import re   # importing regular expression

def check_pattern(df,column,pattern):
    """Returns rows where the column value does NOT match the given regex pattern"""
    mask = ~df[column].astype(str).str.match(pattern)
    bad_rows = df[mask]
    print(f" column '{column}': {mask.sum()} out of {len(df)} don't match the pattern")
    return bad_rows    # to show the pattern of some of bad rows

## for checking empty, whitespaces, and leading or trailing spaces

def missing_value_report(df,col):
    empty_str = (df[col] == '').sum()
    whitespace_only = (df[col].str.strip() == '').sum() - empty_str
    has_leading_trailing = df[col].notnull() & (df[col] != df[col].str.strip())

    print(f"empty_string : {empty_str}")
    print(f"whitespace_only : {whitespace_only}")
    print(f"leading/trailing : {has_leading_trailing.sum()}")

## retrieve nan/ unrecognized nulls(python) values in a clmn
def nan_or_unrecognized_missing(df, col, possible_junk_tokens=None):
    if possible_junk_tokens is None:
        possible_junk_tokens = ['N/A', 'n/a', 'NA', 'missing', 'Missing', '?', '-', 
                              'NULL', 'null', 'None']
    
    is_nan = df[col].isnull()
    is_known_junk = df[col].isin(possible_junk_tokens)
    
    # Combine: anything flagged as junk , but NOT true NaN
    non_recognized_mask = (is_known_junk ) & ~is_nan  #both condition need to be true
    
    print(f"Column: {col}")
    print(f"  True NaN/None:                {is_nan.sum()}")
    print(f"  Non-recognized junk values:   {non_recognized_mask.sum()}")
    print()
    print("Breakdown of non-recognized values found:")
    print(df.loc[non_recognized_mask, col].value_counts())
    
    # return df.loc[non_recognized_mask, col]   #to retrieve those rows where selected column has non recognized junks 

# to remove unicode glitches
import unicodedata

def clean_text(text):
    if pd.isna(text):
        return text
    # Normalize accented characters back to plain ASCII equivalents
    normalized = unicodedata.normalize('NFKD', str(text))
    return normalized.encode('ascii', 'ignore').decode('utf-8')

## date handling udfs

patterns = {
    'YYYY-MM-DD': r'^\d{4}-\d{2}-\d{2}$',
    'DD-MM-YYYY': r'^\d{2}-\d{2}-\d{4}$',
    'DD/MM/YYYY': r'^\d{2}/\d{2}/\d{4}$',
    'Mon DD, YYYY': r'^[A-Za-z]{3} \d{2}, \d{4}$',
}

def detect_format(value, patterns):
    if pd.isnull(value):
        return np.nan
    value = str(value)
    for fmt_name, pattern in patterns.items():
        if re.match(pattern, value):
            return fmt_name
    return 'UNKNOWN'


def detect_day_position(value):
    """
    Returns 'first' if we can prove day comes first (DD/MM or DD-MM),
    Returns 'second' if we can prove day comes second (MM/DD or MM-DD),
    Returns 'ambiguous' if neither number is > 12 (can't tell from this value alone)
    """
    parts = re.split(r'[-/]', str(value))
    if len(parts) != 3:
        return 'invalid'
    try:
        first, second = int(parts[0]), int(parts[1])
    except ValueError:
        return 'invalid'
    
    if first > 12:
        return 'first'       # first number can't be a month → it's the day → DD-MM/DD/MM
    elif second > 12:
        return 'second'      # second number can't be a month → it's the day → MM-DD/MM/DD
    else:
        return 'ambiguous'   # both ≤ 12, can't prove either way from this single value


## order id handling 

# print(missing_value_report(df,'order_id')) #0
# print()
# print(nan_or_unrecognized_missing(df, 'order_id'))   #0

# bad_id = check_pattern(df=df, column='order_id',pattern= r'^[A-Za-z]{2,}-\d{4}-\d+$')

# print(bad_id)

df['order_id'] = df['order_id'].str.replace('_','-',regex= False)

# bad_id = check_pattern(df=df, column='order_id',pattern= r'^[A-Za-z]{2,}-\d{4}-\d+$')
# print(bad_id)   #0

# print(df['order_id'].nunique())    # 26898 (no of distinct order id's)

# print(df['order_id'].nunique(dropna= False)) # to count no of unique values including nan = (26898)

# print(df['order_id'].unique())   # to see actual unique values

# print(df['order_id'].dtypes)   # str

## duplicates handliing

# dupe_mask = df.duplicated(keep=False)   # keep=False also take the original row 
# duplicates = df[dupe_mask].sort_values('order_id')

# print(df.duplicated().sum()) #exact no of those rows which are repeated (21)
# print(f"Found {dupe_mask.sum()} rows involved in duplicates") #42
# print(duplicates[['order_id','order_date','product_id','sales']])

df.drop_duplicates(inplace=True)  
# print(df.duplicated().sum())    #0

#  print(df['order_id'].dtypes)  # str


## order date handling

# print(missing_value_report(df,'order_date'))    #0
# print(nan_or_unrecognized_missing(df, 'order_date')) #0


#  print(df['order_date'].dtypes)  # str


## changing the all uncommon date formats into 'yyyy-mm-dd'

# df['detected_format'] = df['order_date'].apply(lambda x: detect_format(x, patterns))

# See the breakdown — this is the key diagnostic step
# print(df[['detected_format','order_date']].head(30))

# Rows where we're uncertain it's DD/MM because day > 12
# certain_dmy = df[df['order_date'].apply(detect_day_position)]
# print(certain_dmy['order_date'].head(10))

## to specify all the formats in pd.to_datetime's format 
formats_to_try = ['%d-%m-%Y','%m/%d/%Y','%b %d, %Y']
result = pd.Series(pd.NaT,index = df.index)

for fmt in formats_to_try:
    still_unconverted = result.isnull()
    parsed = pd.to_datetime(df.loc[still_unconverted,'order_date'],format = fmt, errors= 'coerce')
    result.loc[still_unconverted] = parsed
    

df['order_date_clean'] = result
# print(f"rows still unconverted: {result.isnull().sum() - df['order_date'].isnull().sum()}")

# print(df[['order_date','order_date_clean']].head(30))

df.drop('order_date',axis= 1,inplace = True)
# print(df.head(10))

df.rename(columns= {'order_date_clean':'order_date'},inplace= True)
# print(df.head(10))

# print(df['order_date'].dtypes)   #datetime64[ns]
# print(df['order_date'].apply(type).value_counts())   # shows exactly how many date types are there


## customer name handling

# print(missing_value_report(df,'customer_name')) #l & t spaces = 5
# print(nan_or_unrecognized_missing(df,'customer_name'))   #nan- 587, junk - 455

df['customer_name'] = df['customer_name'].str.strip().str.title()

junk_tokens_csm = ['Missing','-','?']
df['customer_name'] = df['customer_name'].replace(junk_tokens_csm,np.nan)

# print(df['customer_name'].value_counts(dropna=False).head(30))  #also group the missing records(nan)

# print(df['customer_name'].dtypes)  #str
df['customer_name'] = df['customer_name'].apply(clean_text)   #remove unicodes

print(df['customer_name'].isna().sum())

## shipping cost handling

# print(missing_value_report(df,'shipping_cost'))
# print()
# print(nan_or_unrecognized_missing(df,'shipping_cost'))

# print(df['shipping_cost'].head(20))


# bad_scs = check_pattern(df,'shipping_cost',r'^[0-9]+.[0-9]+$')
# print(bad_scs.tail(15))

df['shipping_cost'] = df['shipping_cost'].str.replace('$','',regex= False)
# OR df['shipping_cost'].str.replace(r'[\$,]', '', regex=True)

# print(df['shipping_cost'].dtypes)

# making shipping cost absolute 

df['shipping_cost'].abs

 ##crosschecking for existence of negative values
# negative_scs = df[df['shipping_cost'] < 0]
# print(negative_scs)

df['shipping_cost'] = pd.to_numeric(df['shipping_cost'],errors='coerce')
# print(df['shipping_cost'].dtypes) # float64

# print(df['shipping_cost'].head(30))


## market clmn handling

# print(nan_or_unrecognized_missing(df,'market'))
# print()
# print(missing_value_report(df,'market'))

# print(df['market'].dtypes) #str

# print(df['market'].value_counts())

df['market'] = df['market'].str.upper()

# print(df['market'].value_counts())


## profit clm handling

# print(nan_or_unrecognized_missing(df,'profit'))
# print()
# print(missing_value_report(df,'profit'))

# print(df['profit'].dtypes)  #str

# bad_pr = check_pattern(df,'profit',r'^[0-9]+.[0-9]+$')
# print(bad_pr.head(15))
# print(bad_pr.shape)    # 13525

# print(df['profit'].head(20))

df['profit'] = pd.to_numeric(df['profit'],errors='coerce')

# print(df['profit'].dtypes)  #float64

# print(nan_or_unrecognized_missing(df,'profit'))

# negative_nan_pr = df[(df['profit'] < 0) | (df['profit'].isna()) ]     ## '|' means - or

# print(negative_nan_pr.shape)  #13525

df['profit'] =df['profit'].round(2)
# print(df['profit'])


## product id clm handling

# print(nan_or_unrecognized_missing(df,'product_id')) 
# print()
# print(missing_value_report(df,'product_id'))
# print()
# print(df['product_id'].dtypes)  #str

# print(df['product_id'].head(30))
  
##following pattern - (upper letter 3 or more digits, 2 or more upper letters, any no of digits)(separated by hyphen) 
# print(check_pattern(df,'product_id',r'^[A-Z]{3,}-[A-Z]{2,}-\d+$'))

## replace 'space dash and then again space or not space' with only 'dash'
df['product_id'] = df['product_id'].str.replace(r'\s*-\s*','-',regex= True)

 ## confirm the replace was applied perfectly
# print(check_pattern(df,'product_id',r'^[A-Z]{3,}-[A-Z]{2,}-\d+$'))


## region clm handling

# print(nan_or_unrecognized_missing(df,'region'))  #0
# print()
# print(missing_value_report(df,'region'))
# print()
# print(df['region'].dtypes)  #str

# print(df['region'].value_counts())

## note:if region are same like market some market names are copied as region values because they are not sub-divided further.


## year clm handling

# print(nan_or_unrecognized_missing(df,'year'))  #0
# print()
# print(missing_value_report(df,'year'))
# print()
# print(df['year'].dtypes)  # int64

# print(df['year'].value_counts())


## product name clm handle

# print(nan_or_unrecognized_missing(df,'product_name'))  #0
# print()
# print(missing_value_report(df,'product_name'))
# print()
# print(df['product_name'].dtypes)  # str

# print(df['product_name'].unique())

# print(df['product_name'].value_counts().head(20))

## removing unicodes from product name clm
df['product_name'] = df['product_name'].apply(clean_text)


## ship mode clm handling

# print(nan_or_unrecognized_missing(df,'ship_mode'))  
# print()
# print(missing_value_report(df,'ship_mode'))
# print()
# print(df['ship_mode'].dtypes)  # str

df['ship_mode'] = df['ship_mode'].str.upper()

sh_md_junks = ['MISSING','-','?']
df['ship_mode'] = df['ship_mode'].replace(sh_md_junks,np.nan)

# print(df['ship_mode'].value_counts(dropna= False))


## country clm handle

# print(nan_or_unrecognized_missing(df,'country'))  #0
# print()
# print(missing_value_report(df,'country'))
# print()
# print(df['country'].dtypes)  # str

df['country'] = df['country'].str.strip()
# (df['country'].value_counts())

# print(df['country'].nunique())     #153

## to show all the distinct country names together at one place
unique_countries = df['country'].unique().tolist()
# print(unique_countries)

# print(df['country'].value_counts().tail(30))

## change the same type of country names to the country names which come maximum times
df['country'] = df['country'].str.replace(
    {'USA':'United States',
     'US':'United States',
     'United States of America':'United States',
     'UK':'United Kingdom'})

# print(df['country'].value_counts())
# print(df['country'].nunique())   #149


## order_priority clm handling

# print(nan_or_unrecognized_missing(df,'order_priority'))  
# print()
# print(missing_value_report(df,'order_priority')) #0
# print()
# print(df['order_priority'].dtypes)  # str

op_junks = ['missing','-','?']
df['order_priority'] = df['order_priority'].replace(op_junks,np.nan)

df['order_priority'] = df['order_priority'].str.upper()
# print(df['order_priority'].value_counts())

## quantity clm handling

# print(nan_or_unrecognized_missing(df,'quantity'))  #0
# print()
# ## print(missing_value_report(df,'quantity')) # won't work in numeric data type
# print()
# print(df['quantity'].dtypes)  # int64

# print(check_pattern(df,'quantity',r'^\d{1,}$'))  # negative values exist

df['quantity'] = df['quantity'].abs()
# print(check_pattern(df,'quantity',r'^\d{1,}$'))   #0 - negative
 

## category clm handling

# print(nan_or_unrecognized_missing(df,'category'))  #0
# print()
# print(missing_value_report(df,'category')) 
# print()
# print(df['category'].dtypes)  # str

df['category'] = df['category'].str.strip().str.title()
# print(df['category'].value_counts())

df['category'] = df['category'].replace(
                   {'Office Supply':'Office Supplies',
                    'Offce Supplies':'Office Supplies',
                    'Tecnology':'Technology',
                    'Frunitre':'Furniture',
                    'Furnitur':'Furniture',
                    'Technolgy':'Technology' 
                  })

# print(df['category'].nunique()) #3


## sub_category clm handling

# print(nan_or_unrecognized_missing(df,'sub_category'))  #0
# print()
# print(missing_value_report(df,'sub_category'))  #0
# print()
# print(df['sub_category'].dtypes)  # str

df['sub_category'] = df['sub_category'].str.title()
# print(df['sub_category'].value_counts())

## ship_date clm handling

# print(nan_or_unrecognized_missing(df,'ship_date'))  #0
# print()
# print(missing_value_report(df,'ship_date'))  #0
# print()
# print(df['ship_date'].dtypes)  # str

# df['detected_format'] = df['ship_date'].apply(lambda x: detect_format(x, patterns))

# See the breakdown — this is the key diagnostic step
# print(df[['detected_format','ship_date']].tail(30))


# print(df['detected_format'].value_counts())  # it can't take correct formats but take all formats where they sure
                             # for example it doesn't take 'yyyy-mm-dd' which has no similar but ambiguous format

# Rows where we're CERTAIN it's DD/MM because day > 12
# certain_dmy = df[df['ship_date'].apply(has_day_over_12)]
# # print(certain_dmy['ship_date'].head(10))


formats_to_try2 = ['%d-%m-%Y','%m/%d/%Y','%b %d, %Y']
result2 = pd.Series(pd.NaT,index = df.index)

for fmt in formats_to_try2:
    still_unconverted2 = result2.isnull()
    parsed2 = pd.to_datetime(df.loc[still_unconverted2,'ship_date'],format = fmt, errors= 'coerce')
    result2.loc[still_unconverted2] = parsed2

df['ship_date_cleaned'] = result2

df.drop('ship_date',axis= 1,inplace = True)

df.rename(columns= {'ship_date_cleaned':'ship_date'},inplace= True)

# print(df['ship_date'].dtypes)     #datetime64

  ## check are there dates of shipping lower than order date
# print(df['order_date'].dtypes) # datetime
# print(df['ship_date'].dtypes) #datetime


# print(df['ship_date'].apply(type).value_counts())   # shows exactly what types are mixed in

invalid_sd = df['order_date'] > df['ship_date'] 
# print(f"Found {invalid_sd.sum()} rows where ship_date is before order_date") #4806
 
 ## to show those rows where the condition is followed
# print(invalid_sd['order_id','order_date','ship_date'])

# print(df['ship_date'].isna().sum())   #0

## to convert invalid shipping dates into pandas' nat(not a time )
df.loc[invalid_sd,'ship_date'] = pd.NaT
# print(df[df['ship_date'] < df['order_date']])

# print(df['ship_date'].isna().sum())   #4806


## to retreive rows where ship date is nat

# print(df['ship_date'].value_counts(dropna= False).head(10))
# print(df['ship_date'].isna().mean()*100)      #9.21 (percentage of nat or nan available in ship date column)



## segment clm handling

# print(nan_or_unrecognized_missing(df,'segment'))  #0
# print()
# print(missing_value_report(df,'segment'))  #0
# print()
# print(df['segment'].dtypes)  # str

df['segment'] = df['segment'].str.title()
# print(df['segment'].value_counts())


## state clm handling

# print(nan_or_unrecognized_missing(df,'state'))  
# print()
# print(missing_value_report(df,'state'))  
# print()
# print(df['state'].dtypes)  # str

df['state'] = df['state'].str.strip()

state_junks = ['-','missing','?']
df['state'] = df['state'].replace(state_junks,np.nan,regex= False)

# print(nan_or_unrecognized_missing(df,'state'))  #junks - 0 , nan exists
# print(missing_value_report(df,'state'))    #0

# print(df['state'].value_counts().tail(30))

df['state'] = df['state'].apply(clean_text)

# print(df['state'].value_counts().head(30))
# print(df['state'].unique())


## discount clm handling

# print(nan_or_unrecognized_missing(df,'discount'))  
# print()
# print(missing_value_report(df,'discount'))  #0
# print()
# print(df['discount'].dtypes)  # str
# print(df['discount'].tail(30))

# print(nan_or_unrecognized_missing(df,'discount'))  

# print(df[df['discount'] < 0])

# print(df['discount'].str.endswith('%').mean()*100)   #4956 (9.4% out of all records)

# print(df[df['discount'].str.endswith('%')].head(20))

## we can't convert a string value into float. so converting discount into numeric is important
df['discount'] = pd.to_numeric(df['discount'],errors='coerce')

def percent_to_decimal(val):
    if pd.isnull(val):
        return val
    s = str(val).strip()
    if s.endswith('%'):
        num = float(s.replace('%', ''))
        return round(num / 100, 4)
    return round(float(s), 4)

# ## for changing percentage values to decimal dividing by 100
# discount_str =  str(df['discount']).strip()
# if discount_str.endswith('%'):
#     num = float(discount_str.replace('%',''))
#     round

df['discount'] = df['discount'].apply(percent_to_decimal)

# print(df['discount'].dtypes)  #str
# print(df['discount'].tail(30))

# print(df['discount'].isna().sum())      #7262


## sales clm handling

# print(nan_or_unrecognized_missing(df,'sales'))  
# print()
# print(missing_value_report(df,'sales'))  #0
# print()
# print(df['sales'].dtypes)  # str

sales_junks = ['missing','-','?']
df['sales'] = df['sales'].replace(sales_junks,np.nan,regex= False)

# print(nan_or_unrecognized_missing(df,'sales'))  
# print(df['sales'].tail(30))
df['sales'] = df['sales'].str.replace('$','',regex= False)
# print(df['sales'].tail(30))

# print(df[df['sales'] < 0])       #no negative

def to_accounting_format(val):
    if pd.isnull(val):
        return val
    s = str(val).replace(',', '').replace('$', '').strip()
    try:
        num = float(s)
    except ValueError:
        return val  # leave truly unparseable junk untouched
    if num < 0:
        return f"({abs(num):,.2f})"   # negatives in parentheses — standard accounting style
    else:
        return f"{num:,.2f}"

df['sales'] = df['sales'].apply(to_accounting_format)

df['sales'] = pd.to_numeric(df['sales'],errors='coerce')

# print(df['sales'].dtypes)  # float

## reordering the columns
col_order = ['order_id', 'order_date', 'ship_date', 'ship_mode', 'customer_name',
             'segment', 'country', 'state', 'region', 'market',
             'product_id', 'category', 'sub_category', 'product_name',
             'sales', 'quantity', 'discount', 'profit', 'shipping_cost',
             'order_priority', 'year']
df = df[col_order]

# print(df.head(30))


## nulls handling in 9 columns
# null_columns = df[['ship_date','ship_mode','customer_name','state','order_priority','profit','shipping_cost','sales','discount']]

# for col in null_columns:
#     missing_pct = df[col].isnull().mean() * 100
#     print(f"{col}: {missing_pct:.2f}% missing")

## % of missingness in those columns
# ship_date - 9.21%
# ship_mode,order_prirority - 1.5%
# customer_name, profit, state, shipping_cost - 2%
# sales - 6.34%
# discount - 13.9%

## nulls(1.5-2%) handling by changing with the column's mode only on categoriacl columns
df['ship_mode'] = df['ship_mode'].fillna(df['ship_mode'].mode()[0])
# print(df['ship_mode'].isnull().mean() * 100)

# print(df['customer_name'].value_counts(dropna=False).sort_values(ascending= False))

# df['customer_name'] = df['customer_name'].fillna('Unknown')
# print(df[df['customer_name'] == 'Unknown'])

# print(df['customer_name'].isnull().mean() * 100)

df['state'] = df['state'].fillna(df['state'].mode()[0])
# print(df['state'].isnull().mean() * 100)

df['order_priority'] = df['order_priority'].fillna(df['order_priority'].mode()[0])
# print(df['order_priority'].isnull().mean() * 100)

def scan_missingness_patterns(df, numeric_cols, categorical_cols, threshold=5):
    """
    For every (numeric column, categorical column) pair, check whether 
    missingness rate varies meaningfully across the categorical column's groups.
    Only returns pairs where the spread exceeds `threshold` percentage points.
    """
    results = []
    for num_col in numeric_cols:
        for cat_col in categorical_cols:
            pattern = df.groupby(cat_col)[num_col].apply(lambda x: x.isnull().mean() * 100)
            spread = pattern.max() - pattern.min()
            if spread > threshold:
                results.append({
                    'numeric_col': num_col,
                    'grouped_by': cat_col,
                    'spread_pct_points': round(spread, 2),
                    'min_missing_pct': round(pattern.min(), 2),
                    'max_missing_pct': round(pattern.max(), 2)
                })
    return pd.DataFrame(results).sort_values('spread_pct_points', ascending=False)

numeric_cols = ['sales','discount']
categorical_cols = ['segment', 'category', 'sub_category', 'region', 'market', 'ship_mode', 'order_priority']

pattern_report = scan_missingness_patterns(df, numeric_cols, categorical_cols, threshold=5)
# print(pattern_report)

# combo_pattern = df.groupby(['order_priority'])['discount'].apply(lambda x: x.isnull().mean() * 100)
# print(combo_pattern.sort_values(ascending=False))

# Since sales missingness is strongly tied to sub_category, fill per sub_category
df['sales'] = df.groupby('sub_category')['sales'].transform(lambda x: x.fillna(x.median()))

# For flagged pairs (from the report above), fill per group
df['discount'] = df.groupby('segment')['discount'].transform(lambda x: x.fillna(x.median()))

# print(df.groupby('segment')['discount'].median())   # check medians are sensibly different across segments
# print(df['discount'].isnull().sum())                  # should now be 0
# print(df['sales'].isna().sum())

df['shipping_cost'] = df['shipping_cost'].fillna(df['shipping_cost'].median())

# df.to_csv("E:\Projects\Portfolio_Projects\Python\Superstore sales analytics\Superstore_cleaned_dt.csv",
#         index=False)

