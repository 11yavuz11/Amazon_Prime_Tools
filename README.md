# 🚀 Amazon Prime Inventory Software 🛒

## Project Overview

This Python project is designed to scrape the prices and shipping fees of products listed by Amazon sellers on non-Prime buyer accounts. 
Amazon often offers free shipping on Prime accounts to encourage more customers to use Prime, 
while non-Prime accounts may have additional shipping costs. 
This software helps gather price and shipping fee data from various marketplaces and stores it in an Excel sheet.

## Getting Started

To get started with the project, follow these steps:

1. Install the required Python libraries using the `requirements.txt` file. Run the following command:

   pip3 install -r requirements.txt


## Use


1. Download the Chrome WebDriver compatible with your computer from this link and place it in the project's main directory.

Link: https://chromedriver.chromium.org/downloads

Note: There is currently a version for Mac, but if you are using Windows or Linux, you may need to download the appropriate version.

2. Update the MAC address in the main.py file. Replace it with your current MAC address; otherwise, the program will not work.

3. Add your products to your inventory, ensuring that SKUs (Stock Keeping Units) start with the following SKU prefixes:

Amazon UK = UK
Amazon US = US
Amazon UAE = UAE
For example, you can use SKU prefixes like "UK1" or "UK2."


4. Add SKUs and ASINs to the inventory.xlsx file. Do not modify the headers.
5. Extract the chromedriver file in the project directory.

6. Open a terminal or command prompt and start the program by running the following command:

python3 main.py

7. The program will prompt you to choose a marketplace. Make your selection (currently supporting Amazon.ae and Amazon.sa).

8. Depending on your internet speed, the data scraping time may vary.

9. Once completed, you will receive an output file and an error file. Use these files to update your inventory.

