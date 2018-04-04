import re
from glob import glob

import pandas as pd

PATTERN_INCIDENT = 'le trafic est (perturbé|interrompu|ralenti)'\
                   '| la rame stationne'
PATTERN_WHY = '\((?P<why>[^\)]*)\)(?:\s+#RATP)'


def read_tweet(path):
    dfs = []
    for path in glob(f'{path}/*.csv'):
        print(path)
        df_line = pd.read_csv(path)
        line = re.findall('\d{1,2}', path)
        print(f'line {line}')
        print(f'shape : {df_line.shape[0]}')
        df_line['ligne'] = re.findall('\d{1,2}', path) * (df_line.shape[0])
        df_line['ligne'] = df_line['ligne'].astype(int)
        dfs.append(df_line)
    return (pd.concat(dfs)
            .reset_index(drop=True)
            .sort_values(['timestamp', 'ligne'], ascending=False))


def get_incidents(df: pd.DataFrame) -> pd.DataFrame:
    return (df[df.text.str.contains(PATTERN_INCIDENT)]
            .assign(reason=lambda x: x.text.str.extract(PATTERN_WHY))
            )
