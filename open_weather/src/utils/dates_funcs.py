import datetime
import pytz
import time

lista_dias_da_semana = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]

dict_unidades_tempo = {
    's': 1,
    'min': 60,
    'h': 3600,
    'd': 86400
}


def easyEncodeASCII(string, replacement_format="__latin-1{0}__"):
    """
    Transforma uma string cheia de caracteres especiais numa string ASCII, substituindo cada caractere especial pelo seu
    código numérico, explicitado no padrão fornecido como parâmetro: Exemplo: "Sabão" = "Sab_latin-1173_o"
    @param string: Uma string para ser recodificada
    @param replacement_format: (opcional) o padrão para ser feita a troca de formatos
    @return: Uma string recodificada ASCII equivalente a string de entrada
    """

    # Closure que recupera o valor da codificação do caractere e formata o valor no padrão fornecido
    def getCharacterCode(char):
        valor_tabela = ord(char)
        if valor_tabela < 128:
            return str(char)
        else:
            if valor_tabela != 65533:
                return replacement_format.format(valor_tabela)
            else:
                return ''

    # Normalizamos a string
    coded_string = str(string, 'latin-1') if not isinstance(string, str) else string

    # Montamos uma string recodificada
    return ''.join([getCharacterCode(char) for char in coded_string])


def formata_intervalo_tempo(qtd_tempo, unidade_em_segundos=1, retornar_dias=False):
    # Ajustamos a quantidade de tempo passado para a unidade
    qtd_tempo = float(qtd_tempo * unidade_em_segundos)

    # Obtemos a quantidade de minutos e segundos
    m, s = divmod(qtd_tempo, 60)

    # Se tivermos 0 minutos:
    if m == 0:
        return "{:02.0f}s".format(float(s))

    # Obtemos a quantidade de horas e minutos
    h, m = divmod(m, 60)

    # Se tivermos 0 horas:
    if h == 0:
        return "{:02.0f}min {:02.0f}s".format(float(m), float(s))

    # Se não queremos retornar os dias
    if not retornar_dias:
        return "{:02.0f}h {:02.0f}min {:02.0f}s".format(float(h), float(m), float(s))

    # Obtemos a quantidade de dias e horas
    d, h = divmod(h, 24)

    # Se tivermos 0 dias:
    if d == 0:
        return "{:02.0f}h {:02.0f}min {:02.0f}s".format(float(h), float(m), float(s))

    # Retornamos a quantidade com dias (maior grão)
    return "{:2.0f}d {:02.0f}h {:02.0f}min {:02.0f}s".format(float(d), float(h), float(m), float(s))
    
def parse_datetime(datahora_entrada=None, formato_entrada=None):
    """
    Realiza o parse de uma datahora de entrada para Datetime, com diversas simplificações
    Caso qualquer um dos parâmetros seja None, é retornada a hora de agora em UTC
    @param datahora_entrada: entrada como string, inteiro, datetime, float, long, ou constante (None, "now", "agora")
    @param formato_entrada: formato da datahora de entrada, caso seja uma string de data.
    @return um objeto datetime equivalente a datahora requisitada
    """

    # Caso a entrada seja uma palavra de extensão
    if datahora_entrada in [None, "now", "agora"] or formato_entrada is None:
        datahora_entrada = datetime.datetime.now().replace(tzinfo=pytz.UTC)

    if datahora_entrada in ["today", "hoje"]:
        datahora_entrada = datetime.datetime.today().replace(tzinfo=pytz.UTC)

    # Ajustamos a data de entrada como objeto Datetime, caso já não seja
    if not isinstance(datahora_entrada, datetime.datetime):

        # Caso seja uma DATE e não datetime:
        if isinstance(datahora_entrada, datetime.date):
            datahora_entrada = datetime.datetime.combine(datahora_entrada, datetime.datetime.min.time())

        # Caso seja uma timestamp, somente se considera como INT
        elif any([isinstance(datahora_entrada, int),
                isinstance(datahora_entrada, float),
                str(datahora_entrada).replace('.', '').replace(",", "").isdigit()]):
            datahora_entrada = datetime.datetime.fromtimestamp(int(datahora_entrada))

        # Caso seja uma string, a formatamos pelo formato de entrada
        elif isinstance(datahora_entrada, str):
            datahora_entrada = easyEncodeASCII(datahora_entrada)
            if isinstance(formato_entrada, list):
                for formato in formato_entrada:
                    try:
                        datahora_entrada = datetime.datetime.strptime(datahora_entrada, formato)
                    except ValueError:
                        pass
                    else:
                        break
                if not isinstance(datahora_entrada, datetime.datetime):
                    raise TypeError("Formato invalido para parse da datahora de entrada!")
            else:
                datahora_entrada = datetime.datetime.strptime(datahora_entrada, formato_entrada)

        # Caso contrário, erro
        else:
            raise TypeError("Tipo invalido para ajuste de datahora de entrada!")

    return datahora_entrada

def localiza_datetime(datahora_entrada, zona):
    try:
        pytz.timezone(zona).localize(datahora_entrada)
        return datahora_entrada
    except ValueError:
        dado_timezone = pytz.timezone(zona)
        datahora_entrada = datahora_entrada.replace(tzinfo=dado_timezone)
        return datahora_entrada

def ajusta_fuso_horario(datahora_entrada, fuso_horario_orig, fuso_horario_dest):
    """
    Converte uma datahora de um fisop para outro, ajustando seu valor
    @param datahora_entrada: um objeto datahora (naive ou não)
    @param fuso_horario_orig: objeto pytz do fuso de origem
    @param fuso_horario_dest: objeto pytz do fuso de destino
    @return uma datahora localizada no fuso de destino, já ajustada
    """

    # Somente atualizamos o fuso horário caso o de origem seja diferente do de destino
    if fuso_horario_dest != fuso_horario_orig:
        try:
            # Localizamos a datahora de entrada para o seu fuso horário fornecido
            datahora_entrada = pytz.timezone(fuso_horario_orig).localize(datahora_entrada)

            # Ajustamos a datahora de entrada para o fuso horário de destino
            datahora_saida = datahora_entrada.astimezone(pytz.timezone(fuso_horario_dest))

        # Caso a datahora de entrada não seja naive, atualizamos seu valor de timezone
        except ValueError:
            # Criamos uma nova datetime no fuso desejado
            dado_timezone = pytz.timezone(fuso_horario_orig)
            datahora_entrada = datahora_entrada.replace(tzinfo=dado_timezone)

            # Ajustamos a datahora de entrada para o fuso horário de destino
            datahora_saida = datahora_entrada.astimezone(pytz.timezone(fuso_horario_dest))

    # Caso não tenhamos ajustes de fuso para fazer
    else:
        datahora_saida = localiza_datetime(datahora_entrada, fuso_horario_dest)

    return datahora_saida

def format_datetime_iterator(datahora_entrada, formato_saida):
    """
    Iterator que formata uma datetiem para cada formato de saida desejado
    @param datahora_entrada: um objeto datetime
    @param formato_saida: uma lista de formatos desejados (ou um único formato desejado)
    @return um ou mais objetos no formato desejado
    """

    # Caso o formato de destino seja "dia_da_semana"
    if str(formato_saida) == "dia_da_semana":

        # Retornamos o nome do dia da semana
        yield lista_dias_da_semana[datahora_entrada.weekday()]

    # Caso o formato de destino seja "datetime"
    if isinstance(formato_saida, datetime.datetime) or formato_saida == "datetime":
        yield datahora_entrada

    # Caso seja "date"
    elif isinstance(formato_saida, datetime.date) or formato_saida == "date":
        yield datahora_entrada.date()

    # Caso seja "timestamp" ou inteiro qualquer
    elif isinstance(formato_saida, int) or formato_saida == "timestamp":
        yield int(time.mktime(datahora_entrada.timetuple()))

    # Caso seja timestamp_ms
    elif formato_saida == "timestamp_ms":
        yield int(time.mktime(datahora_entrada.timetuple()) * 1000)

    # Caso seja como string
    elif isinstance(formato_saida, str):
        yield datetime.datetime.strftime(datahora_entrada, formato_saida)

    # Caso seja uma lista de formatos para retornar:
    elif isinstance(formato_saida, list):
        for formato in formato_saida:
            yield format_datetime(datahora_entrada, formato)

    # Caso contrário, erro
    else:
        raise TypeError("Tipo invalido para ajuste de datahora de saida!")


def format_datetime(datahora_entrada, formato_saida):
    """
    Wrapper ao redor do iterador de formatação de datetime
    @param datahora_entrada: objeto datetime
    @param formato_saida: uma lista de formatos desejados (ou um único formato desejado)
    @return uma lista de objetos formatados ou um único objeto formatado
    """
    if isinstance(formato_saida, list):
        return list(format_datetime_iterator(datahora_entrada, formato_saida))
    else:
        return next(format_datetime_iterator(datahora_entrada, formato_saida))
    

def ajusta_datahora(datahora_entrada,
                fuso_horario_orig='UTC',
                fuso_horario_dest='UTC',
                formato_entrada="%d/%m/%Y %H:%M:%S",
                formato_saida="%d/%m/%Y %H:%M:%S"):
    """
    Normalizador de fuso horário e formato de data

    Acerta o fuso horário de uma data (como string) em um dado fuso horário para outro fuso,
    recebendo a data no formato indicado, e a devolvendo no formato indicado

    Pode receber um único formato de data, receber diversos formatos candidatos para parsear tal data, e retorná-la em
    um ou mais formatos, localizada e ajustada para os fusos desejados.

    @param datahora_entrada: entrada como string, inteiro, datetime, float, long, ou constante (None, "now", "agora")
    @param formato_entrada: (opcional) formato da datahora de entrada, caso seja uma string de data.
    @param formato_saida: (opcional) uma lista de objetos nos formatos desejados (ou no único formato desejado)
    @param fuso_horario_orig: (opcional) um fuso horário conhecido pelo Pytz, como string
    @param fuso_horario_dest: (opcional) um fuso horário conhecido pelo Pytz, como string
    @return um ou mais objetos nos formatos desejados, expressando a hora
    """
    datahora_entrada = parse_datetime(datahora_entrada, formato_entrada)

    datahora_saida = ajusta_fuso_horario(datahora_entrada, fuso_horario_orig, fuso_horario_dest)

    return format_datetime(datahora_saida, formato_saida)