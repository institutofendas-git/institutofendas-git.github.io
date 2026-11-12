# Fonte do site do Instituto Fendas

O site publicado (pasta acima) é gerado a partir desta pasta. Não editar as páginas publicadas à mão.

    python3 curso.py && python3 formato.py && python3 home.py   # gera as fontes das páginas
    python3 previas.py                                          # prévias de WhatsApp (precisa de playwright)
    python3 publicar.py /caminho/de/saida                       # monta o site completo
    python3 montar.py                                           # monta a versão de artefato (arquivos soltos)

- `dados.py`: a ficha de cada evento (vem do PPP) e os formatos.
- `curso.py`: página de evento. `formato.py`: página de formato. `home.py` + `home3-src.html`: página inicial. `src.html`: Final de ano.
- `menu.py`: menu, cabeçalho comum, datas automáticas de campanha. `ativos.py`: imagens e fontes em `/assets`.
- Guia de conteúdo (o que pedir a cada PPP, tamanhos de imagem): wiki de marketing, `instituto-fendas/apoio-a-divulgacao/site-do-instituto.md`.
