import pandas as pd
import numpy as np
import random as rd
import datetime as dt
from faker import Faker

# Set seeds for reproducibility
np.random.seed(42)
rd.seed(42)

print("Starting data generation...")

# Structure definition
structure = {
    'subcategories': ['smartphones', 'laptops', 'tablets', 'accessories', 'smartwatches', 'cameras'],
    'brands': ['Apple', 'Samsung', 'Sony', 'Dell', 'HP', 'Lenovo', 'Microsoft', 'Google'],
    'regions': ['North', 'South', 'East', 'West']
}

# Generate products
all_products = []
product_id = 1

for subcategory in structure['subcategories']:
    for _ in range(15): 
        brand = rd.choice(structure['brands'])
        product_name = f"{brand} {subcategory.capitalize()} {rd.choice(['Pro', 'Plus', 'Max', 'Mini', 'SE'])}"
        base_price = round(rd.uniform(200, 1200), 2)

        product = {
            'product_id': f'P{product_id:04d}',
            'product_name': product_name,
            'subcategory': subcategory,
            'brand': brand,
            'base_price': base_price,
            'cost_price': round(base_price * 0.6, 2), 
            'popularity_factor': rd.randint(1, 10),  
            'seasonal_factor': 1.2,
            'stock_level': rd.randint(15, 80)   
        }

        all_products.append(product)
        product_id += 1

print(f"Generated {len(all_products)} products")

# Customer segments
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
        'income_range': (40000, 80000),
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

# Cities distribution
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

# Generate customers
faker = Faker()
customers = []
customer_id = 1

for i in range(1000):  
    segment = rd.choices(['Premium', 'Regular', 'Budget'], weights=[0.15, 0.6, 0.25])[0]

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
    else:  # Budget
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
        'city': rd.choices(list(cities_distribution.keys()), 
                          weights=[v['weight'] for v in cities_distribution.values()])[0]
    }
    customers.append(customer)
    customer_id += 1

print(f"Generated {len(customers)} customers")

# Generate date range
start_date = dt.datetime(2023, 7, 1)
end_date = dt.datetime(2024, 7, 31)

def generate_dates(start_date, end_date):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += dt.timedelta(days=1)
    return date_list

daily_dates = generate_dates(start_date, end_date)

# Date information function
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

    # Seasonal factors
    month = date_obj.month
    if month in [11, 12]:  # Holiday season
        seasonal_factor = 1.5
    elif month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.2
    elif month in [1, 2, 3]:  # Post-holiday
        seasonal_factor = 0.8
    else:
        seasonal_factor = 1.0

    weekday_multiplier = 1.3 if date_obj.weekday() >= 4 else 1.0
    date_info.update({
        'seasonal_multiplier': seasonal_factor,
        'weekday_multiplier': weekday_multiplier
    })
    return date_info

date_data = [data_information(date) for date in daily_dates]
print(f"Generated {len(date_data)} days of data")

# Sales generation functions
def daily_transactions(date_info, customers, products, base_volume=100):
    daily_volume = base_volume
    daily_volume *= date_info['seasonal_multiplier']
    daily_volume *= date_info['weekday_multiplier']
    
    rand_factor = np.random.uniform(0.8, 1.2)
    daily_volume *= rand_factor
    
    if date_info['month'] in [11, 12]:
        if date_info['is_weekend'] and date_info['day'] in [24, 25, 31]:
            daily_volume *= 3
        elif date_info['is_weekend']:
            daily_volume *= 1.8
    elif date_info['month'] in [6, 7, 8]:
        if date_info['is_weekend']:
            daily_volume *= 1.6
    elif date_info['month'] in [1, 2, 3]:
        daily_volume *= np.random.uniform(0.5, 1.1)
    
    return max(50, int(daily_volume))

def select_product_for_customer(products, customer, date_info):
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
    
    customer_prefs = segment_preferences[customer['segment']]
    preferred_categories = customer_prefs['preferred_categories']
    
    selected_category = rd.choice(preferred_categories)
    category_products = [p for p in products if p['subcategory'] == selected_category]
    
    if not category_products:
        category_products = products
    
    return rd.choice(category_products)

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
        qty += 1
    
    return max(1, qty)

def call_unit_price(product, customer, date_info): 
    unit_price = product['base_price']

    if date_info['month'] in [11, 12]: 
        if date_info['day'] in range(21, 27) and date_info['month'] == 11: 
            unit_price *= 0.7  # Black Friday
        elif date_info['day'] in range(21, 31) and date_info['month'] == 12:
            unit_price *= 0.8  # Christmas
        else: 
            unit_price *= 0.9
    elif date_info['month'] in [6, 7, 8]:
        unit_price *= 0.95

    if customer['segment'] == 'Premium': 
        unit_price *= 0.98
    elif customer['segment'] == 'Budget':
        unit_price *= 0.92

    daily_variation = np.random.uniform(0.95, 1.05)
    unit_price *= daily_variation
    
    return round(unit_price, 2)

def customer_selection_with_history(customers, date_info, cx_history):
    weights = []
    
    for customer in customers:
        if customer['segment'] == 'Premium': 
            weight = 3.0
        elif customer['segment'] == 'Regular': 
            weight = 2.0
        else: 
            weight = 1.0
        
        order_count = cx_history[customer['customer_id']]['order_count']
        if order_count > 0: 
            multiplier = min(order_count * 0.5 + 1, 5.0)
            weight *= multiplier
        
        if date_info['month'] in [11, 12]:  
            weight *= 1.5
        elif date_info['month'] in [6, 7, 8]: 
            weight *= 1.2
        weights.append(weight)

    return rd.choices(customers, weights=weights)[0]

def update_cx_history(cx_history, customer_id, total_sales, date_info):
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
    power_customers = rd.sample(customers, num_power_customers)
    
    for customer in power_customers:
        customer_id = customer['customer_id']
        fake_orders = rd.randint(2, 15)
        fake_spending = rd.randint(500, 5000)
        
        cx_history[customer_id]['order_count'] = fake_orders
        cx_history[customer_id]['total_spent'] = fake_spending
        
        if fake_orders >= 10:
            cx_history[customer_id]['loyalty'] = 'Gold'
        elif fake_orders >= 5:
            cx_history[customer_id]['loyalty'] = 'Silver'
        else:
            cx_history[customer_id]['loyalty'] = 'Bronze'

# Generate sales data
def generate_sales_data(customers, products, date_data): 
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

    for i, date_info in enumerate(date_data): 
        daily_volume = daily_transactions(date_info, customers, products)
        
        for _ in range(daily_volume):
            customer = customer_selection_with_history(customers, date_info, cx_history)
            product = select_product_for_customer(products, customer, date_info)
            quantity = determine_qty(product, customer, date_info) 
            unit_price = call_unit_price(product, customer, date_info)
            total_sales = round(quantity * unit_price, 2)

            current_loyalty = cx_history[customer['customer_id']]['loyalty']
            update_cx_history(cx_history, customer['customer_id'], total_sales, date_info)

            transaction = {
                'transaction_id': f'T{transaction_id:06d}', 
                'date': date_info['date'].strftime('%Y-%m-%d'),
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
    
    return pd.DataFrame(sales_transactions)

# Generate the data
print("Generating sales transactions...")
df_sales = generate_sales_data(customers, all_products, date_data)

print(f"Generated {len(df_sales)} total transactions")
print(f"Date range: {df_sales['date'].min()} to {df_sales['date'].max()}")
print(f"Total revenue: ${df_sales['total_sales'].sum():,.2f}")

# Display sample data
print("\nSample transactions:")
print(df_sales.head(10))

# Monthly summary
print("\nMonthly revenue summary:")
df_sales['date'] = pd.to_datetime(df_sales['date'])
monthly_revenue = df_sales.groupby(df_sales['date'].dt.to_period('M'))['total_sales'].sum()
for month, revenue in monthly_revenue.items():
    print(f"{month}: ${revenue:,.2f}")

print("\nData generation complete! You now have 13 months of data for trend analysis.")


# Save sales transactions to CSV
print("Saving data to CSV files...")

# Save main sales data
df_sales.to_csv('sales_transactions.csv', index=False)
print(f"Saved {len(df_sales)} transactions to 'sales_transactions.csv'")

# Create and save products DataFrame
df_products = pd.DataFrame(all_products)
df_products.to_csv('products.csv', index=False)
print(f"Saved {len(df_products)} products to 'products.csv'")

# Create and save customers DataFrame
df_customers = pd.DataFrame(customers)
df_customers.to_csv('customers.csv', index=False)
print(f"Saved {len(df_customers)} customers to 'customers.csv'")

# Optional: Create a summary report
summary_data = {
    'metric': [
        'Total Transactions',
        'Total Revenue',
        'Average Order Value',
        'Unique Products',
        'Unique Customers',
        'Date Range Start',
        'Date Range End'
    ],
    'value': [
        len(df_sales),
        f"${df_sales['total_sales'].sum():,.2f}",
        f"${df_sales['total_sales'].mean():.2f}",
        df_sales['product_id'].nunique(),
        df_sales['customer_id'].nunique(),
        df_sales['date'].min(),
        df_sales['date'].max()
    ]
}

df_summary = pd.DataFrame(summary_data)
df_summary.to_csv('data_summary.csv', index=False)
print("Saved summary report to 'data_summary.csv'")

print("\nAll CSV files have been created successfully!")
print("Files created:")
print("- sales_transactions.csv (main transaction data)")
print("- products.csv (product catalog)")
print("- customers.csv (customer information)")
print("- data_summary.csv (summary statistics)")