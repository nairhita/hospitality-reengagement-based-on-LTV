
# AI-Driven Hospitality Retention (reengagement) using CLTV 

An enterprise-grade customer lifecycle retention pipeline designed for the hospitality sector. This project combines statistical lifetime value modeling (RFM analytics) with Generative AI orchestration to rescue high-value churn risks natively using historical behavior data.

## The Business Case
Acquiring a new hotel guest costs 5x more than retaining an existing one. This pipeline identifies the top 20% highest-value guests who have gone cold (no bookings in 6+ months) and automatically manufactures hyper-personalized outreach campaigns mapping to their historical stay preferences (e.g., Spa, Fine Dining).

## Pipeline Architecture
1. **`data_generator.py`**: Builds a raw transaction ledger modeling accommodation revenue and ancillary stay metrics.
2. **`cltv_analyzer.py`**: Extracts transaction recency, stay frequency, and monetary baselines to calculate a 3-year projected **Customer Lifetime Value (CLTV)** metric.
3. **`llm_copywriter.py`**: Interfaces with an LLM framework to design bespoke CRM emails highlighting their verified amenity preferences.
4. **`orchestration.py`**: Connects and runs the end-to-end data processing and automation loop.

## Setup & Execution
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Execute the workflow pipeline: `cd src && python orchestration.py`
