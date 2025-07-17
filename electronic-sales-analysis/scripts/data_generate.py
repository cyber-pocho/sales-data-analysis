#columns needed: 
# - date 
# - product_id
# - product_name
# - category
# - quantity 
# - unit_price
# - total_sales
# - customer_id
# - region

#data range= '2023-07-01 to 2024-07-31'
#electronics
# Spikes on weekends and holidays as well as random sale events
# black friday as well as chrsitmas

import pandas as pd
import numpy as np
import random as rd
import datetime as dt
import time 
from faker import Faker


""""
Here we define the structure of the dataset we want to generate 
as closely as possible to the market of electronics, and based 
on websites we've reviewed."""
structure = {
    'subcategories' : ['smartphones', 'laptops', 'tablets', 'accessories', 'smartwatches', 'cameras'],
    'brands': ['Apple', 'Samsung', 'Sony', 'Dell', 'HP', 'Lenovo', 'Microsoft', 'Google'],
    'regions': ['North', 'South', 'East', 'West'],
    'rg_prices' : {
        'smartphones': (300, 1200),
        'laptops': (500, 2500),
        'tablets': (200, 800),
        'accessories': (10, 200),
        'smartwatches': (100, 500),
        'cameras': (150, 1500)
    }
}
"""
Here we have generated a function that will create a product name
that will match the brand and subcategory.
"""
def name_generator(brand, subcategory):
    models = {
        'Smartphones': ['Pro', 'Plus', 'Max', 'Mini'],
        'Laptops': ['Pro', 'Air', 'Gaming', 'Business', 'Ultra'],
        'Tablets': ['Pro', 'Air', 'Mini', 'Plus'],
    }

"""
Here we define the structure of the dataset we want to generate. 
"""
columns = [
    'product_id',
    'product_name',
    'category',
    'subcategory',
    'brand',
    'base_price',
    'cost_price',
    'seasonal_factor',
    'popularity_factor',
    'stock_level'
]

"""
Creating products based on the structure defined above.
"""

all_products = []
product_id = 1

for subcategory in structure['subcategories']:
    for _ in range(15): 
        brand = rd.choice(structure['brands']) #we're picking a random brand
        #attribbutes
        product_name = f"{brand} {subcategory.capitalize()} {rd.choice(['Pro', 'Plus', 'Max', 'Mini', 'SE'])}"
        base_price = round(rd.uniform(200, 1200), 2)  # Random price between 200 and 1200

        #recording the product
        product = {
            'product_id': f'P{product_id:04d}',
            'product_name': product_name,
            'subcategory': subcategory,
            'brand': brand,
            'base_price': base_price,
            'cost_price': round(base_price * 0.6, 2), 
            'popularity_factor': rd.randint(1, 10),  
            'seasonal factor': 1.2,
            'stock_level': rd.randint(15, 80)   
        }

        all_products.append(product)
        product_id += 1

""""Converting the product list to a DataFrame."""

df_product = pd.DataFrame(all_products)
print(f"Generated {len(df_product)} products")

"""SECTION: CUSTOMER DATA GENERATION"""

customer_atributes = {
    'basic_info': ['customer_id', 'first_name', 'last_name', 'email', 'phone'],
    'demographics': ['age', 'gender', 'income_bracket'],
    'location': ['city', 'state', 'country', 'zipcode'], 
    'behavior': ['customer_segment', 'acquisition_date', 'total_orders', 'lifetime_value'],
    'preferences': ['preferred_category', 'average_order_value', 'loyalty_tier']
}

customer_segments = {
    'Premium': {
        "percentage": 0.15, 
        'income_range': (80000, 150000),
        'avg_order_value': (500, 1000),
        'order_frequency': 'high', 
        'preferred_categories': ['smartphones', 'laptops', 'cameras']
    },
    'Regular': {
        'percentage': 0.6,
        'income': (40000, 80000),
        'avg_order_value': (200, 500),
        'order_frequency': 'medium',
        'preferred_categories': ['tablets', 'accessories', 'smartwatches']
    },
    'Budget': {
        'percentage': 0.25,
        'income_range': (20000, 40000),
        'avg_order_value': (50, 200),
        'order_frequency': 'low',
        'preferred_categories': ['accessories', 'smartwatches']
    }
}
"""Settting up Geographcical distribution of customers"""

cities_distribution = {
    'New York': {'weight': 20, 'state': 'NY'},
    'Los Angeles': {'weight': 15, 'state': 'CA'},
    'Chicago': {'weight': 12, 'state': 'IL'},
    'Houston': {'weight': 10, 'state': 'TX'},
    'Phoenix': {'weight': 8, 'state': 'AZ'},
    'Philadelphia': {'weight': 7, 'state': 'PA'},
    'San Antonio': {'weight': 6, 'state': 'TX'},
    'San Diego': {'weight': 5, 'state': 'CA'},
    'Dallas': {'weight': 5, 'state': 'TX'},
    'Other': {'weight': 12, 'state': 'Various'}
}

"""Generating customer data"""

faker = Faker()
customers = []
customer_id = 1
age = 1
income = 1
total_orders = 1

for i in range(1000):  
    segment = rd.choices(['Premium', 'Regular', 'Budget'])[0]  

    first_name = faker.first_name()
    last_name = faker.last_name()
    email = f'{first_name.lower()}.{last_name.lower()}@{faker.free_email_domain()}'

    if segment == 'Premium': 
        age = rd.randint(30, 55)
        income = rd.randint(80000, 150000)
        total_orders = rd.randint(10, 50)

    elif segment == 'Regular': 
        age = rd.randint(25, 45)
        income = rd.randint(40000, 80000)
        total_orders = rd.randint(5, 30)

    elif segment == 'Budget':
        age = rd.randint(18, 35)
        income = rd.randint(20000, 40000)
        total_orders = rd.randint(1, 10)

    customer = {
        'customer_id': f'C{customer_id:04d}', 
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'segment': segment,
        'age': age,
        'income': income,
        'total_orders': total_orders,
        'city': rd.choices(list(cities_distribution.keys()), weights=[v['weight'] for v in cities_distribution.values()])[0]
    }
    customers.append(customer)
    customer_id += 1



""""Date generation"""

start_date = dt.datetime(2023, 7, 1)
end_date = dt.datetime(2024, 7, 31)

def generate_dates(start_date, end_date, n):
    date_list = []
    current_date = start_date

    while current_date <= end_date:
        date_list.append(current_date)
        current_date += dt.timedelta(days=1)
    return date_list
    
daily_dates = generate_dates(start_date, end_date, n=365)

"""Date information for sales analysis"""
def data_information(date_obj):

    date_info = {
        'date': date_obj,
        'year': date_obj.year, 
        'month': date_obj.month, 
        'day': date_obj.day,
        'weekday': date_obj.weekday(), 
        'weekday_name': date_obj.strftime('%A'),
        'month_name': date_obj.strftime('%B'), 
        'quarter': (date_obj.month - 1) // 3 + 1,
        'is_weekend': date_obj.weekday() >= 5,
        'week_of_year': date_obj.isocalendar()[1]
    }

    # Seasonal factors based on month // holiday season
    month = date_obj.month

    if month in [11, 12]:  
        seasonal_factor = 1.5
    elif month in [6, 7, 8]:
        seasonal_factor = 1.2
    elif month in [1, 2, 3]:
        seasonal_factor = 0.8
    else:
        seasonal_factor = 1.0 #standard base value

    weekday_multiplier = 1.3 if date_obj.weekday() >= 4 else 1.0
    date_info.update({
        'seasonal_multiplier': seasonal_factor,
        'weekday_multiplier': weekday_multiplier
    })
    return date_info


date_data = [data_information(date) for date in daily_dates]
df_dates = pd.DataFrame(date_data)
# Converting the product list to a DataFrame

"""SECTION: SALES DATA GENERATION"""

def daily_transactions(date_info, customers, products, base_volume=100):
    daily_volume = base_volume
    daily_volume *= date_info['seasonal_multiplier']
    daily_volume *= date_info['weekday_multiplier']
    
    # randomness
    rand_factor = np.random.uniform(0.8, 1.2)
    daily_volume *= rand_factor
    
    if date_info['month'] in [11, 12]:
        if date_info['is_weekend'] and date_info['day'] in [24, 25, 31]:
            daily_volume *= 3
        elif date_info['is_weekend']:
            daily_volume *= 1.8
        elif date_info['weekday'] in [1,2,3,4]:
            daily_volume *= 1.4
    elif date_info['month'] in [6, 7, 8]:
        if date_info['is_weekend']:
            daily_volume *= 1.6
        elif date_info['weekday'] in [1,2,3,4]:
            daily_volume *= 1.3
    elif date_info['month'] in [1, 2, 3]:
        daily_volume *= np.random.uniform(0.5, 1.1)
    rand_factor_volume = np.random.uniform(0.7, 1.5)
    daily_volume *= rand_factor_volume 
    return max(50, int(daily_volume))

def customer_selection(customers, date_info):
    weights = {
        'Premium': 0.5,
        'Regular': 0.3,
        'Budget': 0.2,
    }
    weights = [weights[customer['segment']] for customer in customers]
    selected_customer = rd.choices(customers, weights=weights)[0]
    return selected_customer

def determine_qty(product, customer, date_info):
    base_qty = {
        'smartphones': [1, 1, 1, 2],
        'laptops': [1, 1, 1, 1],
        'tablets': [1, 1, 2],
        'accessories': [1, 2, 3, 4, 5],
        'smartwatches': [1, 1, 2],
        'cameras': [1, 1, 1, 1]
    }
    possible_qty = base_qty.get(product['subcategory'], [1, 1, 2])
    qty = rd.choice(possible_qty)
    
    if customer['segment'] == 'Premium' and rd.random() < 0.3:
        qty += int(np.random.uniform(1, 3))
    
    return max(1, qty)

def call_unit_price(product, customer, date_info): 
    unit_price = product['base_price']

    if date_info['month'] in [11, 12]: 
        if date_info['day'] in  range(21,27) and date_info['month']== 11: 
            unit_price *= 0.7 #30% dct
        elif date_info['day'] in range(21, 31) and date_info['month'] == 12:
            unit_price *= 0.8 #20% dct
        else: 
            unit_price *= 0.9
    elif date_info['month'] in [6, 7, 8]: #summer sales
        unit_price *= 0.95
    #customer loyalty pricing
    if customer['segment'] == 'Premium': 
        unit_price *= 0.98 #5% dct for premium customers
    elif customer['segment'] == 'Budget':
        unit_price *= 0.92 # better deals for budget customers
    stock_level = product['stock_level']
    if stock_level < 50: 
        unit_price *= 1.1
    elif stock_level > 70: 
        unit_price *= 0.95

    daily_variation = np.random.uniform(0.95, 1.05)
    unit_price *= daily_variation
    

    return round(unit_price, 2)


## Product selection: 

def select_product_for_customer(products, customer, date_info):
    # Use the customer segments you already defined
    segment_preferences = {
        'Premium': {
            'preferred_categories': ['smartphones', 'laptops', 'cameras'],
            'weights': [0.4, 0.35, 0.25]
        },
        'Regular': {
            'preferred_categories': ['tablets', 'accessories', 'smartwatches'],
            'weights': [0.4, 0.35, 0.25]
        },
        'Budget': {
            'preferred_categories': ['accessories', 'smartwatches'],
            'weights': [0.6, 0.4]
        }
    }
    
    # Get customer's preferred categories
    customer_prefs = segment_preferences[customer['segment']]
    preferred_categories = customer_prefs['preferred_categories']
    category_weights = customer_prefs['weights']
    
    # Apply seasonal adjustments to preferences
    if date_info['month'] in [6, 7, 8]:  # Summer
        if 'cameras' in preferred_categories:
            # Boost camera preference in summer
            idx = preferred_categories.index('cameras')
            category_weights[idx] *= 1.5
    
    if date_info['month'] in [11, 12]:  # Holiday season
        if 'smartphones' in preferred_categories:
            # Boost smartphone preference during holidays
            idx = preferred_categories.index('smartphones')
            category_weights[idx] *= 1.3
    
    # Normalize weights
    total_weight = sum(category_weights)
    category_weights = [w/total_weight for w in category_weights]
    
    # Select category based on preferences
    selected_category = rd.choices(preferred_categories, weights=category_weights)[0]
    
    # Filter products by selected category
    category_products = [p for p in products if p['subcategory'] == selected_category]
    
    # If no products in preferred category, fall back to all products
    if not category_products:
        category_products = products
    
    # For premium customers, prefer higher-priced items within category
    if customer['segment'] == 'Premium':
        # Sort by price and give higher weight to expensive items
        category_products.sort(key=lambda x: x['base_price'], reverse=True)
        weights = [1.5 if i < len(category_products)//2 else 1.0 for i in range(len(category_products))]
    elif customer['segment'] == 'Budget':
        # Sort by price and give higher weight to cheaper items
        category_products.sort(key=lambda x: x['base_price'])
        weights = [1.5 if i < len(category_products)//2 else 1.0 for i in range(len(category_products))]
    else:
        # Regular customers - equal weights
        weights = [1.0] * len(category_products)
    
    # Select final product
    selected_product = rd.choices(category_products, weights=weights)[0]
    
    return selected_product

def customer_selection_with_history(customers, date_info, cx_history):
    weights = []
    
    for customer in customers:
        weight = 1.0
        # If customer bought before, make them 2x more likely to buy again
        if customer['segment'] == 'Premium': 
            weight = 3.0
        elif customer['segment'] == 'Regular': 
            weight = 2.0
        else: 
            weight = 1.0
        
        order_count  = cx_history[customer['customer_id']]['order_count']
        if order_count > 0: 
            multiplier  = min(order_count*0.5 + 1, 5.0)
            weight *= multiplier
        
        if date_info['month'] in [11,12]:  
            weight *= 1.5
        elif date_info['month'] in [6, 7, 8]: 
            weight *= 1.2
        weights.append(weight)

    return rd.choices(customers, weights=weights)[0]

def loyalty_discount(unit_price, customer_id, cx_history): #dct code for loyalty from us to the cx
    order_count=cx_history[customer_id]['order_count']
    dct = min(order_count // 5 *0.01, 0.10)
    return unit_price * (1-dct)

def update_cx_history(cx_history, customer_id, total_sales, date_info): #creating tiers based on History
    history = cx_history[customer_id]
    history['order_count'] += 1
    history['total_spent'] += total_sales
    history['last_purchase'] = date_info['date']

    if history['order_count'] >= 10: 
        history['loyalty'] = 'Gold'
    elif history['order_count'] >= 5: 
        history['loyalty'] = 'Silver'
    elif history['order_count'] >= 1: 
        history['loyalty'] = 'Bronze'
    else: 
        history['loyalty'] = 'New'


def create_power_customers(customers, cx_history, num_power_customers=50):
    """Give some customers a head start to ensure we have higher-tier customers"""
    power_customers = rd.sample(customers, num_power_customers)
    
    for customer in power_customers:
        customer_id = customer['customer_id']
        # Give them 2-15 previous "purchases" 
        fake_orders = rd.randint(2, 15)
        fake_spending = rd.randint(500, 5000)
        
        cx_history[customer_id]['order_count'] = fake_orders
        cx_history[customer_id]['total_spent'] = fake_spending
        
        # Update their loyalty tier based on fake history
        if fake_orders >= 10:
            cx_history[customer_id]['loyalty'] = 'Gold'
        elif fake_orders >= 5:
            cx_history[customer_id]['loyalty'] = 'Silver'
        else:
            cx_history[customer_id]['loyalty'] = 'Bronze' 


## Generating the sales data and getting a CSV doc
def generate_sales_data (customers, products, data_data): 
    sales_transactions = []
    transaction_id = 1

    cx_history = {}

    for customer in customers: 
        cx_history[customer['customer_id']] = {
            'order_count': 0,
            'total_spent': 0,
            'last_purchase': None,
            'loyalty': 'New'
        }
    create_power_customers(customers, cx_history, 100)

    for date_info in date_data: 
        daily_volume = daily_transactions(date_info, customers, products)
        for _ in range(daily_volume):
            customer = customer_selection_with_history(customers, date_info, cx_history)
            product = select_product_for_customer(products, customer, date_info)
            quantity = determine_qty(product, customer, date_info) 
            unit_price = call_unit_price(product, customer, date_info)
            total_sales = round(quantity *unit_price)

            current_loyalty = cx_history[customer['customer_id']]['loyalty']

            update_cx_history(cx_history, customer['customer_id'], total_sales, date_info)


            transaction ={
                'transaction_id' : f'T{transaction_id:06d}', 
                'date' : date_info['date'].strftime('%Y-%m-%d'),
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'quantity': quantity,
                'unit_price': unit_price, 
                'total_sales': total_sales, 
                'customer_id': customer['customer_id'], 
                'city': customer['city'],
                'loyalty_tier': current_loyalty 

            }         
            sales_transactions.append(transaction)
            transaction_id += 1

        if i % 30 == 0:
            print(f"Processed {i+1}/{len(date_data)} days, {len(sales_transactions)} transactions so far")
        df_sales = pd.DataFrame(sales_transactions)
        print(f"Generated {len(df_sales)} total transactions")    
        return df_sales
    

df_sales = generate_sales_data(customers, all_products, date_data)
df_sales.to_csv('sales_data.csv', index=False)
print('sales data exported')

df_products = pd.DataFrame(all_products)
df_product.to_csv('customers.csv', index=False)

print("All data exported successfully.")

def generate_summary_stats(df_sales):
    print("=== SALES DATA SUMMARY ===")
    print(f"Total Records: {len(df_sales):,}")
    print(f"Date Range: {df_sales['date'].min()} to {df_sales['date'].max()}")
    print(f"Total Revenue: ${df_sales['total_sales'].sum():,.2f}")
    print(f"Average Transaction: ${df_sales['total_sales'].mean():.2f}")
    print(f"Unique Customers: {df_sales['customer_id'].nunique()}")
    print(f"Unique Products: {df_sales['product_id'].nunique()}")
    
    print("\n=== MONTHLY BREAKDOWN ===")
    monthly_sales = df_sales.groupby(pd.to_datetime(df_sales['date']).dt.to_period('M'))['total_sales'].sum()
    for month, sales in monthly_sales.items():
        print(f"{month}: ${sales:,.2f}")
    
    print("\n=== TOP 5 PRODUCTS ===")
    top_products = df_sales.groupby('product_name')['total_sales'].sum().sort_values(ascending=False).head()
    for product, sales in top_products.items():
        print(f"{product}: ${sales:,.2f}")

generate_summary_stats(df_sales)



def create_data_dictionary():
    data_dict = {
        'Field Name': [
            'transaction_id', 'date', 'product_id', 'product_name', 
            'quantity', 'unit_price', 'total_sales', 'customer_id', 
            'city', 'loyalty_tier'
        ],
        'Data Type': [
            'String', 'Date', 'String', 'String', 
            'Integer', 'Float', 'Float', 'String', 
            'String', 'String'
        ],
        'Description': [
            'Unique transaction identifier (T000001 format)',
            'Transaction date (YYYY-MM-DD format)',
            'Unique product identifier (P0001 format)',
            'Full product name including brand',
            'Number of units purchased',
            'Price per unit (after discounts)',
            'Total transaction value (quantity × unit_price)',
            'Unique customer identifier (C0001 format)',
            'Customer city location',
            'Customer loyalty tier (New, Bronze, Silver, Gold)'
        ],
        'Example': [
            'T000001', '2023-07-01', 'P0001', 'Apple Smartphones Pro',
            '2', '899.99', '1799.98', 'C0001',
            'New York', 'Gold'
        ]
    }
    
    df_dict = pd.DataFrame(data_dict)
    df_dict.to_csv('data_dictionary.csv', index=False)
    print("Data dictionary saved to 'data_dictionary.csv'")
    return df_dict

# Create and display data dictionary
data_dict = create_data_dictionary()
print(data_dict)


def create_documentation():
    doc_content = f"""
# Sales Data Generation Documentation

## Overview
This dataset contains synthetic sales transaction data for an electronics retailer, 
covering a 13-month period from July 2023 to July 2024.

## Dataset Statistics
- **Total Records**: {len(df_sales):,}
- **Date Range**: {df_sales['date'].min()} to {df_sales['date'].max()}
- **Total Revenue**: ${df_sales['total_sales'].sum():,.2f}
- **Unique Customers**: {df_sales['customer_id'].nunique()}
- **Unique Products**: {df_sales['product_id'].nunique()}

## Data Generation Method
- **Seasonal Patterns**: Higher sales during holidays (Nov-Dec) and summer (Jun-Aug)
- **Customer Segments**: Premium (15%), Regular (60%), Budget (25%)
- **Product Categories**: {', '.join(structure['subcategories'])}
- **Geographic Distribution**: {len(set(customer['city'] for customer in customers))} cities

## Customer Loyalty System
- **New**: First-time customers
- **Bronze**: 1-4 purchases
- **Silver**: 5-9 purchases  
- **Gold**: 10+ purchases
- **Discounts**: 1% per 5 purchases (max 10%)

## Files Generated
1. `sales_data.csv` - Main transaction data
2. `products.csv` - Product catalog
3. `customers.csv` - Customer information
4. `data_dictionary.csv` - Field definitions
5. `README.md` - This documentation

## Usage Notes
- All monetary values in USD
- Dates in YYYY-MM-DD format
- No personally identifiable information (synthetic data)
- Suitable for sales analysis, forecasting, and BI dashboard creation

Generated on: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open('README.md', 'w') as f:
        f.write(doc_content)
    
    print("Documentation saved to 'README.md'")

# Create documentation
create_documentation()



def validate_data(df_sales):
    print("=== DATA VALIDATION REPORT ===")
    
    missing_values = df_sales.isnull().sum()
    print(f"Missing Values:\n{missing_values}")
    
    print(f"\nNegative Quantities: {(df_sales['quantity'] < 0).sum()}")
    print(f"Negative Prices: {(df_sales['unit_price'] < 0).sum()}")
    print(f"Negative Total Sales: {(df_sales['total_sales'] < 0).sum()}")
    
    print(f"\nQuantity Range: {df_sales['quantity'].min()} to {df_sales['quantity'].max()}")
    print(f"Price Range: ${df_sales['unit_price'].min():.2f} to ${df_sales['unit_price'].max():.2f}")
    
    print(f"\nDuplicate Transaction IDs: {df_sales['transaction_id'].duplicated().sum()}")
    
    date_range = pd.to_datetime(df_sales['date'])
    print(f"Date Range Valid: {date_range.min()} to {date_range.max()}")
    
    print("\n=== VALIDATION COMPLETE ===")

# Run validation
validate_data(df_sales)

def export_all_data():
    print("Starting data export...")
    
    df_sales = generate_sales_data(customers, all_products, date_data)
    
    df_sales.to_csv('sales_data.csv', index=False)
    pd.DataFrame(all_products).to_csv('products.csv', index=False)
    pd.DataFrame(customers).to_csv('customers.csv', index=False)
    
    create_data_dictionary()
    create_documentation()
    
    generate_summary_stats(df_sales)
    validate_data(df_sales)
    
    print("\n=== EXPORT COMPLETE ===")
    print("Files created:")
    print("- sales_data.csv")
    print("- products.csv") 
    print("- customers.csv")
    print("- data_dictionary.csv")
    print("- README.md")

# Run complete export
export_all_data()