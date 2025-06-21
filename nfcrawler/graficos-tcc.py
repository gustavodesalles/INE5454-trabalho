import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

def main():
    pd.set_option('display.float_format', lambda a: '%.9f' % a)
    # Create dictionary to aggregate valorEstimado by codigoUnidadeGestora
    valor_por_unidade = {}
    valores_dist = {}
    registros_sem_unidade = 0
    for ano in range(2014, 2024 + 1): # muitos registros antes de 2014 não têm valor
        contents = json.load(open(f'licitacoes/licitacoes-{ano}.json'))
        for x in contents:
            item = x['registro']['licitacao']
            codigo_unidade = x['registro']['listUnidadesGestoras'][0]['codigo'] if len(x['registro']['listUnidadesGestoras']) > 0 else None
            valor = float(item['valorEstimado']) if ('valorEstimado' in item and item['valorEstimado'] is not None) else 0

            if codigo_unidade in valor_por_unidade:
                valor_por_unidade[codigo_unidade] += valor
            elif codigo_unidade is not None:
                valor_por_unidade[codigo_unidade] = valor

            if codigo_unidade in valores_dist:
                valores_dist[codigo_unidade].append(valor)
            elif codigo_unidade is not None:
                valores_dist[codigo_unidade] = [valor]

            if codigo_unidade is None:
                registros_sem_unidade += 1
        # print('lalala')
    df = pd.DataFrame(valor_por_unidade.items(), columns=['codigoUnidadeGestora', 'valorEstimado'])
    # print(df)
    # df.plot(kind='bar', x='codigoUnidadeGestora', y='valorEstimado', figsize=(10, 6))
    # print(max(valores_dist[22]))
    print(registros_sem_unidade)
    codigos = list(valores_dist.keys())
    for i in range(0, len(codigos)):
        df_dist = pd.DataFrame([(codigo, valor) for codigo in codigos[i:i+1] for valor in valores_dist[codigo]], columns=['codigoUnidadeGestora', 'valorEstimado'])
        df_dist.boxplot(column='valorEstimado', by='codigoUnidadeGestora', figsize=(10, 6))
        plt.show()

main()