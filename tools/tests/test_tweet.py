import re

from tools import tweet


def test_regex_is_incident():
    incidents = ['09:22, le trafic est interrompu entre Mairie Lilas et Republique (incident technique) #RATP #Ligne11',
                 '12:54, le trafic est perturbé sur la ligne (panne de signalisation)  #RATP #ligne7',
                 '13:31, le trafic est interrompu entre Pte de St-Cloud et Pont de Sevres. Reprise estimée à 13:40. (malaise voyageur) #RATP #Ligne9',
                 "07:48, le trafic est ralenti sur la ligne (incident d'exploitation) #RATP #Ligne12",
                 "11:11, la rame stationne à Pte de Clichy en dir. de Asnieres-Gennevilliers Les Courtilles (malaise voyageur) #RATP #Ligne13",
                 ]
    not_incidents = ['10:17, le trafic est rétabli sur la ligne (incident voyageur)  #RATP #ligne4',
                     'En raison de la piétonnisation des Champs-Elysées, deux accès de la station FD Roosevelt sont fermés et la station… https://t.co/YyMdPduh75',
                     'RT @Ligne3_RATP: La #RATP est partenaire de l’#Expo Paris musique club à la @gaitelyrique. En savoir +',
                     "Incident terminé (incident technique). Retour à un trafic normal sur l'ensemble de la #Ligne7bis #RATP",
                     "20:41, le trafic reprend progressivement (accident grave de personne) #RATP #Ligne8",
                     "Fin d'incident à Châtelet. Le trafic reste perturbé sur l'ensemble de la #Ligne11 #RATP",
                     ]
    regex = re.compile(tweet.PATTERN_INCIDENT)
    for elt in incidents:
        assert regex.search(elt)

    for elt in not_incidents:
        assert not regex.search(elt)


def test_regex_why():
    simple = '13:31, le trafic est interrompu entre Pte de St-Cloud et Pont de Sevres. Reprise estimée à 13:40. (malaise voyageur) #RATP #Ligne9'
    weird = "09:27, le trafic est interrompu entre Nation et Daumesnil (Felix Eboue) (colis suspect) #RATP #Ligne6"
    regex = re.compile(tweet.PATTERN_WHY)
    assert regex.search(simple).group('why') == 'malaise voyageur'
    assert regex.search(weird).group('why') == 'colis suspect'
