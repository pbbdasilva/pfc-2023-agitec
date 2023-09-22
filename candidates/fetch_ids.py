from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import sys, os
from selenium.webdriver.chrome.service import Service as ChromeService
import sys
import re
import platform
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

searchUrl = 'http://buscatextual.cnpq.br/buscatextual/busca.do?metodo=apresentar'
desiredWords = {"Instituto Militar", "Oficiais", "Academia Militar", "Sargentos", "EsSEx", "Exército",
                "Escola Superior de Guerra"}

searchXPath = '''/html/body/form/div/div[4]/div/div/div/div[7]/div/div[1]/a'''
namePath = '/html/body/form/div/div[4]/div/div/div/div[3]/div/div[3]/ol/li/b/a'
idLattesPath = "/html/body/div[1]/div[3]/div/div/div/div[1]/ul/li[2]/span[2]"
candidatesFilePath = "202301Army.xlsx"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
def backTosearchForm():
    driver.get(searchUrl)


def justSearchTab(searchTabId):
    for id in driver.window_handles:
        if id != searchTabId:
            driver.switch_to.window(id)
            driver.close()
    driver.switch_to.window(searchTabId)


def hasOcurrences(desiredStr):
    try:
        html = driver.page_source
        pos = html.find(desiredStr)
        print(f"{desiredStr} found in position: " + str(pos)) if pos != -1 else print(f"{desiredStr} not found")
        return pos != -1
    except Exception as e:
        print(e)
        printError()


def insertName(name):
    driver.find_element(By.XPATH, '//*[@id="textoBusca"]').clear()
    driver.find_element(By.XPATH, '//*[@id="textoBusca"]').send_keys(name)


def setGeneralSearch():
    driver.find_element(By.XPATH, '//*[@id="buscarDemais"]').click()


def extractId(driver, searchTabId, name):
    insertName(driver, name)
    # search
    driver.find_element(By.XPATH, searchXPath).click()
    sleep(1)
    driver.find_element(By.XPATH,
                        '''/html/body/form/div/div[4]/div/div/div/div[7]/div/div[1]/a''').click()  # search button


def isFromOrg(desiredWords):  # return if it should continue
    driver.find_element(By.XPATH, '//*[@id="idbtnabrircurriculo"]').click()
    sleep(1)
    changeTab(searchTabId)
    for word in desiredWords:
        if hasOcurrences(word): return True
    return False


def exists(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


listIndex = 1
pageIndex = 1


def findInList(searchTabId):  # return true if it should continue
    global listIndex
    global pageIndex
    if listIndex == 11:
        print("attention")
    sleep(2)
    try:
        if (not exists(f'/html/body/form/div/div[4]/div/div/div/div[3]/div/div[3]/ol/li[{listIndex}]/b/a')
                and not exists(f'/html/body/form/div/div[4]/div/div/div/div[3]/div/div[3]/ol/li/b/a')):
            hasMoreResults, found, list = False, False, False
            return hasMoreResults, found, list
        elif (not exists(f'/html/body/form/div/div[4]/div/div/div/div[3]/div/div[3]/ol/li[{listIndex + 1}]/b/a')
              and not exists(f'/html/body/form/div/div[4]/div/div/div/div[3]/div/div[4]/a[{pageIndex + 1}]')):
            driver.find_element(By.XPATH, f'/html/body/form/div/div[4]/div/div/div/div[3]/div/div[3]/ol/li/b/a').click()
            hasMoreResults = False
            found = isFromOrg(desiredWords)
            list = True
            return hasMoreResults, found, list
        else:
            try:
                driver.find_element(By.XPATH,
                                    f'/html/body/form/div/div[4]/div/div/div/div[3]/div/div[3]/ol/li[{listIndex}]/b/a').click()
                sleep(1)
                listIndex += 1
                hasMoreResults = True
                found = isFromOrg(desiredWords)
                list = True
                return hasMoreResults, found, list
            except NoSuchElementException:
                try:
                    driver.find_element(By.XPATH,
                                        f'/html/body/form/div/div[4]/div/div/div/div[3]/div/div[4]/a[{pageIndex + 1}]')
                    listIndex = 1
                    pageIndex += 1
                    sleep(2)
                    # click next
                    driver.find_element(By.XPATH,
                                        f'/html/body/form/div/div[4]/div/div/div/div[3]/div/div[4]/a[{pageIndex}]').click()
                    driver.find_element(By.XPATH,
                                        f'/html/body/form/div/div[4]/div/div/div/div[3]/div/div[3]/ol/li[{listIndex}]/b/a').click()
                    hasMoreResults, found, list = True, isFromOrg(desiredWords), True
                    return hasMoreResults, found, list
                except NoSuchElementException:
                    print(e)
                    printError()
                    hasMoreResults, found, list = False, False, True
                    return hasMoreResults, found, list
    except Exception as e:
        backTosearchForm()
        print(e)
        printError()
        hasMoreResults, found, list = False, False, False
        return hasMoreResults, found, list


def extract_id():
    sleep(2)
    return driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/div[1]/ul/li[2]/span[2]').text


def changeTab(currentTab):
    listOfTabs = driver.window_handles
    for id in listOfTabs:
        if id != currentTab: driver.switch_to.window(id)
    sleep(1)


ids = {'name': [], 'id': [], 'rank': []}
driver.get(searchUrl)
searchTabId = driver.current_window_handle
firstTime = True


def processName(name, rank):
    print("starting looking for {} rank {}".format(name, rank))
    ids['name'].append(name)
    ids['rank'].append(rank)
    global listIndex
    global pageIndex
    listIndex = 1
    pageIndex = 1
    insertName(name)
    setGeneralSearch()
    # search
    driver.find_element(By.XPATH, searchXPath).click()
    hasMoreResults, found, lastInList = True, False, False
    while (hasMoreResults and not found):
        hasMoreResults, found, list = findInList(searchTabId)
        if found:
            break
        elif not list:
            driver.back()
        else:
            changeTab(searchTabId)
            justSearchTab(searchTabId)
            driver.find_element(By.XPATH, "/html/body/form/div/div[1]/div/div/div/div[1]/a").click()
    try:
        if found:
            id = extract_id()
            ids['id'].append(id)
            changeTab(searchTabId)
            justSearchTab(searchTabId)
            backTosearchForm()
        else:
            ids['id'].append("Not Found")
    except Exception as e:
        print(e)
        printError()
        ids['id'].append('Error')
    if (len(driver.window_handles) > 1):
        changeTab(searchTabId)
        justSearchTab(searchTabId)
    backTosearchForm()


def printError():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)


if __name__ == "__main__":
    try:
        filtered = pd.read_excel(candidatesFilePath)
        max, current = 20, 1
        for index, row in filtered.iterrows():
            if (current > max): break
            processName(row["NOME"], row['DESCRICAO_CARGO'])
            current += 1
    except Exception as e:
        print(e)
        printError()
        if len(ids['name']) == len(ids['id']) + 1:
            ids(['id']).append('Error')
    filename = "idsResult.csv"
    pd.DataFrame.from_dict(ids).to_csv(filename, index=False)
