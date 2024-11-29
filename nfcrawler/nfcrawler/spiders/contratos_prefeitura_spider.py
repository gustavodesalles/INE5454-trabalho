import datetime

import scrapy
from scrapy.crawler import CrawlerProcess

class ContratosPrefeituraSpider(scrapy.Spider):
    name = 'contratos-prefeitura'

    url = 'https://transparencia.e-publica.net:443/epublica-portal/rest/florianopolis/api/v1/contrato'
    codigo_unidade = None

    def __init__(self, ano_inicial, ano_final, *args, **kwargs):
        super(ContratosPrefeituraSpider, self).__init__(*args, **kwargs)
        self.ano_inicial = int(ano_inicial)
        self.ano_final = int(ano_final)

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
        for ano in range(self.ano_inicial, self.ano_final + 1):
            url = self.url + f'?periodo_inicial=01/01/{ano}&periodo_final=31/12/{ano}'
            if self.codigo_unidade:
                url += f'&codigo_unidade={self.codigo_unidade}'
            res = scrapy.Request(url=url, callback=self.parse)
            yield res

    def parse(self, response):
        resp_rows = response.json()
        for i in range(len(resp_rows['registros'])):
            yield resp_rows['registros'][i]

def main():
    while True:
        ano_inicial = input("Digite o ano inicial: ")
        ano_final = input("Digite o ano final: ")
        if int(ano_inicial) <= int(ano_final):
            break
        print("O ano final não deve ser menor que o ano inicial. Tente novamente.")

    process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_URI': f'contratos-prefeitura-{ano_inicial if ano_inicial == ano_final else f"{ano_inicial}-{ano_final}"}.json'
    })

    process.crawl(ContratosPrefeituraSpider, ano_inicial=ano_inicial, ano_final=ano_final)
    process.start()

if __name__ == "__main__":
    main()