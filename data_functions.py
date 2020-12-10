import pandas as pd
import json
import getopt
import sys
import os

def create_dataframe(csv) -> pd.DataFrame:
    return pd.read_csv(csv)

def create_normalized_time_column(dataframe: pd.DataFrame):
    """
    Se crea una nueva columna para permitir ordenar por fecha de creación del trabajo.
    :param dataframe: pandas dataframe
    :return: dataframe con la nueva columna.
    """
    dataframe['job_time_normalized'] = dataframe['job_time'].apply(get_normalized_time)
    return dataframe

def get_normalized_time(job_time):
    """
    Pasamos el tiempo de la columna "job_time" a horas.
    """
    time = 0
    time_info = str(job_time).split(' ')
    if "hora" in time_info or "horas" in time_info:
        time = int(time_info[1])
    elif "día" in time_info or "días" in time_info:
        time = int(time_info[1]) * 24
    elif "semana" in time_info or "semanas" in time_info:
        time = int(time_info[1]) * 168
    elif "mes" in time_info or "meses" in time_info:
        time = int(time_info[1]) * 720
    return time

def order_jobs_by_post_date(dataframe: pd.DataFrame):
    """
    Nos permite ordenar nuestros datos por fecha.
    :param dataframe: pandas dataframe
    :return: dataframe ordenado por fecha de publicación de trabajo.
    """

    dataframe = create_normalized_time_column(dataframe)
    return dataframe.sort_values('job_time_normalized', ascending=True)

def save_dataframe_as_csv(dataframe, path: str):
    dataframe.to_csv(path, index=False)

def save_dataframe_as_json(dataframe, path: str):
    result = dataframe.to_json(orient='records', force_ascii=False)
    json_data = json.loads(result)
    save_data = json.dumps(json_data, indent=4, ensure_ascii=False).encode('utf8')
    with open(path, "w", encoding='utf-8') as file:
        file.write(save_data.decode('utf8'))

def define_options():
    """
    Utilizado para definir los distintos parametros opcionales para menejar los datos a scrapear.
    """
    csv = False
    json = False
    file_name = "data"
    results_limit = 999999
    ordered_results = False
    location_data = ('Argentina', '100446943')
    help = "--csv:  Exporta los datos en CSV. (Opción por DEFAULT)." \
           "\n--json:  Exporta los datos en JSON." \
           "\n--file_name: valor - Para definir el nombre del archivo de datos (NOMBRE POR DEFAULT: data)." \
           "\n--cant_result: valor - Sirve para definir la cantidad de registros a scrapear (DEFAULT: SIN LÍMITE)." \
           "\n--ordered_results: Sirve para ordenar o no los trabajos por fecha de publicación (DEFAULT: DESACTIVADO)." \
           "\n--world_wide: Nos permite realizar una busqueda global. (REGIÓN POR DEFAULT: ARGENTINA)." \
           "\n"
    try:
        opt, arg = getopt.getopt(sys.argv[1:],'', ['csv', 'json', 'file_name=', 'cant_result=', 'ordered_results',"world_wide","help"])
    except getopt.GetoptError:
        print("Coloque una opción válida.")
        sys.exit(0)
    for opt, arg in opt:
        if opt in ('--csv'):
            csv = True
        elif opt in ('--json'):
            json = True
        elif opt in ('--file_name'):
            if arg is not ('' or None):
                file_name = arg
            else:
                print("Debe ingresar un nombre válido.\n")
                sys.exit(0)
        elif opt in ('--cant_result'):
            try:
                results_limit = int(arg)
            except:
                print("Debe ingresar un límite válido.\n")
                sys.exit(0)
        elif opt in ('--ordered_results'):
            ordered_results = True
        elif opt in ('--world_wide'):
            location_data = ('Todo el mundo', '92000000')
        elif opt in ('--help'):
            print(help)
            sys.exit(0)

    if not csv and not json:
        csv = True

    return csv, json, file_name, results_limit, ordered_results, location_data


def delete_file(file_name: str):
    os.remove(file_name)
