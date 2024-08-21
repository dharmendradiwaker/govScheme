import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests


url = 'https://www.myscheme.gov.in/search'


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        # Configure webdriver options with the desired user agent
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={user_agent}')
service = Service(ChromeDriverManager().install())
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-gpu')  # Necessary if running on Windows
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)



# state_name= WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@id="react-select-36-input"]')))
# state_name.click()
# state_name.send_keys("uttar pradesh")
# state_name.send_keys(Keys.RETURN)


search_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[4]/div[2]/form/input')))
search_field.send_keys("Farmer")


# Wait for the next button to be clickable and click it
next_button = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/main/div[4]/div[2]/form/button[2]")))
next_button.click()

WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[4]/div[2]/div[5]')))



## Function to scrap all data of a scheme
def parse_webpage(url):
    # Send a GET request to the URL
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the full body element
    full_body = soup.find('div', class_='col-span-5 md:col-span-3')

    # Extract state, title, and tags
    state = full_body.find('h2').text.strip()
    title = full_body.find('h1').text.strip()

    tags_container = full_body.find('div', class_='mb-2 md:mb-0 w-full')
    tags_elements = tags_container.find_all('div', class_='cursor-pointer')  # Select all tag divs

    # Collect the text of each tag into a list
    tags = [tag.text.strip() for tag in tags_elements]

    # Initialize the dictionary
    result_dict = {
        'title': title,
        'state': state,
        'tags': tags,
        'head': {}
    }

    # Extract content sections
    content_sections = full_body.find_all('div', class_='pt-10')

    for content in content_sections[:-3]:
        try:
            # Find the header name
            head_name_element = content.find('a', class_='flex flex-row items-center gap-2')
            head_name = head_name_element.text.strip() if head_name_element else 'Unknown'

            # Find the content associated with the header
            head_content_element = content.find('div', class_='grid grid-cols-1 md:flex flex-wrap gap-4 justify-between items-center !items-start w-full mt-6 bg-white dark:bg-dark rounded-2xl !gap-8')
            head_content = head_content_element.text.strip() if head_content_element else 'No content available'

            # Add the header and content to the dictionary
            result_dict['head'][head_name] = head_content

        except Exception as e:
            print(f"Error: {e}")
            continue

    return result_dict


# print(parse_webpage('https://www.myscheme.gov.in/schemes/pmsby'))

## Function to scrap all url from home page and pass all scheme url to get data
def navigate_and_extract_links(driver):
    visited_pages = set()
    current_page = 1
    all_data = []
    
    while True:
        try:
            print(f"Processing page {current_page}...")
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find the full container using BeautifulSoup
            full_containers = soup.find_all('div', class_='mt-2')
            if not full_containers:
                print("Full container not found")
            else:
                full = full_containers[1] if len(full_containers) > 1 else full_containers[0]
                

                # Find all articles
                articles = full.find_all('div', class_='flex flex-col') if full else []
                # Extract and print links
                for article in articles:
                    link_element = article.find('a')
                    if link_element and 'href' in link_element.attrs:
                        link = link_element['href']
                        full_link = 'https://www.myscheme.gov.in'+ link
                        print(full_link)
                        data  = parse_webpage(full_link)

                        # print(data)

                        all_data.append(data)

                    else:
                        print("No link found in article")
            
            # Mark current page as visited
            visited_pages.add(current_page)
            
            # Wait for pagination to be visible
            pagination = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "list-none") and contains(@class, "flex") and contains(@class, "items-center") and contains(@class, "justify-center")]'))
            )
            
            page_buttons = pagination.find_elements(By.XPATH, './/li')
            next_page_found = False
            
            for page_button in page_buttons:
                page_number_text = page_button.text.strip()
                if page_number_text.isdigit():
                    page_number = int(page_number_text)
                    
                    if page_number not in visited_pages:
                        # Locate the page number link and click
                        page_button_element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{page_number}')]"))
                        )
                        
                        # Click the element using JavaScript
                        driver.execute_script("arguments[0].click();", page_button_element)
                        
                        print(f"Navigated to page {page_number}")
                        current_page = page_number
                        next_page_found = True
                        
                        # Wait for the page to load
                        time.sleep(3)  # Adjust wait time as needed
                        break

            if not next_page_found:
                print("No more pages to navigate.")
                break

        except Exception as e:
            print(f"Error navigating to the next page: {e}")
            break

    print(f"Data collected from all pages: {all_data}")
    return all_data


# navigate_and_extract_links(driver)
# time.sleep(5)



## Trying to create a function for filter 
from selenium.webdriver.support.ui import Select

# def extract_data_for_state(driver):
#     state_name = input(str("Enter state Name: "))
#     try:
#         # Locate the filter dropdown container
#         filter_container = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//div[@class="facet__indicator facet__dropdown-indicator css-tlfecz-indicatorContainer"]'))  # Update with the correct XPath
#         )
        
#         # Click to open the dropdown
#         filter_container.click()

        
#         # Wait for the page to update based on the selected state
#         time.sleep(3)  # Adjust sleep time if necessary

#     except Exception as e:
#         print(f"An error occurred while selecting the state: {e}")



# print(extract_data_for_state(driver))








# Print the consolidated dictionary

# faq_sections = driver.find_elements(By.XPATH, '//div[@class="py-4 first:pt-0 last:pb-0 undefined"]')

# for section in faq_sections:
#     try:
#         # Find the question and print it
#         question = section.find_element(By.XPATH, './/div[@class="cursor-pointer undefined"]')
#         print("Question:", question.text)
#         # Wait for the answer container to change from 'hidden' to 'blocked'
#         WebDriverWait(section, 10).until(
#             EC.presence_of_element_located((By.XPATH, './/div[contains(@class, "rounded-b  dark:text-gray-300 mt-3 block  ")]'))
#         )
        
#         # Wait for the answer to become visible
#         answer_container = WebDriverWait(section, 10).until(
#             EC.visibility_of_element_located((By.XPATH, './/div[contains(@class, "rounded-b  dark:text-gray-300 mt-3 block  ")]'))
#         )
        
#         # Find the answer
#         answer = answer_container.find_element(By.XPATH, './/p[@class="text-base leading-relaxed"]')
#         print("Answer:", answer.text)
#         print("-" * 50)  # Separator for better readability
        
#     except Exception as e:
#         print(f"An error occurred: {e}")

# url = 'https://www.myscheme.gov.in/schemes/pmsby'
# response = requests.get(url)
# html_content = response.text
# soup = BeautifulSoup(html_content, 'html.parser')
    
# # Find all FAQ sections
# faq_sections = soup.find_all('div', class_='py-4 first:pt-0 last:pb-0 undefined')

# for section in faq_sections:
#     try:
#         # Find the question
#         question_div = section.find('div', class_='cursor-pointer undefined')
#         if question_div:
#             question = question_div.get_text(strip=True)
#             print("Question:", question)
#         else:
#             print("Question not found")
        
#         # Find the answer container
#         answer_container = section.find('div', class_='rounded-b  dark:text-gray-300 mt-3 hidden ')
#         if answer_container:
#             # Find the answer
#             answer_p = answer_container.find('p', class_='text-base leading-relaxed')
#             if answer_p:
#                 answer = answer_p.get_text(strip=True)
#                 print("Answer:", answer)
#             else:
#                 print("Answer not found")
#         else:
#             print("Answer container not found")
            
#         print("-" * 50)  # Separator for better readability
    
#     except Exception as e:
#         print(f"An error occurred: {e}")

# time.sleep(5)