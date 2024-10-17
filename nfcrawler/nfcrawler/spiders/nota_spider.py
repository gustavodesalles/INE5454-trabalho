import scrapy

class NotaSpider(scrapy.Spider):
    name = 'nota'
    start_urls = [
        'https://portaldatransparencia.gov.br/notas-fiscais/consulta?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2CorgaoSuperiorDestinatario%2CorgaoDestinatario%2CnomeFornecedor%2CcnpjFornecedor%2CmunicipioFornecedor%2CufFornecedor%2CchaveNotaFiscal%2CvalorNotaFiscal%2CdataEmissao%2CtipoEventoMaisRecente%2Cnumero%2Cserie&ordenarPor=municipioFornecedor&direcao=asc'
    ]

    #usar requests para obter chaves das notas fiscais e municípios emitentes do json
    #depois, chamar próximas notas enquanto o botão estiver habilitado
    #finalmente, acionar o outro spider para todas as chaves

    def parse(self, response):
        titulo = response.xpath('//html/body/main/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[8]/span').extract()
        yield {'titulo': titulo}