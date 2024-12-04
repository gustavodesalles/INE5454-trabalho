import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def main():
    for ano in range(2014, datetime.today().year + 1): # muitos registros antes de 2014 não têm valor
        contents = json.load(open(f'licitacoes/licitacoes-{ano}.json'))

        xAxis = []
        yAxis = []
        for i in range(len(contents)):
            if contents[i]['registro']['licitacao']['valorEstimado'] != None:
                xAxis.append(datetime.strptime(contents[i]['registro']['licitacao']['dataEmissao'], '%Y-%m-%d'))
                yAxis.append(contents[i]['registro']['licitacao']['valorEstimado'])

        fig = plt.figure(figsize=(20, 10))
        plt.bar(xAxis, yAxis, color='blue', width=2)
        plt.xlabel('Data')
        plt.ylabel('Valor total')
        plt.title(f'Contratos de {ano}')
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=[3, 6, 9, 12]))
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)

        plt.show()
        fig.savefig(f'graficos/licitacoes-{ano}.png')

if __name__ == '__main__':
    main()