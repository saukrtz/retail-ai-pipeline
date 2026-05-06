import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data(num_rows=10000):
    categories = ['Electronics', 'Fashion', 'Home', 'Beauty', 'Sports']
    products = {
        'Electronics': ['Laptop', 'Phone', 'Tablet', 'Headphones'],
        'Fashion': ['T-Shirt', 'Jeans', 'Shoes', 'Jacket'],
        'Home': ['Lamp', 'Chair', 'Table', 'Rug'],
        'Beauty': ['Lipstick', 'Cream', 'Perfume', 'Soap'],
        'Sports': ['Ball', 'Racket', 'Mat', 'Weights']
    }
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    for i in range(num_rows):
        cat = np.random.choice(categories)
        prod = np.random.choice(products[cat])
        price = np.random.uniform(10, 1000)
        quantity = np.random.randint(1, 10)
        discount = np.random.uniform(0, price * 0.2) # Max 20% discount
        date = start_date + timedelta(days=np.random.randint(0, 90))
        
        data.append({
            'order_id': i + 1,
            'customer_id': np.random.randint(100, 1000),
            'product': prod,
            'category': cat,
            'price': round(price, 2),
            'quantity': quantity,
            'order_date': date.strftime('%Y-%m-%d'),
            'discount': round(discount, 2)
        })
    
    df = pd.DataFrame(data)
    df.to_csv('orders.csv', index=False)
    print(f"Generated {num_rows} rows in orders.csv")

if __name__ == "__main__":
    generate_data()
