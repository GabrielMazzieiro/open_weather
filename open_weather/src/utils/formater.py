from .dates_funcs import ajusta_datahora


def format_api_response(api_response):

    # Recupera a diferença de timezone 
    timezone: int = api_response['city']['timezone']

    #cria a estrutura do dicionario final que será salvo no mongo
    dict_final = {
    "city": api_response['city']['name'],
    'country':api_response['city']['country'],
    'insert_datetime_int_utc':ajusta_datahora('agora', formato_saida='timestamp'),
    'insert_datetime_str_utc':ajusta_datahora('agora', formato_saida="%d/%m/%Y %H:%M:%S") 
    }

    #seleciona os dados principais
    summary = [dict(
        datetime_str_utc = ajusta_datahora(dado['dt'], formato_entrada="timestamp", formato_saida="%d/%m/%Y %H:%M:%S"),
        datetime_int_utc = dado['dt'],
        datetime_int_local = (dado['dt'] + timezone),
        datetime_str_local = ajusta_datahora((dado['dt'] + timezone), formato_entrada="timestamp", formato_saida="%d/%m/%Y %H:%M:%S"),
        local_date = ajusta_datahora((dado['dt'] + timezone), formato_entrada="timestamp", formato_saida="%d/%m/%Y"),
        feels_like = dado['main']['feels_like'],
        temp_min = dado['main']['temp_min'],
        temp_max = dado['main']['temp_max'],
        humidity = dado['main']['humidity'],
        weather = dado['weather'][0]['description'],
        rain_probability = dado['pop']
        
    ) for dado in api_response["list"]]

    #cria um dict de datas retornadas com valores de lista vazios
    dates = {d: list() for d in set([ ajusta_datahora((data['dt'] + timezone), formato_entrada="timestamp", formato_saida="%d/%m/%Y") for data in api_response["list"]])}

    #popula as listas de acordo com a data referente
    for k, v in dates.items():
        for data in summary:
            if data['local_date'] == k:
                v.append(data)

    #adiciona os dados organizados no dict_final
    dict_final.update(dates)

    return dict_final