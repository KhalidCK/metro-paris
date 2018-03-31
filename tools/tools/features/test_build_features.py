from build_features import is_dimanchelike
from build_features import is_paris_holiday, to_profile
from build_features import read_vacances
from datetime import datetime

PATH = '../../data/external/fr-en-calendrier-scolaire.csv'
DF_PATH = read_vacances(PATH)


def test_dimanche_jour_ferie_et_ponts():
    # samedi
    assert is_dimanchelike(datetime(2018, 3, 31))
    # dimanche
    assert is_dimanchelike(datetime(2018, 4, 1))
    # lundi de pâques
    assert is_dimanchelike(datetime(2018, 4, 2))
    """
    TODO=> ponts
    un ou de deux jours entre un jour férié et
    un jour de repos hebdomadaire ou un jour précédant les congés payés.
    """


def test_paris_holiday():
    d = '2018-01-16'
    assert not is_paris_holiday(d, DF_PATH)
    # winter holiday for school
    d = '2018-02-20'
    # summer holiday
    assert is_paris_holiday(d, DF_PATH)
    d = '2018-07-18'
    assert is_paris_holiday(d, DF_PATH)
    # vacances zone B
    d = '2018-03-10'
    assert not is_paris_holiday(d, DF_PATH)


def test_to_profile_vacances_scolaire():
    # vacances
    # 'JOVS': 'Jour Ouvré en période de Vacances Scolaires',
    assert to_profile(datetime(2018, 2, 20), DF_PATH) == 'JOVS'
    assert to_profile(datetime(2018, 7, 10), DF_PATH) == 'JOVS'
    # 'SAVS': 'Samedi en période de Vacances Scolaires',
    assert to_profile(datetime(2018, 2, 17), DF_PATH) == 'SAVS'
    # 'DIJFP': 'Dimanche, Jour Férié et ponts'  # TODO:pont
    # dimanche en période de vacances scolaire
    assert to_profile(datetime(2018, 2, 18), DF_PATH) == 'DIJFP'


def test_to_profile_hors_vacances_scolaire():
    # 'JOHV': 'Jour Ouvré Hors Vacances Scolaires',
    assert to_profile(datetime(2018, 12, 13), DF_PATH) == 'JOHV'
    # 'SAHV': 'Samedi Hors Vacances Scolaires',
    assert to_profile(datetime(2018, 3, 10), DF_PATH) == 'SAHV'
    # 'DIJFP': 'Dimanche, Jour Férié et ponts'  # TODO:pont
