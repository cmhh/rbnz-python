# Fetch Time Series Data from RBNZ Website

**NOTE**: I previously created a [repository](https://github.com/cmhh/rbnz) which included a Scala program that largely did the same thing as this repo, and also included a little data service that could be used to serve the result.  For various reasons, I needed to do something very similar using Python, so thought I'd post the code.  I do not particularly like Python, am not particularly adept at it, and I doubt this code will present as very _Pythonistic_.  But I appreciate that anybody looking at this will likely prefer Python code over Scala code, so here it is...

**Note** it is against the Reserve Bank's [terms of use](https://www.rbnz.govt.nz/about-our-site/terms-of-use) to use an automated agent without permission.

This repo includes a simple Python script which can be used to fetch all Excel files listed on the [Statistical series data files page](https://www.rbnz.govt.nz/statistics/series/data-file-index-page), compile the data, and save to a SQLite database.  Simply run something like:

```bash
python scrape.py rbnz.db
```

Excel files will successfully import if they:

* have a tab named `Data`
* have a tab named `Series Definitions`
* data in `Data` tab must start in row 6, with series IDs in row 5
* `Series Definitions` tab must have 5 columns with header row.

Note that there is a single series which has a non-numeric value, `EXRT.YS45.ZZB17`, which is date-valued.  Rather than create a database schema that can handle multiple types, I just dropped this one series.  **There are a few spreadsheets which _should_ have imported correctly but didn't, and I'll track them down and fix the issue shortly.**  


## Selenium / Chrome / Chromedriver

The program uses Selenium webdriver, and assumes Chrome and [chromedriver](https://chromedriver.chromium.org/) are available, and working correctly.  One easy way to ensure this is the case is to use Docker, and a sufficient `Dockerfile` is provided.

Another relatively easy option, if you're using Chrome locally (if you're using Firefox, say, you'll need to edit `browser.py`), is to create a virtual environment and then put a copy of chromedriver in the `bin` or `Scripts` folder of your virtual environment.  For example, something like:

```bash
python3 -m venv venv
cd venv/bin
wget https://chromedriver.storage.googleapis.com/104.0.5112.79/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
rm chromedriver_linux64.zip
```


## Using the Scripts with Docker

Users first need to build the docker image:

```bash
docker build -t rbnz:python .
```

To create a database:

```bash
docker run --rm \
  -v $PWD/data:/data \
  -u $(id -u):$(id -g) \
  rbnz:python \
  /data/rbnz.db
```

The end result will look something like this:

![](img/defs.png)

![](img/series.png)
