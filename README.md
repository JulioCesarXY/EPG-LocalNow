# 📺 Local Now - EPG & Playlist Engine

[![Atualizar EPG](https://github.com/JulioCesarXY/EPG-LocalNow/actions/workflows/update_epg.yml/badge.svg)](https://github.com/JulioCesarXY/EPG-LocalNow/actions/workflows/update_epg.yml)

Este projeto automatiza a extração da grade de programação (**EPG**) do serviço Local Now, gerando guias de programação no formato padrão XMLTV compatíveis com os principais players de IPTV do mercado (Tivimate, IPTV Smarters, Perfect Player, Next.js Custom Players, etc.).

---

## 📊 Status dos Serviços

| Serviço | Status | Descrição |
| :--- | :--- | :--- |
| **Guia de Programação (XMLTV)** | ![EPG Status](https://img.shields.io/badge/EPG-OPERACIONAL-brightgreen?style=for-the-badge&logo=xml) | Extração automatizada via GitHub Actions rodando 100% diária. |
| **Playlist de Transmissão (M3U8)** | ![Streams Status](https://img.shields.io/badge/STREAMS-EM%20DESENVOLVIMENTO-orange?style=for-the-badge&logo=python) | Motor de bypass de tokens dinâmicos e rotas CDN em fase de testes. |

---

## 🛠️ Como Funciona a Automação

O projeto utiliza um fluxo automatizado integrado para manter o seu guia sempre atualizado sem que você precise rodar nada no seu computador ou celular:

1. **GitHub Actions** aciona um servidor virtual diariamente às 03:00 UTC.
2. O script `generate_epg.py` faz a requisição na API de metadados do serviço (baseado na região/DMA configurada).
3. Os timestamps em formato Unix são convertidos para o padrão estrito do XMLTV (`YYYYMMDDhhmmss +0000`).
4. O arquivo `localnow_epg.xml` é atualizado, formatado e salvo automaticamente no repositório.

---

## 📁 Estrutura de Arquivos

* `generate_epg.py`: Script principal em Python responsável por estruturar os dados da API em XML.
* `localnow_epg.xml`: O arquivo de saída final contendo o guia de programação (gerado automaticamente).
* `.github/workflows/update_epg.yml`: Configuração do GitHub Actions que gerencia o agendamento cron diário.

---

## 🔗 Links de Integração (Como Usar no Player)

Para alimentar o seu player de IPTV, adicione a URL do arquivo bruto (*raw*) do seu repositório:

* **URL do Guia (EPG XMLTV):**
    ```text
    https://raw.githubusercontent.com/JulioCesarXY/EPG-LocalNow/main/localnow_epg.xml
    ```

---

## 🧑‍💻 Instalação Local (Opcional)

Caso queira testar ou rodar o extrator manualmente no seu ambiente de desenvolvimento ou celular (Pydroid 3):

1. Clone o repositório:
   ```bash
   git clone https://github.com/JulioCesarXY/EPG-LocalNow.git
