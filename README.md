# projekt_3
# Třetí Projekt: Web Scraping pro Volby 2017

## Autor
- **Jméno:** Jan Suchý
- **Email:** skeshi65496@gmail.com
- **Discord:**

## Popis
Tento projekt je zaměřen na web scraping dat z volební stránky ČSÚ pro volby v roce 2017. Skript stahuje data o výsledcích voleb z dané URL, zpracovává je a ukládá do CSV souboru.

## Požadavky
Před spuštěním skriptu je nutné nainstalovat následující Python knihovny:
- `requests`
- `beautifulsoup4`

Tyto knihovny lze nainstalovat pomocí následujícího příkazu:
```bash
pip install requests beautifulsoup4

## Použití
Pro spuštění skriptu použijte následující příkaz v příkazovém řádku:
python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_kraj.csv "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101"

## Struktura
Skript je rozdělen do následujících funkcí:

Funkce #sestav_url
Sestaví úplnou URL z relativní URL.

Funkce #ziskej_nazvy_stran
Stáhne a zpracuje názvy stran z dané URL.

Funkce #zpracuj_data
Stáhne a zpracuje hlavní data z první URL.

Funkce #zpracuj_podrobnosti
Stáhne a zpracuje podrobná data z druhé URL.

Hlavní funkce #hlavni
Řídí celý proces stahování a zpracování dat.
