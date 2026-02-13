# Translation for Dicio
Dicio-response = The word { $word } { $exist } || Similar: { $similar } || Origin: { $origin } || Url: { $url }
Dicio-all_languages = All available languages are: { $languages }
Dicio-error = Unexpected error, lang does not exist. Check { $link } to see available languages and ask @{ $dev } to add.
Dicio-check_exist = { $exist ->
    [1] exist
    *[0] does not exist
}
Dicio-url = https://en.wiktionary.org/wiki/{ $word }

Dicio-languages =
    .en = en/en_US
    .en_us = en/en_US
    .en_gb = en/en_GB
    .pt = pt_BR/pt_BR
    .pt_br = pt_BR/pt_BR
    .es = es/es_ES
    .de = de_DE/de_DE_frami
    .fr = fr_FR/fr
    .it = it_IT/it_IT

Dicio-deco_helper = Searches for definitions and information about words in various languages.
Dicio-deco_usage = { $prefix }dicio (word) <lang:en>
Dicio-deco_description = Multilingual dictionary command that returns existence, similarity, and origin of the word.
