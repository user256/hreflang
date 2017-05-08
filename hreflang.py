import requests, csv, os, vars
from bs4 import BeautifulSoup as bs
from lxml import html
from time import sleep

vars.alt = ("en-ie", "en-gb", "en-au", "en-sg", "en-nz", "en", "de-de", "de-at", "de", "fr-fr", "pl-pl", "zh")
vars.missing = []
vars.found = []
vars.csvimport = []

def main():
    i = 0
    csvimport("crawllist.csv")
    langfinder() #find hreflang tag
    #exportmissing("missingalts.csv") #export missing tags
    #print(vars.missing)
    vars.missing = [] #clearing from memory
    hreflangindex() # build dictionary of hreflangs
    indexcheck()
    # exportmissing("nonreciprocal.csv") #export missing tags
    print(vars.missing)

def indexcheck():
    for dict in vars.found:
        if dict:
            for i in dict:
                #print(i, dict[i])
                page = requests.get(dict[i]).content
                tree = html.fromstring(page)
                if tree.xpath('//link[@hreflang=\"' + i + '\"]/@hreflang'):
                    hreflang = tree.xpath('//link[@hreflang=\"' + i + '\"]/@hreflang')[0]
                    href = tree.xpath('//link[@hreflang=\"' + i + '\"]/@href')[0]
                    #print (i, dict[i])
                    #print (hreflang, href)
                    #print( href, dict[i])
                    if href == dict[i]:
                        #print(str.replace(href,"https://www.","https://produk3-local-preview-www."))
                        pass # print("woo fucking hooooooo!!")
                    else:
                        vars.missing.insert(i, {"source": dict[i], "alt": i})
                sleep(1) #So we don't kill the server/get blocked

def hreflangindex():
    for url in vars.csvimport:
        i = 0
        tempdict = {}
        page = requests.get(url[0]).content
        tree = html.fromstring(page)
        for alt in vars.alt:
            if tree.xpath('//link[@hreflang=\"' + vars.alt[i] + '\"]/@hreflang'):
                hreflang = tree.xpath('//link[@hreflang=\"' + vars.alt[i] + '\"]/@hreflang')[0]
                href = tree.xpath('//link[@hreflang=\"' + vars.alt[i] + '\"]/@href')[0]
                tempdict[hreflang] = href
            i += 1
        vars.found.insert(i, tempdict)

def langfinder():
    tempdict = {}
    for url in vars.csvimport:
        i = 0
        x = 0
        html = bs(requests.get(url[0]).content, "html.parser")
        for alt in vars.alt:
            if html.find_all(hreflang=vars.alt[i]):
                #print(html.find_all(hreflang=vars.alt[i]))
                pass
            else:
                vars.missing.insert(i,{"source":url,"alt":alt})
            i += 1
        vars.found.insert(x, tempdict)
    sleep(1)

def exportmissing(filename):
    i = 0
    for x in vars.missing:
        csvexport(filename, vars.missing[i]["alt"], vars.missing[i]["source"][0])
        i +=1

def csvimport(filename):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            vars.csvimport.append(row)

def csvexport(filename, alt, url, comment="language tag not found on"):
    if os.path.isfile(filename):
        with open(filename, "a") as file:
            writer = csv.writer(file)
            writer.writerow([alt, comment, url])
            file.close()
    else:
        with open(filename, "a") as file:
            headers = ["hreflang", "status", "originating page"]
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerow([alt, comment, url])
            file.close()

if __name__ == "__main__":
    main()