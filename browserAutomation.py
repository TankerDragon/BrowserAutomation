# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 07:30:17 2022

@author: user
"""

import time
from selenium import webdriver
from bs4 import BeautifulSoup
import random


#####################################################################
browser = webdriver.Chrome("c:/chromedriver.exe")

browser.get('https://docs.google.com/forms/d/e/1FAIpQLSd3yLjlzybSCRyz8NfcAtcGTA6W4fokgSvyLH5CEqyi5N1V4Q/viewform') #google documen link
time.sleep(3)
soup = BeautifulSoup(browser.page_source,"html.parser")

for i in range(50): #range of loop

    container = browser.find_elements_by_class_name('SG0AAe') #class names might not work in differet devices
    for r in container:
        children = r.find_elements_by_class_name('ajBQVb')
        n = len(children)
        children[random.randint(0, n-1)].click()

    container2 = browser.find_elements_by_class_name('Y6Myld')
    for r in container2:
        clicked = []

        children = r.find_elements_by_class_name('Yri8Nb')
        n = len(children)
        for j in range(n):
            if j not in clicked:
                children[random.randint(0, n-1)].click()
                clicked.append(j)


    #Y6Myld Yri8Nb
    time.sleep(1)
    submit_btn = browser.find_element_by_class_name('Y5sE8d')
    submit_btn.click()

    time.sleep(1)

    submit_another = browser.find_element_by_class_name('c2gzEf').find_element_by_tag_name('a')
    submit_another.click()


    time.sleep(1)

# c2gzEf
browser.close()
browser.quit()

"""
    div = soup.find_all('div', attrs={'class':'SG0AAe'})
    email_input = browser.find_elements_by_tag_name('input')
    
    
    email_input[0].send_keys('erans.com')
    time.sleep(0.5)
    email_input[1].send_keys('@akb21')
    time.sleep(0.5)

    print("LogIn...")
    button = browser.find_element_by_tag_name('button').click()
    time.sleep(3)
    ancer = browser.find_elements_by_tag_name('a')
    ancer[0].click()
    time.sleep(2)
    

    print("Getting Main Drivers Table page...")
    browser.get('')
    time.sleep(6)
    
    
    
    body = div[0].find_all('tbody', attrs={'class':'table-rows'})
    table = body[0].find_all('a', attrs={'class':'tdLink'})
    

    print("Scraping Drivers' ID table...")
    data = []
    for a in table:
        strh = a.attrs['href']
        if len(data) != 0:
            if data[len(data)-1] != strh:
                data.append(strh)
        else:   
            data.append(strh)
    
    
    drivers = []
    db_drivers = []
    not_exist = []
    
    for i in range(len(data)):
        strr = data[i].split('/')
        drivers.append(strr[5])
        
    current_date = data[0].split('/')[6]

    print('Drivers ID table: ', drivers)
    

    print("Recieving Drivers table from Database...")
    data = []
    mycursor.execute("SELECT * FROM `drivers`")
    for i in mycursor:
        db_drivers.append([i[0],i[3],i[4]])
    print(db_drivers)
    

    print("Comparing...")
    for d in drivers:
        is_exist = False
        for db_d in db_drivers:
            if d == db_d[0]:
                is_exist = True
                break
        if not is_exist:
            mycursor.execute("INSERT INTO `drivers` (`driverID`, `name`, `surname`, `lastDay`, `lastTime`) VALUES ('"+d+"', '?', '?', '2022-01-01', '0')")

            print('!!! New Driver has been inserted.')
    
    

    print('Current Date: ' + current_date)
    
    
    ####################################################################
    isbtn_clicked = False

    print("Starting Loop...")
    
    for driver_id in drivers:

        print("Scraping Logs of Driver: "+ driver_id+" ...")
        browser.get('https://app.tteld.com/#/admin/85/logs/driver/'+driver_id+'/'+current_date)
        time.sleep(5)
        if not isbtn_clicked:
            orig_log = browser.find_elements_by_class_name('reportBtn')
            orig_log[3].click()
            time.sleep(3)
            isbtn_clicked = True
        
        soup = BeautifulSoup(browser.page_source,"html.parser")
        body = soup.find_all('tbody', attrs={'class':'body'})
        status = body[1].find_all('span', attrs={'class':'status-indicator'})
        stattus_data = []
        for a in status:
            stattus_data.append(a.text)
        times = body[1].find_all('span', attrs={'class':'start'})
        time_data = []
        for a in times:
            time_data.append(a.text)
        #print(stattus_data, len(stattus_data))
        #print(time_data, len(time_data))
        if len(stattus_data) != len(time_data):
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('ERROR: TWO ARRAYS ARE NOT EQUAL')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        main_data = []
        for i in range(len(stattus_data)):
            if stattus_data[i] == 'DR' or stattus_data[i] == '(PC)':
                arr = [1,strTimeToMinuteTime(time_data[i])]
                main_data.append(arr)
            elif stattus_data[i] == 'ON' or stattus_data[i] == 'OFF' or stattus_data[i] == 'SB' or stattus_data[i] == '(YM)':
                arr = [0,strTimeToMinuteTime(time_data[i])]
                main_data.append(arr)
        space()
        print(main_data,  len(main_data))
        ############################################
        print("Filtering logs...")
        for db_d in db_drivers:
            if db_d[0] == driver_id:
                db_date = db_d[1]
                db_time = db_d[2]
                break
        
        filtered_data = []
        
        if strTimeToDateTime(dateFix(current_date)) == db_date:
            for i in range(len(main_data)):
                if main_data[i][1] > db_time:
                    filtered_data.append(main_data[i])
        else:
            filtered_data = main_data
        #if  == 
        print(str(len(filtered_data))+ " logs have been added.")
        ##########################################
        print("Inserting logs to Database...")
        if len(filtered_data) != 0:
            last_time = filtered_data[len(filtered_data)-1][1]
            mycursor.execute("UPDATE `drivers` SET `lastTime` = '"+str(last_time)+"' WHERE `drivers`.`driverID` = '"+driver_id+"'")
        mycursor.execute("UPDATE `drivers` SET `lastDay` = '"+dateFix(current_date)+"' WHERE `drivers`.`driverID` = '"+driver_id+"'")
        
        #
        for i in range(len(filtered_data)):
            #mycursor.execute("INSERT INTO `log` (`id`, `driverID`, `date`, `time`, `isdriving`) VALUES (NULL, '2094', '2022-02-15', '12345', '0')")
            mycursor.execute("INSERT INTO `log` (`id`, `driverID`, `date`, `time`, `isdriving`) VALUES (NULL, '"+driver_id+"', '"+dateFix(current_date)+"', '"+str(filtered_data[i][1])+"', '"+str(filtered_data[i][0])+"')")
        
    print("Completed succesfully!")
    time.sleep(1)  
    mydb.close()
    browser.close()
    browser.quit()
    
    space()
    for j in range(delay):
        print("Starting new Loop in "+str(delay - j)+" minute(s)...")
        time.sleep(60)







###### just nothing ##########
#soup = browser.page_source,"html.parser"
#table = browser.find_element_by_tag_name('tbody')      
#table=list() 
#table = soup.find("tr", attrs={'class':'ui-widget-content'})
#table = soup.find_elements_by_tag_name('tbody')
#table = soup.find_element_by_class_name('ui-datatable-data')
#table_body = table.find('tbody')    
######

url_split = url.split('/')

date_split = url_split[6].split('-')

current_date = date_split[1]
current_month = date_split[0]
current_year = date_split[2]
driver_id = url_split[5]

data = []

for i in range(8):
    myurl = 'https://portal.bluestareld.com/portal/log/' + driver_id + '/'+ dates(current_month, current_date, current_year, 7-i) + '/0/ET'
    print('getting data of ' + dates(current_month, current_date, current_year, 7-i) + ' ...')
    browser.get(myurl)
    time.sleep(6)
    soup = BeautifulSoup(browser.page_source,"html.parser")
    time.sleep(0.5)
    
    div = soup.find_all('div', attrs={'class':'ui-datatable-tablewrapper'})
    table = div[4].find('tbody', attrs={'class':'ui-datatable-data'})
    rows = table.find_all('tr')
    ##############
    is_first = True
    for row in rows:
        cols = row.find_all('td')
        row_data = []
        for cel in cols:
            #spans = cel.find_all('span')
            #spans = [ele.text.strip() for ele in spans]
            #data.append([ele for ele in spans if ele])
        
            spans = cel.find('span', attrs={'class':'ui-cell-data'})
            #spans = [ele.text.strip() for ele in spans]
            row_data.append(spans.text.strip())
        
            if(is_first):
                row_data[0] = "restored"
                is_first = False
        
        data.append(row_data)

 
print(data)
5515
"""

