** Work in progress **

# Exploration of the Parisian subway

This study began with a discussion : 

> What is the best time to take the metro to avoid the crowd ?
> Is there some data to tackle this question ?

You'll find some answer [here](https://github.com/KhalidCK/metro-paris/blob/master/reports/README.md)

## Install

*optionnal*

Create a virtualenv 

```
make create_environement
```

Download the raw data

```bash
Make download
```

Build the dataset

```bash
make data
```

## Repository organisation

Choice here are heavily inspired by the [cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science)

>We're not talking about bikeshedding the indentation aesthetics or pedantic formatting standards — ultimately, data science code quality is about correctness and reproducibility.:neckbeard:

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
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
├── reports            <- Analysis as Markdown,HTML, PDF, LaTeX, etc.
│   └── img        <-  Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── tools <- Source code for use in this project.
