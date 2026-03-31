from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_roteirizar_payload_minimo():
    payload = {
        'carteira': [{
            'Filial': '64',
            'Romane': '288',
            'Filial (origem)': '57',
            'Série': '84',
            'Nro Doc.': '1541',
            'Data Des': '19/01/2026',
            'Data NF': '30/12/2025',
            'D.L.E.': '20/01/2026',
            'Agendam.': '21/01/2026',
            'Palet': '0',
            'Conf': '',
            'Peso': '8,47',
            'Vlr.Merc.': '135,69',
            'Qtd.': '3',
            'Peso C': '0,00',
            'Classifi': 'TRANSFERENCIA',
            'Tomador': 'QUIMICA AMPARO LTDA',
            'Destinatário': 'DMA DISTRIB',
            'Bairro': 'Centro',
            'Cida': 'Uberlandia',
            'UF': 'MG',
            'NF / Serie': '123/1',
            'Tipo Carga': 'Seca',
            'Qtd.NF': '1',
            'Região': 'Triangulo',
            'Sub-Região': 'Uberlandia',
            'Ocorrências NFs': '',
            'Remetente': 'REMETENTE X',
            'Observação R': '',
            'Ref Cliente': 'REF1',
            'Cidade Dest.': 'Uberlandia',
            'Mesoregião': 'Triangulo Mineiro',
            'Agenda': 'Nao',
            'Tipo C': 'Normal',
            'Última': 'Nao',
            'Status': 'Aberto',
            'Lat.': '-18.91',
            'Lon.': '-48.27'
        }],
        'veiculos': [{
            'id': '1',
            'placa': 'ABC1234',
            'perfil': 'VUC',
            'tipo_veiculo': 'VUC',
            'capacidade_peso_kg': 3000,
            'capacidade_vol_m3': 12,
            'qtd_eixos': 2,
            'max_entregas': 6,
            'max_km_distancia': 50,
            'ocupacao_minima_perc': 70,
            'dedicado': False,
            'tipo_frota': 'propria',
            'filial_id': '1',
            'ativo': True
        }],
        'regionalidades': [{
            'cidade': 'Uberlandia',
            'uf': 'MG',
            'mesorregiao': 'Triangulo Mineiro',
            'microrregiao': 'Uberlandia'
        }],
        'parametros': {
            'usuario_id': '1',
            'filial_id': '1',
            'data_execucao': '2026-03-31T10:00:00'
        }
    }
    response = client.post('/roteirizar', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'sucesso'
    assert data['resumo']['total_carteira'] == 1
