import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    pagina_inicial = 1
    pagina_final = 10

    def parse(self, response):
        produtos = response.css('div.ui-search-result__content')

        for produto in produtos:

            precos = produto.css('span.andes-money-amount__fraction::text').getall()

            centavos = produto.css('span.andes-money-amount__cents::text').getall()

            yield {
                'marca': produto.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                'nome': produto.css('h2.ui-search-item__title::text').get(),
                'preco_antigo_reais': precos[0] if len(precos) > 0 else None,
                'preco_antigo_centavos': centavos[0] if len(centavos) > 0 else None,
                'preco_atual_reais': precos[1] if len(precos) > 1 else None,
                'preco_atual_centavos': centavos[1] if len(centavos) > 1 else None,
                'numero_de_avaliacoes_de_comentarios': produto.css('span.ui-search-reviews__rating-number::text').get(),
                'quantidade_de_avaliacoes': produto.css('span.ui-search-reviews__amount::text').get()
            }
        
        if self.pagina_inicial < self.pagina_final:
            proxima_pagina = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if proxima_pagina:
                self.pagina_inicial += 1
                yield scrapy.Request(url=proxima_pagina, callback=self.parse)