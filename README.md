# My Fintech Lab

## Get HSI components

* `cd aastocks`
* `scrapy crawl hsi`

## Get Hong Kong stock industry code and categories

* `cd aastocks`
* `scrapy crawl industry`

## Caveats

### Using `reticulate` with `pyenv`

Make sure your python version is install with `env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install x.x.x`
Then, in project `.Rprofile`, add line `Sys.setenv(RETICULATE_PYTHON='YOUR VIRTUALENV PYTHON')`

