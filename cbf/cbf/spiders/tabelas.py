import scrapy


def tratar_time(time):
    # Alguns nomes da CBF não estão gramaticalmente corretos ou não estavam de acordo para o meu projeto pessoal

    nome_recebido = ['America', 'Sampaio Correa', 'Boa',
                     'Clube de Esportes Uniao', 'Minas Brasilia', 'CEU ABC', 'America - MG', 'Goianesia', 'Marilia']
    nome_desejado = ['América', 'Sampaio Corrêa',
                     'Boa Esporte', 'União ABC', 'Minas Brasília', 'União ABC', 'América - MG', 'Goianésia', 'Marília']

    if time in nome_recebido:
        index = nome_recebido.index(time)
        return nome_desejado[index]
    elif 'A Definir' in time:
        return 'Selecione'
    else:
        return time


def tratar_cidade(cidade):
    # Alguns nomes da CBF não estão gramaticalmente corretos

    nome_recebido = ['Sao Paulo', 'Braganca Paulista', 'Goiania', 'Florianopolis',
                     'Maceio', 'São Luis', 'Ribeirao Preto', 'Chapeco', 'Nova Iguacu', 'Niteroi', 'Macapa', 'Xanxere', 'Maracanau', 'Criciuma', 'Pocos de Caldas', 'Rondonopolis', 'Joao Pessoa']
    nome_desejado = ['São Paulo', 'Bragança Paulista', 'Goiânia', 'Florianópolis',
                     'Maceió', 'São Luís', 'Ribeirão Preto', 'Chapecó', 'Nova Iguaçu', 'Niterói', 'Macapá', 'Xanxerê', 'Maracanaú', 'Criciúma', 'Poços de Caldas', 'Rondonópolis', 'João Pessoa']

    if cidade in nome_recebido:
        index = nome_recebido.index(cidade)
        return nome_desejado[index]
    elif 'A Definir' in cidade:
        return 'Selecione'
    else:
        return cidade


def tratar_estadio(estadio):
    # Alguns nomes da CBF não estão gramaticalmente corretos ou não estavam de acordo para o meu projeto pessoal

    nome_recebido = ['Manoel Barradas', 'Nilton Santos',
                     'CAT do Cajú']
    nome_desejado = ['Barradão', 'Engenhão',
                     'CAT do Caju']

    if estadio in nome_recebido:
        index = nome_recebido.index(estadio)
        return nome_desejado[index]
    elif 'A Definir' in estadio:
        return 'Selecione'
    else:
        return estadio


def tratar_data(data):
    # Necessitava do padrão xx/xx/xxxx

    if 'A definir' in data:
        return '00/00/0000'
    else:
        dia = int(data.split(', ')[1][0:2])
        ano = data.split(', ')[1][-4::]
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        for item in meses:
            if item in data:
                mes = meses.index(item) + 1
                break
        if dia < 10:
            dia = f'0{dia}'
        if mes < 10:
            mes = f'0{mes}'
        return f'{dia}/{mes}/{ano}'


def tratar_estado(sigla):
    # Necessitava do Estado escrito por extenso

    estados_ab = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
                  'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    estados = ['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo', 'Goiás', 'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará',
               'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins']
    for item in estados_ab:
        if sigla == item:
            index = estados_ab.index(item)

    return estados[index]


# Lista de links dos campeonatos
# Para adicionar um novo campeonato, basta colocar o link ao fim da lista
campeonatos = ['https://www.cbf.com.br/futebol-brasileiro/competicoes/copa-nordeste-masculino', 'https://www.cbf.com.br/futebol-brasileiro/competicoes/copa-brasil-sub20',
               'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-feminino-a1', 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-sub17', 'https://www.cbf.com.br/futebol-brasileiro/competicoes/copa-brasil-masculino']

# Configuração de cada campeonato. Alguns eu queria pegar a arbitragem, outros não.
# Número de jogos e de rodadas serve para descobrir de qual rodada é o jogo, uma vez que a CBF só coloca o nº do jogo.

copa_nordeste = {'nome': 'Copa do Nordeste',
                 'arbitragem': True, 'rodadas': 8, 'jogos_rodada': 8}
copa_br_20 = {'nome': 'Copa do Brasil Sub-20',
              'arbitragem': False, 'rodadas': 1, 'jogos_rodada': 16}
br_fem_a1 = {'nome': 'Brasileiro Feminino - A1',
             'arbitragem': False, 'jogos_rodada': 8, 'rodadas': 15}
br_17 = {'nome': 'Brasileiro - Sub-17', 'arbitragem': False,
         'jogos_rodada': 10, 'rodadas': 9}
copa_br = {'nome': 'Copa do Brasil', 'arbitragem': True,
           'jogos_rodada': 40, 'rodadas': 1}

opcoes_campeonatos = [copa_nordeste, copa_br_20, br_fem_a1, br_17, copa_br]


class TabelasSpider(scrapy.Spider):
    name = 'tabelas'
    allowed_domains = ['www.cbf.com.br']
    start_urls = campeonatos

    def parse(self, response):
        links = response.css(
            '.btn-info::attr(href)').getall()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_jogos)

    def parse_jogos(self, response):
        # Verificando de qual campeonato é o jogo que chegou
        part_links = ['copa-nordeste-masculino', 'copa-brasil-sub20',
                      'campeonato-brasileiro-feminino-a1', 'campeonato-brasileiro-sub17', 'copa-brasil-masculino']
        c = 0
        for item in part_links:
            if item in response.url:
                campeonato_escolhido = opcoes_campeonatos[c]
                break
            c += 1

        times = response.css('.time-nome::text').getall()
        data = tratar_data(response.css(
            '.p-r-20:nth-child(2)::text').get().strip())

        try:
            hora = response.css(
                '.p-r-20~ .p-r-20+ .p-r-20::text').get().strip()
        except Exception:
            hora = '00:00'

        if hora == 'A definir':
            hora = '00:00'

        local = response.css(
            '.col-sm-8 .p-r-20:nth-child(1)::text').getall()[1].strip()
        if 'A definir' in local:
            local = ['A definir', 'A definir', 'Selecione']
        else:
            local = local.split(' - ')
            local[2] = tratar_estado(local[2])
        num_jogo = int(response.css(
            '.text-1::text').get().strip().split('Jogo:')[1].strip())

        # Descobrindo de qual rodada é o jogo
        c = 0
        for i in range(campeonato_escolhido['rodadas']):
            if num_jogo > c and num_jogo <= c+campeonato_escolhido["jogos_rodada"]:
                rodada = i+1
                break
            c += campeonato_escolhido['jogos_rodada']

        # Verificando se é necessário pegar arbitragem
        if campeonato_escolhido['arbitragem']:
            arbitragem_check = response.css('#arbitros tbody th').getall()
            if arbitragem_check:
                repetido_check = response.css('th:contains(Árbitro)').getall()
                if len(repetido_check) < 8:
                    arbitragem_trio = response.css(
                        'td~ td+ td::text, #arbitros a::text').getall()[0:6]
                else:
                    arbitragem_trio = response.css(
                        'td~ td+ td::text, #arbitros a::text').getall()[0:6:2]
                arbitro = assistente_1 = assistente_2 = None
                arb = [arbitro, assistente_1, assistente_2]
                arbitragem = []
                c = 0
                for item in arb:
                    item = f'{arbitragem_trio[c].strip().title()} ({arbitragem_trio[c+1].strip().upper()})'
                    arbitragem.append(item)
                    c += 2

        if campeonato_escolhido['arbitragem']:
            try:
                # dados[0]["arbitro"] = arbitragem[0]
                # dados[0]["assistentes"] = f'{arbitragem[1]} e {arbitragem[2]}'

                yield {
                    "campeonato": campeonato_escolhido["nome"],
                    "home": tratar_time(times[0].strip().split(' - ')[0]),
                    "away": tratar_time(times[1].strip().split(' - ')[0]),
                    "data": f'{data} {hora}',
                    "estadio": tratar_estadio(local[0]),
                    "cidade": tratar_cidade(local[1]),
                    "estado": local[2],
                    "num_jogo": num_jogo,
                    "arbitro": arbitragem[0],
                    "assistentes": f'{arbitragem[1]} e {arbitragem[2]}',
                    "rodada": rodada
                }
            except Exception:
                yield {
                    "campeonato": campeonato_escolhido["nome"],
                    "home": tratar_time(times[0].strip().split(' - ')[0]),
                    "away": tratar_time(times[1].strip().split(' - ')[0]),
                    "data": f'{data} {hora}',
                    "estadio": tratar_estadio(local[0]),
                    "cidade": tratar_cidade(local[1]),
                    "estado": local[2],
                    "num_jogo": num_jogo,
                    "rodada": rodada
                }
        else:
            yield {
                "campeonato": campeonato_escolhido["nome"],
                "home": tratar_time(times[0].strip().split(' - ')[0]),
                "away": tratar_time(times[1].strip().split(' - ')[0]),
                "data": f'{data} {hora}',
                "estadio": tratar_estadio(local[0]),
                "cidade": tratar_cidade(local[1]),
                "estado": local[2],
                "num_jogo": num_jogo,
                "rodada": rodada
            }
