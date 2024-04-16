# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

#
# Imports
#
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from html_table_parser import HTMLTableParser
from optparse import OptionParser
from gettext import gettext as _
import sys
import os
import pandas as pd
import time

#
# Constants
#
USAGE = _('%prog <options>')
DESCRIPTION = _('Search South Carolina Probate Data Records.  The results are output to a .csv file.')
COUNTY = _('Specify a county for the search. Optionally, you can specify multiple ("i.e. -c Aiken -c Charleston") or "ALL" to search all counties.')
LASTNAME = _('Specify the last or business name for the search. You can use "%" to wildcard.')
FIRSTNAME = _('Specify the first name for the search. You can use "%" to wildcard.')
MIDDLENAME = _('Specify the middle name for the search. You can use "%" to wildcard.')
TYPE = _('Specify the type of records to be searched.  Valid values are "Estate" (Default) or "Marriage".')

SITEURL = 'https://www.southcarolinaprobate.net/search/'

class Progress:

    #
    # This class provides progress indication to the User.
    #

    def __init__(self, size):
        self.size = size
        self.count = 1

    def next(self):

        if self.count == self.size:
            self.count = 1
            sys.stdout.write(".\n")
            sys.stdout.flush()
        else:
            self.count = self.count + 1
            sys.stdout.write(".")
            sys.stdout.flush()


def process_county(county, rawdata, progress):

    ###
    #Process the County Search Results and Normalize Data
    ###

    output = []

    match county:
        case 'Aiken':
            for row in rawdata[1:-1]:
                if len(row.find_elements(By.TAG_NAME, "td")) == 9:
                    output.append({
                        'CaseNumber':row.find_elements(By.TAG_NAME, "td")[0].text,
                        'CaseName':row.find_elements(By.TAG_NAME, "td")[1].text,
                        'Party':row.find_elements(By.TAG_NAME, "td")[2].text,
                        'CaseType':row.find_elements(By.TAG_NAME, "td")[3].text,
                        'FilingDate':row.find_elements(By.TAG_NAME, "td")[4].text,
                        'County':row.find_elements(By.TAG_NAME, "td")[5].text,
                        'AppointmentDate':row.find_elements(By.TAG_NAME, "td")[6].text,
                        'CreditorClaimDue':row.find_elements(By.TAG_NAME, "td")[7].text,
                        'CaseStatus':row.find_elements(By.TAG_NAME, "td")[8].text
                    })
                    progress.next()
        case 'Chester' | 'Dorchester Probate':
            for row in rawdata[1:-1]:
                if len(row.find_elements(By.TAG_NAME, "td")) == 9:
                    output.append({
                        'CaseNumber':row.find_elements(By.TAG_NAME, "td")[1].text,
                        'CaseName':row.find_elements(By.TAG_NAME, "td")[2].text,
                        'Party':row.find_elements(By.TAG_NAME, "td")[3].text,
                        'CaseType':row.find_elements(By.TAG_NAME, "td")[4].text,
                        'FilingDate':row.find_elements(By.TAG_NAME, "td")[5].text,
                        'County':row.find_elements(By.TAG_NAME, "td")[6].text,
                        'AppointmentDate':row.find_elements(By.TAG_NAME, "td")[7].text,
                        'CreditorClaimDue':'',
                        'CaseStatus':row.find_elements(By.TAG_NAME, "td")[8].text
                    })
                    progress.next()
        case 'Jasper' | 'Barnwell' | 'Beaufort':
            for row in rawdata[1:-1]:
                if len(row.find_elements(By.TAG_NAME, "td")) == 8:
                    output.append({
                        'CaseNumber':row.find_elements(By.TAG_NAME, "td")[0].text,
                        'CaseName':row.find_elements(By.TAG_NAME, "td")[1].text,
                        'Party':row.find_elements(By.TAG_NAME, "td")[2].text,
                        'CaseType':row.find_elements(By.TAG_NAME, "td")[3].text,
                        'FilingDate':row.find_elements(By.TAG_NAME, "td")[4].text,
                        'County':row.find_elements(By.TAG_NAME, "td")[5].text,
                        'AppointmentDate':row.find_elements(By.TAG_NAME, "td")[6].text,
                        'CreditorClaimDue':'', 
                        'CaseStatus':row.find_elements(By.TAG_NAME, "td")[7].text
                    })
                    progress.next()
        case 'Bamberg' | 'Charleston Probate' | 'Cherokee' | 'Colleton' | 'Florence' | 'Georgetown'| 'Kershaw' | 'Lancaster' | 'Marlboro' | 'Newberry' | 'Oconee' | 'Orangeburg' | 'Sumter':
                for row in rawdata[1:-1]:
                    if len(row.find_elements(By.TAG_NAME, "td")) == 10:
                        output.append({
                            'CaseNumber':row.find_elements(By.TAG_NAME, "td")[1].text,
                            'CaseName':row.find_elements(By.TAG_NAME, "td")[2].text,
                            'Party':row.find_elements(By.TAG_NAME, "td")[3].text,
                            'CaseType':row.find_elements(By.TAG_NAME, "td")[4].text,
                            'FilingDate':row.find_elements(By.TAG_NAME, "td")[5].text,
                            'County':row.find_elements(By.TAG_NAME, "td")[6].text,
                            'AppointmentDate':row.find_elements(By.TAG_NAME, "td")[7].text,
                            'CreditorClaimDue':row.find_elements(By.TAG_NAME, "td")[8].text,
                            'CaseStatus':row.find_elements(By.TAG_NAME, "td")[9].text
                        })
                        progress.next()
    return output

def get_options():
    """
    Parse and return command line options.
    Sets defaults and validates options.

    :return: The options passed by the user.
    :rtype: optparse.Values
    """
    parser = OptionParser(usage=USAGE, description=DESCRIPTION)
    parser.add_option("-c", "--county", action="append", dest="county", help=COUNTY)
    parser.add_option("-t", "--type", dest="type", help=TYPE, default="Estate")
    parser.add_option("-l", "--lastname", dest="lastname", help=LASTNAME)
    parser.add_option("-f", "--firstname", dest="firstname", help=FIRSTNAME)
    parser.add_option("-m", "--middlename", dest="middlename", help=MIDDLENAME)

    (opts, args) = parser.parse_args()

    # validate input
    if opts.county is None:
        print("Please specify ateast one valid county (see -h for help).")
        sys.exit(1)

    if opts.lastname is None and opts.firstname is None  and opts.middlename is None:
        print("Please specify ateast one search criteria (see -h for help).")
        sys.exit(1)

    if (opts.type != 'Estate' and opts.type != 'Marriage'):
        print("Please enter a valid type. (see -h for help).")
        sys.exit(1)

    if opts.type == 'Marriage':
        print("The Marriage type search has not been implemented.")
        sys.exit(1)

    return opts


def main():
    """
    The command entry point.
    """

    _dir = os.getcwd()
    options = get_options()
    progress = Progress(30)
        
    # Run Chrome in headless mode Option
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    total_records = 0

    driver = webdriver.Chrome(options=chrome_options)
    results = []

    for county in options.county: 

        if county == 'Charleston':
            county = 'Charleston Probate'
        elif county == 'Dorchester':
            county = 'Dorchester Probate'

        try: 
            driver.get(SITEURL)

            countySelector = Select(driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_ddlCounties"]'))
            countySelector.select_by_visible_text(county)

            if options.lastname is not None:
                last = driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_tbLastName"]')
                last.send_keys(options.lastname)

            if options.firstname is not None:
                first = driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_tbFirstName"]')
                first.send_keys(options.firstname)

            if options.middlename is not None:
                first = driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_tbMiddleName"]')
                first.send_keys(options.middlename)

            searchButton = driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_btnSearch"]')
            searchButton.click()

            # Wait for search query to complete.
            time.sleep(5)

            page = 1
            end_of_content = False
            start_idx = 0

            #loop over all pages of search results
            while(not end_of_content):

                results_trs = driver.find_elements(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_cgvCases"]/tbody/tr')
        
                if len(results_trs) > 0:
                    *_, last  = results_trs

                    page_results = process_county(county, results_trs, progress)
                    total_records += len(page_results)
                    results.extend(page_results)

                    #last row in result table contains pagination controls
                    pages = last.find_elements(By.TAG_NAME, "a")

                    if len(pages) > 0 and pages[0].text != "":

                        page_found = False
                    
                        for pg in pages:

                            if pg.text != '...':
                    
                                if int(pg.text) == page+1:
                                    page=page+1
                                    pg.click()
                                    page_found = True
                                    time.sleep(5)
                                    break  
                            
                        if not page_found and (page > int(pages[len(pages)-2].text)):
                            if pages[len(pages)-1].text == "...":
                                page=page+1
                                pages[len(pages)-1].click()
                                start_idx = 1
                                time.sleep(5)
                            else:
                                end_of_content = True 

                    else:
                        end_of_content = True 

                else:
                    end_of_content = True 

        except Exception as e:
            print("An error occurred:", e)
            sys.exit(1)

    if len(results) > 0: 
        pd.DataFrame(results).to_csv("results.csv", encoding='utf-8', index=False)
        print(str(total_records) + " Records Found.")
    else:
        print("No Records Found.")

## MAIN
if __name__ == "__main__":
    main()
