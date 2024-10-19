import scrapy
import json

class NotasFiscaisSpider(scrapy.Spider):
    name = "notas-fiscais"
    # Executar o comando "scrapy crawl notas-fiscais -o output.csv"

    # Offset inicial
    offset = 0

    # Tamanho da página
    tamanho_pagina = 20

    # Datas de início e fim
    data_inicial = ['01','09','2024']
    # data_final = ['01','09','2024']
    data_final = []

    # UFs dos fornecedores
    # ufs_fornecedores = ['PA', 'SC']
    ufs_fornecedores = []
    separador_uf = '%2C'

    # Partes da URL da request
    url1 = f'https://portaldatransparencia.gov.br/notas-fiscais/consulta/resultado?paginacaoSimples=true&tamanhoPagina={tamanho_pagina}&offset='
    url2 = '&direcaoOrdenacao=asc&colunaOrdenacao=municipioFornecedor'
    url_uf = f'&ufFornecedor={separador_uf.join(ufs_fornecedores)}' if ufs_fornecedores else ''
    url_de = f'&de={data_inicial[0]}%2F{data_inicial[1]}%2F{data_inicial[2]}' if len(data_inicial) == 3 else ''
    url_ate = f'&ate={data_final[0]}%2F{data_final[1]}%2F{data_inicial[2]}' if len(data_final) == 3 else ''
    url3 = '&colunasSelecionadas=linkDetalhamento%2CorgaoSuperiorDestinatario%2CorgaoDestinatario%2CnomeFornecedor%2CcnpjFornecedor%2CmunicipioFornecedor%2CufFornecedor%2CchaveNotaFiscal%2CvalorNotaFiscal%2CdataEmissao%2CtipoEventoMaisRecente%2Cnumero%2Cserie&_=1729086835821'
    url_nf = 'https://portaldatransparencia.gov.br/notas-fiscais/'

    # Monta URL e faz request da API
    def start_requests(self):
        url = self.url1 + str(self.offset) + self.url2 + self.url_uf + self.url_de + self.url_ate + self.url3
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Obtém informações do JSON em formato de lista de dicionários
        respData = json.loads(response.body).get('data', [])

        if len(respData) == 0 or self.offset >= 60: # Se não houver mais dados, encerra o crawl
            self.log("Consulta encerrada.")
            return

        # Prepara o segundo parse
        for item in respData:
            chave_nf = item.get('chaveNotaFiscal')
            municipio = item.get('municipioFornecedor') # Necessário pois a tela da nota fiscal individual não tem o município
            url_nf_completa = self.url_nf + chave_nf # Monta a URL da nota
            res = scrapy.Request(url=url_nf_completa, callback=self.parse2, meta={'municipio': municipio}) # Passar o município ao parse2
            yield res

        # Incrementa o offset para buscar mais notas
        self.offset += self.tamanho_pagina
        next_url = self.url1 + str(self.offset) + self.url2 + self.url_uf + self.url_de + self.url_ate + self.url3
        yield scrapy.Request(url=next_url, callback=self.parse)

    def parse2(self, response):
        chave_acesso = response.xpath('/html/body/main/div[2]/section[1]/div[1]/div[1]/span/text()').extract()
        valor = response.xpath('//html/body/main/div[2]/section[1]/div[1]/div[2]/span/text()').extract()
        modelo = response.xpath('//html/body/main/div[2]/section[1]/div[2]/div[1]/span/text()').extract()
        serie = response.xpath('//html/body/main/div[2]/section[1]/div[2]/div[2]/span/text()').extract()
        numero = response.xpath('//html/body/main/div[2]/section[1]/div[2]/div[3]/span/text()').extract()
        data_emissao = response.xpath('//html/body/main/div[2]/section[1]/div[2]/div[4]/span/text()').extract()
        natureza_operacao = response.xpath('//html/body/main/div[2]/section[1]/div[3]/div[1]/span/text()').extract()
        situacao = response.xpath('//html/body/main/div[2]/section[1]/div[3]/div[2]/span/text()').extract()
        data_ultima_modificacao = response.xpath('//html/body/main/div[2]/section[1]/div[3]/div[3]/span/text()').extract()

        # Dados do emitente
        cnpj_emitente = response.xpath('//*[@id="emitente"]/div/div/div[1]/span/a/text()').extract()
        nome_razao_social_emitente = response.xpath('//*[@id="emitente"]/div/div/div[2]/span/text()').extract()
        nome_fantasia_emitente = response.xpath('//*[@id="emitente"]/div/div/div[3]/span/text()').extract()
        inscricao_estadual_emitente = response.xpath('//*[@id="emitente"]/div/div/div[4]/span/text()').extract()
        municipio_fornecedor = response.meta.get('municipio')
        uf_emitente = response.xpath('//*[@id="emitente"]/div/div/div[5]/span/text()').extract()

        # Dados do destinatário
        cnpj_destinatario = response.xpath('//*[@id="destinatario"]/div/div[1]/div[1]/span/text()').extract()
        orgao_superior_destinatario = response.xpath('//*[@id="destinatario"]/div/div[1]/div[2]/span/text()').extract()
        orgao_entidade_vinculada = response.xpath('//*[@id="destinatario"]/div/div[1]/div[3]/span/text()').extract()
        uf_destinatario = response.xpath('//*[@id="destinatario"]/div/div[2]/div[1]/span/text()').extract()
        destino_operacao = response.xpath('//*[@id="destinatario"]/div/div[2]/div[2]/span/text()').extract()
        consumidor_final = response.xpath('//*[@id="destinatario"]/div/div[2]/div[3]/span/text()').extract()
        presenca_comprador = response.xpath('//*[@id="destinatario"]/div/div[2]/div[4]/span/text()').extract()
        indicador_ie = response.xpath('//*[@id="destinatario"]/div/div[3]/div[1]/span/text()').extract()

        yield {
            "CHAVE DE ACESSO": chave_acesso,
            "MODELO": modelo,
            "SÉRIE": serie,
            "NÚMERO": numero,
            "NATUREZA DA OPERAÇÃO": natureza_operacao,
            "DATA EMISSÃO": data_emissao,
            "EVENTO MAIS RECENTE": situacao,
            "DATA/HORA EVENTO MAIS RECENTE": data_ultima_modificacao,
            "CPF/CNPJ EMITENTE": cnpj_emitente,
            "RAZÃO SOCIAL EMITENTE": nome_razao_social_emitente,
            "NOME FANTASIA EMITENTE": nome_fantasia_emitente,
            "INSCRIÇÃO ESTADUAL EMITENTE": inscricao_estadual_emitente,
            "UF EMITENTE": uf_emitente,
            "MUNICÍPIO EMITENTE": municipio_fornecedor,
            "CNPJ DESTINATÁRIO": cnpj_destinatario,
            "ÓRGÃO SUPERIOR DESTINATÁRIO": orgao_superior_destinatario,
            "ÓRGÃO ENTIDADE VINCULADA": orgao_entidade_vinculada,
            "UF DESTINATÁRIO": uf_destinatario,
            "INDICADOR IE DESTINATÁRIO": indicador_ie,
            "DESTINO DA OPERAÇÃO": destino_operacao,
            "CONSUMIDOR FINAL": consumidor_final,
            "PRESENÇA DO COMPRADOR": presenca_comprador,
            "VALOR NOTA FISCAL": valor
        }