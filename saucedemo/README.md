# Selenium Login Test - SauceDemo

This project contains automated test cases for the login page of [SauceDemo](https://www.saucedemo.com/) using **Python**, **Selenium**, and **pytest**.

---

## Features

- Test **successful login** with valid credentials.  
- Test **login failure** with invalid credentials.  
- Uses **pytest fixtures** for browser setup and teardown.  
- Works with **Chrome WebDriver** without additional managers.

---

## Project Structure

\`\`\`
saucedemo/
├── tests/
│   ├── login_page.py        # Login page class with credentials and login method
│   └── test_login.py        # Pytest test cases
├── venv/                    # Python virtual environment
└── README.md
\`\`\`

---

## Installation

1. Clone the repository:

\`\`\`bash
git clone <your-repo-url>
cd saucedemo
\`\`\`

2. Create and activate a virtual environment:

\`\`\`bash
python3 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
\`\`\`

3. Install dependencies:

\`\`\`bash
pip install selenium pytest
\`\`\`

---

## Usage

Run all tests:

\`\`\`bash
pytest -v
\`\`\`

Run a specific test file:

\`\`\`bash
pytest -v tests/test_login.py
\`\`\`

---

## How It Works

1. **Fixture \`driver\`** sets up a Chrome browser before each test and closes it after.  
2. **\`Login\` class** contains the URL, valid/invalid credentials, and a login method.  
3. **\`test_login_success\`** checks if a valid login redirects to the inventory page.  
4. **\`test_login_failure\`** checks if the correct error message appears for invalid credentials.

---

## Notes

- Make sure **ChromeDriver** is installed and added to your system PATH.  
- Tests are written using **pytest**, so you can integrate with CI/CD pipelines.
EOL
