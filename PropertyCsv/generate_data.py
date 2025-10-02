import pandas as pd
import numpy as np
from datetime import datetime
import os

def generate_property_data(n_rows=20000):
    # Define cities and their localities
    cities = {
        "Mumbai": ["Andheri", "Bandra", "Juhu", "Powai", "Worli"],
        "Delhi": ["Dwarka", "Rohini", "Vasant Kunj", "South Extension", "Pitampura"],
        "Bangalore": ["Whitefield", "Koramangala", "Indiranagar", "JP Nagar", "HSR Layout"]
    }
    
    # Generate base data
    data = []
    for _ in range(n_rows):
        city = np.random.choice(list(cities.keys()))
        locality = np.random.choice(cities[city])
        bhk = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.3, 0.4, 0.15, 0.05])
        area = int(np.random.normal(bhk * 500, 100))  # Area increases with BHK
        price_per_sqft = int(np.random.normal(12000, 2000))
        price = int((area * price_per_sqft) / 100000)  # Convert to Lakhs
        
        row = {
            'city': city,
            'locality': locality,
            'property_type': np.random.choice(['Apartment', 'Villa', 'Builder Floor'], p=[0.7, 0.1, 0.2]),
            'bedrooms': f'{bhk} BHK',
            'area_sqft': area,
            'price_per_sqft': price_per_sqft,
            'price_lakhs': price,
            'floor': f'{np.random.randint(1, 20)} out of {np.random.randint(20, 25)}',
            'age_years': np.random.randint(0, 20),
            'facing': np.random.choice(['North', 'South', 'East', 'West', 'North East', 'North West', 'South East', 'South West']),
            'parking': np.random.choice(['Yes', 'No'], p=[0.8, 0.2]),
            'furnishing': np.random.choice(['Unfurnished', 'Semi-Furnished', 'Fully Furnished']),
            'availability': np.random.choice(['Ready to Move', 'Under Construction']),
            'maintenance_monthly': int(np.random.normal(5000, 1000)),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        data.append(row)
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Create directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Generate the data
    print("Generating property data...")
    df = generate_property_data(20000)
    
    # Save to CSV
    output_file = f"data/property_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(output_file, index=False)
    
    print(f"\nData saved to {output_file}")
    print(f"Dataset shape: {df.shape}")
    print("\nColumn names:")
    print(list(df.columns))