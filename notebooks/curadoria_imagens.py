"""
Pipeline de Curadoria - imagens

Este módulo contém a função principal de curadoria para arquivos do tipo imagens.
Ela será chamada pelo notebook `c-curadoria.ipynb` para processar arquivos classificados como 'imagens'.
"""

def processar_imagens(df_arquivos, prefixo):
    """
    Parâmetros:
        df_arquivos: DataFrame com colunas ['filename', 'full_path']
        prefixo: string representando o prefixo do projeto (ex: 'FDL')

    Retorno:
        DataFrame atualizado com status de curadoria para curation_audit
    """
    print(f"Iniciando curadoria de arquivos do tipo 'imagens' para o projeto com prefixo '{prefixo}'.")
    # Lógica de curadoria será implementada aqui futuramente
    return df_arquivos
