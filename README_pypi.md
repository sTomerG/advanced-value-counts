<h1>Welcome to advanced-value-counts</h1>

advanced-value-counts is a Python-package containing the `AdvancedValueCounts` class that makes use of pandas' [`.value_counts()`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html), [`.groupby()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) and [seaborn](https://seaborn.pydata.org/) to easily get a lot of info about the counts of a (categorical) column in a pandas DataFrame. The potential of this package is at its peak when wanting info of counts of a column after a grouping: `df.groupby(groupby_col)[column].value_counts()`. Click [here](https://github.com/sTomerG/advanced-value-counts#usage) to read how to use `AdvancedValueCounts`. Read [this medium article](https://medium.com/@tomergabay/advancedvaluecounts-for-eda-2f80e2c74ce1) or consult [this notebook](https://github.com/sTomerG/advanced-value-counts/blob/main/notebooks/medium_notebook.ipynb) for an explanation on the added value of this package.



[**Git repository**](https://github.com/sTomerG/advanced-value-counts). <br><br>
**Table of contents**:
- [Installation for users using PyPi](#installation-for-users-using-pypi)
- [Installation for users without PyPi](#installation-for-users-without-pypi)
- [Usage](#usage)
- [Installation for contributors](#installation-for-contributors)

# Installation for users using PyPi

    pip install advanced-value-counts

If errors surface please upgrade pip and setuptools

    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade setuptools

# Installation for users without PyPi

    git clone https://github.com/sTomerG/advanced-value-counts.git
    cd advanced-value-counts
    pip install -e .
    # optional but potentially crucial
    pip install -r requirements/requirements.txt

To test whether the installation was succesfull run in the advanced-value-counts directory (*DeprecationWarnings* are expected)

    pytest
    

# Usage

Please consult [here](https://github.com/sTomerG/advanced-value-counts#usage).

# Installation for contributors

    git clone https://github.com/sTomerG/advanced-value-counts.git
    cd advanced-value-counts
    python3 -m venv .venv

**Activate the virtual environment** 

Windows:

    .\.venv\Scripts\activate

Linux / MacOS:

    source .venv/bin/activate

**Install requirements**

    python -m pip install --upgrade pip
    pip install -r requirements/requirements.txt

**Test if everything works properly**

(*DeprecationWarnings* are expected)

With tox

    tox

Without tox

    pip install -e .
    pytest