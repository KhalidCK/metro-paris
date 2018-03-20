# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
import json
import pandas as pd
import numpy as np
import re

map_jour_fr = {
    'JOHV': 'Jour Ouvré Hors Vacances Scolaires',
    'SAHV': 'Samedi Hors Vacances Scolaires',
    'JOVS': 'Jour Ouvré en période de Vacances Scolaires',
    'SAVS': 'Samedi en période de Vacances Scolaires',
    'DIJFP': 'Dimanche et Jour Férié et les ponts'
}


def change_trnc(elt):
    if type(elt) != str:
        return np.NaN
    return int(elt.split('-')[0].split('H')[0])


def get_df_profil(path):
    with open(path, 'r') as fd:
        data = json.load(fd)
    pattern = re.compile('.*_(S\d\-\d{4})\.json')
    sem = pattern.match(str(path)).group(1)
    df = pd.DataFrame([elt['fields'] for elt in data])
    df = df.replace({'cat_jour': map_jour_fr})
    fields = ['cat_jour', 'libelle_arret', 'trnc_horr_60', 'pourc_validations']
    return (df.query("code_stif_res=='110'")
            .loc[:, fields]
            .replace('ND', np.NaN)
            .assign(heure=lambda x: x['trnc_horr_60'].apply(change_trnc))
            .assign(sem=[sem] * df.shape[0]))


def build_profil(files):
    """
    Parameters
    ----------
    path: pathlib.Path
    """
    dfs = [
        get_df_profil(path) for path in files.glob('profil-validation*.json')
    ]
    return pd.concat(dfs)


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data ...')
    logger.info('building profile dataset')
    df = build_profil(Path(input_filepath))
    df.reset_index().to_feather(Path(output_filepath)/'profile-2017.feather')
    return


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
