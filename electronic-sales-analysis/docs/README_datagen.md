
# Sales Data Generation Documentation

## Overview
This dataset contains synthetic sales transaction data for an electronics retailer, 
covering a 13-month period from July 2023 to July 2024.

## Dataset Statistics
- **Total Records**: 213
- **Date Range**: 2023-07-01 to 2023-07-01
- **Total Revenue**: $232,780.00
- **Unique Customers**: 178
- **Unique Products**: 79

## Data Generation Method
- **Seasonal Patterns**: Higher sales during holidays (Nov-Dec) and summer (Jun-Aug)
- **Customer Segments**: Premium (15%), Regular (60%), Budget (25%)
- **Product Categories**: smartphones, laptops, tablets, accessories, smartwatches, cameras
- **Geographic Distribution**: 10 cities

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

Generated on: 2025-07-16 20:47:10
