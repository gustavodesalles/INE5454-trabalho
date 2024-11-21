import scrapy


class ComprasPrefeituraSpider(scrapy.Spider):
    name = 'compras-prefeitura'

    url = 'https://transparencia.e-publica.net:443/epublica-portal/rest/florianopolis/api/v1/contrato?periodo_inicial=20/10/2024&periodo_final=20/11/2024&codigo_unidade=1'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        resp_rows = response.json()
        for i in range(len(resp_rows['registros'])):
            yield resp_rows['registros'][i]
        # proxima_pagina = response.xpath('/html/body/div[1]/div/portal-shell/section/div/div[1]/div/div/div/div[3]/div[2]/a[2]').get()
        # if proxima_pagina:
        #     yield response.follow(url=proxima_pagina, callback=self.parse)