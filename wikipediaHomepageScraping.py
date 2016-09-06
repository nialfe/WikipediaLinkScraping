#Imports move these to __init__.py
import csv, os, urllib
from bs4 import BeautifulSoup

class WikipediaHomepageScraping(object):
  def __init__(self, categoryPageUrl):
    self.wikiLinks = []
    self.numWikiLinks = 0
    self.db = {}
    self.baseUrl = "http://www.wikipedia.org/"
    self.linksName = "wikiLinks.txt"
    self.csvName = "NonProfits.csv"

    self.getWikiLinks(categoryPageUrl)
    self.getAllHomepages()

  def getWikiLinks(self, categoryPageUrl):
    if not os.path.isfile(self.linksName) or os.path.getsize(self.linksName) == 0:
      links = self.getSoup(categoryPageUrl).find("div", {"class" : "mw-category"})

      for link in links.find_all("a"):
        href = self.extractHref(link)
        self.wikiLinks.append(href)
        self.numWikiLinks += 1
      self.writeLinksToFile(self.wikiLinks)
    else:
      self.loadFromUrls(self.linksName)
      print "Using old wikiLinks file"

  def getAllHomepages(self):
    if not os.path.isfile(self.csvName) or os.path.getsize(self.csvName) == 0:
      for link in self.wikiLinks:
        link = self.baseUrl + link
        self.getHomepageUrl(link)
      self.writeToCsv()
    else:
      self.readCsvData(self.csvName)

  def getHomepageUrl(self, wikiLink):
    print "getting %s", wikiLink
    soup = self.getSoup(wikiLink)
    child = soup.find(id="External_links")
    if child is None:
      print "COULD NOT FIND EXTERNAL_LINKS "
      return
    unorderedlistElt = child.parent.next_sibling.next_sibling
    link = unorderedlistElt.find('a')
    href = self.extractHref(link)
    orgName = self.extractOrgName(soup)
    self.db[orgName] = href

### HELPER FUNCTIONS
  def extractHref(self, link):
    href = link.get('href')
    return href

  def extractOrgName(self, soup):
    child = soup.find(id="firstHeading")
    return child.getText()


  def getSoup(self, url):
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, 'html.parser')
    return soup
 
  def printHomepages(self):
    count = 0
    for key, value in self.db.iteritems():
      count += 1
      print key, ' ', value
    print "Got %d homepages" % count

  def writeLinksToFile(self, links):
    f = open(self.linksName, "w")
    for link in links:
      link = link + '\n'
      f.write(link)
    f.close()

  def loadFromUrls(self, fileName):
    f = open(fileName, 'r')
    self.wikiLinks = f.readlines()
    f.close()

  def readCsvData(self, fileName):
    f = open(fileName, 'rb')
    try:
      reader = csv.reader(f, delimiter=',')
      for row in reader:
      	self.db[row[0]] = row[1]
    finally:
      f.close()

  def writeToCsv(self):
    f = open(self.csvName, 'w')
    try:
      writer = csv.writer(f)
      writer.writerow( ('Name', 'Website', 'Address', 'Number', 'Hours', 'Subject') )
      for key, value in self.db.iteritems():
        writer.writerow([key, value])
    finally:
      f.close()
"""
  def scrapeHomepage(self, url):

  def getOrgName(self):

  def getOrgWebsite(self):

  def getOrgNumber(self):

  def getOrgEmail(self):

  def getOrgHours(self):
"""

# DELETE AFTER DEV
url = "https://en.wikipedia.org/wiki/Category:Non-profit_organizations_based_in_Chicago,_Illinois"
ob = WikipediaHomepageScraping(url)
