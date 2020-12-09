import pandas as pd
import json
import getopt
import sys
import os

def create_dataframe(csv) -> pd.DataFrame:
    return pd.read_csv(csv)

def create_normalized_time_column(dataframe: pd.DataFrame):
    dataframe['job_time_normalized'] = dataframe['job_time'].apply(get_normalized_time)
    return dataframe

def get_normalized_time(job_time): # Pasamos el tiempo desde que se posteo el trabajo a horas.
    time = 0
    time_info = job_time.split(' ')
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
    csv = False
    json = False
    nombre = "data"
    results_limit = 999999
    ordered_results = False
    help = "--csv:  Exporta los datos en CSV. (Opción por DEFAULT)." \
           "\n--json:  Exporta los datos en JSON." \
           "\n--nombre: valor - Para definir el nombre del archivo de datos (NOMBRE POR DEFAULT: data)." \
           "\n--cant_result: valor - Sirve para definir la cantidad de registros a scrapear (DEFAULT: SIN LÍMITE)." \
           "\n--ordered_results: Sirve para ordenar o no los trabajos por fecha de publicación (DEFAULT: DESACTIVADO)." \
           "\n"
    try:
        opt, arg = getopt.getopt(sys.argv[1:],'', ['csv', 'json', 'nombre=', 'cant_result=', 'ordered_results',"help"])
    except getopt.GetoptError:
        print("Coloque una opción válida.")
        sys.exit(0)
    for opt, arg in opt:
        if opt in ('--csv'):
            csv = True
        elif opt in ('--json'):
            json = True
        elif opt in ('--nombre'):
            if arg is not ('' or None):
                nombre = arg
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
        elif opt in ('--help'):
            print(help)
            sys.exit(0)

    if not csv and not json:
        csv = True

    return csv, json, nombre, results_limit, ordered_results


def delete_file(file_name: str):
    os.remove(file_name)