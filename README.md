# Selenium Automation Project

---

## Overview

Part of a Capstone project made for customer Spåt. The project consists of *physical load metric*, *API*, and this, *software robot*. Together these provide 0-10 indicator of athlete's physical stress after a session, which can be used to prevent injuries, optimize improvements and motivate athletes. These are built on top of existing Spåt Application which gathers data from players with UWB, and displays them in web application. 

This software robot project utilizes Selenium for web automation tasks, specifically for automating login, navigation, and file download operations from a website, followed by uploading data to MongoDB. The automation scripts are designed to run both locally and as scheduled jobs using GitHub Actions.

Current implementation logs in to the Spåt application, goes into sessions, filters to session from desired arena, and iterates through three most recent ones. When iterating through, it downloads the Excel files and renames it to include the 'team_id'. After all .xlsx files have been downloaded, they are processed (code form the API repository) and uploaded to the MongoDB database. 

Originally, we were supposed to get data from another webiste, so this was planned to be easily adaptable to another websites structure, but unfortunately this did not the case in this Capstone project.

---

## Project Structure
Below is an overview of important files and folders in the project:
```plaintext
selenium_project/
│
├── .github/
│   └── workflows/         # GitHub Actions workflows
├── temp/                  # Directory to temporary hold the downloaded data
├── tests/                 # Test cases for automation scripts
├── utils/                 # Utility functions (e.g., logging, helper methods)
├── .env                   # Enviromental secrets, DB connection strings etc. Copy structure from .env-template (local setup)
├── .gitignore             # Specifies intentionally untracked files to ignore
├── main.py                # Main script for the automation
├── README.md              # Project description and setup instructions
├── requirements.txt       # Python dependencies
````

---

## Development and Running Locally

These instructions will guide you through setting up the project on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.11 or later
- pip (Python package installer)

### Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/selenium_project.git
    cd selenium_project
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    
3. **Install Dependecies**:
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Create a `.env` File**:
    Create a .env file in the project root directory. Add the following environment variables:
    ```plaintext
    SPAT_URL=http://example.com
    SPAT_USERNAME=secret
    SPAT_PASSWORD=secret
    MONGODB_URL=mongodb+srv://xxx:xxx@xxx
    ```
    Replace the values with your actual data.
   
5. **Run the Main Script**:
    ```bash
    python main.py
    ```

### Using GitHub Actions
This project is configured to run as an automated job via GitHub Actions, triggered daily. You can customize the schedule by modifying the cron job in the `.github/workflows/schedule_bot.yml` file.



