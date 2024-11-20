# MyScheme.gov.in Web Scraper 🕵️‍♂️

This Python project is designed to scrape scheme data from the **MyScheme.gov.in** website. It uses **Selenium** and **BeautifulSoup** for data extraction and stores the scraped data in a structured JSON format. This project can be helpful for extracting government schemes related to different states and sectors.

## 📋 Features
- Scrapes scheme details from the **MyScheme.gov.in** website.
- Filters and extracts key information such as:
  - **Scheme Title**
  - **State**
  - **Tags**
  - **Headers and Content Sections**
  - **FAQs**
- Supports navigating through multiple pages and collecting data from all available schemes.
- Saves the scraped data in a **JSON** file for further processing.

## ⚙️ Prerequisites
Before running this project, make sure to install the required dependencies.

### Requirements:
- **Python 3.x** (Recommended: Python 3.6 or above)
- **Google Chrome** (Ensure you have the latest version)

### Install dependencies:
You can install the necessary Python packages using `pip`:

```bash
pip install selenium requests beautifulsoup4 pandas webdriver-manager
```

## 🏃‍♂️ How to Run

### Step 1: Clone the repository
Clone this repository to your local machine:

```bash
git clone https://github.com/dharmendradiwaker/govScheme.git
cd my-scheme-web-scraper
```

### Step 2: Install the dependencies
Make sure you've installed all the required dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Run the script
To start scraping data, simply run the script:

```bash
python scraper.py
```

### Step 4: Access Scraped Data
The script will automatically save the collected data into a `scraped_data.json` file in the current working directory. You can view the data in any text editor or use it for further analysis.

## 📝 Code Walkthrough

### Main Components:

1. **Web Scraping with Selenium** 🚀
   - Navigates through multiple pages to extract data from each scheme.
   - Uses **XPath** selectors to find elements on the page.

2. **Data Extraction** 🧐
   - The `parse_webpage(url)` function sends a GET request to fetch scheme details.
   - BeautifulSoup parses the HTML content and extracts the necessary details (like title, tags, FAQs, etc.).

3. **Pagination Handling** 📄
   - Supports handling pagination, automatically clicking on the next page until all pages are scraped.

4. **Data Saving** 💾
   - Once all data is scraped, it is stored in a **JSON** file for later use or analysis.

### Sample Output:
```json
[
    {
        "title": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "state": "Uttar Pradesh",
        "tags": ["Farmer", "Kisan", "Financial Assistance"],
        "head": {
            "Financial Assistance": "₹6000 per year",
            "Eligibility": "Farmers with landholding up to 2 hectares"
        },
        "FAQs": {
            "What is PM-KISAN?": "PM-KISAN provides financial assistance to farmers for their welfare.",
            "How to apply for PM-KISAN?": "Farmers can apply online or through CSC centers."
        }
    }
]
```

## 🌐 Technologies Used:
- **Python** 🐍
- **Selenium** for browser automation
- **BeautifulSoup** for parsing HTML
- **Webdriver Manager** for managing browser drivers
- **Requests** for sending HTTP requests

## 🚧 Limitations:
- The script currently supports scraping of scheme data only from the **MyScheme.gov.in** website.
- The script may require updates in case the website structure changes.

## 💡 Future Enhancements:
- Extend support for scraping other websites related to government schemes.
- Implement better error handling and retries in case of failed requests.
- Add functionality to automatically store the data in a database (e.g., MongoDB, MySQL).

## 🤝 Contributing
Feel free to fork the repository and submit pull requests. Contributions are welcome to improve and extend the functionality of this web scraper!

---

Happy Scraping! 😄

