from selenium import webdriver
from selenium.webdriver.common.keys import Keys

'''
==================================================
                CheckBill(bill)

    checkBill takes a string bill and will return 
    bill prepended with enough 0's to get to a
    length of 8. This function returns the 
    string if it has a length of 8 or more
==================================================
'''

def checkBill(bill):
    billLen = len(bill)
    if billLen < 8:
        x = 8 - billLen
        return (x * '0') + bill
    else:
        return bill

def buildRow(driver, bill, listNumber):
    listNumber = listNumber.replace(',', '')
    listNumber = abs(float(listNumber))

    bill = checkBill(bill)

    try:
        driver.get("https://apps.montgomerycountymd.gov/realpropertytax/")
        bill_search_bar = driver.find_element_by_name("ctl00$MainContent$BillNumber")
        bill_search_bar.clear()
        bill_search_bar.send_keys(bill)
        bill_search_bar.send_keys(Keys.RETURN)
    except:
        driver.find_element_by_xpath('//*[@id="acsFocusFirst"]').click()
        driver.get("https://apps.montgomerycountymd.gov/realpropertytax/")
        bill_search_bar = driver.find_element_by_name("ctl00$MainContent$BillNumber")
        bill_search_bar.clear()
        bill_search_bar.send_keys(bill)
        bill_search_bar.send_keys(Keys.RETURN)

    bill = checkBill(bill)

    try:
        tableChecker = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_grdParcel"]/tbody/tr').get_attribute('class')
        if tableChecker == "empty":
            return [listNumber, '', '', bill, "This Bill is not found", '', '', '', '', '', '', '', '', '']
    except:
        compName = driver.find_element_by_xpath('//*[@id="aspnetForm"]/section/div/div[2]/table/tbody/tr[2]/td[4]/span').text.strip()
        levyYear = driver.find_element_by_xpath('//*[@id="aspnetForm"]/section/div/div[2]/table/tbody/tr[2]/td[1]/span').text.strip()
        billType = driver.find_element_by_xpath('//*[@id="aspnetForm"]/section/div/div[2]/table/tbody/tr[2]/td[2]/span').text.strip()
        balance = abs(float(driver.find_element_by_xpath('//*[@id="aspnetForm"]/section/div/div[2]/table/tbody/tr[2]/td[5]/span').text.strip()))
        
        if listNumber == balance:
            return [listNumber, levyYear, billType, bill, compName, balance, '', '', 'yes', '', '', '', '', '']
        else:
            return [listNumber, levyYear, billType, bill, compName, balance, '', '', '', '', '', '', '', '']

    

    compName = driver.find_element_by_xpath("//*[@id='ctl00_MainContent_grdParcel']/tbody/tr[2]/td[4]").text.upper()
    levyYear = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_grdParcel"]/tbody/tr[2]/td[1]').text
    billType = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_grdParcel"]/tbody/tr[2]/td[2]').text
    balance = abs(float(driver.find_element_by_xpath('//*[@id="ctl00_MainContent_grdParcel"]/tbody/tr[2]/td[5]').text))

    if balance == 0.0:
        if listNumber == 0.0:
            return [listNumber, levyYear, billType, bill, compName, balance, '', '', 'yes', '', '', '', '', '']
        else:
            return [listNumber, levyYear, billType, bill, compName, balance, '', '', '', '', '', '', '', '']

    #At Tax Page
    try:
        driver.find_element_by_link_text("Click").click()
    except:
        driver.find_element_by_xpath('//*[@id="acsFocusFirst"]').click()
        driver.find_element_by_link_text("Click").click()

    propertyAddress = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_lblPropAddress"]').text
    mortgageLine1 = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_lblMortgage"]').text
    mortgageLine2 = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_lblName"]').text
    mortgageLine3 = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_lblCompleteAddress"]').text
    propertyDescription = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_lblPropDesc"]').text
    interest = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_lblInterestDueAmt"]').text

    if interest == "":
        interest = 0.00
        total = balance
    else:
        interest = interest.replace('$', '')
        interest = interest.replace(',', '')
        total = float(interest) + balance

    isTotaleqList = ""

    if (total == listNumber):
        isTotaleqList = 'yes'

    return [listNumber, levyYear, billType, bill, compName, balance, interest, total, 
            isTotaleqList, propertyAddress, mortgageLine1, propertyDescription, mortgageLine2, mortgageLine3]
