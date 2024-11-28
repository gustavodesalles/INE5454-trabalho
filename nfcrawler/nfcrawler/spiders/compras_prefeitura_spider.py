import datetime

import scrapy


class ContratosPrefeituraSpider(scrapy.Spider):
    name = 'contratos-prefeitura'

    url = 'https://transparencia.e-publica.net:443/epublica-portal/rest/florianopolis/api/v1/contrato'
    ano_inicial = 1999
    data_atual = datetime.date.today()
    ano_final = data_atual.year
    codigo_unidade = None
    # codigo_unidade = 1

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
        for ano in range(self.ano_inicial, self.ano_final + 1):
            if ano == self.ano_final:
                url = self.url + f'?periodo_inicial=01/01/{ano}&periodo_final={self.data_atual.day}/{self.data_atual.month}/{self.data_atual.year}'
            else:
                url = self.url + f'?periodo_inicial=01/01/{ano}&periodo_final=31/12/{ano}'
            if self.codigo_unidade:
                url += f'&codigo_unidade={self.codigo_unidade}'
            res = scrapy.Request(url=url, callback=self.parse)
            yield res

    def parse(self, response):
        resp_rows = response.json()
        for i in range(len(resp_rows['registros'])):
            yield resp_rows['registros'][i]

class LicitacoesPrefeituraSpider(scrapy.Spider):
    name = 'licitacoes-prefeitura'

    url = 'https://transparencia.e-publica.net:443/epublica-portal/rest/florianopolis/api/v1/licitacao'
    ano_inicial = 2024
    ano_final = ano_inicial
    codigo_unidade = None
    # codigo_unidade = 1

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