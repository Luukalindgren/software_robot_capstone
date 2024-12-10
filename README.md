# Selenium Automation Project

This project utilizes Selenium for web automation tasks, specifically for automating login, navigation, and file download operations from a website, followed by uploading data to MongoDB. The automation scripts are designed to run both locally and as scheduled jobs using GitHub Actions.

## Getting Started

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
    ````
3. **Install Dependecies**:
    ```bash
    pip install -r requirements.txt
    ````
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

## Project Structure
Below is an overview of important files and folders in the project:
```plaintext
selenium_project/
│
├── venv/                  # Virtual environment
├── tests/                 # Test cases for automation scripts
├── utils/                 # Utility functions (e.g., logging, helper methods)
├── requirements.txt       # Python dependencies
├── main.py                # Main script for the automation
├── README.md              # Project description and setup instructions
├── .gitignore             # Specifies intentionally untracked files to ignore
├── .env                   # Environment variables (local setup)
├── .github/
│   └── workflows/         # GitHub Actions workflows
````

