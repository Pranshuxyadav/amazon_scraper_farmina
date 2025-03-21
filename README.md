# amazon_scraper_farmina
web scraper for Farmina products
................................................................................................................
# Amazon Product Scraper

## Description
This Python script scrapes product details from Amazon using ASINs (Amazon Standard Identification Numbers). It extracts information such as product title, sale price, MRP, and seller details, and saves the data to an Excel file.

## Features
- Fetches product details from Amazon using ASINs.
- Extracts product title, sale price, MRP, and seller information.
- Saves scraped data to an Excel file with a timestamp.
- Reads ASINs from a text file for bulk processing.
- Implements random delays between requests to reduce detection risk.

## Requirements
- Python 3.x
- Required libraries:
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `openpyxl`

Install dependencies using:
```sh
pip install requests beautifulsoup4 pandas openpyxl
```

## Usage
1. Prepare a text file containing ASINs, with each ASIN on a new line.
2. Update the script with the correct path to the ASIN text file.
3. Run the script:
```sh
python inputfile_scraper.py
```

## File Structure
```
📂 project-directory
 ├── inputfile_scraper.py  # Main scraper script
 ├── asins.txt             # ASINs list file (update this with your ASINs)
 ├── results/              # Folder where scraped data is saved
```

## Output
The script saves the extracted product details to an Excel file with a timestamped filename.

## Notes
- Ensure you have a stable internet connection while running the script.
- Amazon may block frequent requests; consider using proxies if needed.
- If you encounter permission errors while saving, ensure the Excel file is not open.

## License
This project is licensed under the MIT License.

## Author
[Pranshu Yadav](https://github.com/pranshuxyadav)

