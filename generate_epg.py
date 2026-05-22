import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import requests

# Endpoint oficial de EPG que você mapeou
EPG_URL = "https://data-store-trans-cdn.api.cms.amdvids.com/live/epg/US/website"
PARAMS = {
    "program_size": "6",  # Pega até 6 horas de grade por canal
    "dma": "678",
    "market": "ksWichita,pbs-kpts"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Origin": "https://localnow.com",
    "Referer": "https://localnow.com/"
}

def format_timestamp_xmltv(timestamp):
    """Converte o timestamp Unix para o padrão estrito exigido pelos players IPTV"""
    try:
        dt = datetime.fromtimestamp(int(timestamp), timezone.utc)
        return dt.strftime("%Y%m%dd%H%M%S +0000")
    except Exception:
        return datetime.now(timezone.utc).strftime("%Y%m%dd%H%M%S +0000")

def main():
    print("[*] Iniciando a extração do Guia de Programação (EPG)...")
    try:
        response = requests.get(EPG_URL, params=PARAMS, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[-] Erro ao conectar com a API de EPG: {e}")
        return

    if "channels" not in data:
        print("[-] Resposta da API inválida (chave 'channels' não encontrada).")
        return

    channels_list = data["channels"]
    print(f"[*] Processando grade de {len(channels_list)} canais...")

    # Cria a tag raiz do XMLTV
    tv_root = ET.Element("tv", attrib={"generator-info-name": "LocalNow Dedicated EPG Generator"})

    for ch in channels_list:
        ch_id = str(ch.get("_id", ""))
        ch_name = ch.get("name", f"Local Now {ch_id}")
        logo = ch.get("logo", "")

        if not ch_id:
            continue

        # 1. Estrutura o bloco do Canal
        xml_channel = ET.SubElement(tv_root, "channel", id=ch_id)
        ET.SubElement(xml_channel, "display-name").text = ch_name
        if logo:
            ET.SubElement(xml_channel, "icon", src=logo)

        # 2. Estrutura os blocos de programas vinculados a este Canal
        programs = ch.get("program", [])
        for prog in programs:
            p_title = prog.get("program_title", "No Program Details")
            p_desc = prog.get("program_description", "")
            start_ts = prog.get("starts_at")
            end_ts = prog.get("ends_at")

            if start_ts and end_ts:
                start_xml = format_timestamp_xmltv(start_ts)
                end_xml = format_timestamp_xmltv(end_ts)

                xml_programme = ET.SubElement(tv_root, "programme", start=start_xml, stop=end_xml, channel=ch_id)
                ET.SubElement(xml_programme, "title", lang="en").text = p_title
                if p_desc:
                    ET.SubElement(xml_programme, "desc", lang="en").text = p_desc

    # Salva o XML formatado
    tree = ET.ElementTree(tv_root)
    try:
        ET.indent(tree, space="  ", level=0)  # Organiza a identação para ficar legível
    except AttributeError:
        pass
    
    output_filename = "localnow_epg.xml"
    tree.write(output_filename, encoding="utf-8", xml_declaration=True)
    print(f"[+] Sucesso! Arquivo '{output_filename}' gerado com toda a grade.")

if __name__ == "__main__":
    main()
