# Facebook Group Media Link Scraper

Scrape information about posts made in Facebook groups, specifically relating to media content links from sites such as (but not limited to) YouTube, Soundcloud, and Bandcamp. The script collects the username, link title, text content, link, source of the link (if applicable, eg youtube, bandcamp etc), date posted, and the amount of reacts for each post, and outputs them to a MongoDB database.

This script was originally written to archive posts for [Great Tunes Radio](https://github.com/hankthetank27/gt-radio), and thus is limited in its scope of application to meet the needs of that project.

## Requirements

This script uses Python 3 with Selenium using the Firefox WebDriver. You will need to have Firefox installed to run.

You will also need to connect to an instance of MongoDB to dump all the data collected.

## Usage

Create a `.env` file in the `/src` directory. Here you can specify environment variables for your Facebook username, password, group URL, and MongoDB URI to output data to.

Ex.

```env
FB_USERNAME=myemail@email.com
FB_PASSWORD=mypassword
GROUP_URL=facebook.com/groups/mycrazygroup
MONGO_URL=mongodb+srv://hereismymongo
```

You can then run the following command to begin scraping.

```sh
python3 scrape_group.py
```
