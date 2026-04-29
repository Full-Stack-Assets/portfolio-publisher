"""
Advanced Flippa Browser Automation Script with Logging and Error Handling
This script provides a robust, production-ready automation solution for drafting SaaS listings on Flippa.
"""

import json
import time
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'flippa_automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FlippaAdvancedAutomation:
    """Advanced Flippa automation with comprehensive error handling and logging."""
    
    def __init__(self, chromedriver_path: Optional[str] = None, headless: bool = False, 
                 timeout: int = 15, delay_between_listings: int = 5):
        """
        Initialize the advanced Flippa automation.
        
        Args:
            chromedriver_path: Path to ChromeDriver executable
            headless: Run browser in headless mode
            timeout: WebDriverWait timeout in seconds
            delay_between_listings: Delay between processing listings in seconds
        """
        self.chromedriver_path = chromedriver_path or "chromedriver"
        self.headless = headless
        self.timeout = timeout
        self.delay_between_listings = delay_between_listings
        self.driver = None
        self.wait = None
        self.processed_count = 0
        self.failed_count = 0
        self.success_count = 0

    def start_browser(self) -> bool:
        """Start the Chrome browser with appropriate options."""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            self.driver = webdriver.Chrome(self.chromedriver_path, options=chrome_options)
            self.wait = WebDriverWait(self.driver, self.timeout)
            logger.info("Browser started successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            return False

    def navigate_to_flippa(self) -> bool:
        """Navigate to Flippa and verify login status."""
        try:
            self.driver.get("https://flippa.com")
            logger.info("Navigated to Flippa homepage.")
            time.sleep(3)
            
            # Check for login indicator
            try:
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "user-profile")))
                logger.info("User is logged in.")
                return True
            except TimeoutException:
                logger.warning("Could not verify login status. Please ensure you are logged in.")
                input("Press Enter after logging in...")
                return True
        except Exception as e:
            logger.error(f"Failed to navigate to Flippa: {e}")
            return False

    def navigate_to_create_listing(self) -> bool:
        """Navigate to the create new listing page."""
        try:
            self.driver.get("https://flippa.com/listings/new")
            logger.info("Navigated to create new listing page.")
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to create listing page: {e}")
            return False

    def fill_listing_form(self, listing_data: Dict) -> bool:
        """
        Fill in the Flippa listing form with provided data.
        
        Args:
            listing_data: Dictionary containing listing information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Fill title
            title_field = self.wait.until(EC.presence_of_element_located((By.ID, "listing-title")))
            title_field.clear()
            title_field.send_keys(f"{listing_data['id']} — {listing_data['name']}")
            logger.info(f"Filled title: {listing_data['name']}")

            # Fill description
            description_field = self.driver.find_element(By.ID, "listing-description")
            description_field.clear()
            description_field.send_keys(listing_data['overview'])
            logger.info("Filled description.")

            # Select category
            try:
                category_select = Select(self.driver.find_element(By.ID, "listing-category"))
                category_select.select_by_visible_text(listing_data['category'])
                logger.info(f"Selected category: {listing_data['category']}")
            except (NoSuchElementException, StaleElementReferenceException):
                logger.warning(f"Could not select category. Continuing...")

            # Fill additional fields if available
            optional_fields = {
                'listing-tech-stack': listing_data.get('tech_stack', ''),
                'listing-monetization': listing_data.get('monetization', ''),
                'listing-metrics': listing_data.get('metrics', ''),
                'listing-operations': listing_data.get('operations', ''),
                'listing-reason-for-sale': listing_data.get('reason_for_sale', ''),
                'listing-included': listing_data.get('included', '')
            }

            for field_id, field_value in optional_fields.items():
                try:
                    field = self.driver.find_element(By.ID, field_id)
                    field.clear()
                    field.send_keys(field_value)
                    logger.debug(f"Filled field: {field_id}")
                except NoSuchElementException:
                    logger.debug(f"Field {field_id} not found. Skipping.")

            logger.info("Form filled successfully.")
            return True
        except Exception as e:
            logger.error(f"Error filling form: {e}")
            return False

    def save_draft(self) -> bool:
        """Save the listing as a draft."""
        try:
            save_button = self.wait.until(EC.element_to_be_clickable((By.ID, "save-draft-button")))
            save_button.click()
            logger.info("Draft saved successfully.")
            time.sleep(2)
            return True
        except TimeoutException:
            logger.error("Save draft button not found or not clickable.")
            return False
        except Exception as e:
            logger.error(f"Error saving draft: {e}")
            return False

    def publish_listing(self) -> bool:
        """Publish the listing."""
        try:
            publish_button = self.wait.until(EC.element_to_be_clickable((By.ID, "publish-button")))
            publish_button.click()
            logger.info("Listing published successfully.")
            time.sleep(2)
            return True
        except TimeoutException:
            logger.error("Publish button not found or not clickable.")
            return False
        except Exception as e:
            logger.error(f"Error publishing listing: {e}")
            return False

    def process_listings(self, listings_data: List[Dict], save_only: bool = True) -> None:
        """
        Process multiple listings with comprehensive error handling.
        
        Args:
            listings_data: List of listing dictionaries
            save_only: If True, save as drafts; if False, publish
        """
        for i, listing in enumerate(listings_data, 1):
            self.processed_count = i
            logger.info(f"\n--- Processing listing {i}/{len(listings_data)}: {listing['name']} ---")
            
            try:
                if not self.navigate_to_create_listing():
                    logger.error(f"Failed to navigate to create listing page for {listing['name']}")
                    self.failed_count += 1
                    continue

                if not self.fill_listing_form(listing):
                    logger.error(f"Failed to fill form for {listing['name']}")
                    self.failed_count += 1
                    continue

                if save_only:
                    if self.save_draft():
                        self.success_count += 1
                    else:
                        self.failed_count += 1
                else:
                    if self.publish_listing():
                        self.success_count += 1
                    else:
                        self.failed_count += 1

                # Add delay between listings
                if i < len(listings_data):
                    logger.info(f"Waiting {self.delay_between_listings} seconds before next listing...")
                    time.sleep(self.delay_between_listings)

            except Exception as e:
                logger.error(f"Unexpected error processing {listing['name']}: {e}")
                self.failed_count += 1

    def close_browser(self) -> None:
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed.")

    def print_summary(self) -> None:
        """Print a summary of the automation run."""
        logger.info("\n" + "="*50)
        logger.info("AUTOMATION SUMMARY")
        logger.info("="*50)
        logger.info(f"Total Processed: {self.processed_count}")
        logger.info(f"Successful: {self.success_count}")
        logger.info(f"Failed: {self.failed_count}")
        logger.info("="*50)

    def run(self, listings_json_path: str, save_only: bool = True) -> None:
        """
        Main execution method.
        
        Args:
            listings_json_path: Path to JSON file containing listing data
            save_only: If True, save as drafts; if False, publish
        """
        try:
            # Load listings data
            logger.info(f"Loading listings from {listings_json_path}...")
            with open(listings_json_path, 'r') as f:
                listings_data = json.load(f)
            logger.info(f"Loaded {len(listings_data)} listings.")

            # Start browser
            if not self.start_browser():
                logger.error("Failed to start browser. Exiting.")
                return

            # Navigate to Flippa
            if not self.navigate_to_flippa():
                logger.error("Failed to navigate to Flippa. Exiting.")
                self.close_browser()
                return

            # Process listings
            self.process_listings(listings_data, save_only=save_only)

            # Print summary
            self.print_summary()

        except FileNotFoundError:
            logger.error(f"Listings file not found: {listings_json_path}")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in listings file: {listings_json_path}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        finally:
            self.close_browser()


if __name__ == "__main__":
    # Example usage
    automation = FlippaAdvancedAutomation(headless=False, timeout=15, delay_between_listings=5)
    automation.run('/home/ubuntu/raw_listings.json', save_only=True)
