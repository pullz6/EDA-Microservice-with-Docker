# Project Title

This is a project that has provides data cleaning and imbalance checking as a eda service through docker. 

---

## Table of Contents

1. [Project Overview](https://www.notion.so/readme-md-Template-in-Github-12c81ba51b198002bc79e96f749cafd6?pvs=21)
2. [Installation](https://www.notion.so/readme-md-Template-in-Github-12c81ba51b198002bc79e96f749cafd6?pvs=21)
3. [Project Structure](https://www.notion.so/readme-md-Template-in-Github-12c81ba51b198002bc79e96f749cafd6?pvs=21)
4. [Contributing](https://www.notion.so/readme-md-Template-in-Github-12c81ba51b198002bc79e96f749cafd6?pvs=21)
5. [Acknowledgments](https://www.notion.so/readme-md-Template-in-Github-12c81ba51b198002bc79e96f749cafd6?pvs=21)

---

## Project Overview

### About

- I have created a Fastapi service we you can upload a csv file and it will clean dataframes and show you the imbalance of data. 

---

## Installation

### Prerequisites

1. Fastapi
2. Docker
3. Uvicorn
4. Custom functions (under eda_processor)
5. Python, Pandas, IO and other utility functions

### Setup

Detailed steps to install and run the project:

```bash
bash
Copy code
# Clone the repository
git clone https://github.com/yourusername/yourprojectname.git

# Navigate into the directory
cd app

# Install dependencies
pip install -r requirements.txt

# (Option 1) Run with docker
docker build -t my_eda_service . 

# (Option 1) Run with docker
docker run -p 8000:8000 my_eda_service

# (Option 2) Run with fastapi and python directory
python app/main.py


```

---

## Project Structure

```bash
bash
Copy code
project-root/
│
├── app/                 # Source files
├── Dockerfile           # Dockerfile to build the docker image
├── README.md            # Project documentation
└── requirements.txt     # Project dependencies

```

The app/ has the scripts eda_processor (which has the custom functions) and main.py (which as the fastapi app)
---

## Contributing

Feel free to submit any pull requests and raise any issues with regards to this repo. 


---

## Acknowledgments

Shout out to Docker , Fastapi documentation. 

---
