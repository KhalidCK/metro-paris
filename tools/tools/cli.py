# -*- coding: utf-8 -*-
import click
import logging
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


def make_gtfs(path, agency_id=439):
    fields = [
        'route_id',
        'stop_id',
        'service_id',
        'route_short_name',
        'trip_short_name',
        'trip_headsign',
        'route_color',
        'trip_id',
        'direction_id',
        'wheelchair_accessible',
        'departure_time',
        'stop_name',
        'stop_lat',
        'stop_lon',
        'wheelchair_boarding',
        'start_date',
        'end_date',
        'day',
    ]

    cats = [
        'route_id',
        'stop_id',
        'service_id',
        'route_short_name',
        'trip_short_name',
        'trip_headsign',
        'route_color',
        'trip_id',
        'direction_id',
        'wheelchair_accessible',
        'stop_name',
        'stop_lat',
        'stop_lon',
        'wheelchair_boarding',
        'start_date',
        'end_date',
        'day',
    ]
    p = Path(path)
    df_routes = pd.read_csv(p/'routes.txt').query('agency_id == @agency_id')
    df_trips = pd.read_csv(p/'trips.txt')
    df_stoptimes = pd.read_csv(p/'stop_times.txt')
    df_stops = pd.read_csv(p/'stops.txt')
    df_calendar = pd.read_csv(p/'calendar.txt')
    tidy_calendar = (df_calendar.melt(id_vars=[
                     'service_id', 'start_date', 'end_date'])
                     .query('value==1')
                     .rename(columns={'variable': 'day'})
                     .drop(columns='value'))

    result = (df_routes.merge(df_trips, on='route_id')
              .merge(tidy_calendar, on='service_id')
              .merge(df_stoptimes, on='trip_id')
              .merge(df_stops, on='stop_id')
              .loc[:, fields]
              )
    for cat in cats:
        result[cat] = result[cat].astype('category')
    return result


def get_schedule(path):
    df = make_gtfs(path, agency_id=439)
    return (df.sort_values(['stop_name', 'trip_headsign', 'departure_time'])
            .loc[:, ['stop_name', 'trip_headsign', 'departure_time', 'day']])


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


def save_xlsx(df, path):
    df.to_excel(path, index=False)


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
    df_profile = build_profil(Path(input_filepath))
    save(df_profile,
         path_out/'profile-2017.feather')
    save_xlsx(df_profile,
              path_out/'profile-2017.xlsx')
    save(build_profil(Path(input_filepath)),
         path_out/'profile-2017.feather')
    logger.info('building nb-validation dataset')
    save(build_nb(Path(input_filepath)),
         path_out/'nb-validation-2017.feather')
    logger.info('building ratp-line dataset')
    save(make_ratp(path_in/'ratp-trafic-2016.json'),
         path_out/'ratp_line.feather')
    logger.info('building gtfs dataset')
    save(get_schedule(path_in),
         path_out/'schedule.feather')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
