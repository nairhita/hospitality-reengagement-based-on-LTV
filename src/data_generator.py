import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_hospitality_data(filepath: str, n_guests: int = 1000):
    """Generates synthetic hotel booking and transaction data."""
    np.random.seed(42)
    today = datetime(2026, 5, 28)
    
    data = []
    
    for guest_id in range(1001, 1001 + n_guests):
        # Assign a segment profile to create realistic variance
        profile = np.random.choice(['Luxury', 'Business', 'Budget'], p=[0.15, 0.35, 0.50])
        
        if profile == 'Luxury':
            n_stays = np.random.randint(3, 15)
            avg_room_revenue = np.random.uniform(400, 800)
            avg_ancillary_revenue = np.random.uniform(150, 400) # Spa/Dining
            fav_amenity = 'Luxury Spa & Fine Dining'
        elif profile == 'Business':
            n_stays = np.random.randint(5, 25)
            avg_room_revenue = np.random.uniform(180, 300)
            avg_ancillary_revenue = np.random.uniform(40, 100) # Room service
            fav_amenity = 'Executive Lounge & High-Speed Wi-Fi'
        else:
            n_stays = np.random.randint(1, 4)
            avg_room_revenue = np.random.uniform(90, 150)
            avg_ancillary_revenue = np.random.uniform(10, 30)
            fav_amenity = 'Free Breakfast & Pool'

        # Generate individual stays over the last 2 years
        for _ in range(n_stays):
            days_ago = np.random.randint(5, 730)
            stay_date = today - timedelta(days=days_ago)
            
            room_bill = np.random.normal(avg_room_revenue, avg_room_revenue * 0.1)
            ancillary_bill = np.random.normal(avg_ancillary_revenue, avg_ancillary_revenue * 0.1)
            total_spend = max(50, room_bill + ancillary_bill)
            
            data.append({
                'guest_id': f"GUEST_{guest_id}",
                'stay_date': stay_date.strftime('%Y-%m-%d'),
                'total_spend': round(total_spend, 2),
                'fav_amenity': fav_amenity
            })

    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Hospitality data successfully initialized at: {filepath}")

if __name__ == "__main__":
    generate_hospitality_data("../data/hotel_transactions.csv")
