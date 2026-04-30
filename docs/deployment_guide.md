# Deployment Guide: Publishing to Flippa and Other Marketplaces

This guide provides step-by-step instructions for deploying your 25 SaaS listings to Flippa and other marketplaces using the provided automation tools and bulk-import assets.

## Table of Contents

1.  [Overview](#overview)
2.  [Method 1: CSV Bulk Import](#method-1-csv-bulk-import)
3.  [Method 2: Browser Automation (Flippa)](#method-2-browser-automation-flippa)
4.  [Marketplace-Specific Instructions](#marketplace-specific-instructions)
5.  [Troubleshooting](#troubleshooting)

## Overview

You have two primary deployment options:

*   **CSV Bulk Import:** Use the `master_listings.csv` file to import listings into marketplaces that support CSV uploads. This method is faster and more reliable for bulk operations.
*   **Browser Automation:** Use the `flippa_automation.py` script to programmatically draft listings on Flippa. This method provides more control and allows for interactive verification before publishing.

## Method 1: CSV Bulk Import

### Supported Marketplaces

The following marketplaces support CSV-based bulk imports:

*   **Flippa:** Via their Super Seller or Partner program (contact Flippa directly for access).
*   **Acquire.com:** Supports structured data imports for verified sellers.
*   **Empire Flippers:** Offers CSV import for agency partners.
*   **Microacquisitions:** Supports bulk listing uploads.

### Steps to Import via CSV

1.  **Locate the Master CSV File**
    ```
    portfolio-publisher/master_listings.csv
    ```

2.  **Log in to Your Marketplace Account**
    Navigate to your account dashboard on the target marketplace.

3.  **Access the Bulk Import Tool**
    Look for an option like "Import Listings," "Bulk Upload," or "CSV Import" in your account settings or seller dashboard.

4.  **Upload the CSV File**
    Select `master_listings.csv` and follow the marketplace's import wizard. Most marketplaces will:
    - Validate the CSV structure
    - Map columns to their internal fields
    - Preview the listings before import
    - Allow you to confirm and proceed

5.  **Review and Publish**
    After import, review each listing in draft form, make any necessary adjustments, and publish.

### CSV File Structure

The `master_listings.csv` contains the following columns:

| Column | Description |
| :--- | :--- |
| ID | Unique identifier for the listing (e.g., A01) |
| Name | Name of the SaaS product |
| Tagline | One-line description of the product |
| Overview | Detailed overview of the product |
| Category | Product category (e.g., "Productivity / Workflow") |
| Tech stack | Technologies used (e.g., "Next.js, Node, Postgres") |
| Monetization | Pricing model (e.g., "SaaS — $39 / $99 / $249") |
| Key Metrics | Current metrics (e.g., "Pre-revenue, early access users") |
| Highlights | Key features (newline-separated) |
| Operations | Time required for operations (e.g., "1–2 hrs/week") |
| Reason for Sale | Reason for selling the asset |
| Included | What's included in the sale |

## Method 2: Browser Automation (Flippa)

### Prerequisites

1.  **Python 3.7+** installed on your system
2.  **Selenium library:** Install via `pip install selenium`
3.  **ChromeDriver:** Download from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/) and ensure it's in your system PATH or specify its path in the script
4.  **Active Flippa Account:** You must be logged into Flippa before running the script

### Installation

1.  **Install Selenium:**
    ```bash
    pip install selenium
    ```

2.  **Download ChromeDriver:**
    - Visit [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)
    - Download the version matching your Chrome browser version
    - Extract and place in a known location (e.g., `/usr/local/bin/chromedriver` on macOS/Linux or `C:\chromedriver.exe` on Windows)

### Running the Automation Script

1.  **Navigate to the Script Location:**
    ```bash
    cd /path/to/flippa_automation.py
    ```

2.  **Run the Script:**
    ```bash
    python3 flippa_automation.py
    ```

    Or, if you need to specify the ChromeDriver path:
    ```bash
    python3 -c "
    from flippa_automation import FlippaAutomation
    automation = FlippaAutomation(chromedriver_path='/path/to/chromedriver', headless=False)
    automation.run('/home/ubuntu/raw_listings.json', save_only=True)
    "
    ```

3.  **Monitor the Process:**
    The script will:
    - Open a Chrome browser window
    - Navigate to Flippa
    - Verify you are logged in
    - Create and fill out a form for each listing
    - Save each listing as a draft (or publish, if `save_only=False`)

4.  **Review Drafts:**
    After the script completes, log into Flippa and review all saved drafts. You can make manual adjustments before publishing.

### Script Options

The `FlippaAutomation` class supports the following options:

*   `chromedriver_path`: Path to the ChromeDriver executable (default: "chromedriver")
*   `headless`: Run the browser in headless mode (no visual window) (default: False)
*   `save_only`: Save listings as drafts instead of publishing (default: True)

### Example: Running in Headless Mode

```python
from flippa_automation import FlippaAutomation

automation = FlippaAutomation(headless=True)
automation.run('/home/ubuntu/raw_listings.json', save_only=True)
```

## Marketplace-Specific Instructions

### Flippa

**CSV Import (Super Seller / Partner Program):**
1.  Contact Flippa sales at [sales@flippa.com](mailto:sales@flippa.com) to inquire about bulk import access.
2.  Once approved, you'll receive instructions for uploading your CSV file.
3.  Follow the CSV Bulk Import section above.

**Browser Automation:**
1.  Use the `flippa_automation.py` script as described in Method 2.
2.  Ensure you are logged into Flippa before running the script.

### Acquire.com

**CSV Import:**
1.  Log into your Acquire.com seller account.
2.  Navigate to "My Listings" > "Bulk Upload."
3.  Download the template CSV from Acquire.com.
4.  Map your `master_listings.csv` columns to Acquire.com's template.
5.  Upload and review.

### Empire Flippers

**CSV Import (Agency Partners):**
1.  Contact Empire Flippers to confirm your agency partner status.
2.  Request access to their bulk upload tool.
3.  Follow their specific CSV format requirements (may differ from the standard format).

## Troubleshooting

### Issue: ChromeDriver Not Found

**Solution:**
- Ensure ChromeDriver is in your system PATH, or specify the full path when initializing `FlippaAutomation`:
  ```python
  automation = FlippaAutomation(chromedriver_path='/full/path/to/chromedriver')
  ```

### Issue: "User Not Logged In" Warning

**Solution:**
- The script will pause and wait for you to manually log into Flippa.
- Log in using your Flippa credentials, then press Enter in the terminal to continue.

### Issue: Form Fields Not Found

**Solution:**
- Flippa's website structure may have changed. Update the CSS selectors in `flippa_automation.py` to match the current form structure.
- Inspect the Flippa website using browser developer tools (F12) to identify the correct element IDs or class names.

### Issue: CSV Import Fails

**Solution:**
- Verify that the CSV file is properly formatted (UTF-8 encoding, correct delimiters).
- Check that all required fields are populated.
- Contact the marketplace's support team for specific error messages.

### Issue: Rate Limiting or Blocking

**Solution:**
- Add delays between requests in the automation script by increasing the `time.sleep()` values.
- Consider running the script during off-peak hours.
- If blocked, wait 24 hours before retrying.

## Best Practices

1.  **Test with a Single Listing First:** Before running the full automation, test with one listing to ensure everything works correctly.
2.  **Review Before Publishing:** Always review listings as drafts before publishing to catch any formatting or data issues.
3.  **Keep Backups:** Maintain a backup of your `master_listings.csv` and original JSON files.
4.  **Monitor Performance:** After publishing, monitor listing performance and engagement metrics on each platform.
5.  **Update Regularly:** Keep your listing data current by regularly updating the JSON files and re-importing as needed.

---

*Generated by Manus AI*
