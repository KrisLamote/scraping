# Wine data

This project is based on an Upwork job posting. This solution was not part of any proposal, just
an exercise based on the actual requirements. The data needs to be scraped from https://bordeauxindex.com.

https://www.upwork.com/jobs/~0188274771ab983871

Original Job Requirements:
    - The script should extract the following columns: Vintage, Wine Name, Wine Details,
      Case Description, Last Trade per Case, Sell Qty, Bid per Case, Spread, Offer per Case, Buy Qty
    - Save the data in a CSV format
    - You don't have to run the script all the way and collect the data. I can do that.

## QAD

Just a quick & dirtly solution; gets the data from the first page

## WINES

Full solution (gets all data), but requires you to obtain the required cookies first:
    - visit & 'inspect' the page
    - in the application tab, you can see the cookies (you'll need key=value; key2=value2; etc)
    - alternatively (better), use the network tab, seclect the nextpage request and copy as cUrl
      this will have a cookies header, which is exactly what you need
