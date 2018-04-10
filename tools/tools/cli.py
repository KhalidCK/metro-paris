# -*- coding: utf-8 -*-
import json
import logging
import re
from pathlib import Path

import click
import numpy as np
import pandas as pd

from tools.build_features import augment_df_nb

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
    df_routes = pd.read_csv(path/'routes.txt').query('agency_id == @agency_id')
    df_trips = pd.read_csv(path/'trips.txt')
    df_stoptimes = pd.read_csv(path/'stop_times.txt')
    df_stops = pd.read_csv(path/'stops.txt')
    df_calendar = pd.read_csv(path/'calendar.txt')
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


def get_meta_stop(df_gtfs):
    fields = ['stop_name',
              'trip_headsign',
              'route_short_name',
              'route_color',
              'stop_lat',
              'stop_lon']
    return (df_gtfs.loc[:, fields]
            .drop_duplicates()
            .reset_index(drop=True)
            .rename(columns={'stop_name': 'stop', 'route_short_name': 'line'})
            .assign(stop=lambda x: x['stop'].str.lower())
            .assign(trip_headsign=lambda x: x['trip_headsign'].str.lower())
            )


def get_schedule(df):
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
    fields = ['cat_jour', 'libelle_arret', 'trnc_horr_60', 'pourc_validations']
    rename = {'cat_jour': 'profile',
              'libelle_arret': 'stop',
              'trnc_horr_60': 'timespan',
              'pourc_validations': 'percentage'}
    return (df.query("code_stif_res=='110'")
            .loc[:, fields]
            .replace('ND', np.NaN)
            .assign(hour=lambda x: x['trnc_horr_60'].apply(change_trnc))
            .assign(sem=[sem] * df.shape[0])
            .rename(columns=rename)
            )


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


def daily_ranking(df_nb_validation, stop_meta, df_vac):
    def set_rank(group):
        group['profile_rank'] = group.traffic_line.rank(ascending=False)
        return group
    dataset = augment_df_nb(df_nb_validation, stop_meta, df_vac)
    return (dataset.groupby(['stop', 'profile'])
            .mean().reset_index()
            .sort_values(['profile', 'traffic_line'], ascending=False)
            .groupby('profile').apply(set_rank)
            ).rename(columns={'traffic_line': 'avg_traffic_per_platform'})


def bi_dataset(df_profile, df_nb_validation, stop_meta, df_vac):
    """ to be used with BI solution (TABLEAU,...)
    """
    ranking_profile = daily_ranking(df_nb_validation, stop_meta, df_vac)
    return pd.merge(df_profile, ranking_profile, on=['profile', 'stop'])


def to_lower(x):
    return x.str.lower() if(x.dtype == 'object') else x


def save(df, path):
    return (df.apply(to_lower)
            .reset_index(drop=True)
            .to_feather(path))


def save_xlsx(df, path):
    df.to_excel(path, index=False)


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    path_raw = Path(input_filepath) / 'raw'
    path_external = Path(input_filepath) / 'external'
    path_out = Path(output_filepath)
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data ...')
    logger.info('building profile dataset')
    df_nb_validation = build_nb(Path(path_raw))
    df_profile = build_profil(Path(path_raw))
    df_gtfs = make_gtfs(path_raw, agency_id=439)
    logger.info('building gtfs dataset')
    save(get_schedule(df_gtfs),
         path_out/'schedule.feather')
    logger.info('building gtfs metadata')
    stop_meta = get_meta_stop(df_gtfs)
    save(stop_meta,
         path_out/'meta_stop.feather')
    save(df_profile,
         path_out/'profile-2017.feather')
    save(build_profil(Path(path_raw)),
         path_out/'profile-2017.feather')
    logger.info('building nb-validation dataset')
    save(df_nb_validation,
         path_out/'nb-validation-2017.feather')
    logger.info('building ratp-line dataset')
    save(make_ratp(path_raw/'ratp-trafic-2016.json'),
         path_out/'ratp_line.feather')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
