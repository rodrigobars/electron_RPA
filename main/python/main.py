from Bot import Bot
import re
import sys
import pandas as pd
import openpyxl
from mytools import modify

def pregao_extract_data(bot, pregao):
    def parse_value(numero: str) -> float:
        try:
            # Price
            # Extraindo a parte numérica do text
            valor = re.search(r'\d+,\d+', numero)
            valor = valor.group()
            # Removendo 2 casas decimais e armazenando o valor
            valor = valor.replace('.', '')
            valor = float(valor.replace(',', '.'))
            return valor
        except:
            # Amount
            quantidade = numero.replace('.', '')
            quantidade = re.search(r'\d+', quantidade)
            quantidade = int(quantidade.group())
            return quantidade

    def parse_item(item) -> dict:
        splited_item = item.split("\n")
        parsed_item = {}
        for data in splited_item:
            splited_data = data.split(": ")
            if "Intervalo Mínimo entre Lances" in splited_data[1]:
                Valor = splited_data[1].split("\t")[0].replace('.', '')
                IntMin = splited_data[2]
                parsed_item.update({"Valor Estimado":parse_value(Valor), "Intervalo Mínimo entre Lances": parse_value(IntMin)})
            elif "Unidade de fornecimento" in splited_data[1]:
                Quantidade = parse_value(splited_data[1])
                Unidade = splited_data[2]
                parsed_item.update({"Quantidade":Quantidade, "Unidade":Unidade})
            elif splited_data[0] == "Item":
                parsed_item.update({"Item":int(splited_data[1])})
            else:
                parsed_item.update({splited_data[0]:splited_data[1]})
            parsed_item.update({"Pregão":pregao})
        return parsed_item

    # Iniciando o carregamento da página
    url = "http://comprasnet.gov.br/livre/pregao/ata0.asp"

    # Abrindo o google chrome no site informado
    bot.get(url)

    navigation_xpath = {
        "uasg": "//input[@id='co_uasg']",
        "num_pregao": "//input[@id='numprp']",
        "select_pregao": f"//a[contains(text(), '{pregao}')]",
        "verificacao_SRP": "//span[contains(text(), 'SRP')]",
        "button_adjudicacao": "//input[@id='btnTermAdj']",
        "verificacao_existencia_adjudicacao": "//tr[@class='mensagem']/td[@align='center']",
        "todos_itens": "//table[@class=\"td\" and @cellspacing=0]/tbody"
    }

    # começa a navegação
    bot.catch_element(xpath=navigation_xpath["uasg"]).send_keys("150182")

    bot.catch_element(xpath=navigation_xpath["num_pregao"]).send_keys(pregao)
    bot.javascript("ValidaForm();")

    bot.catch_element(xpath=navigation_xpath["select_pregao"]).click()

    try:
        bot.catch_element(xpath=navigation_xpath["verificacao_SRP"], maxWaitTime=3)
    except:
        print(f"O pregão {pregao} não é SRP, prosseguindo...") 
        return False

    bot.catch_element(xpath=navigation_xpath["button_adjudicacao"]).click()

    try:
        bot.catch_element(xpath=navigation_xpath["verificacao_existencia_adjudicacao"], maxWaitTime=3)
        print(f"O pregão {pregao} não possui itens adjudicados, prosseguindo...") 
        return False
    except:
        pass

    todos_itens = bot.catch_element(xpath=navigation_xpath["todos_itens"], amount='all')

    itens_list = []

    for item in todos_itens:
        itens_list.append(parse_item(item.text))

    for item in itens_list:
        if item['Situação'] == "Adjudicado":
            adjudicacao = bot.catch_element(f"//tr[@class=\"tex3b\"]/td[contains(text(),\"Item: {item['Item']}\")]/../../../../table[2]/tbody/tr/td")
            item.update(parse_item(adjudicacao.text))
            list_info = re.sub(" , pelo melhor lance de | e a quantidade de | Unidade .", "|", item["Adjudicado para"]).rstrip()[:-1].split("|")
            Valor = parse_value(list_info[1])
            item.update({"Empresa":list_info[0], "Valor":Valor})

    # Criar um DataFrame a partir da lista de dicionários
    # Retorna um dataframe
    return pd.DataFrame.from_dict(itens_list)

# sys.argv[0] trás o caminho completo do arquivo python que ele quer executar
pregoes = sys.argv[1:]

# Inicia o bot
bot = Bot()
bot.start(headless=False)

# Cria um novo livro do Excel vazio
workbook = openpyxl.Workbook()
worksheet = workbook.active

# Nomeando o cabeçalho
worksheet['A1'] = "Item"
worksheet['B1'] = "Pregão"
worksheet['C1'] = "Descrição"
worksheet['D1'] = "Descrição Complementar"
worksheet['E1'] = "Tratamento Diferenciado"
worksheet['F1'] = "Aplicabilidade Decreto 7174"
worksheet['G1'] = "Aplicabilidade Margem de Preferência"
worksheet['H1'] = "Quantidade"
worksheet['I1'] = "Unidade"
worksheet['J1'] = "Valor Estimado"
worksheet['K1'] = "Intervalo Mínimo entre Lances"
worksheet['L1'] = "Situação"
worksheet['M1'] = "Adjudicado completo"
worksheet['N1'] = "Empresa"
worksheet['O1'] = "Valor"

# Alterando o zoom inicial
worksheet.sheet_view.zoomScale = 70

# Adiciona os dados do seu DataFrame à planilha
for pregao in pregoes:
    print(f"\nIniciando a extração do pregão {pregao}...")
    df = pregao_extract_data(bot=bot, pregao=pregao)
    # Caso o pregão não seja SRP ele retornará False
    if df is not False:
        for row in df.values:
            worksheet.append(row.tolist())
            

worksheet = modify(worksheet, index=1, on_horizontal_direction=True, hOrientation='center', vOrientation='center', wrap_text=True, font_bold=True, row_space=60, cell_color='f5425a', border=True)
worksheet = modify(worksheet, index=1, hOrientation='center', vOrientation='center', cell_color='A5B0A2', font_bold=True, row_space=140, col_space=7, border=True)
worksheet = modify(worksheet, index=[2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], hOrientation='center', vOrientation='center', border=True, col_space=15, wrap_text=True)
worksheet = modify(worksheet, index=[3, 4], border=True, col_space=30, wrap_text=True)
worksheet = modify(worksheet, index=5, border=True, col_space=15, wrap_text=True)

workbook.save("extract_data.xlsx")