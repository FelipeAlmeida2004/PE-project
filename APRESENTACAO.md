# Diretrizes da Apresentação — Análise Descritiva do ENEM 2024

> **Duração total:** 30–35 minutos
> **Apresentadores:** 7
> **Tempo médio por bloco:** 4–6 minutos
> **Tom:** estritamente descritivo — descrever o que os números mostram, **sem opinião, sem inferência causal, sem julgamento de valor**.

---

## Visão geral do projeto

Projeto da disciplina de Probabilidade e Estatística que aplica técnicas de **estatística descritiva** sobre os microdados oficiais do ENEM 2024 (INEP). O pipeline (em Python/pandas/matplotlib) lê os CSVs de `PARTICIPANTES_2024` e `RESULTADOS_2024`, produz tabelas de frequência, medidas-resumo, gráficos e tabelas de contingência salvos em `src/database/2024/ANALISES/`.

**Tamanho da base após `dropna` por variável:**
- Participantes totais: **4.332.935**
- Notas CN / MT (dia 2): **3.004.981**
- Notas CH / LC / Redação (dia 1): **3.167.955**

---

## Distribuição dos blocos (7 apresentadores)

| # | Apresentador | Bloco | Duração |
|---|---|---|---|
| 1 | P1 | Introdução, fonte dos dados, captura | ~5 min |
| 2 | P2 | Vieses, limitações e variáveis analisadas | ~5 min |
| 3 | P3 | Análise qualitativa (frequências, barras, pizza) | ~5 min |
| 4 | P4 | Análise quantitativa contínua (notas, histogramas, Sturges) | ~5 min |
| 5 | P5 | Medidas-resumo e dispersão (média, mediana, moda, variância, quartis, boxplot) | ~5–6 min |
| 6 | P6 | Relações entre variáveis (dispersão, contingência) | ~5 min |
| 7 | P7 | Conclusão e encerramento | ~3–4 min |

---

# 🎤 BLOCO 1 — Introdução e Captura dos Dados *(P1 — ~5 min)*

### Slide 1 — Capa
- Título: *Análise Descritiva dos Microdados do ENEM 2024*
- Disciplina, instituição, integrantes, data.

### Slide 2 — O que é o ENEM e Objetivo do trabalho
- Exame Nacional do Ensino Médio, aplicado pelo INEP.
- Avalia conhecimentos em 4 áreas + Redação (2 dias de prova).
- Edição 2024 → base usada neste trabalho.
- Descrever, com técnicas de estatística descritiva, o perfil dos participantes e o desempenho nas provas.
- **Não há inferência causal nem comparação de mérito** — apenas descrição.

### Slide 3 — Fonte dos dados
- Microdados oficiais do INEP — `Microdados ENEM 2024` (portal `gov.br/inep`).
- Arquivos disponibilizados: `PARTICIPANTES_2024.csv`, `RESULTADOS_2024.csv`, `ITENS_PROVA_2024.csv`.
- Acompanha dicionário (`Dicionário_Microdados_Enem_2024.xlsx`), Leia-me, edital, manual de redação, matriz de referência e cadernos/gabaritos.

### Slide 4 — Como os dados foram capturados
- Coleta na **inscrição** (questionário socioeconômico Q001–Q023, dados demográficos, local de prova) — autodeclarado pelo candidato.
- Coleta no **dia da prova** (presença, treineiro, tipo de prova, língua estrangeira).
- **Notas (TRI)**: itens objetivos corrigidos por gabarito + cálculo de proficiência via *Teoria de Resposta ao Item*; redação por dois corretores humanos + terceiro em caso de discrepância.
- Anonimização e divulgação pública pelo INEP após processamento.

### Slide 5 — Pipeline do projeto
Esquema simples:
```
CSV INEP  →  pandas (leitura, dropna)
          →  Frequências / Estatísticas / Gráficos
          →  CSVs + PNGs em src/database/2024/ANALISES/
```
Bibliotecas: `pandas`, `numpy`, `matplotlib`, `scipy`.

---

# 🎤 BLOCO 2 — Vieses, Limitações e Variáveis *(P2 — ~5 min)*

### Slide 6 — Vieses inerentes à base
Apresentar **factualmente**, sem julgar:

1. **Viés de autosseleção** — só estão na base quem se inscreveu no ENEM. Não representa toda a população brasileira em idade escolar nem todos os concluintes do Ensino Médio.
2. **Viés de abstenção** — ~27% dos inscritos não comparecem ou não geram nota válida. Comparar `N=4.332.935` (inscritos) vs `N≈3.000.000` (com nota).
3. **Notas zeradas / faltas** — provas em branco, eliminação, ou redação fora do tema geram nota `0`, deslocando a média e gerando moda 0 em CH e Redação.
4. **Variáveis autodeclaradas** — sexo, cor/raça, renda, escolaridade dos pais → sujeitas a erro de preenchimento.
5. **Diferença entre Dia 1 e Dia 2** — N(CH/LC/RED) = 3.167.955 > N(CN/MT) = 3.004.981 → ~163 mil candidatos compareceram só no 1º dia.
6. **Cobertura geográfica desigual** — SP/MG/BA concentram volume; estados pequenos têm massa amostral menor.
7. **Renda (Q006) binária na base disponível** — neste recorte só aparecem categorias **A** e **B**, limitando granularidade da análise de renda.

### Slide 7 — Limitações metodológicas do projeto
- Análise estritamente **descritiva** (sem testes inferenciais robustos além do χ² na contingência).
- Diagramas de dispersão usam **amostra de 10.000 pontos** para viabilidade visual (random_state=42).
- Bins do histograma definidos pela **regra de Sturges**: `k = 1 + 3,322·log₁₀(n)`.

### Slide 8 — Classificação das variáveis analisadas

| Tipo | Subtipo | Variáveis |
|---|---|---|
| **Qualitativa** | Nominal | `SG_UF_PROVA` (UF), `TP_LINGUA` (língua estrangeira), `TP_SEXO` |
| **Qualitativa** | Ordinal | `Q001`/`Q002` (escolaridade pai/mãe), `Q006` (renda familiar) |
| **Quantitativa** | Discreta | `TP_FAIXA_ETARIA`, `NU_NOTA_REDACAO` |
| **Quantitativa** | Contínua | `NU_NOTA_CN`, `NU_NOTA_CH`, `NU_NOTA_LC`, `NU_NOTA_MT` |

### Slide 9 — Checklist das análises realizadas
Listar (do README) o que será mostrado nos próximos blocos:
- Tabela de Frequência (qualitativa e contínua)
- Histograma
- Média / Mediana / Moda
- Variância / Desvio Padrão
- Amplitude / IQR
- Quartis / Percentis
- Boxplot
- Gráficos de Barras / Pizza
- Diagrama de Dispersão
- Tabela de Contingência

---

# 🎤 BLOCO 3 — Análise Qualitativa *(P3 — ~5 min)*

> **Regra para esse bloco:** ler a frequência mais alta, mais baixa, e descrever a forma da distribuição. Nada além disso.

### Slide 10 — Tabela de Frequência: Renda Familiar (Q006)
- Mostrar a tabela `frequencia_Q006.csv`:
  - Categoria **A**: 3.139.039 (**72,45%**)
  - Categoria **B**: 1.193.896 (**27,55%**)
- **Leitura descritiva:** ~72% dos respondentes está na faixa A; ~28% na faixa B.

### Slide 11 — Gráfico de Barras / Pizza: Renda Familiar
- Mostrar `barras_Q006.png` + `pizza_Q006.png`.
- Descrever: barra A é ~2,6× maior que B.

### Slide 12 — UF de Prova (Top 10)
- Mostrar `barras_SG_UF_PROVA_top10.png` e `pizza_SG_UF_PROVA_top10.png`.
- Descrever os três estados mais frequentes da base (ler do gráfico).
- Observação factual: estados populosos concentram inscrições.

### Slide 13 — Sexo (TP_SEXO)
- Mostrar `barras_TP_SEXO.png` e `pizza_TP_SEXO.png`.
- Ler proporção F / M.

### Slide 14 — Escolaridade dos pais (Q001 e Q002)
- Mostrar `barras_Q001.png`, `pizza_Q001.png`, `barras_Q002.png`, `pizza_Q002.png`.
- Q001 e Q002 têm 8 categorias (A–H).
- Descrever qual categoria predomina em cada caso e comparar visualmente pai vs mãe.

### Slide 15 — Língua Estrangeira (TP_LINGUA)
- Mostrar `barras_TP_LINGUA.png` e `pizza_TP_LINGUA.png`.
- Descrever proporção Inglês vs Espanhol.

---

# 🎤 BLOCO 4 — Análise Quantitativa Contínua *(P4 — ~5 min)*

### Slide 16 — Método: classes por Sturges
- Fórmula: `k = ceil(1 + 3,322·log₁₀(n))`.
- Para n ≈ 3 milhões → k ≈ 23 classes.
- Amplitude da classe = (máx − mín) / k.

### Slide 17 — Histograma: Matemática (NU_NOTA_MT)
- Mostrar `histograma_NU_NOTA_MT.png`.
- **Descrição factual da forma:** distribuição assimétrica à direita; concentração principal na faixa 380–500; cauda longa para notas altas.
- Tabela `frequencia_continua_NU_NOTA_MT.csv`: classe modal `[418,22 – 460,04)` com 18,39%.

### Slide 18 — Histograma: Ciências da Natureza (NU_NOTA_CN)
- Mostrar `histograma_NU_NOTA_CN.png`.
- Forma: aproximadamente simétrica em torno de ~490, cauda curta dos dois lados.

### Slide 19 — Histograma: Ciências Humanas (NU_NOTA_CH)
- Mostrar `histograma_NU_NOTA_CH.png`.
- Forma: simétrica, deslocada à direita de CN.

### Slide 20 — Histograma: Linguagens (NU_NOTA_LC)
- Mostrar `histograma_NU_NOTA_LC.png`.
- Forma: a mais concentrada das objetivas (menor dispersão).

### Slide 21 — Histograma: Redação (NU_NOTA_REDACAO)
- Mostrar `histograma_NU_NOTA_REDACAO.png`.
- Forma: distribuição **discretizada em múltiplos de 20/40**, bimodalidade visível com picos próximos a 0 e a 600–800, pico residual em 1000.
- Comentar pico em 0 = redações zeradas (fuga ao tema, branco, ofensa aos direitos humanos, etc.).

### Slide 22 — Comparativo: histogramas lado a lado
- Mostrar `histogramas_NU_NOTA_CN_NU_NOTA_CH_NU_NOTA_LC_NU_NOTA_MT_NU_NOTA_REDACAO.png`.
- Descrever que as 4 objetivas têm escala TRI (~0–1000 com massa em 350–700), enquanto Redação ocupa toda a escala 0–1000 com saltos discretos.

---

# 🎤 BLOCO 5 — Medidas-Resumo *(P5 — ~5–6 min)*

> Apresentar a **tabela de descritivas** como slide central (vem de `descritiva_*.csv`) e ir descrevendo coluna por coluna.

### Slide 23 — Tabela mestre de estatísticas descritivas

| Campo | N | Média | Mediana | Moda | Desvio-padrão | Mín | Máx | Q1 | Q3 | IQR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| NU_NOTA_CN | 3.004.981 | 493,93 | 488,40 | 430,2 | 79,06 | 0 | 867,2 | 431,4 | 550,2 | 118,8 |
| NU_NOTA_CH | 3.167.955 | 511,01 | 516,30 | 0,0 | 93,06 | 0 | 819,7 | 446,4 | 576,2 | 129,8 |
| NU_NOTA_LC | 3.167.955 | 524,47 | 531,50 | 540,7 | 69,96 | 0 | 795,8 | 484,1 | 572,1 | 88,0 |
| NU_NOTA_MT | 3.004.981 | 526,97 | 499,00 | 421,1 | 114,22 | 0 | 961,9 | 431,2 | 610,8 | 179,6 |
| NU_NOTA_REDACAO | 3.167.955 | 624,59 | 640,00 | 0,0 | 216,34 | 0 | 1000,0 | 520,0 | 780,0 | 260,0 |

### Slide 24 — Tendência central: Média, Mediana, Moda
- Descrever, para cada prova, a relação entre as três medidas.
- Observações factuais (sem opinião):
  - **MT:** média (526,97) > mediana (499,00) → assimetria à direita.
  - **CH / REDAÇÃO:** moda = 0 → grande quantidade de notas zeradas.
  - **LC:** média ≈ mediana ≈ moda → distribuição mais simétrica.

### Slide 25 — Dispersão: Variância e Desvio Padrão
- Maior dispersão: **Redação (σ = 216,34)**.
- Menor dispersão: **LC (σ = 69,96)**.
- Entre as objetivas, **MT (σ = 114,22)** tem maior espalhamento.
- Variâncias completas (tabela do CSV `descritiva_*.csv`).

### Slide 26 — Amplitude e IQR
- Amplitude:
  - REDACAO: 1000,0 (única que atinge nota máxima do exame)
  - MT: 961,9 (maior entre as objetivas)
  - LC: 795,8 (menor amplitude)
- IQR (Q3 − Q1):
  - REDACAO: 260
  - MT: 179,6
  - CH: 129,8
  - CN: 118,8
  - LC: 88,0
- Leitura: 50% central das notas de LC cabe em 88 pontos; o de Redação ocupa 260 pontos.

### Slide 27 — Quartis e Percentis
- Mostrar `percentis_*.csv`:
  - P10 / P25 / P50 / P75 / P90 / P95 / P99.
- Destacar fato: **P99 da Matemática = 827,5** e **P99 da Redação = 960,0**.

### Slide 28 — Boxplot comparativo
- Mostrar `boxplot_NU_NOTA_CN_NU_NOTA_CH_NU_NOTA_LC_NU_NOTA_MT_NU_NOTA_REDACAO.png`.
- Descrever:
  - Caixa de **LC** é a mais estreita → menor dispersão.
  - Caixa de **Redação** é a mais alta → maior dispersão.
  - **MT** tem mediana abaixo do centro da caixa → assimetria à direita.
  - **REDACAO** apresenta whisker inferior atingindo 0 e mediana próxima do topo da caixa → assimetria à esquerda.
  - Outliers inferiores em CN, CH, LC e MT correspondem às notas zeradas.

---

# 🎤 BLOCO 6 — Relações entre Variáveis *(P6 — ~5 min)*

### Slide 29 — Diagrama de dispersão: CN × MT
- Mostrar `dispersao_NU_NOTA_CN_x_NU_NOTA_MT.png` (amostra de 10 mil pontos).
- Reportar o coeficiente `r` exibido na imagem.
- Descrição factual: nuvem alongada em torno da reta de regressão → associação linear positiva forte entre desempenho em CN e MT.

### Slide 30 — Diagrama de dispersão: CH × LC
- Mostrar `dispersao_NU_NOTA_CH_x_NU_NOTA_LC.png`.
- Reportar `r`. Descrever forma da nuvem.
- Geralmente correlação positiva mais alta entre as duas provas de leitura/texto.

### Slide 31 — Diagrama de dispersão: MT × Redação
- Mostrar `dispersao_NU_NOTA_MT_x_NU_NOTA_REDACAO.png`.
- Reportar `r`. Descrever:
  - Pontos alinhados em colunas horizontais (efeito da escala discreta de redação em múltiplos de 20/40).
  - Banda inferior em y = 0 (redações zeradas, qualquer que seja MT).

### Slide 32 — Tabela de contingência: Sexo × Renda
- Mostrar `heatmap_TP_SEXO_x_Q006.png` + `contingencia_TP_SEXO_x_Q006.csv`:
  - Frequências absolutas (F/M × A/B).
  - % por linha (distribuição de renda condicional ao sexo).
- Reportar estatística χ², graus de liberdade, p-valor e conclusão automática gerada pelo script (`Associação significativa` ou `Sem associação significativa`).

### Slide 33 — Tabela de contingência: Escolaridade da Mãe × Renda
- Mostrar `heatmap_Q002_x_Q006.png` + `contingencia_Q002_x_Q006.csv`.
- Descrever quais combinações (linha A–H × coluna A/B) concentram mais massa.
- Reportar χ² / p-valor.

---

# 🎤 BLOCO 7 — Conclusão e Encerramento *(P7 — ~3–4 min)*

### Slide 34 — Conclusão (descritiva)
Fechar relembrando, **sem opinião**:
1. **Cobertura:** 4,3 milhões de inscritos; ~3 milhões com notas válidas em cada prova.
2. **Perfil dos respondentes:** distribuição entre sexos próxima de paritária; renda concentrada na categoria A (~72%); escolaridade dos pais concentrada nas faixas iniciais do questionário; predomínio do inglês como língua estrangeira escolhida.
3. **Notas:**
   - Médias das objetivas próximas de 500 (efeito da padronização TRI).
   - Maior dispersão em **Redação** e em **Matemática**; menor em **Linguagens**.
   - Notas zeradas (moda 0) marcam fortemente CH e Redação.
4. **Associações:**
   - Correlação linear positiva forte entre as quatro provas objetivas (especialmente CN × MT).
   - χ² indica associação estatisticamente significativa entre `Sexo × Renda` e entre `Escolaridade da Mãe × Renda` (reportar p-valores do script).
5. **Limites do estudo:** análise descritiva, sem inferências causais; renda restrita a duas categorias na base disponível; amostragem para dispersão.

### Slide 35 — Encerramento
- Repositório do projeto (GitHub).
- Reconhecimentos / referências:
  - INEP — Microdados ENEM 2024.
  - Documentação técnica: `Leia_Me_Enem_2024.pdf`, `enem_procedimentos_de_analise.pdf`, `matriz_referencia_enem.pdf`.
- "Perguntas?"

---

## ⏱️ Cronometragem sugerida

| Bloco | Slides | Tempo | Acumulado |
|---|---|---|---|
| 1 — Intro / Captura | 1–5 | 5:00 | 5:00 |
| 2 — Vieses / Variáveis | 6–9 | 5:00 | 10:00 |
| 3 — Qualitativa | 10–15 | 5:00 | 15:00 |
| 4 — Contínua / Histogramas | 16–22 | 5:00 | 20:00 |
| 5 — Medidas-resumo / Boxplot | 23–28 | 6:00 | 26:00 |
| 6 — Relações | 29–33 | 5:00 | 31:00 |
| 7 — Conclusão / Encerramento | 34–35 | 3:00 | **34:00** |

Margem de 1–2 min para transições entre apresentadores e perguntas rápidas → encaixa em 30–35 min.

---

## 📋 Checklist de preparação

- [ ] Imagens em alta resolução (`src/database/2024/ANALISES/*.png`) embutidas direto no slide.
- [ ] Tabelas com casas decimais padronizadas (2 casas).
- [ ] Fonte legível à distância (≥ 24 pt para corpo).
- [ ] Cada apresentador ensaiar o próprio bloco em ≤ 6 min.
- [ ] Transição entre apresentadores anunciada em voz ("a seguir, X falará sobre Y").
- [ ] Não usar adjetivos avaliativos ("bom", "ruim", "preocupante") — substituir por descrições numéricas.
- [ ] Reportar χ²/r/p-valor exatamente como aparecem nos arquivos gerados.
- [ ] Backup dos CSVs/PNGs em pasta local caso a internet falhe na apresentação.
