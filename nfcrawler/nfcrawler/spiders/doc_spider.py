import scrapy

class DocSpider(scrapy.Spider):
    name = 'doc_spider'
    start_urls = [
        'https://portaldatransparencia.gov.br/notas-fiscais/52241036629597000185550010000038721421323220'
    ]

    def parse(self, response):
        chave_acesso = response.xpath('/html/body/main/div[2]/section[1]/div[1]/div[1]/span/text()').extract()
        valor = response.xpath('//html/body/main/div[2]/section[1]/div[1]/div[2]/span/text()').extract()
        modelo = response.xpath('//html/body/main/div[2]/section[1]/div[2]/div[1]/span/text()').extract()
        serie = response.xpath('//html/body/main/div[2]/section[1]/div[2]/div[2]/span/text()').extract()
        numero = response.xpath('//html/body/main/div[2]/section[1]/div[2]/div[3]/span/text()').extract()
        data_emissao = response.xpath('//html/body/main/div[2]/section[1]/div[2]/div[4]/span/text()').extract()
        natureza_operacao = response.xpath('//html/body/main/div[2]/section[1]/div[3]/div[1]/span/text()').extract()
        situacao = response.xpath('//html/body/main/div[2]/section[1]/div[3]/div[2]/span/text()').extract()
        data_ultima_modificacao = response.xpath('//html/body/main/div[2]/section[1]/div[3]/div[3]/span/text()').extract()

        #DADOS DO EMITENTE
        cnpj_emitente = response.xpath('//*[@id="emitente"]/div/div/div[1]/span/a/text()').extract()
        nome_razao_social_emitente = response.xpath('//*[@id="emitente"]/div/div/div[2]/span/text()').extract()
        nome_fantasia_emitente = response.xpath('//*[@id="emitente"]/div/div/div[3]/span/text()').extract()
        inscricao_estadual_emitente = response.xpath('//*[@id="emitente"]/div/div/div[4]/span/text()').extract()
        uf_emitente = response.xpath('//*[@id="emitente"]/div/div/div[5]/span/text()').extract()

        #DADOS DO DESTINATÁRIO
        cnpj_destinatario = response.xpath('//*[@id="destinatario"]/div/div[1]/div[1]/span/text()').extract()
        orgao_superior_destinatario = response.xpath('//*[@id="destinatario"]/div/div[1]/div[2]/span/text()').extract()
        orgao_entidade_vinculada = response.xpath('//*[@id="destinatario"]/div/div[1]/div[3]/span/text()').extract()
        uf_destinatario = response.xpath('//*[@id="destinatario"]/div/div[2]/div[1]/span/text()').extract()
        destino_operacao = response.xpath('//*[@id="destinatario"]/div/div[2]/div[2]/span/text()').extract()
        consumidor_final = response.xpath('//*[@id="destinatario"]/div/div[2]/div[3]/span/text()').extract()
        presenca_comprador = response.xpath('//*[@id="destinatario"]/div/div[2]/div[4]/span/text()').extract()
        indicador_ie = response.xpath('//*[@id="destinatario"]/div/div[3]/div[1]/span/text()').extract()

        yield {
            'chave_acesso': chave_acesso,
            'valor': valor,
            'modelo': modelo,
            'serie': serie,
            'numero': numero,
            'data_emissao': data_emissao,
            'natureza_operacao': natureza_operacao,
            'situacao': situacao,
            'data_ultima_modificacao': data_ultima_modificacao,
            'cnpj_emitente': cnpj_emitente,
            'nome_fantasia_emitente': nome_fantasia_emitente,
            'uf_emitente': uf_emitente,
            'cnpj_destinatario': cnpj_destinatario,
            'orgao_superior_destinatario': orgao_superior_destinatario,
            'orgao_entidade_vinculada': orgao_entidade_vinculada,
            'uf_destinatario': uf_destinatario,
            'destino_operacao': destino_operacao,
            'consumidor_final': consumidor_final,
            'presenca_comprador': presenca_comprador,
            'indicador_ie': indicador_ie
        }