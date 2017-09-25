'''
Created on 06 giu 2017

@author: ROCCO - GERARDO
'''

from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

url = 'http://www.amsterdamtips.com/tips/parking-in-amsterdam.php'

#the method opens the connection and parses the costs of the various electric charge points for the "url" set in url variable
def getElectricChargeCost():
    
    #open connection
    conn = urlopen(url)
    page_html = conn.read()
    conn.close()
    
    #parse the table
    page_soup = soup(page_html, "html.parser")
    tables = page_soup.findAll("table")
    parkingCost1 = extractData(tables[2])
    parkingCost2 = extractData(tables[3])
    parkingCost = parkingCost1 + parkingCost2
    return parkingCost

#the method gets the informations from the tables contained in the web page related to the url
def extractData(table):
    rows = table.findChildren('tr')
    rows = rows[1:]
    rowFormatted = []
    for row in rows:
        cells = row.findChildren('td')
        rowFormatted.append([cells[1], cells[-1]])   
    parkingCost = []        
    for row in rowFormatted:    
        rowClean = []
        for cell in row:           
            value = list(cell.stripped_strings)
            string = ' '.join(value)
            string = string.split()
            string = ' '.join(string)
            rowClean.append(string)
        parkingCost.append(rowClean)
    return parkingCost

