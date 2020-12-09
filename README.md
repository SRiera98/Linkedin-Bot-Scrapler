# Sistema de Tickets
### Herramienta de scraping hecha con el framework:
[![N|Solid](https://scrapy.org/img/scrapylogo.png)](https://scrapy.org/)

#### Se realizó scraping de los trabajos de Linkeding Argentina para facilitar la exportacion de estos datos a CSV o a JSON.
# Ayuda y uso básico de la aplicación
Al momento de ejecutar **main.py** se realiza de la siguiente manera:

  - ######  **python3 main.py argumentos (definidos abajo)**

### Comandos o argumentos disponibles


	--csv:  Exporta los datos en CSV. (Opción por DEFAULT).
	--json:  Exporta los datos en JSON.
	--nombre: valor - Para definir el nombre del archivo de datos (NOMBRE POR DEFAULT: data).
	--cant_result: valor - Sirve para definir la cantidad de registros a scrapear (DEFAULT: SIN LÍMITE).
	--results_ordered: Sirve para ordernar o no los trabajos por fecha de publicación (DEFAULT: DESACTIVADO).
    --help: Nos permite obtener información acerca de los comandos.
