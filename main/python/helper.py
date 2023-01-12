from Bot import Bot

def todos_pregoes(bot: object, uasg: int, ano=0):
    bot.get("https://www2.comprasnet.gov.br/siasgnet-atasrp/public/principal.do")
    bot.catch_element(use="//div[@id='oCMenu_menuConsultas']").click()
    bot.catch_element(use="//div[@id='oCMenu_menuPesquisarLicitacaoSRP']").click()
    bot.catch_element(use="//input[@id='id_numeroUasg_uasg_01']").send_keys(uasg)
    bot.javascript("javascript:consultarUasgAjax_uasg_01(document.getElementById('id_numeroUasg_uasg_01').value);")
    if ano: bot.catch_element("//input[@name='parametro.anoLicitacao']").send_keys(ano)
    bot.catch_element("//input[@id='idModalidadesCompra5']").click()
    bot.javascript("javascript:pesquisarLicitacaoSRP();")
    pregoes = []
    while True:
        lista = bot.catch_element(use="//tr[@class='odd']/td[3]", amount='all') + bot.catch_element(use="//tr[@class='even']/td[3]", amount='all')
        for pregao in lista:
            num_pregao, ano_pregao = pregao.text.split("/")
            pregoes.append(str(int(num_pregao))+ano_pregao)
        bot.catch_element(use=".pagelinks a:nth-last-child(2)", method="CSS_SELECTOR").click()
        try:
            bot.catch_element(use="//img[@src='../resource/imagens/displaytag/last_inactive.gif']", maxWaitTime=1)
            break
        except:
            continue

    return(pregoes)