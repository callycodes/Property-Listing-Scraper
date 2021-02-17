
Hey, thanks for checking out my repo.

What you see here is an EXTREMELY tempermental attempt at me scraping information from the Rightmove website. This script is largely based on using css selectors and element selectors, so every couple of months it may break as Rightmove update their site.

It's pretty simple, but was very tedious. The application uses Flask, so it creates a local server you can query at the following url:

http://localhost:5000/rightmove?url=[rightmoveurlhere]

The application scrapes and returns the following information in JSON format:
{
  "added": "",
  "address": "",
  "features": [],
  "letting_info": { 
    "deposit": "",
    "furnish_type": "",
    "let_available": "",
    "let_type": "" },
  "photo": "",
  "photo_count": ,
  "price_per_month":"",
  "price_per_week": "",
  "property_info": {
    "bathrooms": "",
    "bedrooms": "",
    "property_type": "" },
  "realtor": {
    "name": "",
    "telephone": "" },
  "stations": [
    { "distance": "",
      "name": "",
      "type": "" }
  ],
  "url": ""
}

Pretty nifty huh.

I was inspired by Mike over at Simplescraper, his site offered a really simple way, using an extension to select elements on a page, and instantly created an API I could query to scrape my specified elements. However, as this is contributing towards my final year project, I thought it's best I knock my own up from scratch. Plus, this can do a couple of things Mike's wouldn't have been capable of!

To run the application, make sure you have Python3 installed. Simply run:

python3 main.py

You may have to install some packages but you can find all of these package names within the script.

Use this properly, I am not responsible for any misuse of the script and it is purely an educational data scraper which I need for my university project.

Thanks!
