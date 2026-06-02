import os
import pandas as pd
from data_generator import generate_hospitality_data
from cltv_analyzer import HospitalityCLTVAnalyzer
from llm_copywriter import LLMCopywriter

def main():
    data_file = "../data/hotel_transactions.csv"
    
    # Step 1: Ensure dataset exists
    if not os.path.exists(data_file):
        print("Data files missing. Executing simulation script...")
        generate_hospitality_data(data_file, n_guests=1000)

    # Step 2: Extract RFM and CLTV metrics
    print("\n--- Executing CLTV Analysis Engine ---")
    analyzer = HospitalityCLTVAnalyzer(data_file)
    cltv_metrics = analyzer.compute_rfm_cltv()
    
    # Step 3: Isolate high-value churn targets
    at_risk_vips = analyzer.identify_at_risk_high_value_guests(cltv_metrics)
    print(f"Identified {len(at_risk_vips)} high-value guests at risk of churn (No stay in 180+ days).")
    
    # Step 4: Run targeted LLM re-engagement campaigns for top candidates
    print("\n--- Launching Automated LLM Personalization Campaign ---")
    copywriter = LLMCopywriter()
    
    # Take the top 3 highest-value at-risk profiles to showcase in output
    campaign_targets = at_risk_vips.head(3)
    
    for _, guest in campaign_targets.iterrows():
        print(f"\nGenerating campaign creative for: {guest['guest_id']}")
        print(f"| Projected CLTV: ${guest['cltv_score']:,.2f} | Days Since Last Stay: {guest['recency_days']}")
        
        email_content = copywriter.generate_reengagement_email(
            guest_id=guest['guest_id'],
            cltv=guest['cltv_score'],
            last_amenity=guest['fav_amenity']
        )
        print("-" * 50)
        print(email_content)
        print("-" * 50)

if __name__ == "__main__":
    main()
