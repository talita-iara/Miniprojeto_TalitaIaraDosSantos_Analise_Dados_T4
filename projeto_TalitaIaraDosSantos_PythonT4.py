import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# Importar arquivo
ARQUIVO = "Base Varejo.csv"

with open(ARQUIVO, mode="r", encoding="utf-8-sig", newline="") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=";")
    total_linhas_csv = sum(1 for _ in leitor)

# Carregar a base com pandas
df = pd.read_csv(ARQUIVO, sep=";", encoding="utf-8-sig")

# Limpeza dos dados 
# As colunas Unnamed estão totalmente vazias, então não serão necessárias.
colunas_vazias = [
    coluna for coluna in df.columns
    if coluna.startswith("Unnamed")
]

# Quantidade de duplicatas antes da limpeza
duplicados_antes = df.duplicated().sum()

# Remover as colunas totalmente vazias
df = df.drop(columns=colunas_vazias)

# Remover registros completamente duplicados, mas sem remover linhas com o mesmo ID de compra, pois uma compra pode possuir vários itens.
df = df.drop_duplicates()


# A categoria #N/D será ajustada para "SEM CATEGORIA".
def tratar_categoria(categoria):

    if pd.isna(categoria) or str(categoria).strip() == "":
        return "SEM CATEGORIA"

    elif str(categoria).strip() == "#N/D":
        return "SEM CATEGORIA"

    else:
        return categoria

df["PR_CAT"] = df["PR_CAT"].apply(tratar_categoria)


# Converter a coluna DATA para datetime.
datas_unicas = df["DATA"].unique()

datas_convertidas = {
    data: datetime.strptime(data, "%d/%m/%Y")
    for data in datas_unicas
}

df["DATA"] = df["DATA"].map(datas_convertidas)

# Funções 
# Informações gerais da base
def informacoes_base():

    print("\nInformações da base:")

    print("\nQuantidade de registros no CSV:", total_linhas_csv)

    print("\nQuantidade de registros após a limpeza:", len(df))

    print("\nColunas da base:")
    print(df.columns.tolist())

    print("\nTipos de dados:")
    print(df.dtypes)


# Ver problemas encontrados nos dados
def verificar_dados():

    print("\nAnálise dos dados")

    print("\nValores nulos por coluna:")
    print(df.isnull().sum())

    print("\nQuantidade de registros duplicados encontrados:",
          duplicados_antes)

    print("\nColunas totalmente vazias encontradas:")
    print(colunas_vazias)

    print("\nCategorias após o tratamento:")
    print(df["PR_CAT"].value_counts(dropna=False))

    # Verificação das datas depois da conversão
    print("\nDatas inválidas após a limpeza:",
          df["DATA"].isnull().sum())

# Estatísticas do número de filhos
def estatisticas_filhos():

    print("\nEstatística por número de filhos: ")

    filhos = df["CL_FHL"]

    print("\nContagem:", filhos.count())
    print("Média:", filhos.mean())
    print("Mediana:", filhos.median())
    print("Desvio padrão:", filhos.std())
    print("Moda:", filhos.mode().tolist())
    print("Mínimo:", filhos.min())
    print("Máximo:", filhos.max())

    print("\nQuartis:")
    print("25%:", filhos.quantile(0.25))
    print("50%:", filhos.quantile(0.50))
    print("75%:", filhos.quantile(0.75))


# Quantidade de compras por gênero
def compras_por_genero():
    compras_genero = (
        df.groupby("CL_GENERO")["CO_ID"]
        .nunique()
        .sort_values(ascending=False)
    )

    print("\nCompras por gênero: ")
    print(compras_genero)


# Quantidade de itens por categoria
def itens_por_categoria():

    vendas_categoria = (
        df.groupby("PR_CAT")["PR_ID"]
        .count()
        .sort_values(ascending=False)
    )

    print("\nItens por categoria: ")
    print(vendas_categoria)


# Quantidade de compras por segmento
def compras_por_segmento():

    compras_segmento = (
        df.groupby("CL_SEG")["CO_ID"]
        .nunique()
        .sort_values(ascending=False)
    )

    print("\nCompras por segmento: ")
    print(compras_segmento)


# Mostrar produtos mais vendidos
def produtos_mais_vendidos():

    produtos = (
        df.groupby("PR_NOME")["PR_ID"]
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\nOs 10 produtos mais vendidos: ")
    print(produtos)


# Gráficos
# Gráfico de compras por gênero
def grafico_genero():

    compras_genero = (
        df.groupby("CL_GENERO")["CO_ID"]
        .nunique()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(7, 5))

    compras_genero.plot(kind="bar")

    plt.title("Quantidade de Compras por Gênero")
    plt.xlabel("Gênero")
    plt.ylabel("Quantidade de Compras")
    plt.tight_layout()
    plt.show()

# Gráfico de itens por categoria
def grafico_categoria():

    vendas_categoria = (
        df.groupby("PR_CAT")["PR_ID"]
        .count()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(9, 5))

    vendas_categoria.plot(kind="bar")

    plt.title("Quantidade de Itens por Categoria")
    plt.xlabel("Categoria")
    plt.ylabel("Quantidade de Itens")
    plt.tight_layout()
    plt.show()


# Gráfico de compras ao longo do tempo
def grafico_compras_mes():

    compras_por_mes = (
        df.groupby(df["DATA"].dt.to_period("M"))["CO_ID"]
        .nunique()
    )

    plt.figure(figsize=(10, 5))

    compras_por_mes.plot(kind="line", marker="o")

    plt.title("Quantidade de Compras ao Longo do Tempo")
    plt.xlabel("Mês")
    plt.ylabel("Quantidade de Compras")
    plt.tight_layout()
    plt.show()


# Gráfico do número de filhos
def grafico_filhos():

    # Cada cliente será contado apenas uma vez
    clientes = df.drop_duplicates(subset="CL_ID")

    quantidade_filhos = (
        clientes["CL_FHL"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(7, 5))

    quantidade_filhos.plot(kind="bar")

    plt.title("Quantidade de Clientes por Número de Filhos")
    plt.xlabel("Número de Filhos")
    plt.ylabel("Quantidade de Clientes")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.show()


# Gráfico dos 10 produtos mais vendidos
def grafico_produtos():

    produtos = (
        df.groupby("PR_NOME")["PR_ID"]
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 6))

    produtos.plot(kind="bar")

    plt.title("10 Produtos Mais Vendidos")
    plt.xlabel("Produto")
    plt.ylabel("Quantidade de Itens")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


#Conclusões

def conclusoes():

    compras_genero = (
        df.groupby("CL_GENERO")["CO_ID"]
        .nunique()
        .sort_values(ascending=False)
    )

    vendas_categoria = (
        df.groupby("PR_CAT")["PR_ID"]
        .count()
        .sort_values(ascending=False)
    )

    compras_segmento = (
        df.groupby("CL_SEG")["CO_ID"]
        .nunique()
        .sort_values(ascending=False)
    )

    compras_por_mes = (
        df.groupby(df["DATA"].dt.to_period("M"))["CO_ID"]
        .nunique()
    )

    filhos = df["CL_FHL"]

    genero_maior = compras_genero.idxmax()
    categoria_maior = vendas_categoria.idxmax()
    segmento_maior = compras_segmento.idxmax()
    mes_maior = compras_por_mes.idxmax()
    quantidade_mes_maior = compras_por_mes.max()

    print("\n===== CONCLUSÕES =====")

    print(
        f"\n- O gênero com maior quantidade de compras foi: "
        f"{genero_maior}."
    )

    print(
        f"- A categoria com maior quantidade de itens foi: "
        f"{categoria_maior}."
    )

    print(
        f"- O segmento com maior quantidade de compras foi: "
        f"{segmento_maior}."
    )

    print(
        f"- O mês com maior quantidade de compras foi {mes_maior}, "
        f"com {quantidade_mes_maior} compras."
    )

    print(
        f"- A média de filhos dos clientes foi de "
        f"{filhos.mean():.2f}, e a mediana foi "
        f"{filhos.median()}."
    )

    print("\nProblemas encontrados e tratados:")

    print(
        f"- Foram encontradas {duplicados_antes} "
        f"linhas duplicadas."
    )

    print("- Foram removidas as colunas totalmente vazias.")

    print(
        "- A categoria #N/D foi tratada como "
        "'SEM CATEGORIA'."
    )

    print(
        "- A coluna DATA foi convertida para "
        "o formato datetime."
    )

# Salvar dados tratados
def salvar_base():

    df.to_csv(
        "df_limpo.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nBase limpa salva como: df_limpo.csv")
salvar_base()

# Manu de opções
while True:

    print("\n==========================================")
    print("        ANÁLISE DE DADOS - VAREJO")
    print("==========================================")
    print("1  - Informações da base")
    print("2  - Valores nulos e duplicados")
    print("3  - Estatísticas do número de filhos")
    print("4  - Compras por gênero")
    print("5  - Itens por categoria")
    print("6  - Compras por segmento")
    print("7  - 10 produtos mais vendidos")
    print("8  - Gráfico de compras por gênero")
    print("9  - Gráfico de itens por categoria")
    print("10 - Gráfico de compras por mês")
    print("11 - Gráfico de número de filhos")
    print("12 - Gráfico dos 10 produtos mais vendidos")
    print("13 - Conclusões")
    print("0  - Sair")

    opcao = input("\nDigite a opção desejada: ")

    if opcao == "1":
        informacoes_base()

    elif opcao == "2":
        verificar_dados()

    elif opcao == "3":
        estatisticas_filhos()

    elif opcao == "4":
        compras_por_genero()

    elif opcao == "5":
        itens_por_categoria()

    elif opcao == "6":
        compras_por_segmento()

    elif opcao == "7":
        produtos_mais_vendidos()

    elif opcao == "8":
        grafico_genero()

    elif opcao == "9":
        grafico_categoria()

    elif opcao == "10":
        grafico_compras_mes()

    elif opcao == "11":
        grafico_filhos()

    elif opcao == "12":
        grafico_produtos()

    elif opcao == "13":
        conclusoes()

    elif opcao == "0":
        print("\nPrograma encerrado.")
        break

    else:
        print("\nOpção inválida. Digite novamente.")