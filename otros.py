# Desarrollado por Jorge Ruperez Lopez y David Posadas Valverde, pertenecientes al grupo T2

""" Funciones varias
"""
def unir_str_por_linea(str1: str, str2: str) -> str:
    """ Funcion para unir dos strings linea por linea
    :param str1: Primer string para unir
    :param str2: Segundo string para unir
    :return: La union de los dos string en el input
    """
    return "\n".join([x1 + x2 for x1, x2 in zip(*map(lambda x: x.split("\n"), [str1, str2]))])