import pandas as pd
from datetime import datetime, timedelta
import random

# Helper functions for dates
def get_random_past_date(max_days_ago=180):
    days_ago = random.randint(1, max_days_ago)
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

def calculate_refresh_date(created_date, tier=None):
    created = datetime.strptime(created_date, "%Y-%m-%d")
    if tier == "Tier 1":
        # Weekly refresh
        return (created + timedelta(days=7)).strftime("%Y-%m-%d")
    elif tier == "Tier 2":
        # Monthly refresh
        return (created + timedelta(days=30)).strftime("%Y-%m-%d")
    elif tier == "Tier 3":
        # Quarterly refresh
        return (created + timedelta(days=90)).strftime("%Y-%m-%d")
    else:
        # Default 90 days
        return (created + timedelta(days=90)).strftime("%Y-%m-%d")

# 1. ACCOUNT INFO
account_info_data = [
    {
        "account_id": "ACCT-00001",
        "company_name": "Highway Express Logistics",
        "industry": "Transportation & Logistics",
        "fleet_size": 28,
        "offroad_units": 5,
        "address": "1234 Cargo Way",
        "city": "Dallas",
        "state": "TX",
        "zip_code": "75201",
        "country": "USA",
        "account_status": "Active",
        "target_qualification": "Qualified",
        "created_date": "2024-10-15",
        "last_enriched_date": "2025-03-25",
        "next_refresh_date": "2025-04-01",  # Tier 1 weekly refresh
        "confidence_score": 87,
        "source_systems": "ZoomInfo; Internal DB",
        "notes": "Recent fleet additions reported in Q1."
    },
    {
        "account_id": "ACCT-00002",
        "company_name": "Greenfield Haulers",
        "industry": "Transportation & Logistics",
        "fleet_size": 19,  # Below threshold, for example
        "offroad_units": 51,  # But qualifies via off-road units
        "address": "789 Roadrunner Ln",
        "city": "Atlanta",
        "state": "GA",
        "zip_code": "30301",
        "country": "USA",
        "account_status": "Prospect",
        "target_qualification": "Qualified",
        "created_date": "2024-11-20",
        "last_enriched_date": "2025-03-20",
        "next_refresh_date": "2025-04-20",  # Tier 2 monthly refresh
        "confidence_score": 82,
        "source_systems": "D&B; Internal DB",
        "notes": "Large off-road fleet potential."
    }
]
df_account_info = pd.DataFrame(account_info_data)

# 2. CONTACT INFO
contact_info_data = [
    {
        "contact_id": "CONTACT-1001",
        "full_name": "Jane Smith",
        "title": "Head of Operations",
        "email": "[email protected]",
        "phone": "555-123-4567",
        "created_date": "2024-10-20",
        "last_verified_date": "2025-03-25",
        "next_refresh_date": "2025-04-01",  # Tier 1 account refresh
        "preferred_contact_method": "Email",
        "associated_account_id": "ACCT-00001"
    },
    {
        "contact_id": "CONTACT-1002",
        "full_name": "John Doe",
        "title": "Director of Procurement",
        "email": "[email protected]",
        "phone": "555-987-6543",
        "created_date": "2024-11-05",
        "last_verified_date": "2025-03-22",
        "next_refresh_date": "2025-04-01",  # Tier 1 account refresh
        "preferred_contact_method": "Phone",
        "associated_account_id": "ACCT-00001"
    },
    {
        "contact_id": "CONTACT-2001",
        "full_name": "Alice Johnson",
        "title": "Logistics Manager",
        "email": "[email protected]",
        "phone": "555-654-3210",
        "created_date": "2024-12-10",
        "last_verified_date": "2025-03-28",
        "next_refresh_date": "2025-04-20",  # Tier 2 account refresh
        "preferred_contact_method": "Email",
        "associated_account_id": "ACCT-00002"
    }
]
df_contact_info = pd.DataFrame(contact_info_data)

# 3. DUN & BRADSTREET SAMPLE API RESPONSE
dnb_api_data = [
    {
        "duns_number": "123456789",
        "company_name": "Highway Express Logistics",
        "total_employees": 250,
        "annual_revenue": 45000000,
        "primary_industry": "Freight Transportation",
        "address": "1234 Cargo Way, Dallas, TX",
        "created_date": "2024-10-15",
        "last_updated": "2025-03-25",
        "next_refresh_date": "2025-04-01"  # Tier 1 account refresh
    },
    {
        "duns_number": "987654321",
        "company_name": "Greenfield Haulers",
        "total_employees": 150,
        "annual_revenue": 25000000,
        "primary_industry": "Trucking",
        "address": "789 Roadrunner Ln, Atlanta, GA",
        "created_date": "2024-11-20",
        "last_updated": "2025-03-20",
        "next_refresh_date": "2025-04-20"  # Tier 2 account refresh
    }
]
df_dnb_api = pd.DataFrame(dnb_api_data)

# 4. ZOOMINFO SAMPLE API RESPONSE
zoominfo_api_data = [
    {
        "zoominfo_id": "Z-0001",
        "company_name": "Highway Express Logistics",
        "website": "www.highwayexpress.com",
        "contact_count": 5,
        "phone": "+1-555-111-2222",
        "city": "Dallas",
        "state": "TX",
        "created_date": "2024-10-15",
        "last_enriched": "2025-03-25",
        "next_refresh_date": "2025-04-01"  # Tier 1 account refresh
    },
    {
        "zoominfo_id": "Z-0002",
        "company_name": "Greenfield Haulers",
        "website": "www.greenfieldhaulers.com",
        "contact_count": 3,
        "phone": "+1-555-333-4444",
        "city": "Atlanta",
        "state": "GA",
        "created_date": "2024-11-20",
        "last_enriched": "2025-03-20",
        "next_refresh_date": "2025-04-20"  # Tier 2 account refresh
    }
]
df_zoominfo_api = pd.DataFrame(zoominfo_api_data)

# 5. CLEARBIT SAMPLE API RESPONSE
clearbit_api_data = [
    {
        "domain": "highwayexpress.com",
        "company_name": "Highway Express Logistics",
        "tech_stack": "Salesforce, HubSpot",
        "employees": 250,
        "location": "Dallas, TX",
        "created_date": "2024-10-18",
        "last_verified": "2025-03-25",
        "next_refresh_date": "2025-04-01"  # Tier 1 account refresh
    },
    {
        "domain": "greenfieldhaulers.com",
        "company_name": "Greenfield Haulers",
        "tech_stack": "Marketo, Oracle ERP",
        "employees": 150,
        "location": "Atlanta, GA",
        "created_date": "2024-11-25",
        "last_verified": "2025-03-22",
        "next_refresh_date": "2025-04-20"  # Tier 2 account refresh
    }
]
df_clearbit_api = pd.DataFrame(clearbit_api_data)

# 6. RSS FEED RECORD
rss_feed_data = [
    {
        "source": "LogisticsTimes.com",
        "title": "Highway Express Announces New Fleet Purchases",
        "company": "Highway Express Logistics",
        "summary": "Company to add 5 new 18-wheelers to fleet in Q2.",
        "created_date": "2025-02-15",
        "next_refresh_date": "2025-05-15"  # Default 90 days for RSS feeds
    },
    {
        "source": "FreightDaily News",
        "title": "Greenfield Haulers Expands Off-Road Capabilities",
        "company": "Greenfield Haulers",
        "summary": "Greenfield invests in 10 new excavators this quarter.",
        "created_date": "2025-02-20",
        "next_refresh_date": "2025-05-20"  # Default 90 days for RSS feeds
    }
]
df_rss_feed = pd.DataFrame(rss_feed_data)

# 7. WEB SCRAPE (e.g., "what is the fleet count of amazon?")
web_scrape_data = [
    {
        "query": "what is the fleet count of amazon",
        "output": "Amazon operates an estimated 40,000+ vehicles globally (example data)",
        "method": "Automated web scraping using X method",
        "created_date": "2025-03-01",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "next_refresh_date": "2025-05-30",  # Default 90 days for web scrapes
        "notes": "Scraped from news articles and official statements."
    },
    {
        "query": "what is the fleet count of walmart",
        "output": "Walmart's private fleet numbers over 10,000 trucks (example data)",
        "method": "Automated web scraping using X method",
        "created_date": "2025-03-05",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "next_refresh_date": "2025-06-03",  # Default 90 days for web scrapes
        "notes": "Used multiple sources, unverified."
    }
]
df_web_scrape = pd.DataFrame(web_scrape_data)

# 8. ENRICHMENT CADENCES
enrichment_cadences_data = [
    {
        "account_id": "ACCT-00001",
        "company_name": "Highway Express Logistics",
        "tier": "Tier 1",
        "refresh_frequency": "Weekly",
        "created_date": "2024-10-15",
        "last_refresh_date": "2025-03-25",
        "next_scheduled_refresh": "2025-04-01",
        "fleet_size": 28,
        "sales_cycle_status": "Active Deal",
        "success_potential": "High",
        "notes": "Active expansion discussions"
    },
    {
        "account_id": "ACCT-00002",
        "company_name": "Greenfield Haulers",
        "tier": "Tier 2",
        "refresh_frequency": "Monthly",
        "created_date": "2024-11-20",
        "last_refresh_date": "2025-03-20",
        "next_scheduled_refresh": "2025-04-20",
        "fleet_size": 19,
        "sales_cycle_status": "Prospecting",
        "success_potential": "Medium",
        "notes": "Regular monitoring due to off-road fleet potential"
    },
    {
        "account_id": "ACCT-00003",
        "company_name": "Sunset Delivery Services",
        "tier": "Tier 3",
        "refresh_frequency": "Quarterly",
        "created_date": "2024-12-10",
        "last_refresh_date": "2025-03-10",
        "next_scheduled_refresh": "2025-06-10",
        "fleet_size": 12,
        "sales_cycle_status": "Dormant",
        "success_potential": "Low",
        "notes": "Minimal engagement, barely meets threshold"
    }
]
df_enrichment_cadences = pd.DataFrame(enrichment_cadences_data)

# 9. SCORING LOGIC
scoring_logic_data = [
    {
        "account_id": "ACCT-00001",
        "company_name": "Highway Express Logistics",
        "data_completeness_score": 95,  # out of 100
        "data_recency_score": 85,       # out of 100
        "source_quality_score": 90,      # out of 100
        "final_confidence_score": 91.5,  # weighted average
        "created_date": "2024-10-15",
        "last_calculation_date": "2025-03-25",
        "next_calculation_date": "2025-04-01",  # Tier 1 weekly refresh
        "completeness_factors": {
            "company_info": True,
            "address": True,
            "contacts": True,
            "fleet_data": True
        },
        "days_since_verification": 5,
        "primary_verification_source": "Direct Phone Verification"
    },
    {
        "account_id": "ACCT-00002",
        "company_name": "Greenfield Haulers",
        "data_completeness_score": 85,
        "data_recency_score": 75,
        "source_quality_score": 80,
        "final_confidence_score": 81.5,
        "created_date": "2024-11-20",
        "last_calculation_date": "2025-03-20",
        "next_calculation_date": "2025-04-20",  # Tier 2 monthly refresh
        "completeness_factors": {
            "company_info": True,
            "address": True,
            "contacts": True,
            "fleet_data": False
        },
        "days_since_verification": 10,
        "primary_verification_source": "Web Scraping"
    },
    {
        "account_id": "ACCT-00003",
        "company_name": "Sunset Delivery Services",
        "data_completeness_score": 70,
        "data_recency_score": 65,
        "source_quality_score": 60,
        "final_confidence_score": 66.5,
        "created_date": "2024-12-10",
        "last_calculation_date": "2025-03-10",
        "next_calculation_date": "2025-06-10",  # Tier 3 quarterly refresh
        "completeness_factors": {
            "company_info": True,
            "address": True,
            "contacts": False,
            "fleet_data": False
        },
        "days_since_verification": 30,
        "primary_verification_source": "Public Records"
    }
]
df_scoring_logic = pd.DataFrame(scoring_logic_data)

# 10. HEALTH CHECK KPIs - ACCOUNT LEVEL
account_health_check_kpis_data = [
    # ACCT-00001 (Tier 1) Health Checks
    {
        "account_id": "ACCT-00001",
        "company_name": "Highway Express Logistics",
        "tier": "Tier 1",
        "metric_name": "Last Verified Date Coverage",
        "created_date": "2024-10-15",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-04-01",  # Weekly refresh (Tier 1)
        "score": 97.5,
        "target": 90.0,
        "status": "Above Target"
    },
    {
        "account_id": "ACCT-00001",
        "company_name": "Highway Express Logistics",
        "tier": "Tier 1",
        "metric_name": "Contact Data Completeness",
        "created_date": "2024-10-15",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-04-01",  # Weekly refresh (Tier 1)
        "score": 100.0,
        "target": 95.0,
        "status": "Above Target"
    },
    {
        "account_id": "ACCT-00001",
        "company_name": "Highway Express Logistics",
        "tier": "Tier 1",
        "metric_name": "Bounce/Invalid Rate",
        "created_date": "2024-10-15",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-04-01",  # Weekly refresh (Tier 1)
        "score": 2.5,  # Lower is better for bounce rate
        "target": 5.0,
        "status": "Above Target"
    },
    {
        "account_id": "ACCT-00001",
        "company_name": "Highway Express Logistics",
        "tier": "Tier 1",
        "metric_name": "Enrichment Turnaround Time",
        "created_date": "2024-10-15",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-04-01",  # Weekly refresh (Tier 1)
        "score": 18.5,  # Hours
        "target": 24.0,
        "status": "Above Target"
    },
    {
        "account_id": "ACCT-00001",
        "company_name": "Highway Express Logistics",
        "tier": "Tier 1",
        "metric_name": "Fleet Size Accuracy",
        "created_date": "2024-10-15",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-04-01",  # Weekly refresh (Tier 1)
        "score": 95.0,
        "target": 90.0,
        "status": "Above Target"
    },
    
    # ACCT-00002 (Tier 2) Health Checks
    {
        "account_id": "ACCT-00002",
        "company_name": "Greenfield Haulers",
        "tier": "Tier 2",
        "metric_name": "Last Verified Date Coverage",
        "created_date": "2024-11-20",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-04-20",  # Monthly refresh (Tier 2)
        "score": 90.0,
        "target": 90.0,
        "status": "At Target"
    },
    {
        "account_id": "ACCT-00002",
        "company_name": "Greenfield Haulers",
        "tier": "Tier 2",
        "metric_name": "Contact Data Completeness",
        "created_date": "2024-11-20",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-04-20",  # Monthly refresh (Tier 2)
        "score": 96.0,
        "target": 95.0,
        "status": "Above Target"
    },
    {
        "account_id": "ACCT-00002",
        "company_name": "Greenfield Haulers",
        "tier": "Tier 2",
        "metric_name": "Bounce/Invalid Rate",
        "created_date": "2024-11-20",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-04-20",  # Monthly refresh (Tier 2)
        "score": 4.5,  # Lower is better for bounce rate
        "target": 5.0,
        "status": "Above Target"
    },
    {
        "account_id": "ACCT-00002",
        "company_name": "Greenfield Haulers",
        "tier": "Tier 2",
        "metric_name": "Enrichment Turnaround Time",
        "created_date": "2024-11-20",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-04-20",  # Monthly refresh (Tier 2)
        "score": 55.0,  # Hours
        "target": 72.0,
        "status": "Above Target"
    },
    {
        "account_id": "ACCT-00002",
        "company_name": "Greenfield Haulers",
        "tier": "Tier 2",
        "metric_name": "Fleet Size Accuracy",
        "created_date": "2024-11-20",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-04-20",  # Monthly refresh (Tier 2)
        "score": 92.0,
        "target": 90.0,
        "status": "Above Target"
    },
    
    # ACCT-00003 (Tier 3) Health Checks
    {
        "account_id": "ACCT-00003",
        "company_name": "Sunset Delivery Services",
        "tier": "Tier 3",
        "metric_name": "Last Verified Date Coverage",
        "created_date": "2024-12-10",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-06-10",  # Quarterly refresh (Tier 3)
        "score": 75.0,
        "target": 90.0,
        "status": "Below Target"
    },
    {
        "account_id": "ACCT-00003",
        "company_name": "Sunset Delivery Services",
        "tier": "Tier 3",
        "metric_name": "Contact Data Completeness",
        "created_date": "2024-12-10",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-06-10",  # Quarterly refresh (Tier 3)
        "score": 80.0,
        "target": 95.0,
        "status": "Below Target"
    },
    {
        "account_id": "ACCT-00003",
        "company_name": "Sunset Delivery Services",
        "tier": "Tier 3",
        "metric_name": "Bounce/Invalid Rate",
        "created_date": "2024-12-10",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-06-10",  # Quarterly refresh (Tier 3)
        "score": 8.5,  # Lower is better for bounce rate
        "target": 5.0,
        "status": "Below Target"
    },
    {
        "account_id": "ACCT-00003",
        "company_name": "Sunset Delivery Services",
        "tier": "Tier 3",
        "metric_name": "Enrichment Turnaround Time",
        "created_date": "2024-12-10",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-06-10",  # Quarterly refresh (Tier 3)
        "score": 70.0,  # Hours
        "target": 72.0,
        "status": "Within Target"
    },
    {
        "account_id": "ACCT-00003",
        "company_name": "Sunset Delivery Services",
        "tier": "Tier 3",
        "metric_name": "Fleet Size Accuracy",
        "created_date": "2024-12-10",
        "kpi_date": "2025-03-25",
        "next_refresh_date": "2025-06-10",  # Quarterly refresh (Tier 3)
        "score": 85.0,
        "target": 90.0,
        "status": "Below Target"
    }
]
df_account_health_check_kpis = pd.DataFrame(account_health_check_kpis_data)

# 11. HEALTH CHECK KPIs - TIER LEVEL AGGREGATION (TRANSPOSED)
tier_health_check_kpis_transposed_data = [
    {
        "kpi_name": "Last Verified Date Coverage",
        "description": "Percentage of accounts with at least one contact verified within the last 30 days. Indicates how current your contact information is and whether you need to initiate verification processes.",
        "tier_1_value": 92.5,
        "tier_2_value": 88.0,
        "tier_3_value": 75.0,
        "target": 90.0,
        "status": "Mixed Performance"
    },
    {
        "kpi_name": "Contact Data Completeness",
        "description": "Percentage of accounts with at least one valid email and phone number on record. Essential for outreach capabilities and ensuring sales teams can easily connect with prospects.",
        "tier_1_value": 97.0,
        "tier_2_value": 94.0,
        "tier_3_value": 85.0,
        "target": 95.0,
        "status": "Mixed Performance"
    },
    {
        "kpi_name": "Bounce/Invalid Rate",
        "description": "Rate at which outreach attempts (emails, calls) fail due to invalid data. Lower is better. Directly impacts campaign effectiveness and provides feedback on data quality.",
        "tier_1_value": 3.5,
        "tier_2_value": 6.0,
        "tier_3_value": 8.5,
        "target": 5.0,
        "status": "Mixed Performance"
    },
    {
        "kpi_name": "Duplicate Record Incidence",
        "description": "Percentage of duplicate accounts or contacts identified. Lower is better. Duplicates create confusion, waste resources, and distort analytics and reporting.",
        "tier_1_value": 1.0,
        "tier_2_value": 1.5,
        "tier_3_value": 3.5,
        "overall_value": 1.8,
        "target": 2.0,
        "status": "Mixed Performance"
    },
    {
        "kpi_name": "Enrichment Turnaround Time",
        "description": "Average time from 'Enrichment Request' to 'Data Loaded in CRM'. Lower is better. Measures operational efficiency and data availability speed for sales teams.",
        "tier_1_value": 18.5,
        "tier_2_value": 55.0,
        "tier_3_value": 70.0,
        "urgent_requests_value": 20.5,
        "routine_requests_value": 65.0,
        "target_urgent": 24.0,
        "target_routine": 72.0,
        "status": "Within Target"
    },
    {
        "kpi_name": "Fleet Size Accuracy",
        "description": "Percentage alignment between reported fleet numbers and verified official data.",
        "tier_1_value": 95.0,
        "tier_2_value": 92.0,
        "tier_3_value": 85.0,
        "overall_value": 92.5,
        "target": 90.0,
        "status": "Mixed Performance"
    }
]
df_tier_health_check_kpis_transposed = pd.DataFrame(tier_health_check_kpis_transposed_data)

# Alternative presentation approach: Separate KPI definitions for reference
kpi_definitions_data = [
    {
        "kpi_name": "Last Verified Date Coverage",
        "definition": "Percentage of accounts with at least one contact verified within the last 30 days.",
        "importance": "Indicates how current your contact information is and whether you need to initiate verification processes.",
        "calculation": "Count of accounts with verification in last 30 days / Total accounts in tier",
        "target": "90% of Tier 1 and 2 accounts, 75% for Tier 3"
    },
    {
        "kpi_name": "Contact Data Completeness",
        "definition": "Percentage of accounts with at least one valid email and phone number on record.",
        "importance": "Essential for outreach capabilities and ensuring sales teams can easily connect with prospects.",
        "calculation": "Count of accounts with complete contact data / Total accounts in tier",
        "target": "95% of Tier 1 and 2 accounts, 80% for Tier 3"
    },
    {
        "kpi_name": "Bounce/Invalid Rate",
        "definition": "Rate at which outreach attempts (emails, calls) fail due to invalid data.",
        "importance": "Directly impacts campaign effectiveness and provides feedback on data quality.",
        "calculation": "Number of bounced/invalid contacts / Total outreach attempts",
        "target": "Below 5% for Tier 1, below 7% for Tier 2, below 10% for Tier 3"
    },
    {
        "kpi_name": "Duplicate Record Incidence",
        "definition": "Percentage of duplicate accounts or contacts identified during the month.",
        "importance": "Duplicates create confusion, waste resources, and distort analytics and reporting.",
        "calculation": "Count of identified duplicates / Total records",
        "target": "Below 2% overall, with stricter 1% target for Tier 1"
    },
    {
        "kpi_name": "Enrichment Turnaround Time",
        "definition": "Average time from 'Enrichment Request' to 'Data Loaded in CRM'.",
        "importance": "Measures operational efficiency and data availability speed for sales teams.",
        "calculation": "Sum of request-to-completion time / Number of requests",
        "target": "Under 24 hours for urgent requests; under 72 hours for routine refresh cycles"
    },
    {
        "kpi_name": "Fleet Size Accuracy",
        "definition": "Percentage alignment between reported fleet numbers and verified official data.",
        "importance": "Measures the reliability of a key qualification data point for targeting and segmentation accuracy.",
        "calculation": "Count of accounts with verified fleet data / Total accounts with fleet data",
        "target": "90%+ alignment with official data sources within the last 90 days"
    }
]
df_kpi_definitions = pd.DataFrame(kpi_definitions_data)

# WRITE TO EXCEL (MULTIPLE SHEETS)
with pd.ExcelWriter("sample_data_workbook_final.xlsx", engine="xlsxwriter") as writer:
    df_account_info.to_excel(writer, sheet_name="Account Info", index=False)
    df_contact_info.to_excel(writer, sheet_name="Contact Info", index=False)
    df_dnb_api.to_excel(writer, sheet_name="DNB API", index=False)
    df_zoominfo_api.to_excel(writer, sheet_name="ZoomInfo API", index=False)
    df_clearbit_api.to_excel(writer, sheet_name="Clearbit API", index=False)
    df_rss_feed.to_excel(writer, sheet_name="RSS Feed", index=False)
    df_web_scrape.to_excel(writer, sheet_name="Web Scrape", index=False)
    df_enrichment_cadences.to_excel(writer, sheet_name="Enrichment Cadences", index=False)
    df_scoring_logic.to_excel(writer, sheet_name="Scoring Logic", index=False)
    df_account_health_check_kpis.to_excel(writer, sheet_name="Account Health Checks", index=False)
    df_tier_health_check_kpis_transposed.to_excel(writer, sheet_name="Tier Health Checks", index=False)
    df_kpi_definitions.to_excel(writer, sheet_name="KPI Definitions", index=False)

print("Excel workbook 'sample_data_workbook_final.xlsx' created successfully with transposed tier health checks and KPI definitions!")
