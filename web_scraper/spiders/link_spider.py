import scrapy


class LinkSpider(scrapy.Spider):
    name = "links"
    start_urls = [
        'https://exrx.net/Lists/ExList/NeckWt',
        'https://exrx.net/Lists/KettlebellExercises',
        'https://exrx.net/Lists/ExList/ShouldWt',
        'https://exrx.net/Lists/ExList/ArmWt',
        'https://exrx.net/Lists/ExList/ForeArmWt',
        'https://exrx.net/Lists/ExList/BackWt',
        'https://exrx.net/Lists/ExList/ChestWt',
        'https://exrx.net/Lists/ExList/WaistWt',
        'https://exrx.net/Lists/ExList/HipsWt',
        'https://exrx.net/Lists/ExList/ThighWt',
        'https://exrx.net/Lists/ExList/CalfWt',
        'https://exrx.net/Lists/OlympicWeightlifting',
        'https://exrx.net/Lists/PowerExercises',
        'https://exrx.net/Lists/CardioExercises',
        'https://exrx.net/Lists/OtherExercises',
    ]

    def parse(self, response, **kwargs):
        for ref in response.css('div.col-sm-6 a::attr(href)').getall():
            yield {
                'dir': response.urljoin(ref)
            }
