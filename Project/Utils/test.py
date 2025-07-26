import xlsxwriter

wb = xlsxwriter.Workbook('fichier.xlsx')
ws = wb.add_worksheet()

# Insère les données à afficher
data = [1, 2, 3]
ws.write_column('A1', data)

# Crée un objet Chart de type colonne
chart = wb.add_chart({'type': 'column'})

# Ajoute une série de données
chart.add_series({'values': '=Sheet1!$A$1:$A$3'})

# Insère le graphique dans la feuille de calcul
ws.insert_chart('C1', chart)

wb.close()
