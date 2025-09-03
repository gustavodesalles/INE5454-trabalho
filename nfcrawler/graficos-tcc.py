import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

def main(tipo):
    pd.set_option('display.float_format', lambda a: '%.9f' % a)
    # Create dictionary to aggregate valorEstimado by codigoUnidadeGestora
    valor_por_unidade = {}
    valores_dist = {}
    for ano in range(2021, 2024 + 1): # muitos registros antes de 2014 não têm valor
        registros_sem_unidade = 0
        registros_sem_valor = 0
        if tipo == 'licitacoes':
            contents = json.load(open(f'licitacoes/licitacoes-{ano}.json'))
            for x in contents:
                item = x['registro']['licitacao']
                codigo_unidade = [x['denominacao'].strip() for x in x['registro']['listUnidadesGestoras']] if len(x['registro']['listUnidadesGestoras']) > 0 else None
                valor = float(item['valorEstimado']) if ('valorEstimado' in item and item['valorEstimado'] is not None) else 0

                if codigo_unidade is not None:
                    for c in codigo_unidade:
                        if c in valor_por_unidade:
                            valor_por_unidade[c] += valor
                        elif c is not None:
                            valor_por_unidade[c] = valor

                        if c in valores_dist:
                            valores_dist[c].append(valor)
                        elif c is not None:
                            valores_dist[c] = [valor]

                if codigo_unidade is None:
                    registros_sem_unidade += 1
                    print(item['numero'])
                if valor == 0:
                    registros_sem_valor += 1
        elif tipo == 'contratos':
            contents = json.load(open(f'contratos/contratos-{ano}.json'))
            for x in contents:
                item = x['registro']['contrato']
                codigo_unidade = x['registro']['unidadeGestora']['denominacao'].strip()
                valor = float(item['valorTotal']) if ('valorTotal' in item and item['valorTotal'] is not None) else 0

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
                if valor == 0:
                    registros_sem_valor += 1
        # print('lalala')
        df = pd.DataFrame(valor_por_unidade.items(), columns=['codigoUnidadeGestora', 'valorEstimado'])
        print(df)
        # df.plot(kind='bar', x='codigoUnidadeGestora', y='valorEstimado', figsize=(10, 6))
        # print(max(valores_dist[22]))
        print(f'Ano {ano}: {len(contents)} registros')
        print(f'Ano {ano}: {registros_sem_unidade} registros sem unidade gestora') #print(registros_sem_unidade)
        print(f'Ano {ano}: {registros_sem_valor} registros sem valor estimado')
        # codigos = list(valores_dist.keys())
        # for i in range(0, len(codigos)):
        #     df_dist = pd.DataFrame([(codigo, valor) for codigo in codigos[i:i+1] for valor in valores_dist[codigo]], columns=['codigoUnidadeGestora', 'valorEstimado'])
        df_dist = pd.DataFrame([(codigo, valor) for codigo in ['Prefeitura Municipal de Florianópolis', 'Instituto de Previdência Social dos Servidores Públicos'] for valor in valores_dist.get(codigo, [])], columns=['codigoUnidadeGestora', 'valorEstimado'])
        df_dist.boxplot(column='valorEstimado', by='codigoUnidadeGestora', figsize=(10, 6))
        plt.title(f"Distribuição de valores estimados de {'licitações' if tipo == 'licitacoes' else 'contratos'} das principais unidades gestoras no ano {ano}")
        plt.yscale('log')
        plt.xlabel('Unidade Gestora')
        plt.ylabel('Valor estimado (R$)')
        plt.show()

def variacao_valores_licitacoes_e_contratos():
    valores_licitacoes = {}
    valores_contratos = {}
    count_licitacoes = {}
    count_contratos = {}
    for ano in range(2014, 2024 + 1):
        contents = json.load(open(f'licitacoes/licitacoes-{ano}.json'))
        count_licitacoes[ano] = len(contents)
        valores_licitacoes[ano] = 0
        valores_contratos[ano] = 0
        for x in contents:
            item = x['registro']['licitacao']
            valor = float(item['valorEstimado']) if ('valorEstimado' in item and item['valorEstimado'] is not None) else 0
            valores_licitacoes[ano] += float(valor)
        contents = json.load(open(f'contratos/contratos-{ano}.json'))
        count_contratos[ano] = len(contents)
        for x in contents:
            item = x['registro']['contrato']
            valor = float(item['valorTotal']) if ('valorTotal' in item and item['valorTotal'] is not None) else 0
            valores_contratos[ano] += float(valor)

    anos = list(range(2014, 2025))
    valores_l = [valores_licitacoes[ano] for ano in anos]
    valores_c = [valores_contratos[ano] for ano in anos]
    
    # Criar gráficos de variação anual
    plt.figure(figsize=(12, 6))
    plt.plot(anos, valores_l, color='blue', marker='o', label='Valores de Licitações')
    plt.plot(anos, valores_c, color='maroon', marker='s', label='Valores de Contratos')

    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Valor Total (R$)', fontsize=12)
    plt.yscale('log')
    plt.title('Variação Anual dos Valores de Licitações e Contratos (2014-2024)', fontsize=14, pad=20)

    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(anos, rotation=45)
    plt.tight_layout()
    plt.show()

    # Criar gráficos de quantidade anual
    plt.figure(figsize=(12, 6))
    bar_width = 0.35

    r1 = range(len(anos))
    r2 = [x + bar_width for x in r1]

    plt.bar(r1, [count_licitacoes[ano] for ano in anos], color='blue', width=bar_width, label='Número de Licitações')
    plt.bar(r2, [count_contratos[ano] for ano in anos], color='maroon', width=bar_width, label='Número de Contratos')

    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Quantidade', fontsize=12)
    plt.title('Quantidade Anual de Licitações e Contratos (2014-2024)', fontsize=14, pad=20)
    plt.xticks([r + bar_width / 2 for r in range(len(anos))], anos, rotation=45)

    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.3, axis='y')
    plt.tight_layout()

    plt.show()

def principais_fornecedores():
    fornecedores = {}
    for ano in range(2014, 2024 + 1):
        contents = json.load(open(f'contratos/contratos-{ano}.json'))
        for x in contents:
            fornecedor = x['registro']['fornecedor']
            soma_valores = 0
            for item in x['registro']['listItens']:
                soma_valores += float(item['valorTotal']) if ('valorTotal' in item and item['valorTotal'] is not None) else 0
            if fornecedor['pessoa']['nome'] not in fornecedores:
                fornecedores[fornecedor['pessoa']['nome']] = 0
            fornecedores[fornecedor['pessoa']['nome']] += soma_valores

    # Sort the dictionary by value in descending order
    sorted_fornecedores = sorted(fornecedores.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_fornecedores)
    # Create a bar chart using the first ten items in 'sorted_fornecedores'
    plt.figure(figsize=(12, 6))
    bar_width = 0.35

    r1 = range(10)

    names = [item[0] for item in sorted_fornecedores[:10]]
    values = [item[1] for item in sorted_fornecedores[:10]]

    plt.barh(r1, values, color='coral', height=bar_width, label='Valor Total')
    plt.gca().invert_yaxis()

    plt.xlabel('Valor em milhões de R$', fontsize=12)
    plt.ylabel('Fornecedor', fontsize=12)
    # plt.title('Valor Total de Contratos por Fornecedor (2014-2024)', fontsize=14, pad=20)
    # plt.yticks([r - bar_width / 5 for r in range(10)], names)
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f"{x / 1e6:.0f}"))
    plt.yticks([r for r in range(10)], names)

    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.3, axis='y')
    plt.tight_layout()

    plt.show()

def comparar_valor_contrato_e_empenhos():
    for ano in range(2014, 2024 + 1):
        contents = json.load(open(f'contratos/contratos-{ano}.json'))
        contents_internos = json.load(open(f'contratos-interno/contratos_1999-2017.json')) if ano <= 2017 else json.load(open(f'contratos-interno/contratos_2018-2024.json'))
        for x in contents:
            item = x['registro']['contrato']
            item_interno = next((c for c in contents_internos if c['numero'] == item['numero']), None)
            if item_interno is None:
                print(item['numero'])
            else:
                valor = float(item['valorTotal']) if ('valorTotal' in item and item['valorTotal'] is not None) else 0
                if len(item_interno['empenhos']) > 0:
                    soma_valores_empenhos = 0
                    for empenho in item_interno['empenhos']:
                        soma_valores_empenhos += float(empenho['valorPago']) if ('valorPago' in empenho and empenho['valorPago'] is not None) else 0
                        # soma_valores_empenhos += float(empenho['valorEmpenhado']) if ('valorEmpenhado' in empenho and empenho['valorEmpenhado'] is not None) else 0
                    if soma_valores_empenhos > valor:
                        print(f'{item["numero"]}: {valor} - {round(soma_valores_empenhos, 2)}')

# main('contratos')
# main('licitacoes')
# variacao_valores_licitacoes_e_contratos()
principais_fornecedores()
# comparar_valor_contrato_e_empenhos()