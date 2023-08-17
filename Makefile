

build:
	python scraper_siglas-uc/scraper_siglas.py
	python scraper_siglas-uc/scraper_detalles.py
	python scraper_siglas-uc/menus.py
	python scraper_siglas-uc/detalles_sp.py
	scrapy crawl programas
	python scraper_siglas-uc/programas.py
	python modelo/crear_archivos.py
	
