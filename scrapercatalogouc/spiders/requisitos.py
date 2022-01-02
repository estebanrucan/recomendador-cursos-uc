import scrapy
import codecs
import json
import os

with codecs.open(os.path.join("scraper_siglas-uc", "outputs", "siglas.json"), "rU", encoding="utf-8") as js:
    data = json.load(js)

siglas = list()

for line in data.values():
    siglas += line


class RequisitosSpider(scrapy.Spider):
    name = "requisitos"
    start_urls = [
        "https://catalogo.uc.cl/"
    ]
    custom_settings = {
        "FEEDS": {
            "scrapercatalogouc/outputs/requisitos.json": {
                "format"            : "json",
                "encoding"          : "utf-8",
                "store_empty"       : False,
                "fields"            : None,
                "indent"            : 4,
                "item_export_kwargs": {
                    "export_empty_fields": True,
                },
            },
            "scrapercatalogouc/outputs/requisitos.csv": {
                "format"            : "csv",
                "encoding"          : "utf-8",
                "store_empty"       : False,
                "item_export_kwargs": {
                    "export_empty_fields": True,
                },
            }
        },
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT"    : "Esteban"
    }

    def parse(self, response):

        base_url = lambda ID: f"index.php?tmpl=component&option=com_catalogo&view=requisitos&sigla={ID}"

        for sigla in siglas:
            yield response.follow(
                base_url(sigla),
                callback  = self.parse_requisitos,
                cb_kwargs = {"sigla": sigla}
            )

    def parse_requisitos(self, response, **kwargs):
        sigla       = kwargs["sigla"]
        requisitos  = response.xpath("//span/text()").extract()

        yield {
            "sigla"                                        : sigla,
            "Prerrequisitos"                               : requisitos[0],
            "Relación entre prerrequisitos y restricciones": requisitos[1],
            "Restricciones"                                : requisitos[2],
            "Equivalencias"                                : requisitos[3]
        }