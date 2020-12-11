# web-scraping-challenge
This assignment utilizes pandas, beautifulsoup, splinter & chrome driver to scrape data off various websites provided in the instructions. The data is dynimcally found using splinter, navigated using chrome driving and imported using beautiful soup. Pandas is used to convert a table found on one of the sites and re-imported as a html table.

The full script is placed in a function called scrape which is initialized when opening the application as well as trigged when clicking a button. It brings in the latest article and body text, a featured image, the table & several images of the Martian hemisphere. 

The displayed data is presented in a html web page that utilizes bootstrap to quickly and neatly organize a simple template.

Occasionally an error is thrown when running the app.py but when refreshed in the web browser or run again, it is functional.
