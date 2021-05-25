# A-Recommender-system-for-vacation-Rentals-Using-Natural-Language-Processing-and-Deep-Learning
The project is carried out to build a Recommender system for Vacation Rentals in Canada. We use Natural Language processing, and Prediction algorithms model Vacation Reviews and ratings 
for building the Recommender system. Data was obtained by scraping the website www.tripadvisor.ca with the keyword 'Vacation Rentals'.

The website was chosen because it has been ranked as one of the most popular website for vacation bookings. Though the data was dependent on date, we believe that it is a general 
representation of the vacaton rental available in the country. the scraping was performed with selenium in a python 3 environment. After the scraping, data cleaning was carried out
in python to get the needed variables. Exploratory Data Analysis as Explained in the EDA section focused mainly on exploring the relationshp with the variables and the frequency of
data occurence. There was no need to apply feature engineering to the dataset. however, Excel was used to seperate the location of the city and province.

Natural Language Processing was performed on the reviews variable.  
After preprocessing, classical models and deep learning model was applied on the dataset to give modelling scores. 
The recommender system was built using Content-based Recommender system after processing the data with TFID(Term Frequency Vectorizer)

### Requirements for webscraping
* import selenium
* import webdriver
* import options
* import WebdriverException
* Enter Search Term *Vacation Rentals* on website Tripadvisor.ca
* Scrape search result based on specified parameters.
* Recommendation: Run the webscraper on a GPU or a distributed system for faster result

### Requirements for Web Application
* Install Streamlit and components
* Wrap recommender model in a streamlit application and run application
* Ensure the dataset is in the same envrionment as the web app 

### Requirements For App Deployment #####
* **Dockerfile**
* **app.yaml : configuration**
* **Gcloud sdk**

Commands
* List Projects
	* **gcloud projects list**
* To change to the project you created you can use
	* **gcloud config set project your project_name**
* To check for the current project you use
	* **gcloud config get-value project**
* To deploy our app we will be using
	* **gcloud app deploy**

By
Frankline Ononiwu

