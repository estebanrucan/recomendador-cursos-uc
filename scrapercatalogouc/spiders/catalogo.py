import scrapy
import codecs
import json

with codecs.open("./scraper_siglas-uc/outputs/siglas.json", "rU", encoding="utf-8") as js:
    data = json.load(js)

siglas = list()

for line in data.values():
    siglas += line


class CatalogoUcSpider(scrapy.Spider):
    name = "programas"
    start_urls = [
        "https://catalogo.uc.cl/"
    ]
    custom_settings = {
        'FEEDS': {
            'scraper_siglas-uc/outputs/programas.json': {
                'format'            : 'json',
                'encoding'          : 'utf-8',
                'store_empty'       : False,
                'fields'            : None,
                'indent'            : 4,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            },
            'scraper_siglas-uc/outputs/programas.csv': {
                'format'            : 'csv',
                'encoding'          : 'utf-8',
                'store_empty'       : False,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            }
        },
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT"    : "Esteban"
    }

    def parse(self, response):

        base_url = lambda ID: f"index.php?tmpl=component&option=com_catalogo&view=programa&sigla={ID}"

        for escuela, siglas in data.items():
            for sigla in siglas:
                yield response.follow(
                    base_url(sigla),
                    callback=self.parse_programa,
                    cb_kwargs= {"sigla": sigla, "escuela": escuela}
                )

    def parse_programa(self, response, **kwargs):
        sigla       = kwargs["sigla"]
        escuela     = kwargs["escuela"]
        description = " ".join(response.xpath("//pre/text()").extract())

        yield {
            "escuela"    : escuela,
            "sigla"      : sigla,
            "description": description
        }