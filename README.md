# BigQuery-to-Zoho-sync-Pipeline

Automated Data Synchronisation from Google BigQuery to Zoho Applications

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

---

## 🚀 Overview

The `BigQuery-to-Zoho-sync-Pipeline` is a robust Python-based solution designed to automate the synchronisation of data from Google BigQuery, your powerful data warehouse, directly into various Zoho Sheets. This pipeline ensures that your operational Zoho data is always up-to-date with the latest insights and analytics derived from BigQuery, eliminating manual data transfers and maintaining data consistency across your business systems.

This project is ideal for organisations that leverage BigQuery for advanced analytics and require that processed, aggregated, or transformed data be reflected in their Zoho operational tools for sales, marketing, finance, or customer service teams.

## ✨ Features

*   **Automated Data Extraction**: Seamlessly query and extract data from specified BigQuery tables or views.
*   **Flexible Data Mapping**: Designed to allow easy configuration for mapping BigQuery fields to Zoho module fields.
*   **Modular Synchronisation**: `sync_scripts` directory allows for individual scripts to handle different Zoho modules or data entities.
*   **Error Handling & Logging**: Includes mechanisms to catch errors during data processing and API calls.
*   **Email Notifications**: Utilises `email_utils.py` to send status updates, success confirmations, or error alerts.
*   **Idempotent Operations**: Designed to handle updates and inserts efficiently, preventing duplicate records (implementation details may vary per sync script).
*   **Environment Variable Configuration**: Securely manage API keys, credentials, and other sensitive information.

## 🛠️ Tech Stack

*   **Python**: The core programming language for the pipeline logic.
*   **Google BigQuery API**: For interacting with your BigQuery datasets.
*   **Zoho API**: For pushing data into Zoho Sheets.
*   **`google-cloud-bigquery`**: Python client library for BigQuery.
*   **`requests`**: For making HTTP requests to the Zoho API (or a specific Zoho Python SDK).
*   **`python-dotenv`**: For managing environment variables.

## ⚙️ Installation

Follow these steps to set up the BigQuery-to-Zoho sync pipeline locally.

### Prerequisites

*   Python 3.8+
*   Google Cloud Project with BigQuery API enabled.
*   A Zoho account with API access enabled (and necessary module permissions).
*   `gcloud` CLI installed and authenticated (optional, for local testing with application default credentials).

### Steps

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Ayo-G/BigQuery-to-Zoho-sync-Pipeline.git
    cd BigQuery-to-Zoho-sync-Pipeline
    ```

2.  **Create a Virtual Environment**:
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Assuming a `requirements.txt` file exists with necessary libraries like `google-cloud-bigquery`, `requests`, `python-dotenv`)*

4.  **Configuration**:
    Create a `.env` file in the project's root directory to store your credentials and configuration.

    ```ini
    # Google BigQuery Configuration
    GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
    BIGQUERY_PROJECT_ID=your-gcp-project-id

    # Zoho API Configuration
    ZOHO_CLIENT_ID=your_zoho_client_id
    ZOHO_CLIENT_SECRET=your_zoho_client_secret
    ZOHO_REFRESH_TOKEN=your_zoho_refresh_token
    ZOHO_API_DOMAIN=https://accounts.zoho.com # e.g., https://accounts.zoho.eu for EU data centers
    ZOHO_API_URL=https://www.zohoapis.com # e.g., https://www.zohoapis.eu

    # Email Notification Configuration (for email_utils.py)
    EMAIL_SENDER_ADDRESS=sender@example.com
    EMAIL_SENDER_PASSWORD=your_email_password # Use app-specific passwords for Gmail/Outlook
    EMAIL_RECEIVER_ADDRESSES=receiver1@example.com,receiver2@example.com
    EMAIL_SMTP_SERVER=smtp.example.com # e.g., smtp.gmail.com
    EMAIL_SMTP_PORT=587 # e.g., 587 for TLS
    ```
    *   **Google Service Account**: Ensure your service account has the necessary permissions to read from BigQuery. Download the JSON key and provide its path.
    *   **Zoho API Credentials**: Obtain your Client ID, Client Secret, and a Refresh Token from the Zoho API Console. Refer to the Zoho API documentation for details on generating these.
    *   **Email Credentials**: Configure your SMTP server details for sending email notifications.

## 🚀 Usage

Once configured, you can run the pipeline from the command line.

1.  **Activate Virtual Environment (if not already active)**:
    ```bash
    source venv/bin/activate
    ```

2.  **Run the Main Pipeline Script**:
    ```bash
    python main.py
    ```
    *(The `main.py` script will orchestrate the execution of the various synchronization scripts located in `sync_scripts/`)*

3.  **Scheduling**:
    For continuous or periodic synchronization, you can schedule `main.py` to run using:
    *   **Cron Job (Linux/macOS)**:
        ```bash
        # Example: Run every hour
        0 * * * * /path/to/your/BigQuery-to-Zoho-sync-Pipeline/venv/bin/python /path/to/your/BigQuery-to-Zoho-sync-Pipeline/main.py >> /var/log/bigquery_zoho_sync.log 2>&1
        ```
    *   **Windows Task Scheduler**: Configure a task to run the Python script.
    *   **Cloud Schedulers**: For cloud-native deployments, consider Google Cloud Scheduler, AWS EventBridge, or Azure Logic Apps to trigger the pipeline.

## 📂 Project Structure

```
BigQuery-to-Zoho-sync-Pipeline/
├── .env                  # Environment variables for configuration (ignored by Git)
├── main.py               # Main entry point for the synchronisation pipeline
├── email_utils.py        # Utility functions for sending email notifications
├── requirements.txt      # Python dependencies
├── sync_scripts/         # Directory containing individual synchronisation scripts
│   ├── __init__.py       # Makes sync_scripts a Python package
│   ├── sync_leads.py     # Example script to sync leads from BigQuery to Zoho CRM
│   ├── sync_accounts.py  # Example script to sync accounts from BigQuery to Zoho CRM
│   └── ...               # Other synchronisation scripts for different Zoho modules
└── README.md             # This README file
```

*   **`main.py`**: This script acts as the orchestrator. It loads configurations, initialises clients (BigQuery, Zoho), and calls the relevant synchronization functions from `sync_scripts`.
*   **`email_utils.py`**: Contains functions to compose and send emails, typically used for reporting success/failure or progress of the sync jobs.
*   **`sync_scripts/`**: This directory is designed to hold individual Python modules, each responsible for synchronizing a specific type of data or a particular Zoho module. This modular approach keeps the codebase organized and makes it easy to add new synchronization tasks.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5.  Push to the branch (`git push origin feature/AmazingFeature`).
6.  Open a Pull Request.

Please make sure your code follows good practices and includes appropriate tests if applicable.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
