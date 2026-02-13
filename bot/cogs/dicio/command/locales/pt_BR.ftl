# Translation for Dicio
Dicio-response = A palavra { $word } { $exist } || Similares: { $similar } || Origem: { $origin } || Url: { $url }
Dicio-all_languages = Todos os idiomas disponíveis são: { $languages }
Dicio-error = Erro inesperado, idioma não existe. Verifique { $link } para ver os idiomas disponíveis e @{ $dev } para adicionar.
Dicio-check_exist = { $exist ->
    [1] existe
    *[0] não existe
}
Dicio-url = https://dicio.com.br/{ $word }

Dicio-languages =
    .pt_br = pt_BR/pt_BR
    .pt = pt_BR/pt_BR
    .pt_pt = pt_PT/pt_PT
    .en = en/en_US
    .en_us = en/en_US
    .en_gb = en/en_GB
    .es = es/es_ES
    .es_es = es/es_ES
    .es_mx = es_MX/es_MX
    .de = de_DE/de_DE_frami
    .fr = fr_FR/fr
    .it = it_IT/it_IT
    .ko_kr = ko_KR/ko_KR
    .ru_ru = ru_RU/ru_RU

Dicio-deco_helper = Pesquisa definições e informações sobre palavras em diversos idiomas.
Dicio-deco_usage = { $prefix }dicio (palavra) <lang:pt_br>
Dicio-deco_description = Comando de dicionário multilingue que retorna existência, similares e origem da palavra.
