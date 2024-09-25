import requests

'''
url = "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/"

1. Pega a lista dos anos | ata/ordinarias
2. Seleciona o Id (id_eleicao) com base no ano (geralmente é o primeiro item da lista)
3. Obtém os dados das UFES | eleicao/eleicao-atual?idEleicao=<id_eleicao>
4. Seleciona a sigla do estado (ues.<sigla>)
5. Seleciona o código do cargo (ues.resumoCandidaturas.<codigo_cargo>)
6. Obtém os municípios | eleicao/buscar/<sigla>/<id_eleicao>/municipios
7. Seleciona o código do município (municipios.<codigo_mun>)
8. Obtém as candidaturas | candidatura/listar/2024/<codigo_mun>/<id_eleicao>/<codigo_cargo>/candidatos
9. Obtém o ID do candidato (candidatos.[*].<id_candidato>)
10. Acessa o link do candidato | candidatura/buscar/2024/<codigo_mun>/<id_eleicao>/candidato/<id_candidato>
11. Obtém todos os dados do candidato
- numero
- nomeUrna
- nomeCompleto
- nomeColigacao
- id
- fotoUrl
'''


def crawler():
    base_url = "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/"

    req = lambda path: requests.get(base_url + path).json()

    def get_election_id():
        years = req("ata/ordinarias")
        return years[0]["id"]
    
    def get_ufes(election_id):
        data = req(f"eleicao/eleicao-atual?idEleicao={election_id}")
        cargos = data['resumoCandidaturas']
        cargo_data = [cargo for cargo in cargos if cargo['nome'] == 'Vereador'][0]
        return data['ues'], cargo_data['codigo']
    
    def get_municipios(election_id, uf_sigla):
        data = req(f"eleicao/buscar/{uf_sigla.upper()}/{election_id}/municipios")
        municipios_ids = [municipio['codigo'] for municipio in data['municipios']]
        return municipios_ids
    
    def get_candidates_id(election_id, cargo_id, municipio_id):
        data = req(f"candidatura/listar/2024/{municipio_id}/{election_id}/{cargo_id}/candidatos")
        return [candidate['id'] for candidate in data['candidatos']]
    
    def get_candidate(election_id, uf_sigla, municipio_id, candidate_id):
        data = req(f"candidatura/buscar/2024/{municipio_id}/{election_id}/candidato/{candidate_id}")
        new_candidate = {
            'election_number': data['numero'],
            'candidate_nick': data['nomeUrna'],
            'candidate_name': data['nomeCompleto'],
            'nomeColigacao': data['nomeColigacao'],
            'site_id': data['id'],
            'image_url': data['fotoUrl'],
            'municipio_id': municipio_id,
            'uf': uf_sigla,
            'election_id': election_id,
            'site_id': candidate_id,
        }
        return new_candidate

    candidates = []
    
    election_id = get_election_id()

    ufes, cargo_id = get_ufes(election_id)

    for uf in ufes:
        uf_sigla = uf['sigla']
        if uf_sigla == 'BR':
            continue
        municipios_ids = get_municipios(election_id, uf_sigla)
        for municipio_id in municipios_ids:
            candidates_id = get_candidates_id(election_id, cargo_id, municipio_id)
            for candidate_id in candidates_id:
                candidate = get_candidate(election_id, uf_sigla, municipio_id, candidate_id)
                candidates.append(candidate)
                print(candidate['site_id'], candidate['candidate_nick'])

    return candidates