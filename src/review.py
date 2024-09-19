import os
import re

import automatic_code_review_commons as commons


def extrair_strings_arquivo_por_linha(conteudo):
    regex = r'([\'"])(.*?)(?<!\\)\1'

    resultado = []

    for numero_linha, linha in enumerate(conteudo.splitlines(), start=1):
        matches = re.findall(regex, linha)

        for match in matches:
            string_extraida = match[1].replace('\\"', '"').replace("\\'", "'")
            resultado.append((numero_linha, string_extraida, linha))

    return resultado


def ler_arquivos_pasta(path, changes):
    todas_strings = []

    for change in changes:
        caminho_arquivo = os.path.join(path, change['new_path'])

        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                strings_arquivo = extrair_strings_arquivo_por_linha(conteudo)

                for numero_linha, string, conteudo_linha in strings_arquivo:
                    todas_strings.append((caminho_arquivo, numero_linha, string, conteudo_linha))

        except Exception as e:
            print(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")

    return todas_strings


def __check_regex_list(regex_list, text, inverted=False):
    if inverted:
        for regex in regex_list:
            if re.match(regex, text):
                return False

        return True

    for regex in regex_list:
        if re.match(regex, text):
            return True

    return False


def __review_by_config(strings, path_source, config):
    comments = []

    regex_file = config['regexFile']
    regex_string = config['regex']
    inverted = 'inverted' in config and config['inverted']
    comment = config['message']
    string_to_ignore = config['stringToIgnore']

    language = None
    string_line_regex = ".*"

    if 'language' in config:
        language = config['language']

    if 'stringLineRegex' in config:
        string_line_regex = config['stringLineRegex']

    for arquivo, linha, string, conteudo_linha in strings:
        if not __check_regex_list(regex_file, arquivo):
            continue

        if not __check_regex_list(regex_string, string, inverted):
            continue

        if __check_regex_list(string_to_ignore, string):
            continue

        if not __check_regex_list(string_line_regex, conteudo_linha):
            continue

        comment_path = arquivo.replace(path_source, "")[1:]
        comment_description = comment
        comment_description = comment_description.replace("${TEXT}", string)
        comment_description = comment_description.replace("${FILE_PATH}", comment_path)
        comment_description = comment_description.replace("${LINE}", str(linha))

        comments.append(commons.comment_create(
            comment_id=commons.comment_generate_id(comment_description),
            comment_path=comment_path,
            comment_description=comment_description,
            comment_snipset=True,
            comment_end_line=linha,
            comment_start_line=linha,
            comment_language=language,
        ))

    return comments


def review(config):
    merge = config['merge']
    changes = merge['changes']
    path_source = config['path_source']

    comments = []

    strings = ler_arquivos_pasta(path_source, changes)

    for config in config['data']:
        comments.extend(__review_by_config(strings, path_source, config))

    return comments
