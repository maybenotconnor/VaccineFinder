# Vinny's Vaccine Finder

Scrapes data from https://vaxfinder.mass.gov and texts you the results.

## Get the code

Use Github desktop or the command line:
```
git clone https://github.com/gdancik/VaccineFinder.git
```
## Switch to the VaccineFinder directory

From the command line:
```
cd VaccineFinder
```
## Configure the webscraper

- Set the zip code in `vaccinescraper.py`
- Set your e-mail and recipients in `credentials.py` (gmail address is required)
  - Use a python list to specify multiple recipients
- Set locations to skip in `ignore.txt`.  

## Run the code
```
python vaccinescraper.py
```

