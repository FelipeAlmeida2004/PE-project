from config import Config
from dict_data_collect import Notas, Participante
from analises.freq_table import FrequencyTable

def main():

    #  Definição dos caminhos dos arquivos e sheets
    path_dict = Config.PATH_DICT
    sheet_name_participante = Config.SHEET_NAME[0]
    sheet_name_notas = Config.SHEET_NAME[1]
    path_part = Config.DATA[0]
    path_result = Config.DATA[1]


    # =================== COLETA =====================

    # Coleta dos campos de Participantes e Resultados
    participante = Participante(path_dict, sheet_name_participante)
    notas = Notas(path_dict, sheet_name_notas)

    # len 38 -> 0-17(info-part), 16-38(socio)
    list_part = participante.save_copy_fields()

    # len 42 -> 0-1(info-part), 2-10(info-escola), 11-14(info-local), 15-35(info-obj), 36-42(info-redacao)
    list_result = notas.save_copy_fields() 

    print("Participantes: \n", list_part)
    print("Notas: \n", list_result)

    # =================== ANALISE =====================

    # Analise de frequência de faixa salárial -> Campo["Q007"]
    freq_table = FrequencyTable(path_part, list_part[21])
    freq_table.execute()

if __name__ == "__main__":
    main()