import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt
from os import path


def lectura(archivo):

    if path.exists(archivo):
        print("\nExiste el archivo\n")
    else:
        print("\n------------------No Existe el Archivo-----------------\n")
    df = pd.read_csv(archivo)
    df = pd.DataFrame(df.groupby(['topic'], as_index=False).apply(lambda x: x.sum()))
    df['text'] = df['text'].astype('str')

    return df


def procesamiento(df):
    df['text'] = df.apply(lambda x: x['text'].lower(), axis=1)
    df['tokens'] = df.apply(lambda x: re.split('\W+', x['text']), axis=1)
    df['conteo'] = df.apply(lambda x: Counter(x['tokens']), axis=1)
    df['N'] = df.apply(lambda x: sum(x['conteo'].values()), axis=1)
    df['V'] = df.apply(lambda x: len(x['conteo']), axis=1)
    return df


def grafica(df):
    print("---------creacion de la grafica-------")
    plt.scatter(df['N'], df['V'])
    plt.title('Tokens vs Vocabulario')
    plt.xlabel('Tokens')
    plt.ylabel('Vocabulario')
    plt.savefig('tokensVocabulario')
    plt.show()
    print("---------fin de la grafica-------")





