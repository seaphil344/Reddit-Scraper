import time
import csv
import sys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def scrape_comments(url, output_file):
    firefox_options = Options()
    #firefox_options.add_argument("-headless")

    driver_service = FirefoxService()
    driver = webdriver.Firefox(service=driver_service, options=firefox_options)

    driver.get(url)

    print("Scraping comments...")

    try:
        div_contents = []
        
        while True:
            try:
                scroll_to_bottom(driver)
                show_more_button = driver.find_element(By.CSS_SELECTOR, "button.button-small.button-brand.inline-flex.items-center.justify-center")
                show_more_button.click()
                time.sleep(2)
            except NoSuchElementException:
                # No more "show more" button, exit the loop
                break

        comment_elements = driver.find_elements(By.CSS_SELECTOR, "shreddit-comment div.py-0.xs\\:ml-xs.inline-block.max-w-full")
        for comment_element in comment_elements:
            p_elements = comment_element.find_elements(By.CSS_SELECTOR, "p")
            p_texts = [p_element.text for p_element in p_elements]
            comment_text = "\n".join(p_texts)
            div_contents.append(comment_text)
            print(f"Scraped comment: {comment_text}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        output_file_csv = output_file + ".csv"
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Comment Text'])
            for comment_text in div_contents:
                writer.writerow([comment_text])

        print(f"Data saved to {output_filename}.csv")
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <URL> <output_file>")
        sys.exit(1)

    url = sys.argv[1]
    output_filename = sys.argv[2]
    scrape_comments(url, output_filename)
