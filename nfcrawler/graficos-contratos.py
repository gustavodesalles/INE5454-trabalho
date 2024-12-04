import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def main():
    for ano in range(1999, datetime.today().year + 1):
        contents = json.load(open(f'contratos/contratos-{ano}.json'))

        xAxis = []
        yAxis = []
        for i in range(len(contents)):
            if contents[i]['registro']['contrato']['valorTotal'] != None:
                xAxis.append(datetime.strptime(contents[i]['registro']['contrato']['assinatura'], '%Y-%m-%d'))
                yAxis.append(contents[i]['registro']['contrato']['valorTotal'])

        fig = plt.figure(figsize=(20, 10))
        plt.bar(xAxis, yAxis, color='maroon', width=2)
        plt.xlabel('Data')
        plt.ylabel('Valor total')
        plt.title(f'Contratos de {ano}')
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=[3, 6, 9, 12]))
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)

        plt.show()
        fig.savefig(f'graficos/contratos-{ano}.png')

if __name__ == '__main__':
    main()