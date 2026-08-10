import re

CNPJ_ORGAO = "00394429000100"

CNPJ_LIMPO = re.sub(
    r"\D",
    "",
    CNPJ_ORGAO,
)

UASG_ALVO = "120195"

PAGE_SIZE = 50