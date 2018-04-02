import pandas as pd
from workalendar.europe import France

CAL = France()

map_jour_fr = {
    'JOHV': 'Jour Ouvré Hors Vacances Scolaires',
    'SAHV': 'Samedi Hors Vacances Scolaires',
    'JOVS': 'Jour Ouvré en période de Vacances Scolaires',
    'SAVS': 'Samedi en période de Vacances Scolaires',
    'DIJFP': 'Dimanche, Jour Férié et ponts'  # TODO:pont
}


def is_dimanchelike(day):
    """Dimanche, Jour Férié
    """
    return not CAL.is_working_day(day)


def read_vacances(path):
    mapping = {'Académies': 'academie',
               'Date de début': 'begin',
               'Date de fin': 'end',
               'Description': 'description'}

    df = (pd.read_csv(path)
          .rename(columns=mapping)
          )
    for d in ['begin', 'end']:
        df[d] = pd.to_datetime(df[d])
    return df


def is_paris_holiday(day, df):
    return not df.query('(academie == "Paris") and (begin <= @day <end)').empty


def to_profile(day, df):
    """
    Parameters
    ----------
    day:datetime
    """
    def jour_ouvre(nb):
        return 4 >= nb >= 0

    def is_samedi(nb):
        return nb == 5

    weekday = day.weekday()
    if is_paris_holiday(day, df):
        if jour_ouvre(weekday):
            # 'JOVS': 'Jour Ouvré en période de Vacances Scolaires',
            return 'JOVS'
        elif is_samedi(weekday):
            # 'SAVS': 'Samedi en période de Vacances Scolaires',
            return 'SAVS'
        else:
            # 'DIJFP': 'Dimanche, Jour Férié et ponts'  # TODO:pont
            return 'DIJFP'
    else:
        # 'JOHV': 'Jour Ouvré Hors Vacances Scolaires',
        if jour_ouvre(weekday):
            return 'JOHV'
        elif is_samedi(weekday):
            return 'SAHV'
        else:
            # 'DIJFP': 'Dimanche, Jour Férié et ponts'  # TODO:pont
            return 'DIJFP'


def add_profile(df_nb_validation, df_vac):
    """ add profile to nb_validation dataset
    see `map_jour` for details
    """
    days = df_nb_validation.date.drop_duplicates().reset_index(drop=True)
    profile = days.apply(lambda x: to_profile(x, df_vac))
    profile.name = 'profile'
    mapping = pd.concat([days, profile], axis=1)
    return pd.merge(df_nb_validation, mapping, on='date')


def augment_df_nb(df_nb_validation, stop_meta, df_vac):
    """ merge on 'stop'

    Fields added
    'is_end': is it the first or last stop of a line
    'line': name of the line
    'nbline': nb of lines going through the station
    'stop_lat'
    'stop_lon'
    """
    nb_lines = (stop_meta[['stop', 'line']]
                .groupby('stop')[['line']]
                .nunique()
                .rename(columns={'line': 'nbline'})
                .reset_index()
                )
    dataset = add_profile(df_nb_validation, df_vac)
    dataset = pd.merge(dataset, nb_lines, on='stop')
    dataset['traffic_line'] = dataset.value / dataset.nbline
    dataset['is_end'] = dataset.stop.isin(stop_meta.trip_headsign)
    fields = ['stop', 'line', 'stop_lat', 'stop_lon']
    dataset = pd.merge(dataset,
                       stop_meta[fields].drop_duplicates(),
                       on='stop')
    return (dataset
            .drop(columns='value')
            .dropna()
            .drop_duplicates())
