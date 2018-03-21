# Paris metro

** WORK IN PROGRESS **

Exploration of the Parisian subway.

This study began with a discussion : 

> What is the best time to take the metro to avoid the crowd ?
> Is there some data to tackle this question ?

After some google search, the [iledefrance-mobilites](https://www.iledefrance-mobilites.fr/) has some interesting report and also a dedicated [open data portal](https://opendata.stif.info/page/home/)

The most promising data are about the number of user per day and an hourly *profile* break down per hour.

There is no data regarding past incident, you can only access this information via a real-time API.

However, there is a tweeter account,like this [one](https://twitter.com/Ligne7_RATP) for each metro line.It can probably be used to retrieve historical information.

## Repository organisation

This repository organisation is heavily inspired by the [cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science)

```
├── Makefile           <- Makefile with commands like `make data` or `make download`
├── README.md          
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── notebooks          <- Jupyter notebooks. 
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── data           <- Scripts to download or generate data
│   │   └── make_dataset.py
│   │
```
