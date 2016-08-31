#Imports move these to __init__.py
import urllib
from bs4 import BeautifulSoup

class WikipediaHomepageScraping(object):
  def __init__(self, categoryPageUrl):
    self.wikiLinks = []
    self.numWikiLinks = 0
    self.db = {}

    self.getWikiLinks(categoryPageUrl)

    self.baseUrl = "http://www.wikipedia.org/"
    self.getAllHomepages()

  def getWikiLinks(self, categoryPageUrl):
    links = self.getSoup(categoryPageUrl).find("div", {"class" : "mw-category"})

    for link in links.find_all("a"):
      orgName, href = self.extractHrefAndText(link, True)
      self.wikiLinks.append(href)

  def getAllHomepages(self):
    for link in self.wikiLinks:
      link = self.baseUrl + link
      self.getHomepageUrl(link)
    self.printHomepages()

  def getHomepageUrl(self, wikiLink):
    print "getting %s", wikiLink
    soup = self.getSoup(wikiLink)
    child = soup.find(id="External_links")
    if child is None:
      print "COULD NOT FIND EXTERNAL_LINKS "
      return
    unorderedlistElt = child.parent.next_sibling.next_sibling
    link = unorderedlistElt.find('a')
    orgName, href = self.extractHrefAndText(link, False)
    self.db[orgName] = href

### HELPER FUNCTIONS
    #Input: an anchor tag and a boolean value whether it should increment the    instance var numWikiLinks
    #Effects: returns innerHtml and href
    #  Will increment if needed
  def extractHrefAndText(self, link, increment):
    href = link.get('href')
    orgName = link.getText()
    if increment:
      self.numWikiLinks +=1
    return orgName, href

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
