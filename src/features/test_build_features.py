from build_features import is_dimanchelike, is_paris_holiday, to_profile
from datetime import datetime

path = '../../data/external/fr-en-calendrier-scolaire.csv'


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
    assert not is_paris_holiday(d, path)
    # winter holiday for school
    d = '2018-02-20'
    # summer holiday
    assert is_paris_holiday(d, path)
    d = '2018-07-18'
    assert is_paris_holiday(d, path)
    # vacances zone B
    d = '2018-03-10'
    assert not is_paris_holiday(d, path)


def test_to_profile_vacances_scolaire():
    # vacances
    # 'JOVS': 'Jour Ouvré en période de Vacances Scolaires',
    assert to_profile(datetime(2018, 2, 20), path) == 'JOVS'
    assert to_profile(datetime(2018, 7, 10), path) == 'JOVS'
    # 'SAVS': 'Samedi en période de Vacances Scolaires',
    assert to_profile(datetime(2018, 2, 17), path) == 'SAVS'
    # 'DIJFP': 'Dimanche, Jour Férié et ponts'  # TODO:pont
    # dimanche en période de vacances scolaire
    assert to_profile(datetime(2018, 2, 18), path) == 'DIJFP'


def test_to_profile_hors_vacances_scolaire():
    # 'JOHV': 'Jour Ouvré Hors Vacances Scolaires',
    assert to_profile(datetime(2018, 12, 13), path) == 'JOHV'
    # 'SAHV': 'Samedi Hors Vacances Scolaires',
    assert to_profile(datetime(2018, 3, 10), path) == 'SAHV'
    # 'DIJFP': 'Dimanche, Jour Férié et ponts'  # TODO:pont
