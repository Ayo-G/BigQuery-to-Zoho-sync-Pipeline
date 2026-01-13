# BigQuery to Zoho Sheets Sync Pipeline


## Overview

This project is a serverless data pipeline that synchronises query results from **BigQuery** into **Zoho Sheets** on a scheduled basis.

It was built to support a company-wide migration away from Google Workspace, where multiple operational dashboards depended on Google Sheets as their final reporting layer. The pipeline preserves near–real-time access to dashboards while removing the need for manual exports or uploads.

The system is designed for reliability, simplicity, and fast iteration in a production environment.


## Problem Context

After migrating from Google Workspace to Zoho Workspace:

- Existing Google Sheets–based dashboards could no longer refresh automatically
- Teams resorted to manually exporting data from BigQuery and uploading it to Zoho Sheets
- Reporting became inconsistent, error-prone, and time-consuming
- Available third-party connectors did not meet scheduling or reliability requirements

The goal was not just to move data, but to **restore trust in operational reporting** with minimal disruption to non-technical teams.


## High-Level Architecture

**Source**
- BigQuery (single source of truth)

**Processing**
- Python (Pandas) for light transformations
- Parameterized SQL queries

**Orchestration**
- Cloud Scheduler triggers
- Cloud Functions (serverless execution)

**Destination**
- Zoho Sheets via Zoho API

**Flow**
1. Cloud Scheduler triggers a Cloud Function on a defined schedule
2. The function runs a configured BigQuery SQL query
3. Query results are transformed into a Zoho-compatible format
4. Target sheet ranges are cleared and rewritten
5. Logs are emitted for success or failure

This design prioritizes observability and ease of debugging over unnecessary abstraction.


## Key Design Decisions

### Serverless Execution
Cloud Functions were chosen to:
- Reduce infrastructure management overhead
- Enable fast deployment during a tight migration timeline
- Scale automatically with usage

### Overwrite Instead of Append
Each sync clears and rewrites the target sheet range to:
- Prevent duplicate or partial data
- Keep Zoho Sheets aligned with BigQuery as the source of truth
- Simplify recovery after failures

### Configurable Queries
The pipeline supports multiple datasets by defining:
- Query logic
- Destination sheet IDs
- Target ranges
- Schedules

This allows one pipeline to power multiple dashboards without duplication.

### Explicit Error Handling
Failures are logged with enough context to:
- Identify the failed dataset
- Debug authentication or API issues
- Rerun affected syncs safely


## Features

- Syncs 8+ distinct BigQuery datasets to Zoho Sheets
- Secure Zoho API authentication handling
- Idempotent writes to prevent data corruption
- Structured logging for observability
- Schedule-based execution using Cloud Scheduler
- Supports multiple dashboards and business use cases


## Setup & Configuration (High-Level)

> This project is designed for internal use. Details may need adjustment for your environment.

**Prerequisites**
- Google Cloud Project
- BigQuery datasets and queries
- Zoho API credentials
- Python 3.x

**Configuration includes**
- BigQuery query definitions  
- Zoho Sheet IDs and target ranges  
- Authentication tokens  
- Scheduler frequency  

See inline code comments for environment-specific setup.


## Results & Impact

- Eliminated 2+ hours of daily manual reporting work
- Migrated 12 operational dashboards from Google Sheets to Zoho Sheets
- Maintained uninterrupted dashboard access during workspace migration
- Achieved ~99.5% pipeline reliability after deployment
- Enabled operations, customer success, and product teams to continue data-driven decision-making


## Limitations & Tradeoffs

- Schema changes in BigQuery require manual updates to sheet mappings
- Large datasets may approach Zoho API limits
- Monitoring is log-based rather than dashboard-driven

These were acceptable trade-offs given the migration timeline and operational priorities.


## Related Links

- **Portfolio Case Study**: https://rebrand.ly/ayo-g  
- **Technical Deep-Dive Article**: [Medium Article](https://ayo-g.medium.com/bigquery-to-zoho-sheet-sync-pipeline-1782cd3208b3)  


## Author

**Ayomide Gbadegesin**  
Analytics Engineer  

- GitHub: https://github.com/Ayo-G  
- LinkedIn: https://linkedin.com/in/ayo-g/



---
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
