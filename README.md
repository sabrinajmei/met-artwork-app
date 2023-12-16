# Snapshot of The MET
**OPAN 3244 Freestyle Project**

## Description

Metropolitan Museum of Art App: This app accesses data from The Metropolitan Museum of Art Collection API to generate an email spotlighting a specific work of art from The Met, with corresponding information and background on the artwork.

## Table of Contents

- [Installation](#installation)
  - [Virtual Environment](#virtual-environment)
  - [Environment Variables](#environment-variables)
  - [Dependencies](#dependencies)
- [Usage](#usage)
  - [Running the Program](#running-the-program)
  - [Testing](#testing)

## Installation

# Virtual Environment
Create and activate a virtual environment:

```sh
conda create -n met-app python=3.10
conda activate met-app
```

# Environment Variables
Obtain a unique Sendgrid API Key. Follow the setup instructions to create an account, verify your account, setup a single sender, and obtain an API Key.

Create a ".env" file and paste in the following contents:

SENDGRID_API_KEY="_________"
SENDER_ADDRESS="example.gmail.com"

# Dependencies
Install required packages:

```sh
pip install -r requirements.txt
```

## Usage

# Running the Program
Run the Met app:

```sh
python app/app.py
```
# Testing
Paste the following to test 5 functions and ensure the program is running properly. 

```sh
pytest -s test/test.py
```