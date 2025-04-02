import pandas as pd
from datetime import datetime, timedelta
import random
import uuid
import numpy as np

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
        "company_name": "MegaLogistics Inc.",
        "industry": "Logistics",
        "fleet_size": 125,
        "offroad_units": 45,
        "address": "1500 Logistics Way",
        "city": "Chicago",
        "state": "IL",
        "zip_code": "60601",
        "country": "USA",
        "account_status": "Active",
        "target_qualification": "Qualified",
        "created_date": "2024-09-15",
        "last_enriched_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "next_refresh_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "confidence_score": 95,
        "source_systems": "ZoomInfo; D&B; Internal DB",
        "notes": "Parent company with multiple subsidiaries"
    },
    {
        "account_id": "ACCT-00002",
        "company_name": "MegaLogistics - Western Division",
        "industry": "Logistics",
        "fleet_size": 58,
        "offroad_units": 12,
        "address": "3800 Freight Avenue",
        "city": "Denver",
        "state": "CO",
        "zip_code": "80202",
        "country": "USA",
        "account_status": "Active",
        "target_qualification": "Qualified",
        "created_date": "2024-10-05",
        "last_enriched_date": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
        "next_refresh_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
        "confidence_score": 90,
        "source_systems": "ZoomInfo; Internal DB",
        "notes": "Subsidiary of MegaLogistics Inc."
    },
    {
        "account_id": "ACCT-00003",
        "company_name": "TransGlobal Shipping",
        "industry": "Freight",
        "fleet_size": 42,
        "offroad_units": 0,
        "address": "250 Harbor Drive",
        "city": "Boston",
        "state": "MA",
        "zip_code": "02210",
        "country": "USA",
        "account_status": "Active",
        "target_qualification": "Qualified",
        "created_date": "2024-09-22",
        "last_enriched_date": (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"),
        "next_refresh_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
        "confidence_score": 80,
        "source_systems": "D&B; Internal DB",
        "notes": "Potential duplicate records in system"
    },
    {
        "account_id": "ACCT-00004",
        "company_name": "Trans-Global Shipping Ltd",
        "industry": "Transportation",
        "fleet_size": 42,
        "offroad_units": 0,
        "address": "250 Harbor Drive",
        "city": "Boston",
        "state": "MA",
        "zip_code": "02210",
        "country": "USA",
        "account_status": "Active",
        "target_qualification": "Qualified",
        "created_date": "2024-10-15",
        "last_enriched_date": (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"),
        "next_refresh_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
        "confidence_score": 85,
        "source_systems": "ZoomInfo; Web Scrape",
        "notes": "Possible duplicate of TransGlobal Shipping"
    },
    {
        "account_id": "ACCT-00005",
        "company_name": "FastFreight Solutions",
        "industry": "Logistics",
        "fleet_size": 85,
        "offroad_units": 30,
        "address": "742 Delivery Street",
        "city": "Atlanta",
        "state": "GA",
        "zip_code": "30303",
        "country": "USA",
        "account_status": "Active",
        "target_qualification": "Qualified",
        "created_date": "2024-10-01",
        "last_enriched_date": (datetime.now() - timedelta(days=25)).strftime("%Y-%m-%d"),
        "next_refresh_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "confidence_score": 88,
        "source_systems": "ZoomInfo; D&B",
        "notes": "Incomplete hierarchy information"
    },
    {
        "account_id": "ACCT-00006",
        "company_name": "FastFreight Europe GmbH",
        "industry": "Logistics",
        "fleet_size": 35,
        "offroad_units": 15,
        "address": "Logistikstraße 24",
        "city": "Berlin",
        "state": "N/A",
        "zip_code": "10115",
        "country": "Germany",
        "account_status": "Active",
        "target_qualification": "Qualified",
        "created_date": "2024-07-15",
        "last_enriched_date": (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d"),
        "next_refresh_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "confidence_score": 75,
        "source_systems": "Web Scrape; D&B",
        "notes": "Missing parent relationship to FastFreight Solutions"
    },
    {
        "account_id": "ACCT-00007",
        "company_name": "Express Delivery Holdings",
        "industry": "Courier Services",
        "fleet_size": 150,
        "offroad_units": 10,
        "address": "5000 Shipping Plaza",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "country": "USA",
        "account_status": "Active",
        "target_qualification": "Qualified",
        "created_date": "2024-09-30",
        "last_enriched_date": (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d"),
        "next_refresh_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "confidence_score": 93,
        "source_systems": "ZoomInfo; D&B; Clearbit",
        "notes": "Global parent company"
    },
    {
        "account_id": "ACCT-00008",
        "company_name": "Express Delivery Japan",
        "industry": "Courier Services",
        "fleet_size": 45,
        "offroad_units": 0,
        "address": "3-2-1 Shipping District",
        "city": "Tokyo",
        "state": "N/A",
        "zip_code": "100-0004",
        "country": "Japan",
        "account_status": "Active",
        "target_qualification": "Qualified",
        "created_date": "2024-09-20",
        "last_enriched_date": (datetime.now() - timedelta(days=18)).strftime("%Y-%m-%d"),
        "next_refresh_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
        "confidence_score": 85,
        "source_systems": "ZoomInfo; Web Scrape",
        "notes": "Subsidiary of Express Delivery Holdings"
    },
    {
        "account_id": "ACCT-00009",
        "company_name": "Express Delivery Service",
        "industry": "Courier Services",
        "fleet_size": 15,
        "offroad_units": 0,
        "address": "456 Courier Road",
        "city": "Chicago",
        "state": "IL",
        "zip_code": "60607",
        "country": "USA",
        "account_status": "Prospect",
        "target_qualification": "Under Review",
        "created_date": "2024-08-15",
        "last_enriched_date": (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"),
        "next_refresh_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "confidence_score": 65,
        "source_systems": "Web Scrape",
        "notes": "Not related to Express Delivery Holdings despite similar name"
    },
    {
        "account_id": "ACCT-00010",
        "company_name": "CargoSmart Inc.",
        "industry": "Freight",
        "fleet_size": 65,
        "offroad_units": 25,
        "address": "800 Transportation Blvd",
        "city": "Dallas",
        "state": "TX",
        "zip_code": "75201",
        "country": "USA",
        "account_status": "Active",
        "target_qualification": "Qualified",
        "created_date": "2024-09-25",
        "last_enriched_date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
        "next_refresh_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "confidence_score": 90,
        "source_systems": "ZoomInfo; D&B",
        "notes": "Recently acquired SmallHaul LLC (not yet reflected in hierarchy)"
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
        "next_refresh_date": "2025-05-15",  # Default 90 days for RSS feeds
        "category": "Account"  # Adding category
    },
    {
        "source": "FreightDaily News",
        "title": "Greenfield Haulers Expands Off-Road Capabilities",
        "company": "Greenfield Haulers",
        "summary": "Greenfield invests in 10 new excavators this quarter.",
        "created_date": "2025-02-20",
        "next_refresh_date": "2025-05-20",  # Default 90 days for RSS feeds
        "category": "Account"  # Adding category
    },
    {
        "source": "FMCSA.dot.gov",
        "title": "New Regulations for ELD Compliance",
        "company": "N/A",
        "summary": "FMCSA announces updated Electronic Logging Device requirements affecting all commercial carriers.",
        "created_date": "2025-03-10",
        "next_refresh_date": "2025-03-17",  # Weekly refresh for regulatory content
        "category": "Global"  # Adding category - global market intelligence
    },
    {
        "source": "FMCSA.dot.gov",
        "title": "Safety Compliance Report Q1 2025",
        "company": "N/A",
        "summary": "Quarterly summary of carrier compliance rates and enforcement actions across the industry.",
        "created_date": "2025-03-15",
        "next_refresh_date": "2025-03-22",  # Weekly refresh
        "category": "Global"  # Adding category - global market intelligence
    }
]
df_rss_feed = pd.DataFrame(rss_feed_data)

# 7. WEB SCRAPE (e.g., "what is the fleet count of amazon?")
web_scrape_data = [
    {
        "query": "what is the fleet count of amazon",
        "output": "Amazon operates an estimated 40,000+ vehicles globally (example data)",
        "method": "Automated web scraping using X method",
        "frequency": "recurring",
        "created_date": "2025-03-01",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "next_refresh_date": "2025-05-30",  # Default 90 days for web scrapes
        "notes": "Scraped from news articles and official statements.",
        "category": "Account"  # Adding category
    },
    {
        "query": "what is the fleet count of walmart",
        "output": "Walmart's private fleet numbers over 10,000 trucks (example data)",
        "method": "Automated web scraping using X method",
        "frequency": "new",
        "created_date": "2025-03-05",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "next_refresh_date": "2025-06-03",  # Default 90 days for web scrapes
        "notes": "Used multiple sources, unverified.",
        "category": "Account"  # Adding category
    },
    {
        "query": "FMCSA carrier safety ratings",
        "output": "As of Q1 2025, 75% of carriers have satisfactory ratings, 15% conditional, 10% unsatisfactory (example data)",
        "method": "FMCSA.dot.gov API and structured data extraction",
        "frequency": "recurring",
        "created_date": "2025-03-10",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "next_refresh_date": "2025-03-17",  # Weekly refresh for regulatory data
        "notes": "Authoritative source directly from DOT database.",
        "category": "Global"  # Adding category - global market intelligence
    },
    {
        "query": "FMCSA Hours of Service compliance statistics",
        "output": "Recent enforcement blitz found 8.5% of drivers with HOS violations (example data)",
        "method": "FMCSA.dot.gov data scraping and report aggregation",
        "frequency": "recurring",
        "created_date": "2025-03-15",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "next_refresh_date": "2025-03-22",  # Weekly refresh
        "notes": "Combined data from multiple FMCSA enforcement reports.",
        "category": "Global"  # Adding category - global market intelligence
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

# 11. DATA SOURCES OVERVIEW
data_sources_overview = [
    {
        "source_name": "ZoomInfo",
        "refresh_rate": "Weekly for Tier 1, Monthly for Tier 2, Quarterly for Tier 3",
        "data_type": "Both new and refresh data",
        "collection_method": "API",
        "owner": "Sales Operations",
        "cost": "$3,500/month",
        "access_credentials": "API key stored in secure vault",
        "data_quality_score": 92,
        "fields_provided": "Company details, contacts, technologies, etc.",
        "typical_response_time": "1-2 seconds",
        "rate_limits": "10,000 requests/day",
        "notes": "Primary source for all contact data"
    },
    {
        "source_name": "Dun & Bradstreet",
        "refresh_rate": "Monthly for all tiers",
        "data_type": "Primarily verification of existing data",
        "collection_method": "API",
        "owner": "Data Team",
        "cost": "$2,800/month",
        "access_credentials": "OAuth2 tokens",
        "data_quality_score": 95,
        "fields_provided": "Financial data, employee count, industry codes",
        "typical_response_time": "2-3 seconds",
        "rate_limits": "5,000 requests/day",
        "notes": "Authoritative source for company verification"
    },
    {
        "source_name": "Clearbit",
        "refresh_rate": "Weekly for Tier 1, Monthly for others",
        "data_type": "Enrichment of existing records",
        "collection_method": "API",
        "owner": "Marketing Operations",
        "cost": "$1,200/month",
        "access_credentials": "API key in configuration file",
        "data_quality_score": 88,
        "fields_provided": "Technology stack, social profiles, etc.",
        "typical_response_time": "0.5-1 seconds",
        "rate_limits": "20,000 requests/day",
        "notes": "Used primarily for technology stack insights"
    },
    {
        "source_name": "Web Scraping",
        "refresh_rate": "On-demand",
        "data_type": "New data acquisition",
        "collection_method": "Custom Python scripts",
        "owner": "Data Engineering Team",
        "cost": "Internal resource cost only",
        "access_credentials": "N/A",
        "data_quality_score": 75,
        "fields_provided": "Public fleet information, news mentions",
        "typical_response_time": "5-30 minutes per batch",
        "rate_limits": "Throttled to avoid IP blocking",
        "notes": "Used for supplemental data not available via APIs"
    },
    {
        "source_name": "RSS Feeds",
        "refresh_rate": "Daily",
        "data_type": "New data for event-driven updates",
        "collection_method": "RSS Aggregator Service",
        "owner": "Marketing Team",
        "cost": "$300/month",
        "access_credentials": "Service account",
        "data_quality_score": 82,
        "fields_provided": "News, acquisitions, fleet changes",
        "typical_response_time": "Real-time",
        "rate_limits": "Unlimited",
        "notes": "Triggers event-based enrichment workflows"
    },
    {
        "source_name": "Internal CRM",
        "refresh_rate": "Real-time",
        "data_type": "Source of truth for account status",
        "collection_method": "Salesforce API",
        "owner": "Sales Operations",
        "cost": "Included in Salesforce license",
        "access_credentials": "OAuth via connected app",
        "data_quality_score": 90,
        "fields_provided": "Account status, sales cycle info, contacts",
        "typical_response_time": "1 second",
        "rate_limits": "100,000 requests/day",
        "notes": "System of record for all prospect/customer data"
    },
    {
        "source_name": "Government DOT Records",
        "refresh_rate": "Quarterly",
        "data_type": "Verification of fleet data",
        "collection_method": "Batch download + processing",
        "owner": "Data Team",
        "cost": "Free",
        "access_credentials": "Public data",
        "data_quality_score": 98,
        "fields_provided": "Official fleet size, DOT numbers, compliance",
        "typical_response_time": "24-48 hours for processing",
        "rate_limits": "N/A",
        "notes": "Most accurate source for fleet verification"
    },
    {
        "source_name": "SONAR API",
        "refresh_rate": "Weekly for Tier 1, Monthly for Tier 2-3",
        "data_type": "High-frequency transportation & supply chain data",
        "collection_method": "API",
        "owner": "Supply Chain Analytics Team",
        "cost": "$4,200/month",
        "access_credentials": "API token with role-based access",
        "data_quality_score": 94,
        "fields_provided": "Market rates, capacity data, freight indices across trucking, rail, ocean, and air",
        "typical_response_time": "1-2 seconds",
        "rate_limits": "15,000 requests/day",
        "notes": "Premium source for supply chain intelligence and market rate benchmarking"
    }
]
df_data_sources = pd.DataFrame(data_sources_overview)

# 12. ACCOUNT HIERARCHY & DUPLICATE MANAGEMENT DATA
# Creating accounts with hierarchy issues and duplicates
hierarchy_accounts = [
    # Parent company and subsidiaries
    {
        "account_id": "AC" + str(uuid.uuid4())[:8],
        "account_name": "MegaLogistics Inc.",
        "parent_account_id": None,
        "ultimate_parent_id": None,
        "domain": "megalogistics.com",
        "industry": "Logistics",
        "annual_revenue": "$750M",
        "headquarters": "Chicago, IL",
        "global_presence": "Yes",
        "duplicate_score": 0,
        "hierarchy_score": 100,
        "tier": 1,
        "last_verified_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "hierarchy_complete": True,
        "duplicate_status": "N/A"
    },
    {
        "account_id": "AC" + str(uuid.uuid4())[:8],
        "account_name": "MegaLogistics - Western Division",
        "parent_account_id": "AC12345678",  # Will be updated with actual IDs after creation
        "ultimate_parent_id": "AC12345678",  # Will be updated with actual IDs after creation
        "domain": "west.megalogistics.com",
        "industry": "Logistics",
        "annual_revenue": "$250M",
        "headquarters": "Denver, CO",
        "global_presence": "No",
        "duplicate_score": 0,
        "hierarchy_score": 100,
        "tier": 2,
        "last_verified_date": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
        "hierarchy_complete": True,
        "duplicate_status": "N/A"
    },
    # Duplicate account scenario
    {
        "account_id": "AC" + str(uuid.uuid4())[:8],
        "account_name": "TransGlobal Shipping",
        "parent_account_id": None,
        "ultimate_parent_id": None,
        "domain": "transglobalshipping.com",
        "industry": "Freight",
        "annual_revenue": "$320M",
        "headquarters": "Boston, MA",
        "global_presence": "Yes",
        "duplicate_score": 0,
        "hierarchy_score": 80,
        "tier": 2,
        "last_verified_date": (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"),
        "hierarchy_complete": False,
        "duplicate_status": "N/A"
    },
    {
        "account_id": "AC" + str(uuid.uuid4())[:8],
        "account_name": "Trans-Global Shipping Ltd",
        "parent_account_id": None,
        "ultimate_parent_id": None,
        "domain": "transglobalshipping.com",
        "industry": "Transportation",
        "annual_revenue": "$320M",
        "headquarters": "Boston, MA",
        "global_presence": "Yes",
        "duplicate_score": 85,
        "hierarchy_score": 40,
        "tier": 2,
        "last_verified_date": (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"),
        "hierarchy_complete": False,
        "duplicate_status": "Potential Duplicate"
    },
    # Incomplete hierarchy scenario
    {
        "account_id": "AC" + str(uuid.uuid4())[:8],
        "account_name": "FastFreight Solutions",
        "parent_account_id": None,
        "ultimate_parent_id": None,
        "domain": "fastfreight.com",
        "industry": "Logistics",
        "annual_revenue": "$450M",
        "headquarters": "Atlanta, GA",
        "global_presence": "Yes",
        "duplicate_score": 0,
        "hierarchy_score": 35,
        "tier": 1,
        "last_verified_date": (datetime.now() - timedelta(days=25)).strftime("%Y-%m-%d"),
        "hierarchy_complete": False,
        "duplicate_status": "N/A"
    },
    {
        "account_id": "AC" + str(uuid.uuid4())[:8],
        "account_name": "FastFreight Europe GmbH",
        "parent_account_id": None,  # Missing parent link
        "ultimate_parent_id": None,  # Missing ultimate parent link
        "domain": "fastfreight.eu",
        "industry": "Logistics",
        "annual_revenue": "$150M",
        "headquarters": "Berlin, Germany",
        "global_presence": "Yes",
        "duplicate_score": 0,
        "hierarchy_score": 25,
        "tier": 3,
        "last_verified_date": (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d"),
        "hierarchy_complete": False,
        "duplicate_status": "N/A"
    },
    # Multinational with similar naming
    {
        "account_id": "AC" + str(uuid.uuid4())[:8],
        "account_name": "Express Delivery Holdings",
        "parent_account_id": None,
        "ultimate_parent_id": None,
        "domain": "expressdelivery.com",
        "industry": "Courier Services",
        "annual_revenue": "$890M",
        "headquarters": "New York, NY",
        "global_presence": "Yes",
        "duplicate_score": 0,
        "hierarchy_score": 90,
        "tier": 1,
        "last_verified_date": (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d"),
        "hierarchy_complete": True,
        "duplicate_status": "N/A"
    },
    {
        "account_id": "AC" + str(uuid.uuid4())[:8],
        "account_name": "Express Delivery Japan",
        "parent_account_id": "AC87654321",  # Will be updated with actual IDs after creation
        "ultimate_parent_id": "AC87654321",  # Will be updated with actual IDs after creation
        "domain": "expressdelivery.jp",
        "industry": "Courier Services",
        "annual_revenue": "$210M",
        "headquarters": "Tokyo, Japan",
        "global_presence": "No",
        "duplicate_score": 72,
        "hierarchy_score": 90,
        "tier": 2,
        "last_verified_date": (datetime.now() - timedelta(days=18)).strftime("%Y-%m-%d"),
        "hierarchy_complete": True,
        "duplicate_status": "Not a Duplicate - Subsidiary"
    },
    # Similar company but actually different
    {
        "account_id": "AC" + str(uuid.uuid4())[:8],
        "account_name": "Express Delivery Service",
        "parent_account_id": None,
        "ultimate_parent_id": None,
        "domain": "eds-courier.com",
        "industry": "Courier Services",
        "annual_revenue": "$45M",
        "headquarters": "Chicago, IL",
        "global_presence": "No",
        "duplicate_score": 65,
        "hierarchy_score": 100,
        "tier": 3,
        "last_verified_date": (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"),
        "hierarchy_complete": True,
        "duplicate_status": "Not a Duplicate - Different Company"
    },
    # Company with acquisition
    {
        "account_id": "AC" + str(uuid.uuid4())[:8],
        "account_name": "CargoSmart Inc.",
        "parent_account_id": None,
        "ultimate_parent_id": None,
        "domain": "cargosmart.com",
        "industry": "Freight",
        "annual_revenue": "$380M",
        "headquarters": "Dallas, TX",
        "global_presence": "Yes",
        "duplicate_score": 0,
        "hierarchy_score": 60,
        "tier": 1,
        "last_verified_date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
        "hierarchy_complete": False,
        "duplicate_status": "N/A"
    }
]

# Fixing parent relationships after creation (normally would be done with proper SFDC IDs)
# This is just for demonstration purposes
parent_companies = {
    "MegaLogistics Inc.": None,
    "MegaLogistics - Western Division": "MegaLogistics Inc.",
    "TransGlobal Shipping": None,
    "Trans-Global Shipping Ltd": None,
    "FastFreight Solutions": None,
    "FastFreight Europe GmbH": "FastFreight Solutions",  # Should be linked but isn't
    "Express Delivery Holdings": None,
    "Express Delivery Japan": "Express Delivery Holdings",
    "Express Delivery Service": None,
    "CargoSmart Inc.": None
}

# Create a dictionary to map company names to account IDs
account_id_map = {}
for account in hierarchy_accounts:
    account_id_map[account["account_name"]] = account["account_id"]

# Update parent IDs based on the parent company mapping
for account in hierarchy_accounts:
    parent_name = parent_companies[account["account_name"]]
    if parent_name:
        if parent_name in account_id_map:
            account["parent_account_id"] = account_id_map[parent_name]
            # Also find ultimate parent
            current_parent = parent_name
            while parent_companies[current_parent] is not None:
                current_parent = parent_companies[current_parent]
            account["ultimate_parent_id"] = account_id_map[current_parent]

# Create contacts for each account
hierarchy_contacts = []
for account in hierarchy_accounts:
    # Create 2-4 contacts per account
    num_contacts = random.randint(2, 4)
    for i in range(num_contacts):
        positions = ["CEO", "CFO", "COO", "VP of Operations", "Fleet Manager", "Logistics Director", 
                     "Supply Chain Manager", "Transportation Manager"]
        
        # For some accounts, create duplicate contacts
        if "Trans-Global" in account["account_name"] and i == 0:
            # Create a duplicate contact for the duplicate account
            duplicate_idx = next((idx for idx, acct in enumerate(hierarchy_accounts) 
                                if "TransGlobal" in acct["account_name"]), None)
            if duplicate_idx is not None:
                # Find an existing contact to duplicate
                dup_contact = next((c for c in hierarchy_contacts 
                                    if c["account_id"] == hierarchy_accounts[duplicate_idx]["account_id"]), None)
                if dup_contact:
                    # Create a slightly modified duplicate
                    hierarchy_contacts.append({
                        "contact_id": "CT" + str(uuid.uuid4())[:8],
                        "account_id": account["account_id"],
                        "first_name": dup_contact["first_name"],
                        "last_name": dup_contact["last_name"],
                        "email": dup_contact["first_name"].lower() + "." + dup_contact["last_name"].lower() + "@" + account["domain"],
                        "phone": dup_contact["phone"],
                        "position": dup_contact["position"],
                        "linkedin_url": "linkedin.com/in/" + dup_contact["first_name"].lower() + dup_contact["last_name"].lower(),
                        "last_contact_date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
                        "notes": "Potential duplicate contact",
                        "duplicate_score": 95,
                        "duplicate_status": "Potential Duplicate"
                    })
                    continue
        
        # Otherwise create a normal contact
        hierarchy_contacts.append({
            "contact_id": "CT" + str(uuid.uuid4())[:8],
            "account_id": account["account_id"],
            "first_name": random.choice(["John", "Sarah", "Robert", "Lisa", "Michael", "Emma", "David", "Jennifer"]),
            "last_name": random.choice(["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson"]),
            "email": "",  # Will be generated
            "phone": f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "position": random.choice(positions),
            "linkedin_url": "",  # Will be generated
            "last_contact_date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
            "notes": random.choice(["Key decision maker", "Technical contact", "Initial outreach made", "Responded positively", ""]),
            "duplicate_score": 0,
            "duplicate_status": "N/A"
        })
        
        # Generate email and LinkedIn URL
        latest_contact = hierarchy_contacts[-1]
        latest_contact["email"] = latest_contact["first_name"].lower() + "." + latest_contact["last_name"].lower() + "@" + account["domain"]
        latest_contact["linkedin_url"] = "linkedin.com/in/" + latest_contact["first_name"].lower() + latest_contact["last_name"].lower()

# Convert to dataframes
df_hierarchy_accounts = pd.DataFrame(hierarchy_accounts)
df_hierarchy_contacts = pd.DataFrame(hierarchy_contacts)

# Create functions for identifying duplicates and hierarchy issues

def identify_potential_duplicates(accounts_df):
    """
    Identifies potential duplicate accounts based on name similarity and domain.
    Returns a dataframe with duplicate pairs and scores.
    """
    duplicates = []
    
    # Get unique domains
    domains = accounts_df["domain"].unique()
    
    for domain in domains:
        # Get accounts with this domain
        domain_accounts = accounts_df[accounts_df["domain"] == domain]
        
        if len(domain_accounts) > 1:
            # Multiple accounts with same domain
            for i, account1 in domain_accounts.iterrows():
                for j, account2 in domain_accounts.iterrows():
                    if i < j:  # Avoid comparing the same pair twice
                        # Calculate name similarity (simplified)
                        name_similarity = 0
                        if account1["account_name"].lower() == account2["account_name"].lower():
                            name_similarity = 100
                        else:
                            # Simple word overlap calculation
                            words1 = set(account1["account_name"].lower().replace('-', ' ').split())
                            words2 = set(account2["account_name"].lower().replace('-', ' ').split())
                            if words1 and words2:
                                name_similarity = int(100 * len(words1.intersection(words2)) / len(words1.union(words2)))
                        
                        # Check other factors
                        same_hq = account1["headquarters"] == account2["headquarters"]
                        same_industry = account1["industry"] == account2["industry"]
                        same_revenue = account1["annual_revenue"] == account2["annual_revenue"]
                        
                        # Calculate overall duplicate score
                        duplicate_score = name_similarity * 0.6
                        if same_hq:
                            duplicate_score += 20
                        if same_industry:
                            duplicate_score += 10
                        if same_revenue:
                            duplicate_score += 10
                        
                        duplicate_score = min(int(duplicate_score), 100)
                        
                        if duplicate_score > 50:  # Threshold for potential duplicates
                            duplicates.append({
                                "account1_id": account1["account_id"],
                                "account1_name": account1["account_name"],
                                "account2_id": account2["account_id"],
                                "account2_name": account2["account_name"],
                                "duplicate_score": duplicate_score,
                                "same_domain": True,
                                "same_hq": same_hq,
                                "same_industry": same_industry,
                                "same_revenue": same_revenue,
                                "recommended_action": "Merge" if duplicate_score > 75 else "Review",
                                "status": "Open"
                            })
    
    # Also look for similar names with different domains
    for i, account1 in accounts_df.iterrows():
        for j, account2 in accounts_df.iterrows():
            if i < j and account1["domain"] != account2["domain"]:
                # Calculate name similarity for different domains
                words1 = set(account1["account_name"].lower().replace('-', ' ').split())
                words2 = set(account2["account_name"].lower().replace('-', ' ').split())
                if words1 and words2:
                    name_similarity = int(100 * len(words1.intersection(words2)) / len(words1.union(words2)))
                    
                    if name_similarity > 70:  # High name similarity with different domains
                        # Calculate hierarchy probability
                        same_hq = account1["headquarters"] == account2["headquarters"]
                        same_industry = account1["industry"] == account2["industry"]
                        
                        # Different score calculation for possible subsidiaries
                        subsidiary_score = name_similarity * 0.7
                        if same_industry:
                            subsidiary_score += 15
                        
                        subsidiary_score = min(int(subsidiary_score), 100)
                        
                        if subsidiary_score > 60:  # Threshold for potential hierarchy relationship
                            duplicates.append({
                                "account1_id": account1["account_id"],
                                "account1_name": account1["account_name"],
                                "account2_id": account2["account_id"],
                                "account2_name": account2["account_name"],
                                "duplicate_score": subsidiary_score,
                                "same_domain": False,
                                "same_hq": same_hq,
                                "same_industry": same_industry,
                                "same_revenue": False,
                                "recommended_action": "Check Hierarchy" if subsidiary_score > 75 else "Review",
                                "status": "Open"
                            })
    
    return pd.DataFrame(duplicates)

def evaluate_hierarchy_completeness(accounts_df):
    """
    Evaluates the completeness of account hierarchies.
    Returns a dataframe with hierarchy scores and recommendations.
    """
    hierarchy_analysis = []
    
    # Group accounts by ultimate parent ID (if available)
    accounts_with_parents = accounts_df[accounts_df["parent_account_id"].notna()]
    
    # For each account with a parent, verify hierarchy completeness
    for _, account in accounts_df.iterrows():
        score = 100  # Start with perfect score
        issues = []
        
        # Check if parent_account_id exists but ultimate_parent_id doesn't
        if pd.notna(account["parent_account_id"]) and pd.isna(account["ultimate_parent_id"]):
            score -= 30
            issues.append("Missing ultimate parent reference")
        
        # Check if this account should be a parent but isn't identified as one
        potential_subsidiaries = accounts_df[
            (accounts_df["account_name"].str.contains(account["account_name"].split()[0], case=False)) & 
            (accounts_df["account_id"] != account["account_id"])
        ]
        
        if len(potential_subsidiaries) > 0 and account["parent_account_id"] is None:
            for _, subsidiary in potential_subsidiaries.iterrows():
                if subsidiary["parent_account_id"] != account["account_id"]:
                    score -= 10
                    issues.append(f"Potential missing subsidiary link: {subsidiary['account_name']}")
        
        # Check for orphaned subsidiaries (those with similar names but no parent link)
        if pd.isna(account["parent_account_id"]):
            for word in account["account_name"].split():
                if word not in ["Inc.", "Ltd", "LLC", "GmbH", "Corp.", "Corporation", "The", "Of", "And"]:
                    potential_parents = accounts_df[
                        (accounts_df["account_name"].str.contains(word, case=False)) & 
                        (accounts_df["account_id"] != account["account_id"])
                    ]
                    
                    if len(potential_parents) > 0:
                        score -= 15
                        parent_names = ", ".join(potential_parents["account_name"].tolist())
                        issues.append(f"Potential missing parent link to: {parent_names}")
                        break
        
        # Ensure score doesn't go below 0
        score = max(score, 0)
        
        hierarchy_analysis.append({
            "account_id": account["account_id"],
            "account_name": account["account_name"],
            "has_parent": pd.notna(account["parent_account_id"]),
            "has_ultimate_parent": pd.notna(account["ultimate_parent_id"]),
            "hierarchy_score": score,
            "hierarchy_complete": score > 80,
            "issues": "; ".join(issues) if issues else "None",
            "recommended_action": "Fix Hierarchy" if score < 80 else "None"
        })
    
    return pd.DataFrame(hierarchy_analysis)

# Generate analysis
df_duplicate_analysis = identify_potential_duplicates(df_hierarchy_accounts)
df_hierarchy_analysis = evaluate_hierarchy_completeness(df_hierarchy_accounts)

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
    df_data_sources.to_excel(writer, sheet_name="Data Sources Overview", index=False)
    df_hierarchy_accounts.to_excel(writer, sheet_name="Account Hierarchy Data", index=False)
    df_hierarchy_contacts.to_excel(writer, sheet_name="Hierarchy Contacts", index=False)
    df_duplicate_analysis.to_excel(writer, sheet_name="Duplicate Analysis", index=False)
    df_hierarchy_analysis.to_excel(writer, sheet_name="Hierarchy Analysis", index=False)
    
    # Format the Data Sources Overview sheet
    workbook = writer.book
    data_sources_sheet = writer.sheets["Data Sources Overview"]
    
    # Add column width formatting
    data_sources_sheet.set_column('A:A', 20)  # Source name
    data_sources_sheet.set_column('B:B', 40)  # Refresh rate
    data_sources_sheet.set_column('C:C', 25)  # Data type
    data_sources_sheet.set_column('D:D', 25)  # Collection method
    data_sources_sheet.set_column('E:E', 20)  # Owner
    data_sources_sheet.set_column('F:F', 15)  # Cost
    data_sources_sheet.set_column('G:G', 30)  # Access credentials
    data_sources_sheet.set_column('H:H', 15)  # Data quality score
    data_sources_sheet.set_column('I:I', 40)  # Fields provided
    data_sources_sheet.set_column('J:J', 20)  # Typical response time
    data_sources_sheet.set_column('K:K', 20)  # Rate limits
    data_sources_sheet.set_column('L:L', 40)  # Notes
    
    # Format the Duplicate Analysis sheet
    dup_sheet = writer.sheets["Duplicate Analysis"]
    dup_sheet.set_column('A:B', 15)  # Account IDs
    dup_sheet.set_column('C:D', 30)  # Account names
    dup_sheet.set_column('E:E', 15)  # Duplicate score
    dup_sheet.set_column('J:J', 20)  # Recommended action
    
    # Format the Hierarchy Analysis sheet
    hier_sheet = writer.sheets["Hierarchy Analysis"]
    hier_sheet.set_column('A:A', 15)  # Account ID
    hier_sheet.set_column('B:B', 30)  # Account name
    hier_sheet.set_column('G:G', 40)  # Issues
    hier_sheet.set_column('H:H', 20)  # Recommended action

print("Excel workbook 'sample_data_workbook_final.xlsx' created successfully with Account Hierarchy and Duplicate Management data!")
