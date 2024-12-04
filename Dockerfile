# TEMPLATE FROM CHATGPT

# # Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Install dependencies
# RUN apt-get update && apt-get install -y wget unzip \
#     && rm -rf /var/lib/apt/lists/*

# # Install ChromeDriver and Chrome
# RUN wget -N https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
#     && apt-get install -y ./google-chrome-stable_current_amd64.deb

# RUN wget -N https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
#     && unzip chromedriver_linux64.zip \
#     && mv chromedriver /usr/local/bin/

# # Set working directory
# WORKDIR /app

# # Copy script and dependencies
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

# # Copy your bot script
# COPY main.py main.py

# # Run the bot
# CMD ["python", "main.py"]
