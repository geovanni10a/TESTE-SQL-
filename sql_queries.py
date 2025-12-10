def criar_insert_sql(nome_tabela_destino: str, array_dados: list[dict]) -> str:
    """
    Cria um SQL INSERT para um array de dicionários com chaves iguais.
    
    :param nome_tabela_destino: Nome da tabela de destino no SQL SERVER. Deve incluir o nome do esquema.
    :type nome_tabela_destino: str
    :param array_dados: Array com os dados a serem inseridos. Os itens do array (dicionários) devem conter as mesmas chaves.
    :type array_dados: list[dict]
    :return: string SQL INSERT formata para inserção na tabela de destino com os dados da lista
    :rtype: str
    """

    keys = array_dados[0].keys()

    sql_insert = f"INSERT INTO {nome_tabela_destino} ({', '.join(keys)}) VALUES"

    for dado in array_dados:
        itens = dado.values()
        sql_insert += f"\n({', '.join(itens)}),"

    sql_insert = sql_insert[:len(sql_insert)-1] + ";"

    return sql_insert