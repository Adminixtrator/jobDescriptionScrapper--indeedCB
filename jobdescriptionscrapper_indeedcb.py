# -*- coding: utf-8 -*-
"""jobDescriptionScrapper--indeedCB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S_mBryC4ltvQGwCY7Zv_SDHIygAjvtE8

## Not exactly ***Open Source*** yunno, so no comments ✌️😌✌️
"""

import requests
from bs4 import BeautifulSoup
import time
import urllib


"""### Scrape Indeed JD"""


class indeedScraper():
      
  def extract_job_title_from_result(soup):
    jobTitles = []
    for div in soup.find_all(name="div", attrs={"id": "viewJobSSRRoot"}):
      for a in div.find_all(name="h1"):
        jobTitles.append(a.text.strip())
    try:
      return jobTitles[0]
    except:
      return ''

  def extract_job_location_from_result(soup):
    jobLocation = []
    for div in soup.find_all(name="div", attrs={"class": "jobsearch-DesktopStickyContainer-subtitle"}):
      for a in div.find_all(name="div"):
        jobLocation.append(a.text.strip())
    try:
      return jobLocation[1]
    except:
      return ''

  def extract_company_job_posting_from_result(soup, URL):
    companyJobPosting = []
    for div in soup.find_all(name="div", attrs={"id": "applyButtonLinkContainer"}):
      for a in div.find_all(name="a", attrs={"role": "link"}):
        companyJobPosting.append(a['href'])
    try:
      return companyJobPosting[0]
    except:
      return URL

  def extract_job_policy_from_result(soup):
    jobPolicy = []
    for div in soup.find_all(name="div", attrs={"class": "jobsearch-DesktopStickyContainer-subtitle"}):
      for a in div.find_all(name="div"):
        jobPolicy.append(a.text.strip())
    try:
      return ' | '.join(jobPolicy[-2:])
    except:
      return ''

  def extract_full_jd_from_result(soup):
    fullJD = []
    fullJDString = ""
    for div in soup.find_all(name="div", attrs={"id": "jobDescriptionText"}):
      for lines in div.find_all(name="div"):
        fullJD.append(lines.text.strip())
    cache = list(dict.fromkeys(fullJD))
    for i in cache:
      if i != "" and fullJDString.find(i) < 0:
        if i.isupper() or i.find(':') > 0:
          fullJDString = fullJDString + "\n\n" + i
        else:
          fullJDString = fullJDString + "\n" + i
    return fullJDString

  def extract_job_poster_and_age_from_result(soup):
    jobPosterAndAge = []
    for div in soup.find_all(name="div", attrs={"class": "jobsearch-JobMetadataFooter"}):
      for a in div.find_all(name="div"):
        jobPosterAndAge.append(a.text.strip())
    try:
      return " | ".join([jobPosterAndAge[0], jobPosterAndAge[1]])
    except:
      return ''



"""### Scrape CB JD

"""


class cbScraper():
      
  def extract_job_title_from_result(soup):
    jobTitles = []
    for div in soup.find_all(name="div", attrs={"class": "data-display"}):
      for a in soup.find_all(name="h2", attrs={"class": "h3"}):
        jobTitles.append(a.text.strip())
    try:
      return jobTitles[0]
    except:
      return ''

  def extract_job_location_from_result(soup):
    jobLocation = []
    for div in soup.find_all(name="div", attrs={"class": "data-display"}):
      for a in div.find_all(name="div", attrs={"class": "data-details"}):
        for b in a.find_all(name="span"):
          jobLocation.append(b.text.strip())
    return " | ".join(jobLocation)

  def extract_company_job_posting_from_result(soup):
    companyJobPosting = []
    for div in soup.find_all(name="div", attrs={"class": "data-display"}):
      for a in div.find_all(name="a", attrs={"data-gtm": "job-action|apply-internal-top"}):
        companyJobPosting.append(a['href'])
    try:
      return companyJobPosting[0]
    except:
      return ''

  def extract_full_jd_from_result(soup):
    fullJD = []
    fullJDString = ""
    for div in soup.find_all(name="div", attrs={"class": "jdp-description-details"}):
      for a in soup.find_all(name="div", attrs={"class": "col-mobile-full"}):
        for lines in div.find_all(name="div"):
          fullJD.append(lines.text.strip())
    cache = list(dict.fromkeys(fullJD))
    for i in cache:
      if i != "" and fullJDString.find(i) < 0 and fullJDString.find(");") < 0:
        fullJDString = fullJDString + "\n\n" + i
    return fullJDString[:-95]

  def extract_job_salary_from_result(soup):
    jobSalaries = []
    for div in soup.find_all(name="div", attrs={"class": "data-snapshot"}):
      for a in soup.find_all(name="div", attrs={"class": "block"}):
        jobSalaries.append(a.text.strip())
    try:
      return jobSalaries[0]
    except:
      return ''



if __name__ == '__main__':
  
  URL = input("URl: ")
  JDLoc = input("isIndeed: ")
  page = requests.get(URL)
  JDsoup = BeautifulSoup(page.text, "html.parser")
  responseJson = {}

  if JDLoc.lower() == 'yes':
    jobTitle = indeedScraper.extract_job_title_from_result(JDsoup)
    jobLocation = indeedScraper.extract_job_location_from_result(JDsoup)
    refUrl = indeedScraper.extract_company_job_posting_from_result(JDsoup, URL)
    jobPolicy = indeedScraper.extract_job_policy_from_result(JDsoup)
    JD = indeedScraper.extract_full_jd_from_result(JDsoup)
    footer = indeedScraper.extract_job_poster_and_age_from_result(JDsoup)
    responseJson["jobTitle"] = jobTitle
    responseJson["jobLP"] = jobLocation + " | " + jobPolicy
    responseJson["applyUrl"] = refUrl
    responseJson["fullJD"] = JD
    responseJson["salary"] = ""
    responseJson["footer"] = footer
  else:
    jobTitle = cbScraper.extract_job_title_from_result(JDsoup)
    jobLocation = cbScraper.extract_job_location_from_result(JDsoup)
    refUrl = cbScraper.extract_company_job_posting_from_result(JDsoup)
    JD = cbScraper.extract_full_jd_from_result(JDsoup)
    jobPay = cbScraper.extract_job_salary_from_result(JDsoup)
    responseJson["jobTitle"] = jobTitle
    responseJson["jobLP"] = jobLocation
    responseJson["applyUrl"] = refUrl
    responseJson["fullJD"] = JD
    responseJson["salary"] = jobPay
    responseJson["footer"] = ""
    
  print(responseJson)


