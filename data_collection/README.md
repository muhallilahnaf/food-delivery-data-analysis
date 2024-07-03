**Navigation:**

[1. Data collection (scraping)]()\
[2. Data preprocessing](../data_preprocessing)\
[3. Data integration](../data_integration)\
[4. Data analysis](../data_analysis)

## 1. Data Collection (scraping)

To collect data from the food delivery app, we use the web version of the platform to search all restaurants for a given city and location (latitude, longitude). Then, we call the API for each restaurant to get the desired data.

The following scripts are used for data collection process:

0. `.env`

Create a `.env` file in the root directory with the following template:

```
CSS_SELECTOR=< css selector for each restaurant node in web page >
URL=< url of food delivery app web version containing restaurant list for given city, location >
API_RESTAURANT=< api url of restaurant data for each restaurant code >
```

Contact me for the `.env` file.

1. `fetch_restaurant_list.py`

This script uses Selenium to open a web browser, load the web version of the food delivery app and search restaurants for a given city and location (latitude, longitude).

Since the list of restaurants is loaded dynamically, we scroll programmatically (with a given number of retries) until all restaurants are loaded.

Then we store the restaurant name and restaurant code (which will be used for the API calls later) in a JSON file (`restaurant_list.json`) inside the `data` folder.

2. `fetch_restaurant_data.py`

This script calls the API for each restaurant (using the restaurant code) and stores the JSON response data in a JSON file (`restaurant_data.json`) inside the `data` folder .

**NB:**
- *All the scripts are written such that we can re-run the scripts to continue the process, should any error occur or we run out of retries while scraping. At each step, data is not overwritten, rather missing data is added and differences are shown in console.*
- *After performing data preprocessing once, we know which columns/values we want to keep. So we can simplify the process for future by calling the API and only save the required key-values instead of saving all of them and then filtering.*
