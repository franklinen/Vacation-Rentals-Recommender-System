import os, sys, traceback
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

try:
    # Location of Chrome Driver
    os.chdir(r'C:\Users\MAIN\TripAdvisor')

    # Trip Advisor Root Link for Scraping
    url_root = 'https://www.tripadvisor.ca/Search?default_scope=&singleSearchBox=&geo=153339&pid=3826&redirect=&startTime=1565651307571&uiOrigin=MASTHEAD&q=vacation%20rentals&supportedSearchTypes=find_near_stand_alone_query&enableNearPage=true&returnTo=https%253A__2F____2F__www__2E__tripadvisor__2E__ca__2F__&searchSessionId=40DC37297CF1527F8D491D54C694D91E1565651271714ssid&social_typeahead_2018_feature=true&sid=40DC37297CF1527F8D491D54C694D91E1565651519966&ssrc=v&rf=3'

    # Output File
    writer = pd.ExcelWriter(r'C:\Users\MAIN\TripAdvisor - Attempt5.xlsx', engine = 'xlsxwriter')

    # Datasets
    search_results = pd.DataFrame(columns=['Title','Bubble_Count','Review_Count','Address','Review_Block','Reviews','Page_Num'])
    pos= 0
    try:
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        if os.path.exists(os.path.join(os.getcwd(),'chromedriver.exe')):

            # Starting up Selenium
            delay = 2  # time to wait on each page load before reading the page
            chrome_options = Options()
            chrome_options.add_argument("--disable-extensions")
            driver = webdriver.Chrome(options=chrome_options)  # options are Chrome() Firefox() Safari()

            # Getting a listing of all search results
            page_count = 0
            driver.get(url_root)

            max_pages = 0
            time.sleep(delay)
            if driver.find_elements_by_class_name('pageNum'):
                pages = driver.find_elements_by_class_name('pageNum')
                max_pages= [page.text for page in pages][-1]

            while True:
                page_count = page_count + 1
                if page_count <= 9:
                    print("Visiting Search Results Page: 0{} of {}".format(page_count,max_pages))
                else:
                    print("Visiting Search Results Page: {} or {}".format(page_count,max_pages))
                time.sleep(delay)

                cards00 = driver.find_elements_by_class_name('result-card')

                for ol in cards00:
                    data = []
                    div_1 = div_2 = div_3 = div_4 = div_5 = div_6 = ''
                    # Getting Information
                    if ol.find_elements_by_class_name('result-title'):
                        div_1 = ol.find_element_by_class_name('result-title').text
                    if ol.find_elements_by_class_name('ui_bubble_rating'):
                        div_2 = ol.find_element_by_class_name('ui_bubble_rating').get_attribute('alt')
                    if ol.find_elements_by_class_name('review_count'):
                        div_3 = ol.find_element_by_class_name('review_count').text
                    if ol.find_elements_by_class_name('address'):
                        div_4 = ol.find_element_by_class_name('address').text
                    if ol.find_elements_by_class_name('review-block'):
                        div_5 = ol.find_element_by_class_name('review-block').text
                    if ol.find_elements_by_class_name('review_count'):
                        div_6 = ol.find_element_by_class_name('review_count').get_attribute('href')
                    # Adding new details to the dataframe
                    if len(div_1+div_2+div_3+div_4+div_5+div_6) != 0:
                        data.append(div_1)
                        data.append(div_2)
                        data.append(div_3)
                        data.append(div_4)
                        data.append(div_5)
                        data.append(div_6)
                        if page_count <= 9:
                            data.append("Page: 0{}".format(page_count))
                        else:
                            data.append("Page: {}".format(page_count))

                        search_results.loc[pos] = data
                        pos+=1

                # Check if Next Button is Active
                next_button = driver.find_element_by_class_name('next')
                if 'ui_button nav next primary disabled' in next_button.get_attribute('class'):
                    break;
                try:
                    next_button.click()
                except WebDriverException:
                    print("Next Button is not Clickable")

            # Clean up
            del cards00, data
            del div_1, div_2, div_3, div_4, div_5, div_6
            del max_pages, page_count, pages, pos
            del url_root

        else:
            print("Chrome Driver File Missing. No JIRA Tickets can be downloaded.")
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        print("Trackback:\n{}".format(traceback.format_exc()))
    except ValueError:
        print("Could not convert data to an integer.")
        print("Trackback:\n{}".format(traceback.format_exc()))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Trackback:\n{}".format(traceback.format_exc()))
        raise
    finally:
        if os.path.exists(os.path.join(os.getcwd(),'chromedriver.exe')):
            driver.close()
            driver.quit()

    # Datasets
    reviews_overview = pd.DataFrame(columns=['Reviews', 'Overview_n_about_the_owner', 'Amenities', 'Rates', 'Fees', 'Map_information'])
    reviews_overview_pos = 0
    try:
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        if os.path.exists(os.path.join(os.getcwd(),'chromedriver.exe')):

            # Starting up Selenium
            delay = 2  # time to wait on each page load before reading the page
            chrome_options = Options()
            chrome_options.add_argument("--disable-extensions")
            driver = webdriver.Chrome(options=chrome_options)  # options are Chrome() Firefox() Safari()

            # Getting all reviews for search results
            reviewlink_list = [x.strip() for x in list(set(search_results.Reviews.tolist())) if x.strip()]

            # Results Overview
            for idx, reviewlink in enumerate(reviewlink_list):
                if len(reviewlink_list) <= 9:
                    print("Review Link #0{} of {} : {}".format(idx+1,len(reviewlink_list),reviewlink))
                else:
                    print("Review Link #{} of {} : {}".format(idx+1,len(reviewlink_list),reviewlink))

                driver.get(reviewlink)
                time.sleep(delay)

                data01 = []
                overview_n_about_the_owner = amenities = availability = rates = fees = map_information = ''
                # Expanding Overview
                if driver.find_elements_by_class_name('vr-overview-Overview__seeMore--351YP'):
                    expand = driver.find_element_by_class_name('vr-overview-Overview__seeMore--351YP')
                    time.sleep(delay)
                    if 'More' in expand.text:
                        try:
                            expand.click()
                        except WebDriverException:
                            print("Overview Button is not Clickable")
                        time.sleep(delay)
                # Overview_n_about_the_owner
                if driver.find_elements_by_class_name('ppr_priv_vr_rental_detail_page_overview_and_amenities'):
                    overview_n_about_the_owner = driver.find_element_by_class_name('ppr_priv_vr_rental_detail_page_overview_and_amenities').text

                # Amenities
                if driver.find_elements_by_class_name('vr-amenities-Amenities__amenitiesList--1gfwW '):
                    amenities = driver.find_element_by_class_name('vr-amenities-Amenities__amenitiesList--1gfwW ').text

                # Expanding Availability
                if driver.find_elements_by_class_name('vr-rates-section-RatesSection__seeMoreLess--15zvH'):
                    expand = driver.find_element_by_class_name('vr-rates-section-RatesSection__seeMoreLess--15zvH')
                    time.sleep(delay)
                    if 'See more rates and fees' in expand.text:
                        try:
                            expand.click()
                        except WebDriverException:
                            print("Availability Button is not Clickable")
                        time.sleep(delay)

                if driver.find_elements_by_class_name('vr-rates-section-RatesSection__defaultRateContainer--3mf2p'):
                    rates = driver.find_element_by_class_name('vr-rates-section-RatesSection__defaultRateContainer--3mf2p').text

                if driver.find_elements_by_class_name('vr-rates-section-RatesSection__ratesSection--12AC4'):
                    fees = driver.find_element_by_class_name('vr-rates-section-RatesSection__ratesSection--12AC4').text

                # Expanding Map Information
                if driver.find_elements_by_class_name('vr-map-MapRelatedInformation__expandItText--2gNfL'):
                    expand = driver.find_element_by_class_name('vr-map-MapRelatedInformation__expandItText--2gNfL')
                    time.sleep(delay)
                    if 'More' in expand.text:
                        try:
                            expand.click()
                        except WebDriverException:
                            print("Map Button is not Clickable")
                        time.sleep(delay)
                # Map_information
                if driver.find_elements_by_class_name('vr-map-MapSection__content--1YhjN'):
                    map_information = driver.find_element_by_class_name('vr-map-MapSection__content--1YhjN').text

                # Adding new details to the dataframe
                if len(overview_n_about_the_owner+amenities+map_information) != 0:
                    data01.append(reviewlink)
                    data01.append(overview_n_about_the_owner)
                    data01.append(amenities)
                    data01.append(rates)
                    data01.append(fees)
                    data01.append(map_information)

                    reviews_overview.loc[reviews_overview_pos] = data01
                    reviews_overview_pos+=1

        else:
            print("Chrome Driver File Missing. No JIRA Tickets can be downloaded.")
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        print("Trackback:\n{}".format(traceback.format_exc()))
    except ValueError:
        print("Could not convert data to an integer.")
        print("Trackback:\n{}".format(traceback.format_exc()))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Trackback:\n{}".format(traceback.format_exc()))
        raise
    finally:
        if os.path.exists(os.path.join(os.getcwd(),'chromedriver.exe')):
            driver.close()
            driver.quit()

    # Datasets
    reviews_results = pd.DataFrame(columns=['Reviews', 'Review_Comments'])
    reviews_results_pos = 0
    try:
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        if os.path.exists(os.path.join(os.getcwd(),'chromedriver.exe')):

            # Starting up Selenium
            delay = 2  # time to wait on each page load before reading the page
            chrome_options = Options()
            chrome_options.add_argument("--disable-extensions")
            driver = webdriver.Chrome(options=chrome_options)  # options are Chrome() Firefox() Safari()

            # Reviews
            for idx, reviewlink in enumerate(reviewlink_list):
                if idx >= 165:
                    if len(reviewlink_list) <= 9:
                        print("Review Link Comments #0{} of {} : {}".format(idx+1,len(reviewlink_list),reviewlink))
                    else:
                        print("Review Link Comments #{} of {} : {}".format(idx+1,len(reviewlink_list),reviewlink))

                    driver.get(reviewlink)
                    time.sleep(delay)

                    #Reviews
                    if driver.find_elements_by_class_name('ppr_priv_vr_rental_detail_page_overview_and_amenities'):
                        page_count = max_review_pages = 0
                        time.sleep(delay)
                        if driver.find_elements_by_class_name('pageNum'):
                            pages = driver.find_elements_by_class_name('pageNum')
                            max_review_pages= [page.text for page in pages][-1]

                        while True:
                            time.sleep(delay)
                            # Get Reviews
                            reviews00 = driver.find_elements_by_class_name('review-container')
                            for review in reviews00:
                                # Expanding all reviews on current page
                                if review.find_elements_by_class_name('ulBlueLinks'):
                                    expand = review.find_element_by_class_name('ulBlueLinks')
                                    time.sleep(delay)
                                    if 'More' in expand.text:
                                        try:
                                            expand.click()
                                        except WebDriverException:
                                            print("Review Button is not Clickable")
                                        time.sleep(delay)
                                data02 = []
                                details = ''
                                details = review.text
                                # Adding new details to the dataframe
                                if len(details) != 0:
                                    data02.append(reviewlink)
                                    data02.append(details)
                                    reviews_results.loc[reviews_results_pos] = data02
                                    reviews_results_pos+=1
                            # to loop through review list
                            if driver.find_elements_by_class_name('next'):
                                reviews_next = driver.find_element_by_class_name('next')
                                #if 'inactive' in elm.get_attribute('class'):
                                if 'nav next ui_button primary disabled' in reviews_next.get_attribute('class'):
                                    break
                                try:
                                    reviews_next.click()
                                    time.sleep(delay)
                                except WebDriverException:
                                    print("Review Next Button is not Clickable")
                            else:
                                break
        else:
            print("Chrome Driver File Missing. No JIRA Tickets can be downloaded.")
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        print("Trackback:\n{}".format(traceback.format_exc()))
    except ValueError:
        print("Could not convert data to an integer.")
        print("Trackback:\n{}".format(traceback.format_exc()))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Trackback:\n{}".format(traceback.format_exc()))
        raise
    finally:
        if os.path.exists(os.path.join(os.getcwd(),'chromedriver.exe')):
            driver.close()
            driver.quit()
except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))
    print("Trackback:\n{}".format(traceback.format_exc()))
except ValueError:
    print("Could not convert data to an integer.")
    print("Trackback:\n{}".format(traceback.format_exc()))
except:
    print("Unexpected error:", sys.exc_info()[0])
    print("Trackback:\n{}".format(traceback.format_exc()))
    raise
finally:
    # Exporting Search Results to File
    if not search_results.empty:
        search_results.drop_duplicates(subset=['Title','Bubble_Count','Review_Count','Address','Review_Block','Reviews','Page_Num'], keep=False)
        search_results.to_excel(writer, index=False, sheet_name='Search_Results')
    # Exporting Results Overview to File
    if not reviews_overview.empty:
        reviews_overview.drop_duplicates(subset=['Reviews', 'Overview_n_about_the_owner', 'Amenities', 'Rates', 'Fees', 'Map_information'], keep=False)
        reviews_overview.to_excel(writer, index=False, sheet_name='Reviews_Overview')
    # Exporting Search Results to File
    if not reviews_results.empty:
        reviews_results.drop_duplicates(subset=['Reviews', 'Review_Comments'], keep=False)
        reviews_results.to_excel(writer, index=False, sheet_name='Reviews_Results')
    writer.save()
    writer.close()



#search_results.head()
#reviews_overview.head()
#reviews_results.head()
#search_results.to_csv('C:/Users/MAIN/Desktop/Rentals.csv', encoding='utf-8')
#reviews_results.to_csv('C:/Users/MAIN/Desktop/Reviews.csv', encoding='utf-8')
#reviews_overview.to_csv('C:/Users/MAIN/Desktop/Overview.csv', encoding='utf-8')
