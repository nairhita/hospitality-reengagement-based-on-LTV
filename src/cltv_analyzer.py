import pandas as pd
from datetime import datetime

class HospitalityCLTVAnalyzer:
    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)
        self.df['stay_date'] = pd.to_datetime(self.df['stay_date'])
        self.analysis_date = datetime(2026, 5, 28)

    def compute_rfm_cltv(self) -> pd.DataFrame:
        """Calculates Recency, Frequency, Monetary metrics, and assigns a CLTV Score."""
        # Aggregate transactional data per guest
        guest_profiles = self.df.groupby('guest_id').agg(
            last_stay_date=('stay_date', 'max'),
            frequency=('stay_date', 'count'),
            total_monetary=('total_spend', 'sum'),
            fav_amenity=('fav_amenity', 'first')
        ).reset_index()

        # Compute Recency (days since last stay)
        guest_profiles['recency_days'] = (self.analysis_date - guest_profiles['last_stay_date']).dt.days

        # Establish Simple Historic CLTV Formula:
        # CLTV = Average Order Value * Frequency
        guest_profiles['avg_order_value'] = guest_profiles['total_monetary'] / guest_profiles['frequency']
        
        # Project future value factor using a 3-year multiplier bounded by retention weights
        guest_profiles['cltv_score'] = round(guest_profiles['total_monetary'] * 1.5, 2)
        return guest_profiles

    def identify_at_risk_high_value_guests(self, cltv_df: pd.DataFrame, 
                                            top_percentile: float = 0.20, 
                                            recency_threshold_days: int = 180) -> pd.DataFrame:
        """Filters guests who are in the top 20% of lifetime value but haven't booked in 6+ months."""
        cltv_threshold = cltv_df['cltv_score'].quantile(1 - top_percentile)
        
        at_risk_high_value = cltv_df[
            (cltv_df['cltv_score'] >= cltv_threshold) & 
            (cltv_df['recency_days'] >= recency_threshold_days)
        ].copy()
        
        return at_risk_high_value.sort_values(by='cltv_score', ascending=False)
