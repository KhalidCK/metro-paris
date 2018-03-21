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


def load_stif(path):
    data = json.load(open(path))
    df = pd.DataFrame([elt['fields'] for elt in data])
    return df


def read_json(path):
    df = load_stif(path)
    pattern = re.compile('.*_(S\d\-\d{4})\.json')
    sem = pattern.match(str(path)).group(1)
    return (df, sem)


def make_ratp(path):
    data = json.load(open(path))
    df = pd.DataFrame([elt['fields'] for elt in data])
    df = df.drop(columns=['rang', 'ville', 'reseau', 'trafic'])
    to_keep = ['station', 'arrondissement_pour_paris']
    reshaped = pd.melt(df, to_keep, value_name='ligne').dropna()
    int_type = ['arrondissement_pour_paris']
    reshaped[int_type] = reshaped[int_type].astype(int)
    return (reshaped
            .dropna()
            .drop(columns='variable')
            .rename(columns={'arrondissement_pour_paris': 'arrondissement'})
            .astype(str)
            )


def change_trnc(elt):
    if type(elt) != str:
        return np.NaN
    return int(elt.split('-')[0].split('H')[0])


def get_df_nb(path):
    fields = ['categorie_titre', 'jour', 'libelle_arret', 'nb_vald']
    df, sem = read_json(path)
    df = df[fields].rename(columns={'categorie_titre': 'kind',
                                    'jour': 'date',
                                    'libelle_arret': 'stop',
                                    'nb_vald': 'value'})
    df = df.query('value != "Moins de 5"').dropna()
    df.loc[:, 'date'] = pd.to_datetime(df.loc[:, 'date'])
    df['value'] = df['value'].astype(int)
    return (df.assign(sem=[sem] * df.shape[0]))


def get_df_profil(path):
    df, sem = read_json(path)
    df = df.replace({'cat_jour': map_jour_fr})
    fields = ['cat_jour', 'libelle_arret', 'trnc_horr_60', 'pourc_validations']
    return (df.query("code_stif_res=='110'")
            .loc[:, fields]
            .replace('ND', np.NaN)
            .assign(heure=lambda x: x['trnc_horr_60'].apply(change_trnc))
            .assign(sem=[sem] * df.shape[0]))


def build(files, processing):
    """
    Parameters
    ----------
    path: pathlib.Path
    processing: function
    """
    dfs = [processing(path) for path in files]
    return pd.concat(dfs)


def build_profil(path):
    """
    parameters
    ----------
    path: pathlib.path
    """
    return build(path.glob('profil-validation*.json'), get_df_profil)


def build_nb(path):
    """
    parameters
    ----------
    path: pathlib.path
    """
    return build(path.glob('nb-validation*.json'), get_df_nb)


def save(df, path):
    df.reset_index(drop=True).to_feather(path)


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    path_in = Path(input_filepath)
    path_out = Path(output_filepath)
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data ...')
    logger.info('building profile dataset')
    save(build_profil(Path(input_filepath)),
         path_out/'profile-2017.feather')
    logger.info('building nb-validation dataset')
    save(build_nb(Path(input_filepath)),
         path_out/'nb-validation-2017.feather')
    logger.info('building ratp-line dataset')
    save(make_ratp(path_in/'ratp-trafic-2016.json'),
         path_out/'ratp_line.feather')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
