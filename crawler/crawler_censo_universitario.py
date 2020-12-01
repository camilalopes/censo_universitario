import os
from typing import List

import asyncio
import lxml.html
from aiohttp import ClientSession, ClientTimeout, StreamReader
from aiohttp.client_exceptions import ClientPayloadError
from rarfile import RarFile
from zipfile import ZipFile


CAMINHO_DADOS = f"{os.path.realpath('..')}/dados/"


async def extrai_url_dados(ano: int, session: ClientSession) -> List:
    response = await session.request(
        method='GET',
        url=f'https://www.gov.br/inep/pt-br/areas-de-atuacao/'
            f'pesquisas-estatisticas-e-indicadores/censo-da-educacao-superior/resultados/{ano}'
    )
    html = lxml.html.fromstring(await response.text())
    url = html.cssselect("a[href*='microdados/microdados']")[0].attrib['href']
    return url


async def inicia_extracao_dados_censo(anos: List) -> None:
    timeout = ClientTimeout(total=60*20)
    async with ClientSession(timeout=timeout) as session:
        tarefas = [salva_dados_censo(ano, session) for ano in anos]
        await asyncio.gather(*tarefas)


async def salva_dados_censo(ano: int, session: ClientSession) -> None:
    url = await extrai_url_dados(ano, session)
    dados = await extrai_dados_censo(url, session)
    nome_arquivo = url.split('/')[-1].split('_')[-1]
    print(f'Salvando os dados de {url}')
    with open(CAMINHO_DADOS+nome_arquivo, 'wb') as arquivo:        
        try:
            conteudo = await dados.read()
            arquivo.write(conteudo)
            print(f'Salvo {url}')
        except ClientPayloadError:
            print(f'Não foi possível salvar {url}')


async def extrai_dados_censo(url: str, session: ClientSession) -> StreamReader:
    response = await session.request(method='GET', url=url)
    return response.content


def descompacta_arquivos(anos: List) -> None:
    for ano in anos:
        print(f'Descompactando dados {ano}')
        caminho_arquivo = CAMINHO_DADOS+ano
        with ZipFile(f'{caminho_arquivo}.zip', 'r') as arquivo_zip:
            for zip_info in arquivo_zip.infolist():
                nome_arquivo = zip_info.filename
                if 'ALUNO' in nome_arquivo:
                    if '.rar' in nome_arquivo:
                        zip_info.filename = 'aluno.rar'
                        arquivo_zip.extract(zip_info, caminho_arquivo)
                        descompacta_arquivo(arquivo_compactado=RarFile(f'{caminho_arquivo}/aluno.rar', 'r'),
                                            caminho_arquivo=caminho_arquivo)
                        break
                    if '.zip' in nome_arquivo:
                        zip_info.filename = 'aluno.zip'
                        arquivo_zip.extract(zip_info, caminho_arquivo)
                        descompacta_arquivo(arquivo_compactado=ZipFile(f'{caminho_arquivo}/aluno.zip', 'r'),
                                            caminho_arquivo=caminho_arquivo)
                        break
                    if '.CSV' in nome_arquivo:
                        zip_info.filename = 'DM_ALUNO.CSV'
                        arquivo_zip.extract(zip_info, caminho_arquivo)
                        break


def descompacta_arquivo(arquivo_compactado, caminho_arquivo: str) -> None:
    with arquivo_compactado as arquivo:
        for info in arquivo.infolist():
            if 'ALUNO.CSV' in info.filename:
                arquivo.extract(info, caminho_arquivo)


if __name__ == '__main__':
    anos = ['2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009']
    asyncio.run(inicia_extracao_dados_censo(anos))
    descompacta_arquivos(anos)
