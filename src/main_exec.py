from config import Config
from dict_data_collect import Notas, Participante

def main():
    path_dict = Config.PATH_DICT
    sheet_name_participante = Config.SHEET_NAME[0]
    sheet_name_notas = Config.SHEET_NAME[1]

    participante = Participante(path_dict, sheet_name_participante)
    notas = Notas(path_dict, sheet_name_notas)

    list_part = participante.save_copy_fields()
    list_result = notas.save_copy_fields()

    print("Participantes:", list_part)
    print("Notas:", list_result)


if __name__ == "__main__":
    main()