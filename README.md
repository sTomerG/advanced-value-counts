<h1>Welcome to advanced-value-counts</h1>

advanced-value-counts is a Python-package containing the `AdvancedValueCounts` class that makes use of pandas' [`.value_counts()`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html), [`.groupby()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) and [seaborn](https://seaborn.pydata.org/) to easily get a lot of info about the counts of a (categorical) column in a pandas DataFrame. The potential of this package is at its peak when wanting info of counts of a column after a grouping: `df.groupby(groupby_col)[column].value_counts()`. See [Usage](#usage) on how to use `AdvancedValueCounts`. Read [this medium article](https://medium.com/@tomergabay/advancedvaluecounts-for-eda-2f80e2c74ce1) or consult [this notebook](https://github.com/sTomerG/advanced-value-counts/blob/main/notebooks/medium_notebook.ipynb) for an explanation on the added value of this package.


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

The example below uses a modified version of the [Titanic dataset from Kaggle](https://www.kaggle.com/c/titanic), which can be found in this GitRepo [here](https://github.com/sTomerG/advanced-value-counts/tree/main/tests/data/titanic.csv). 

The code of this notebook can be found [here](https://github.com/sTomerG/advanced-value-counts/tree/main/notebooks/usage_notebook.ipynb).


```python
from advanced_value_counts.avc import AdvancedValueCounts
import pandas as pd

# read in the data file
df = pd.read_csv('../tests/data/titanic.csv', usecols=['CabinArea','Title'])
df.head()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CabinArea</th>
      <th>Title</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>Mr.</td>
    </tr>
    <tr>
      <th>1</th>
      <td>C</td>
      <td>Mrs.</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NaN</td>
      <td>Miss.</td>
    </tr>
    <tr>
      <th>3</th>
      <td>C</td>
      <td>Mrs.</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NaN</td>
      <td>Mr.</td>
    </tr>
  </tbody>
</table>
</div>




```python
# create an instance of AdvancedValueCounts
avc = AdvancedValueCounts(df=df, column='Title')

# print the AdvancedValueCounts DataFrame
avc.avc_df
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ratio</th>
      <th>count</th>
    </tr>
    <tr>
      <th>Title</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Mr.</th>
      <td>0.580247</td>
      <td>517</td>
    </tr>
    <tr>
      <th>Miss.</th>
      <td>0.204265</td>
      <td>182</td>
    </tr>
    <tr>
      <th>Mrs.</th>
      <td>0.140292</td>
      <td>125</td>
    </tr>
    <tr>
      <th>Master.</th>
      <td>0.044893</td>
      <td>40</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>0.007856</td>
      <td>7</td>
    </tr>
    <tr>
      <th>Rev.</th>
      <td>0.006734</td>
      <td>6</td>
    </tr>
    <tr>
      <th>Major.</th>
      <td>0.002245</td>
      <td>2</td>
    </tr>
    <tr>
      <th>Col.</th>
      <td>0.002245</td>
      <td>2</td>
    </tr>
    <tr>
      <th>Mlle.</th>
      <td>0.002245</td>
      <td>2</td>
    </tr>
    <tr>
      <th>Countess.</th>
      <td>0.001122</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Capt.</th>
      <td>0.001122</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Ms.</th>
      <td>0.001122</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Sir.</th>
      <td>0.001122</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Lady.</th>
      <td>0.001122</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Mme.</th>
      <td>0.001122</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Don.</th>
      <td>0.001122</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Jonkheer.</th>
      <td>0.001122</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



Set `min_group_count` to 5 to group small groups into `'_other'` group


```python
avc.min_group_count = 5
avc.avc_df
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ratio</th>
      <th>count</th>
    </tr>
    <tr>
      <th>Title</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Mr.</th>
      <td>0.580247</td>
      <td>517</td>
    </tr>
    <tr>
      <th>Miss.</th>
      <td>0.204265</td>
      <td>182</td>
    </tr>
    <tr>
      <th>Mrs.</th>
      <td>0.140292</td>
      <td>125</td>
    </tr>
    <tr>
      <th>Master.</th>
      <td>0.044893</td>
      <td>40</td>
    </tr>
    <tr>
      <th>_other</th>
      <td>0.015713</td>
      <td>14</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>0.007856</td>
      <td>7</td>
    </tr>
    <tr>
      <th>Rev.</th>
      <td>0.006734</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



Parameters of the `AdvancedValueCounts` class to adjust for small groups for a single column: 


```python
dropna: bool = False
min_group_count: int = 1 # does not effect NA or the '_other' group
min_group_ratio: float = 0 # does not effect NA or the '_other' group
```

It is also possible to use `column` in combination with parameter `groupy_col: str = None` to mimick the behaviour of `df.groupby(groupby_col)[column].value_counts()`


```python
avc_grouped = AdvancedValueCounts(df=df, column='Title', groupby_col='CabinArea')
avc_grouped.avc_df
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>count</th>
      <th>subgroup_ratio</th>
      <th>subgr_r_diff_subgr_all</th>
      <th>r_vs_total</th>
    </tr>
    <tr>
      <th>CabinArea</th>
      <th>Title</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="5" valign="top">A</th>
      <th>Col.</th>
      <td>1</td>
      <td>0.066667</td>
      <td>0.064422</td>
      <td>0.001122</td>
    </tr>
    <tr>
      <th>Lady.</th>
      <td>1</td>
      <td>0.066667</td>
      <td>0.065544</td>
      <td>0.001122</td>
    </tr>
    <tr>
      <th>Master.</th>
      <td>1</td>
      <td>0.066667</td>
      <td>0.021773</td>
      <td>0.001122</td>
    </tr>
    <tr>
      <th>Mr.</th>
      <td>11</td>
      <td>0.733333</td>
      <td>0.153086</td>
      <td>0.012346</td>
    </tr>
    <tr>
      <th>Sir.</th>
      <td>1</td>
      <td>0.066667</td>
      <td>0.065544</td>
      <td>0.001122</td>
    </tr>
    <tr>
      <th>...</th>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">_na</th>
      <th>Mrs.</th>
      <td>81</td>
      <td>0.117904</td>
      <td>-0.022388</td>
      <td>0.090909</td>
    </tr>
    <tr>
      <th>Ms.</th>
      <td>1</td>
      <td>0.001456</td>
      <td>0.000333</td>
      <td>0.001122</td>
    </tr>
    <tr>
      <th>Rev.</th>
      <td>6</td>
      <td>0.008734</td>
      <td>0.002000</td>
      <td>0.006734</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>4</td>
      <td>0.005822</td>
      <td>-0.002034</td>
      <td>0.004489</td>
    </tr>
    <tr>
      <th>_total</th>
      <td>687</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.771044</td>
    </tr>
  </tbody>
</table>
<p>74 rows × 4 columns</p>
</div>



To get a better overview of the data, set attributes to adjust group size and round the ratios


```python
avc_grouped.min_group_ratio = 0.05
avc_grouped.min_subgroup_count = 5
avc_grouped.round_ratio = 3
avc_grouped.avc_df
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>count</th>
      <th>subgroup_ratio</th>
      <th>subgr_r_diff_subgr_all</th>
      <th>r_vs_total</th>
    </tr>
    <tr>
      <th>CabinArea</th>
      <th>Title</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="6" valign="top">B</th>
      <th>Miss.</th>
      <td>14</td>
      <td>0.298</td>
      <td>0.094</td>
      <td>0.016</td>
    </tr>
    <tr>
      <th>Mr.</th>
      <td>16</td>
      <td>0.340</td>
      <td>-0.240</td>
      <td>0.018</td>
    </tr>
    <tr>
      <th>Mrs.</th>
      <td>10</td>
      <td>0.213</td>
      <td>0.073</td>
      <td>0.011</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>1</td>
      <td>0.021</td>
      <td>0.013</td>
      <td>0.001</td>
    </tr>
    <tr>
      <th>_other</th>
      <td>6</td>
      <td>0.127</td>
      <td>0.111</td>
      <td>0.007</td>
    </tr>
    <tr>
      <th>_total</th>
      <td>47</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.053</td>
    </tr>
    <tr>
      <th rowspan="6" valign="top">C</th>
      <th>Miss.</th>
      <td>12</td>
      <td>0.203</td>
      <td>-0.001</td>
      <td>0.013</td>
    </tr>
    <tr>
      <th>Mr.</th>
      <td>29</td>
      <td>0.492</td>
      <td>-0.088</td>
      <td>0.033</td>
    </tr>
    <tr>
      <th>Mrs.</th>
      <td>14</td>
      <td>0.237</td>
      <td>0.097</td>
      <td>0.016</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>1</td>
      <td>0.017</td>
      <td>0.009</td>
      <td>0.001</td>
    </tr>
    <tr>
      <th>_other</th>
      <td>3</td>
      <td>0.051</td>
      <td>0.035</td>
      <td>0.003</td>
    </tr>
    <tr>
      <th>_total</th>
      <td>59</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.066</td>
    </tr>
    <tr>
      <th rowspan="8" valign="top">_all</th>
      <th>Master.</th>
      <td>40</td>
      <td>0.045</td>
      <td>NaN</td>
      <td>0.045</td>
    </tr>
    <tr>
      <th>Miss.</th>
      <td>182</td>
      <td>0.204</td>
      <td>NaN</td>
      <td>0.204</td>
    </tr>
    <tr>
      <th>Mr.</th>
      <td>517</td>
      <td>0.580</td>
      <td>NaN</td>
      <td>0.580</td>
    </tr>
    <tr>
      <th>Mrs.</th>
      <td>125</td>
      <td>0.140</td>
      <td>NaN</td>
      <td>0.140</td>
    </tr>
    <tr>
      <th>Rev.</th>
      <td>6</td>
      <td>0.007</td>
      <td>NaN</td>
      <td>0.007</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>7</td>
      <td>0.008</td>
      <td>NaN</td>
      <td>0.008</td>
    </tr>
    <tr>
      <th>_other</th>
      <td>14</td>
      <td>0.016</td>
      <td>NaN</td>
      <td>0.016</td>
    </tr>
    <tr>
      <th>_total</th>
      <td>891</td>
      <td>1.000</td>
      <td>NaN</td>
      <td>1.000</td>
    </tr>
    <tr>
      <th rowspan="8" valign="top">_na</th>
      <th>Master.</th>
      <td>33</td>
      <td>0.048</td>
      <td>0.003</td>
      <td>0.037</td>
    </tr>
    <tr>
      <th>Miss.</th>
      <td>135</td>
      <td>0.197</td>
      <td>-0.007</td>
      <td>0.152</td>
    </tr>
    <tr>
      <th>Mr.</th>
      <td>424</td>
      <td>0.617</td>
      <td>0.037</td>
      <td>0.476</td>
    </tr>
    <tr>
      <th>Mrs.</th>
      <td>81</td>
      <td>0.118</td>
      <td>-0.022</td>
      <td>0.091</td>
    </tr>
    <tr>
      <th>Rev.</th>
      <td>6</td>
      <td>0.009</td>
      <td>0.002</td>
      <td>0.007</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>4</td>
      <td>0.006</td>
      <td>-0.002</td>
      <td>0.004</td>
    </tr>
    <tr>
      <th>_other</th>
      <td>4</td>
      <td>0.006</td>
      <td>-0.010</td>
      <td>0.004</td>
    </tr>
    <tr>
      <th>_total</th>
      <td>687</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.771</td>
    </tr>
    <tr>
      <th rowspan="7" valign="top">_other</th>
      <th>Master.</th>
      <td>5</td>
      <td>0.051</td>
      <td>0.006</td>
      <td>0.006</td>
    </tr>
    <tr>
      <th>Miss.</th>
      <td>21</td>
      <td>0.214</td>
      <td>0.010</td>
      <td>0.024</td>
    </tr>
    <tr>
      <th>Mr.</th>
      <td>48</td>
      <td>0.490</td>
      <td>-0.090</td>
      <td>0.054</td>
    </tr>
    <tr>
      <th>Mrs.</th>
      <td>20</td>
      <td>0.204</td>
      <td>0.064</td>
      <td>0.022</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>1</td>
      <td>0.010</td>
      <td>0.002</td>
      <td>0.001</td>
    </tr>
    <tr>
      <th>_other</th>
      <td>3</td>
      <td>0.031</td>
      <td>0.015</td>
      <td>0.003</td>
    </tr>
    <tr>
      <th>_total</th>
      <td>98</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.110</td>
    </tr>
  </tbody>
</table>
</div>



Parameters of the `AdvancedValueCounts` class to adjust for groupsize in a grouped-by `AdvancedValueCounts` <br>


```python
# for groupby_col:
dropna: bool = False
max_groups: int = None # does not effect NA or the '_other' group
min_group_count: int = 1 # does not effect NA or the '_other' group
min_group_ratio: float = 0 # does not effect NA or the '_other' group

# for column:
dropna: bool = False
max_subgroups: int = None # does not effect NA or the '_other' group
min_subgroup_count: int = 1 # does not effect NA or the '_other' group
min_subgroup_ratio: float = 0 # does not effect NA or the '_other' group
min_subgroup_ratio_vs_total: float = 0 # does not effect NA or the '_other' group
```

To get a plot of the `AdvancedValueCounts.avc_df`:


```python
avc_grouped.get_plot(normalize=True) # normalize = True is default value
```


    
![value count plot](https://github.com/sTomerG/advanced-value-counts/blob/main/notebooks/images/avc_plot.png?raw=true)
    


To get a DataFrame without the summary_statistics such as `'_all'` and `'_total'`:


```python
avc_grouped.unsummerized_df
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>count</th>
      <th>subgroup_ratio</th>
      <th>subgr_r_diff_subgr_all</th>
      <th>r_vs_total</th>
    </tr>
    <tr>
      <th>CabinArea</th>
      <th>Title</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="5" valign="top">B</th>
      <th>Miss.</th>
      <td>14</td>
      <td>0.298</td>
      <td>0.094</td>
      <td>0.016</td>
    </tr>
    <tr>
      <th>Mr.</th>
      <td>16</td>
      <td>0.340</td>
      <td>-0.240</td>
      <td>0.018</td>
    </tr>
    <tr>
      <th>Mrs.</th>
      <td>10</td>
      <td>0.213</td>
      <td>0.073</td>
      <td>0.011</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>1</td>
      <td>0.021</td>
      <td>0.013</td>
      <td>0.001</td>
    </tr>
    <tr>
      <th>_other</th>
      <td>6</td>
      <td>0.127</td>
      <td>0.111</td>
      <td>0.007</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">C</th>
      <th>Miss.</th>
      <td>12</td>
      <td>0.203</td>
      <td>-0.001</td>
      <td>0.013</td>
    </tr>
    <tr>
      <th>Mr.</th>
      <td>29</td>
      <td>0.492</td>
      <td>-0.088</td>
      <td>0.033</td>
    </tr>
    <tr>
      <th>Mrs.</th>
      <td>14</td>
      <td>0.237</td>
      <td>0.097</td>
      <td>0.016</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>1</td>
      <td>0.017</td>
      <td>0.009</td>
      <td>0.001</td>
    </tr>
    <tr>
      <th>_other</th>
      <td>3</td>
      <td>0.051</td>
      <td>0.035</td>
      <td>0.003</td>
    </tr>
    <tr>
      <th rowspan="7" valign="top">_na</th>
      <th>Master.</th>
      <td>33</td>
      <td>0.048</td>
      <td>0.003</td>
      <td>0.037</td>
    </tr>
    <tr>
      <th>Miss.</th>
      <td>135</td>
      <td>0.197</td>
      <td>-0.007</td>
      <td>0.152</td>
    </tr>
    <tr>
      <th>Mr.</th>
      <td>424</td>
      <td>0.617</td>
      <td>0.037</td>
      <td>0.476</td>
    </tr>
    <tr>
      <th>Mrs.</th>
      <td>81</td>
      <td>0.118</td>
      <td>-0.022</td>
      <td>0.091</td>
    </tr>
    <tr>
      <th>Rev.</th>
      <td>6</td>
      <td>0.009</td>
      <td>0.002</td>
      <td>0.007</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>4</td>
      <td>0.006</td>
      <td>-0.002</td>
      <td>0.004</td>
    </tr>
    <tr>
      <th>_other</th>
      <td>4</td>
      <td>0.006</td>
      <td>-0.010</td>
      <td>0.004</td>
    </tr>
    <tr>
      <th rowspan="6" valign="top">_other</th>
      <th>Master.</th>
      <td>5</td>
      <td>0.051</td>
      <td>0.006</td>
      <td>0.006</td>
    </tr>
    <tr>
      <th>Miss.</th>
      <td>21</td>
      <td>0.214</td>
      <td>0.010</td>
      <td>0.024</td>
    </tr>
    <tr>
      <th>Mr.</th>
      <td>48</td>
      <td>0.490</td>
      <td>-0.090</td>
      <td>0.054</td>
    </tr>
    <tr>
      <th>Mrs.</th>
      <td>20</td>
      <td>0.204</td>
      <td>0.064</td>
      <td>0.022</td>
    </tr>
    <tr>
      <th>_na</th>
      <td>1</td>
      <td>0.010</td>
      <td>0.002</td>
      <td>0.001</td>
    </tr>
    <tr>
      <th>_other</th>
      <td>3</td>
      <td>0.031</td>
      <td>0.015</td>
      <td>0.003</td>
    </tr>
  </tbody>
</table>
</div>



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




