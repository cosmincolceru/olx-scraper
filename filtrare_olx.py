from bs4 import BeautifulSoup
from jmespath import search
import requests
import re

print('Filtreaza dupa:')
print('1 - An')
print('2 - Pret')
print('3 - Stare')
print('4 - Marca')
print('5 - Tip produs')
print('6 - Produse care sa pot si schimba')
print('7 - Capacitate')
print('8 - Vezi produsele in garantie')
print('9 - Culoare')
print('10 - Sistem de operare')
varianta = int(input())
varianta2 = 0
pretmax = 0
cap = 0
if varianta == 1:
	print('1 - Vezi produsele mai vechi de 2010')
	print('2 - Vezi produsele mai noi de 2010')
	varinata2 = int(input())
elif varianta == 2:
	print('Introdu pretul maxim al produselor: ')
	pretmax = int(input())
elif varianta == 3:
	print('1 - Produse noi')
	print('2 - Produse produse utilizate')
	varinata2 = int(input())
elif varianta == 4:
	print('1 - Samsung')
	print('2 - Huawei')
	print('3 - Apple')
	print('4 - HP')
	print('5 - Lenovo')
	print('6 - Asus')
	varianta2 = int(input())
elif varianta == 5:
	print('1 - Telefon')
	print('2 - Laptop')
	print('3 - Calculator')
	print('4 - Tableta')
	print('5 - Masina de spalat')
	print('6 - Sistem de navigatie')
	varianta2 = int(input())
elif varianta == 7:
	print('Introdu capaciatea minima')
	cap = int(input())
elif varianta == 9:
	print('1 - Alb')
	print('2 - Negru')
	print('3 - Albastru')
	print('4 - Rosu')
	varianta2 = int(input())
elif varianta == 10:
	print('1 - Windows')
	print('2 - Linux')
	print('3 - Mac')
	print('4 - Android')
	print('5 - IOS')
	varianta2 = int(input())

f = open('produse_filtrate.html', 'w', encoding='utf-8')
f.write('''
<html>
	<head>
		<title>OLX - Produse Filtrate</title>
	</head>
	<body>
		<ul>
''')

output=[]
for x in range(5):
	html_text=requests.get("https://www.olx.ro/electronice-si-electrocasnice/?page={x}").text
	soup=BeautifulSoup(html_text,'lxml')
	jobs=soup.find_all("tr",class_="wrap")
	for job in jobs:
		link=job.find("a").get("href")
		Produs=job.strong.text
		categorie=job.find("small",class_="breadcrumb x-normal").text.replace("\n","").lstrip()

		Produs=Produs.replace("\u00e2","a")
		Produs=Produs.replace("\u021b","t")
		Produs=Produs.replace("\u0219","s")
		Produs=Produs.replace("\u2019","'")
		Produs=Produs.replace("\u00ee","i")
		Produs=Produs.replace("\u2022\t","i")
		Produs=Produs.replace("\u0103","a")
		Produs=Produs.replace("\u0102"," ")
		Produs=Produs.replace("\u2013"," ")
		# print(Produs) Titlu
		html_text2=requests.get(link).text
		soup1=BeautifulSoup(html_text2,'lxml')

		if(soup1.find("div",class_="css-g5mtbi-Text")):
			descriere=soup1.find("div",class_="css-g5mtbi-Text").text.replace("\u0103","a")
			descriere=descriere.replace("\u00e2","a")
			descriere=descriere.replace("\u021b","t")
			descriere=descriere.replace("\u0219","s")
			descriere=descriere.replace("\u2019","'")
			descriere=descriere.replace("\u00ee","i")
			descriere=descriere.replace("\u2022\t","i")
			descriere=descriere.replace("\u00a0"," ")
			descriere=descriere.replace("\u0102"," ")
			descriere=descriere.replace("\u2022"," ")
			descriere=descriere.replace("\u00ce"," ")
		  
			an = re.search(r'20\d\d', Produs)
			if an == None:
				an = re.search(r'20\d\d', descriere) 

			pret = re.search(r'\d+\s*([Ll]ei|[Ee]uro|ron|RON)', descriere)
			if pret == None:
				pret = re.search(r'\d+\s*([Ll]ei|[Ee]uro|ron|RON)', Produs)
			
			stareNoua = re.search(r'[Nn]ou|[Nn]efolosit|[Nn]eutilizat|[Ss]igilat', descriere)
			stareVeche = re.search(r'[Vv]echi|[Ff]olosit|[Uu]tilizat|[Nn]esigilat', descriere)

			samsung = re.search(r'[Ss]amsung', descriere)
			huawei = re.search(r'[Hh]uawei', descriere)
			apple = re.search(r'[Aa]pple|[Ii][pP]hone|[Ii][Pp]ad|[Ii][Mm]ac', descriere)
			hp = re.search(r'HP|hp', descriere)
			lenovo = re.search(r'[Ll]enovo', descriere)
			asus = re.search(r'[Aa]sus', descriere)

			telefon = re.search(r'[Tt]elefon|[Ii]phone', descriere)
			laptop = re.search(r'[Ll]aptop|[Nn]otebook|[Uu]ltrabook|[Mm]acbook', descriere)
			calculator = re.search(r'[Cc]alculator|PC|pc|iMac|[Cc]omputer', descriere)
			tableta = re.search(r'[Tt]ableta|[Ii][Pp]ad', descriere)
			masina_de_spalat = re.search(r'[Mm]asina de spalat', descriere)
			gps = re.search(r'gps|GPS|[Nn]avigare|[Nn]avigatie', descriere)

			schimb = re.search(r'[Ss]chimb', descriere)

			capacitate = re.search(r'\d+\s*(g|G|m|M|t|T)(b|B)', descriere)

			garantie = re.search(r'[Gg]arantie', descriere)

			alb = re.search(r'[Aa]lb|[Wh]ite', descriere)
			negru = re.search(r'[Nn]egru|[Bb]lack', descriere)
			albastru = re.search(r'[Aa]lbastru|[Bb]leu|[Bb]lue', descriere)
			rosu = re.search(r'[Rr]osu|[Rr]ed', descriere)

			windows = re.search(r'[Ww]indows|WINDOWS', descriere)
			linux = re.search(r'[Ll]inux|[Uu]buntu', descriere)
			mac = re.search(r'[Mm]ac', descriere)
			andoid = re.search(r'[Aa]ndroid', descriere)
			ios = re.search(r'IOS|ios|[Ii]os', descriere)

			if varianta == 1:
				if varianta2 == 1:
					if an:
						if int(an.group()) < 2010:
							print(Produs)
							f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				else:
					if an:
						if int(an.group()) >= 2010:
							print(Produs)
							f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
			elif varianta == 2:
				if pret:
					if int(pret.group()) < pretmax:
						print(Produs)
						f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
			elif varianta == 3:
				if varianta2 == 1:
					if stareNoua:
						print(Produs)
						f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				else:
					if stareVeche:
						print(Produs)
						f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
			elif varianta == 4:
				if varianta2 == 1 and samsung:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 2 and huawei:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 3 and apple:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 4 and hp:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 5 and lenovo:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 6 and asus:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
			elif varianta == 5:
				if varianta2 == 1 and telefon:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 2 and laptop:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 3 and calculator:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 4 and tableta:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 5 and masina_de_spalat:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 6 and gps:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
			elif varianta == 6:
				if schimb:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
			elif varianta == 7:
				if capacitate:
					capacitate = capacitate.group()[:-2]
					print(capacitate)
					if int(capacitate) > cap:
						print(Produs)
						f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
			elif varianta == 8:
				if garantie:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
			elif varianta == 9:
				if varianta2 == 1 and alb:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 2 and negru:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 3 and albastru:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 4 and rosu:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
			elif varianta == 10:
				if varianta2 == 1 and windows:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 2 and linux:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 3 and mac:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 4 and andoid:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')
				elif varianta2 == 5 and ios:
					print(Produs)
					f.write(f'<li><a href="{link}">{Produs}</a></li>\n')

f.write('''
		</ul>
	</body>
</html>
''')
