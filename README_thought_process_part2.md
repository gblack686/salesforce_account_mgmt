# Design Approach & Methodology

## Data Pipeline Architecture

This section outlines the thought process and architecture behind our data enrichment automation framework.

### Data Sources Integration

Our primary data sources include:

- **Commercial Providers (Clay)**:
  - Clearbit: Technology stack and digital footprint data
  - ZoomInfo: Contact and organizational hierarchy information
  - Dun & Bradstreet: Company verification and financial data
  - Clay Validated Email Waterfall: Set of hierarchal email providers and validators
  - Clay Linkedin Company Information: General company and contact information. 
  
- **Public Data Collection**:
  - Automated web scrapers for public company information
  - RSS and news feeds for event-driven updates
  - FMCSA.gov integration for authoritative fleet size and carrier information

### Industry-Specific Enrichment

- Enhanced focus on transportation-specific data sources (FMCSA, DOT records)
- Custom data model for fleet composition and vehicle types
- SONAR API integration for supply chain intelligence and market rates

### Enrichment Strategy & Timing

We've established three timing categories for enrichment operations:

| Timing Type | Description | Use Case |
|-------------|-------------|----------|
| New Account | Immediate enrichment | First-time data population |
| Scheduled Cleaning | Regular cadence | Maintaining data freshness |
| Event-Driven | Triggered by external events | Responding to market changes |

### Tiered Service Model

Accounts are categorized into tiers that determine enrichment frequency:

| Tier | Refresh Frequency | Criteria |
|------|-------------------|----------|
| Tier 1 | Weekly | High-value accounts, active sales cycle |
| Tier 2 | Monthly | Medium-value prospects |
| Tier 3 | Quarterly | Lower-priority accounts |

The tier assignment is **automatically recalculated** based on an algorithm that runs whenever a record in the account changes, ensuring optimal resource allocation.

### Dashboard & Reporting

Sales leadership dashboards provide visibility into:

- **Account-level KPIs**:
  - Data quality scores
  - Most recent contact strategy
  - Estimated market value
  - Sales conversion metrics

- **Tier-level KPIs**:
  - Aggregated performance metrics
  - Compliance with verification timelines
  - Data completeness scores

These dashboards integrate seamlessly with Salesforce, delivering both real-time alerts and scheduled reports to sales leadership.

### Data Quality Framework

Because our data pipeline is designed for frequent updates, we maintain continuous visibility into CRM health through:

- Last verified date coverage tracking
- Contact data completeness metrics
- Bounce/invalid rate monitoring
- Duplicate record identification
- Enrichment turnaround time measurement
- Fleet size data accuracy verification

The complete metrics framework is available in the "Tier Health Checks" and "KPI Definitions" sheets of our workbook.

## Account Hierarchy & Duplicate Management Strategy

### Problem Analysis

After analyzing the SFDC instance, we identified several critical issues that are causing significant frustration:

1. **Duplicate Detection Challenges**:
   - Traditional fuzzy matching alone fails to distinguish between subsidiaries and true duplicates
   - Identical or similar company names appearing across multiple entities creates confusion
   - Multinational companies often have similar names with different domains, leading to false positives
   - Multiple entries occurring when companies are created through different channels (web forms, manual entry, data imports)

2. **Hierarchy Management Issues**:
   - Missing parent-child relationships between obviously related companies
   - Inconsistent naming conventions across related entities
   - Ultimate parent company often not properly identified
   - Geographically distributed subsidiaries frequently disconnected from parent entities
   - Acquisitions and mergers not properly reflected in the account structure

### Algorithmic Approach

To solve these challenges, I developed a multi-dimensional scoring system based on:

1. **Duplicate Detection Algorithm**:
   - Name similarity weighted at 60% of the overall score using tokenization and word overlap analysis
   - Domain equivalence given 20% weight as primary indicator of true duplicates
   - Location/headquarters match accounting for 10% of score to identify geographically distributed entities
   - Industry and revenue match accounting for 10% of score to confirm operational similarity

2. **Hierarchy Relationship Detection**:
   - Pattern recognition in naming conventions (e.g., "Company X - Division Y")
   - Domain hierarchy analysis (e.g., regional.company.com vs company.com)
   - Geographic distribution patterns typical of multinational organizations
   - Industry alignment analysis to distinguish between similarly named but unrelated entities
   - Revenue proportion patterns between potential parent-subsidiary relationships

### Data Modeling Considerations

The solution required extending the standard Salesforce account model with:

1. **Enhanced Account Object**:
   - Proper parent_account_id relationship field usage
   - New ultimate_parent_id field to facilitate rollup reporting
   - Hierarchy_score field measuring completeness of relationships
   - Duplicate_score field capturing potential duplicate likelihood
   - Hierarchy_verified_date tracking when relationships were last validated

2. **Relationship Documentation**:
   - Custom hierarchy visualization using Lightning components
   - Account relationship map for sales team reference
   - Automatic flagging of potential hierarchy issues
   - Confidence scoring for suggested relationships

### Operational Process Design

The implementation follows a systematic workflow:

1. **Initial Data Assessment** (Week 1-2):
   - Baseline current duplicate rate (estimated 15-20%)
   - Measure hierarchy completeness (estimated 40-50%)
   - Quantify impact on sales processes and lead routing
   - Document common patterns in duplicate creation

2. **Prevention System Design** (Week 3-4):
   - Create real-time duplicate detection API
   - Build custom Lightning components for account creation with immediate feedback
   - Enhance standard SFDC duplicate rules with custom logic
   - Develop hierarchy suggestion engine for new account creation

3. **Automated Cleanup Development** (Week 5-8):
   - Build batch processing system for duplicate detection
   - Create workbench UI for data steward review
   - Implement hierarchical relationship suggestions
   - Develop merge preservation logic to maintain critical history

4. **Governance Framework** (Week 9-12):
   - Establish data stewardship model with designated owners
   - Create weekly data quality reporting workflow
   - Implement audit trail for all merge operations
   - Design continuous improvement metrics

### Technical Architecture

The technical implementation relies on:

1. **Core Components**:
   - Custom APEX classes for advanced string matching and fuzzy logic
   - Batch Apex for processing large account volumes
   - Custom Lightning components for visualization
   - REST API endpoints for real-time verification

2. **Integration Points**:
   - D&B Clean API for hierarchy verification
   - ZoomInfo company data for subsidiary detection
   - Custom SOQL queries for pattern matching
   - Salesforce Flow for automation

3. **Success Metrics Framework**:
   - Tracking duplicate rate over time (target: <1%)
   - Measuring hierarchy completeness (target: >95%)
   - Monitoring data steward intervention rate (target: decrease by 80%)
   - Measuring sales team satisfaction via quarterly surveys

This comprehensive approach addresses not only the immediate cleanup needs but establishes sustainable processes to prevent future occurrences, ultimately creating a more reliable account foundation in Salesforce.
