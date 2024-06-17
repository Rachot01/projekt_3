"""
projekt_3.py: 3. projekt 
author: Jan Suchý
email: skeshi65496@gmail.com
discord:
"""

# Importy
import requests
from bs4 import BeautifulSoup
import argparse

# Funkce pro sestavení úplné URL z relativní URL
def sestav_url(base_url, relative_url):
    if '/' in base_url:
        return base_url[:base_url.rfind('/')] + "/" + relative_url
    return base_url

# Funkce pro získání názvů stran z dané URL
def ziskej_nazvy_stran(stranky_url):
    response = requests.get(stranky_url)  
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser') 
        radky = soup.find_all('tr') 
        seznam_stran = []
        for radek in radky:
            bunky = radek.find_all("td")
            if len(bunky) == 5:  
                nazev_strany = bunky[1].get_text().strip() 
                if nazev_strany not in seznam_stran:
                    seznam_stran.append(nazev_strany)  
        return seznam_stran
    else:
        print("Nepodarilo se stahnout data")
        return []

# Funkce pro zpracování hlavních dat z první URL
def zpracuj_data(prvni_url, soubor, strany_url):
    response = requests.get(prvni_url) 
    if response.status_code == 200:  
        soup = BeautifulSoup(response.content, 'html.parser')  
        radky = soup.find_all('tr')  
        cislo_radku = 0
        with open(soubor, 'w', encoding='cp1250') as f: 
            f.write("Kod oblasti;Nazev oblasti;Registrovany volici;Obalky;Platné hlasy;")
            seznam_stran = ziskej_nazvy_stran(strany_url)  
            f.write(";".join(seznam_stran))
            f.write("\n")
            for radek in radky:
                bunky = radek.find_all("td") 
                if len(bunky) >= 2:  
                    cislo_radku += 1
                    prvni_bunka = bunky.pop(0)
                    druha_bunka = bunky.pop(0)
                    odkazy = prvni_bunka.find_all("a")  
                    if odkazy:
                        prvni_odkaz = odkazy.pop(0)
                        relativni_url = prvni_odkaz.get('href') 
                        druha_url = sestav_url(prvni_url, relativni_url) 
                        radek_data = prvni_bunka.get_text().strip() + ";" + druha_bunka.get_text().strip()
                        seznam_stran = zpracuj_podrobnosti(druha_url, f, radek_data, cislo_radku, seznam_stran) 
            if cislo_radku == 1 and seznam_stran:
                f.write(";".join(seznam_stran))
                f.write("\n")
    else:
        print("Nepodarilo se stahnout data")

# Funkce pro zpracování podrobných dat z druhé URL
def zpracuj_podrobnosti(druha_url, soubor, radek_data, cislo_radku, seznam_stran):
    response = requests.get(druha_url)  
    if response.status_code == 200:  
        soup = BeautifulSoup(response.content, 'html.parser')  
        radky = soup.find_all('tr') 
        radek_info = ""
        seznam_hlasu = []
        for radek in radky:
            bunky = radek.find_all("td") 
            if len(bunky) == 9: 
                prvni_bunka = bunky.pop(3)
                druha_bunka = bunky.pop(3)
                platne_hlasy_bunka = bunky.pop(5)
                radek_info = prvni_bunka.get_text().strip() + ";" + druha_bunka.get_text().strip() + ";" + platne_hlasy_bunka.get_text().strip()
            if len(bunky) == 5:  
                nazev_strany = bunky.pop(1)
                hlasy_strany = bunky.pop(1)
                if cislo_radku == 1:
                    seznam_stran.append(nazev_strany.get_text().strip())  
                seznam_hlasu.append(hlasy_strany.get_text().strip())  
        soubor.write(radek_data + ";" + radek_info + ";" + ";".join(seznam_hlasu))
        soubor.write("\n")
        return seznam_stran
    else:
        print("Nepodarilo se stahnout data")
        return seznam_stran

# Hlavní funkce skriptu
def hlavni(url, soubor, strany_url):
    zpracuj_data(url, soubor, strany_url)

if __name__ == '__main__':
    # Nastavení argumentů příkazového řádku
    parser = argparse.ArgumentParser(description='Skript pro webscraping')
    parser.add_argument('url', type=str, help='URL adresa stránky pro stazeni')
    parser.add_argument('soubor', type=str, help='Vystupni soubor')
    parser.add_argument('strany_url', type=str, help='URL pro ziskani nazvu stran')
    args = parser.parse_args()
    hlavni(args.url, args.soubor, args.strany_url)
