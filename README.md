# 📱 Web Scraping for Used Smartphones (Dubizzle & MobileMisr)

## 🎯 Objective
This project aims to **scrape pricing data for used smartphones** (e.g., *iPhone 13, Samsung S22*) from two Egyptian e-commerce websites:

- [Dubizzle](https://www.dubizzle.com.eg)
- [Mobile Misr](https://mobilemasr.com)

The goal is to collect and save data such as product name, price, location, and listing URL for analytical or comparison purposes.

---

## 🧠 Project Overview

Each website has its own Python scraping script:

| File Name | Description |
|------------|--------------|
| **`dubizzle_scraper_bs4.py`** | Dubizzle scraper built using `Requests` and `BeautifulSoup`. Worked until **20/10/2025** before Dubizzle increased its bot protection. |
| **`dubizzle_scraper_playwright.py`** | Updated Dubizzle scraper using **Playwright + Stealth** to bypass protection and continue scraping. |
| **`mobile_misr_scraper.py`** | Scraper for MobileMisr using `Requests` and `BeautifulSoup`. |
| **`dubizzle_products.csv`** | Saved results from Dubizzle scraping. |
| **`MobileMisr.csv`** | Saved results from MobileMisr scraping. |

---

## ⚙️ How It Works

Each script follows the same general steps:

1. Prompts the user to input a search term (e.g., `iphone 13`).
2. Builds a search URL dynamically.
3. Iterates through multiple pages (pagination handling).
4. Extracts key information:
   - Product Name / Description  
   - Price  
   - Location  
   - Listing URL  
   - Page Number  
5. Saves the results to a CSV file.

---

## 🧩 Required Libraries

### For `BeautifulSoup` scripts:
```bash
pip install requests beautifulsoup4 lxml

## ⚙️ For `playwright` scripts:

```bash
pip install playwright playwright-stealth
playwright install
```

## 🚀 How to Run

### ▶️ 1. Run Dubizzle Scraper (BeautifulSoup version)

⚠️ **Note:** This script stopped working after **20/10/2025** due to new site protection.

```bash
python dubizzle_scraper_bs4.py
```

---

### ▶️ 2. Run Dubizzle Scraper (Playwright version)

✅ **This is the updated working version:**

```bash
python dubizzle_scraper_playwright.py
```

---

### ▶️ 3. Run MobileMisr Scraper

```bash
python mobile_misr_scraper.py
```

---

## 💡 Technical Notes

- Before **20/10/2025**, Dubizzle could be scraped easily using `requests` + `BeautifulSoup`.
- After that date, the website added **anti-bot protection**, blocking static scrapers.
- To fix this, I switched to **Playwright with Stealth**, which simulates real user behavior.
- I had no prior experience with Playwright, so I used **LLMs (AI tools)** to help rewrite and debug the code.

---

## 📊 Output Files

| File | Website | Description |
|------|----------|-------------|
| `dubizzle_products.csv` | Dubizzle | Used smartphone listings scraped dynamically |
| `MobileMisr.csv` | Mobile Misr | Used smartphone listings scraped with BeautifulSoup |

---

## 🧱 Features Implemented

✅ Handles pagination  
✅ Basic error handling & retries  
✅ Logs progress with print statements  
✅ Supports two websites  
✅ CSV output for further analysis  

---
