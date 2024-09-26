import requests

"""
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
"""


def crawler():
    base_url = "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/"

    def req(path):
        try:
            return requests.get(base_url + path).json()
        except Exception as e:
            print("Houve um erro na requisição:", e)
            return None

    req = lambda path: requests.get(base_url + path).json()

    def get_election_id():
        years = req("ata/ordinarias")
        if years is None:
            return None
        return years[0]["id"]

    def get_ufes(election_id):
        data = req(f"eleicao/eleicao-atual?idEleicao={election_id}")
        if data is None:
            return None
        cargos = data["resumoCandidaturas"]
        cargo_data = [cargo for cargo in cargos if cargo["nome"] == "Vereador"][0]
        return data["ues"], cargo_data["codigo"]

    def get_municipios(election_id, uf_sigla):
        data = req(f"eleicao/buscar/{uf_sigla.upper()}/{election_id}/municipios")
        if data is None:
            return None
        return data["municipios"]

    def get_candidates_id(election_id, cargo_id, municipio):
        municipio_id = municipio["codigo"]
        data = req(
            f"candidatura/listar/2024/{municipio_id}/{election_id}/{cargo_id}/candidatos"
        )
        if data is None:
            return None
        return [candidate["id"] for candidate in data["candidatos"]]

    def get_candidate(election_id, uf_sigla, municipio, candidate_id):
        municipio_id = municipio["codigo"]
        data = req(
            f"candidatura/buscar/2024/{municipio_id}/{election_id}/candidato/{candidate_id}"
        )
        if data is None:
            return None
        new_candidate = {
            "number": data["numero"],
            "nick": data["nomeUrna"],
            "name": data["nomeCompleto"],
            "nomeColigacao": data["nomeColigacao"],
            "site_id": data["id"],
            "image_url": data["fotoUrl"],
            "municipio_id": municipio_id,
            "uf": uf_sigla,
            "election_id": election_id,
            "site_id": candidate_id,
            "municipio": municipio["nome"],
            "region": "SUDESTE",
            "year": "2024",
        }
        return new_candidate

    candidates = []

    while True:
        election_id = get_election_id()
        if election_id:
            break

    _, cargo_id = get_ufes(election_id)
    uf_sigla = "MG"

    municipios = get_municipios(election_id, uf_sigla)
    if municipios is None:
        return None
    municipio_barroso = [
        municipio for municipio in municipios if municipio["nome"].upper() == "BARROSO"
    ][0]
    candidates_ids = get_candidates_id(election_id, cargo_id, municipio_barroso)
    if candidates_ids is None:
        return None
    for candidate_id in candidates_ids:
        candidate = get_candidate(
            election_id, uf_sigla, municipio_barroso, candidate_id
        )
        if candidate is None:
            continue
        candidates.append(candidate)
        print(candidate["site_id"], candidate["nick"], candidate["uf"])

    return candidates
