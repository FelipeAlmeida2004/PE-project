from config import Config
from dict_data_collect import Notas, Participante
from analises.freq_table import FrequencyTable
from analises.freq_table_cont import FrequencyTableContinua
from analises.estat_descritiva import EstatisticaDescritiva
from analises.graficos import Graficos
from analises.tabela_contingencia import TabelaContingencia


def main():

    # =================== CONFIGURAÇÕES =====================
    path_dict   = Config.PATH_DICT
    path_part   = Config.DATA[0]   # CSV de participantes
    path_result = Config.DATA[1]   # CSV de resultados/notas

    participante = Participante(path_dict, Config.SHEET_NAME[0])
    notas        = Notas(path_dict, Config.SHEET_NAME[1])

    list_part   = participante.save_copy_fields()
    list_result = notas.save_copy_fields()

    # Campos de notas (ajuste os índices conforme seu dicionário)
    NOTAS_FIELDS = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]

    # Campos qualitativos de participantes
    CAMPO_UF          = "SG_UF_PROVA"       # Estado (nominal)       # Língua estrangeira (nominal)
    CAMPO_RENDA       = "Q006"               # Renda familiar (ordinal)
    CAMPO_ESC_PAI     = "Q001"               # Escolaridade do pai (ordinal)
    CAMPO_ESC_MAE     = "Q002"               # Escolaridade da mãe (ordinal)
    CAMPO_SEXO        = "TP_SEXO"

    # =================== [✅] FREQ. QUALITATIVA (Renda) =====================
    print("\n>>> [1/7] Tabela de Frequência – Renda Familiar")
    freq_renda = FrequencyTable(path_part, CAMPO_RENDA)
    freq_renda.execute(plot_type="bar")

    # =================== [2/7] FREQ. CONTÍNUA (Notas) =====================
    print("\n>>> [2/7] Tabela de Frequência Contínua – Notas")
    for nota in NOTAS_FIELDS:
        print(f"\n  >> {nota}")
        ftc = FrequencyTableContinua(path_result, nota)
        ftc.execute()

    # =================== [3/7] ESTATÍSTICAS DESCRITIVAS =====================
    # Média, Mediana, Moda + Variância, Desvio Padrão + Amplitude, IQR
    # Quartis, Percentis → tudo junto em EstatisticaDescritiva
    print("\n>>> [3/7] Estatísticas Descritivas – Notas")
    ed = EstatisticaDescritiva(path_result, NOTAS_FIELDS)
    ed.execute(save_csv=True, save_boxplot=True, save_histogramas=True)

    # =================== [4/7] GRÁFICOS DE BARRAS / PIZZA =====================
    print("\n>>> [4/7] Gráficos – Variáveis Qualitativas")
    g = Graficos(path_part)

    # UF (muitos valores → top 10)
    g.execute_qualitativas(CAMPO_UF, top_n=10)


    # Renda familiar
    g.execute_qualitativas(CAMPO_RENDA)

    # Escolaridade pai e mãe
    g.execute_qualitativas(CAMPO_ESC_PAI)
    g.execute_qualitativas(CAMPO_ESC_MAE)
    g.execute_qualitativas(CAMPO_SEXO)

    g = Graficos(path_result)
    # Língua estrangeira (variável qualitativa presente no CSV de resultados/notas)
    g.execute_qualitativas("TP_LINGUA")

    # =================== [5/7] DIAGRAMA DE DISPERSÃO =====================
    print("\n>>> [5/7] Diagramas de Dispersão – Notas")
    g_notas = Graficos(path_result)

    # Ciências da Natureza × Matemática (espera-se correlação alta)
    g_notas.execute_dispersao("NU_NOTA_CN", "NU_NOTA_MT", amostra=10_000)

    # Ciências Humanas × Linguagens
    g_notas.execute_dispersao("NU_NOTA_CH", "NU_NOTA_LC", amostra=10_000)

    # Redação × Nota média objetiva
    g_notas.execute_dispersao("NU_NOTA_MT", "NU_NOTA_REDACAO", amostra=10_000)

    # =================== [6/7] TABELA DE CONTINGÊNCIA =====================
    print("\n>>> [6/7] Tabela de Contingência – Sexo × Renda")
    tc = TabelaContingencia(path_part, CAMPO_SEXO, CAMPO_RENDA)
    tc.execute()

    # Escolaridade Mãe × Renda (variáveis ordinais relacionadas)
    print("\n>>> [6/7] Tabela de Contingência – Escolaridade Mãe × Renda")
    tc2 = TabelaContingencia(path_part, CAMPO_ESC_MAE, CAMPO_RENDA)
    tc2.execute()

    print("\n✅ Todas as análises concluídas!")


if __name__ == "__main__":
    main()