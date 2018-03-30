from workalendar.europe import France
import pandas as pd

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


def is_paris_holiday(strday, path):
    df = read_vacances(path).query('academie == "Paris"')
    return not df.query('begin <= @strday <end').empty


def to_profile(day, path):
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
    if is_paris_holiday(day.strftime('%Y-%m-%d'), path):
        print('holiday')
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
