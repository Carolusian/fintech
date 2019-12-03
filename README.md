# My Fintech Lab

## Caveats

### Using `reticulate` with `pyenv`

Make sure your python version is install with `env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install x.x.x`
Then, in project `.Rprofile`, add line `Sys.setenv(RETICULATE_PYTHON='YOUR VIRTUALENV PYTHON')`
