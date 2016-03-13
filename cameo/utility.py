# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import re
import json
from geopy.geocoders import GoogleV3
#共用工具程式
class Utility:
    
    #儲存檔案
    def overwriteSaveAs(self, strFilePath=None, unicodeData=None):
        with open(strFilePath, "w+") as file:
            file.write(unicodeData.encode("utf-8"))
    
    #將 dict 物件的內容寫入到 json 檔案內
    def writeObjectToJsonFile(self, dicData=None, strJsonFilePath=None):
        with open(strJsonFilePath, "w+") as jsonFile:
            jsonFile.write(json.dumps(dicData, ensure_ascii=False, indent=4, sort_keys=True).encode("utf-8"))
    
    #取得子目錄的路徑
    def getSubFolderPathList(self, strBasedir=None):
        lstStrSubFolderPath = []
        for base, dirs, files in os.walk(strBasedir):
            if base == strBasedir:
                for dir in dirs:
                    strFolderPath = base + "\\" + dir
                    lstStrSubFolderPath.append(strFolderPath)
        return lstStrSubFolderPath
    
    #取得 strBasedir 目錄中，檔名以 strSuffixes 結尾的檔案路徑
    def getFilePathListWithSuffixes(self, strBasedir=None, strSuffixes=None):
        lstStrFilePathWithSuffixes = []
        for base, dirs, files in os.walk(strBasedir): 
            if base == strBasedir:#just check base dir
                for strFilename in files:
                    if strFilename.endswith(strSuffixes):#find target files
                        strFilePath = base + "\\" + strFilename
                        lstStrFilePathWithSuffixes.append(strFilePath)
        return lstStrFilePathWithSuffixes
        
    #轉換 簡化數字字串 成 純數字 (ex:26.3k -> 26300)
    def translateNumTextToPureNum(self, strNumText=None):
        strNumText = strNumText.lower()
        fPureNum = 0.0
        strFloatPartText = re.match("^([0-9\.]*)k?m?$", strNumText)
        if strFloatPartText != None:
            strFloatPartText = strFloatPartText.group(1)
            if strNumText.endswith("k"):
                fPureNum = float(strFloatPartText) * 1000
            elif strNumText.endswith("m"):
                fPureNum = float(strFloatPartText) * 1000000
            else:
                fPureNum = float(strFloatPartText) * 1
        return int(fPureNum)
        
    #轉換 剩餘日期表示字串 成 純數字 (ex:100 day left -> 100)
    def translateTimeleftTextToPureNum(self, strTimeleftText=None):
        intDays = 0
        if strTimeleftText == None:
            return intDays
        strTimeleftText = strTimeleftText.lower().strip()
        if "hours left" in strTimeleftText:
            strHoursText = re.match("^([0-9]*) hours left$", strTimeleftText)
            if strHoursText != None:
                strHoursText = strHoursText.group(1)
                intDays = (int(strHoursText)+24)/24 #不足24h以1天計
        elif "days left" in strTimeleftText:
            strDaysText = re.match("^([0-9]*) days left$", strTimeleftText)
            if strDaysText != None:
                strDaysText = strDaysText.group(1)
                intDays = int(strDaysText)
        else:
            intDays = 0
        return intDays
        
    #使用 geopy 查找 洲別 資料 (目前不可用)
    def geopy(self):
        geolocator = GoogleV3()
        location, (x, y) = geolocator.geocode("dubai")
        print(location, x, y)
        
    #使用 國家對照表 查找 洲別 資料
    def getContinentByCountryName(self, strCountryName=None):
        countries = [
            {"code": "AD", "continent": "Europe", "name": "Andorra", "capital": "Andorra la Vella"},
            {"code": "AF", "continent": "Asia", "name": "Afghanistan", "capital": "Kabul"},
            {"code": "AG", "continent": "North America", "name": "Antigua and Barbuda"},
            {"code": "AL", "continent": "Europe", "name": "Albania", "capital": "Tirana"},
            {"code": "AM", "continent": "Asia", "name": "Armenia", "capital": "Yerevan"},
            {"code": "AO", "continent": "Africa", "name": "Angola", "capital": "Luanda"},
            {"code": "AR", "continent": "South America", "name": "Argentina", "capital": "Buenos Aires"},
            {"code": "AT", "continent": "Europe", "name": "Austria", "capital": "Vienna"},
            {"code": "AU", "continent": "Oceania", "name": "Australia", "capital": "Canberra"},
            {"code": "AZ", "continent": "Asia", "name": "Azerbaijan", "capital": "Baku"},
            {"code": "BB", "continent": "North America", "name": "Barbados", "capital": "Bridgetown"},
            {"code": "BD", "continent": "Asia", "name": "Bangladesh", "capital": "Dhaka"},
            {"code": "BE", "continent": "Europe", "name": "Belgium", "capital": "Brussels"},
            {"code": "BF", "continent": "Africa", "name": "Burkina Faso", "capital": "Ouagadougou"},
            {"code": "BG", "continent": "Europe", "name": "Bulgaria", "capital": "Sofia"},
            {"code": "BH", "continent": "Asia", "name": "Bahrain", "capital": "Manama"},
            {"code": "BI", "continent": "Africa", "name": "Burundi", "capital": "Bujumbura"},
            {"code": "BJ", "continent": "Africa", "name": "Benin", "capital": "Porto-Novo"},
            {"code": "BN", "continent": "Asia", "name": "Brunei Darussalam", "capital": "Bandar Seri Begawan"},
            {"code": "BO", "continent": "South America", "name": "Bolivia", "capital": "Sucre"},
            {"code": "BR", "continent": "South America", "name": "Brazil"},
            {"code": "BS", "continent": "North America", "name": "Bahamas", "capital": "Nassau"},
            {"code": "BT", "continent": "Asia", "name": "Bhutan", "capital": "Thimphu"},
            {"code": "BW", "continent": "Africa", "name": "Botswana", "capital": "Gaborone"},
            {"code": "BY", "continent": "Europe", "name": "Belarus", "capital": "Minsk"},
            {"code": "BZ", "continent": "North America", "name": "Belize", "capital": "Belmopan"},
            {"code": "CA", "continent": "North America", "name": "Canada", "capital": "Ottawa"},
            {"code": "CD", "continent": "Africa", "name": "Democratic Republic of the Congo", "capital": "Kinshasa"},
            {"code": "CG", "continent": "Africa", "name": "Republic of the Congo", "capital": "Brazzaville"},
            {"code": "CI", "continent": "Africa", "name": u"Côte d'Ivoire"},
            {"code": "CI", "continent": "Africa", "name": u"Cote d'Ivoire"},
            {"code": "CL", "continent": "South America", "name": "Chile", "capital": "Santiago"},
            {"code": "CM", "continent": "Africa", "name": "Cameroon"},
            {"code": "CN", "continent": "Asia", "name": u"People's Republic of China"},
            {"code": "CN", "continent": "Asia", "name": u"China"},
            {"code": "CO", "continent": "South America", "name": "Colombia"},
            {"code": "CR", "continent": "North America", "name": "Costa Rica"},
            {"code": "CU", "continent": "North America", "name": "Cuba", "capital": "Havana"},
            {"code": "CV", "continent": "Africa", "name": "Cape Verde", "capital": "Praia"},
            {"code": "CY", "continent": "Asia", "name": "Cyprus", "capital": "Nicosia"},
            {"code": "CZ", "continent": "Europe", "name": "Czech Republic", "capital": "Prague"},
            {"code": "DE", "continent": "Europe", "name": "Germany", "capital": "Berlin"},
            {"code": "DJ", "continent": "Africa", "name": "Djibouti", "capital": "Djibouti City"},
            {"code": "DK", "continent": "Europe", "name": "Denmark", "capital": "Copenhagen"},
            {"code": "DM", "continent": "North America", "name": "Dominica", "capital": "Roseau"},
            {"code": "DO", "continent": "North America", "name": "Dominican Republic", "capital": "Santo Domingo"},
            {"code": "EC", "continent": "South America", "name": "Ecuador", "capital": "Quito"},
            {"code": "EE", "continent": "Europe", "name": "Estonia", "capital": "Tallinn"},
            {"code": "EG", "continent": "Africa", "name": "Egypt", "capital": "Cairo"},
            {"code": "ER", "continent": "Africa", "name": "Eritrea", "capital": "Asmara"},
            {"code": "ET", "continent": "Africa", "name": "Ethiopia", "capital": "Addis Ababa"},
            {"code": "FI", "continent": "Europe", "name": "Finland", "capital": "Helsinki"},
            {"code": "FJ", "continent": "Oceania", "name": "Fiji", "capital": "Suva"},
            {"code": "FR", "continent": "Europe", "name": "France", "capital": "Paris"},
            {"code": "GA", "continent": "Africa", "name": "Gabon", "capital": "Libreville"},
            {"code": "GE", "continent": "Asia", "name": "Georgia", "capital": "Tbilisi"},
            {"code": "GH", "continent": "Africa", "name": "Ghana", "capital": "Accra"},
            {"code": "GM", "continent": "Africa", "name": "The Gambia", "capital": "Banjul"},
            {"code": "GN", "continent": "Africa", "name": "Guinea", "capital": "Conakry"},
            {"code": "GR", "continent": "Europe", "name": "Greece", "capital": "Athens"},
            {"code": "GT", "continent": "North America", "name": "Guatemala", "capital": "Guatemala City"},
            {"code": "GT", "continent": "North America", "name": "Haiti", "capital": "Port-au-Prince"},
            {"code": "GW", "continent": "Africa", "name": "Guinea-Bissau", "capital": "Bissau"},
            {"code": "GY", "continent": "South America", "name": "Guyana", "capital": "Georgetown"},
            {"code": "HN", "continent": "North America", "name": "Honduras", "capital": "Tegucigalpa"},
            {"code": "HU", "continent": "Europe", "name": "Hungary", "capital": "Budapest"},
            {"code": "ID", "continent": "Asia", "name": "Indonesia", "capital": "Jakarta"},
            {"code": "IE", "continent": "Europe", "name": "Republic of Ireland", "capital": "Dublin"},
            {"code": "IL", "continent": "Asia", "name": "Israel", "capital": "Jerusalem"},
            {"code": "IN", "continent": "Asia", "name": "India", "capital": "New Delhi"},
            {"code": "IQ", "continent": "Asia", "name": "Iraq", "capital": "Baghdad"},
            {"code": "IR", "continent": "Asia", "name": "Iran", "capital": "Tehran"},
            {"code": "IS", "continent": "Europe", "name": "Iceland"},
            {"code": "IT", "continent": "Europe", "name": "Italy", "capital": "Rome"},
            {"code": "JM", "continent": "North America", "name": "Jamaica", "capital": "Kingston"},
            {"code": "JO", "continent": "Asia", "name": "Jordan", "capital": "Amman"},
            {"code": "JP", "continent": "Asia", "name": "Japan", "capital": "Tokyo"},
            {"code": "KE", "continent": "Africa", "name": "Kenya", "capital": "Nairobi"},
            {"code": "KG", "continent": "Asia", "name": "Kyrgyzstan", "capital": "Bishkek"},
            {"code": "KI", "continent": "Oceania", "name": "Kiribati", "capital": "Tarawa"},
            {"code": "KP", "continent": "Asia", "name": "North Korea", "capital": "Pyongyang"},
            {"code": "KR", "continent": "Asia", "name": "South Korea", "capital": "Seoul"},
            {"code": "KW", "continent": "Asia", "name": "Kuwait", "capital": "Kuwait City"},
            {"code": "LB", "continent": "Asia", "name": "Lebanon", "capital": "Beirut"},
            {"code": "LI", "continent": "Europe", "name": "Liechtenstein", "capital": "Vaduz"},
            {"code": "LR", "continent": "Africa", "name": "Liberia", "capital": "Monrovia"},
            {"code": "LS", "continent": "Africa", "name": "Lesotho", "capital": "Maseru"},
            {"code": "LT", "continent": "Europe", "name": "Lithuania", "capital": "Vilnius"},
            {"code": "LU", "continent": "Europe", "name": "Luxembourg", "capital": "Luxembourg City"},
            {"code": "LV", "continent": "Europe", "name": "Latvia", "capital": "Riga"},
            {"code": "LY", "continent": "Africa", "name": "Libya", "capital": "Tripoli"},
            {"code": "MG", "continent": "Africa", "name": "Madagascar", "capital": "Antananarivo"},
            {"code": "MH", "continent": "Oceania", "name": "Marshall Islands", "capital": "Majuro"},
            {"code": "MK", "continent": "Europe", "name": "Macedonia", "capital": "Skopje"},
            {"code": "ML", "continent": "Africa", "name": "Mali", "capital": "Bamako"},
            {"code": "MM", "continent": "Asia", "name": "Myanmar", "capital": "Naypyidaw"},
            {"code": "MN", "continent": "Asia", "name": "Mongolia", "capital": "Ulaanbaatar"},
            {"code": "MR", "continent": "Africa", "name": "Mauritania", "capital": "Nouakchott"},
            {"code": "MT", "continent": "Europe", "name": "Malta", "capital": "Valletta"},
            {"code": "MU", "continent": "Africa", "name": "Mauritius", "capital": "Port Louis"},
            {"code": "MV", "continent": "Asia", "name": "Maldives"},
            {"code": "MW", "continent": "Africa", "name": "Malawi", "capital": "Lilongwe"},
            {"code": "MX", "continent": "North America", "name": "Mexico", "capital": "Mexico City"},
            {"code": "MY", "continent": "Asia", "name": "Malaysia", "capital": "Kuala Lumpur"},
            {"code": "MZ", "continent": "Africa", "name": "Mozambique", "capital": "Maputo"},
            {"code": "NA", "continent": "Africa", "name": "Namibia", "capital": "Windhoek"},
            {"code": "NE", "continent": "Africa", "name": "Niger", "capital": "Niamey"},
            {"code": "NG", "continent": "Africa", "name": "Nigeria", "capital": "Abuja"},
            {"code": "NI", "continent": "North America", "name": "Nicaragua", "capital": "Managua"},
            {"code": "NL", "continent": "Europe", "name": "Kingdom of the Netherlands"},
            {"code": "NL", "continent": "Europe", "name": "Netherlands"},
            {"code": "NO", "continent": "Europe", "name": "Norway", "capital": "Oslo"},
            {"code": "NP", "continent": "Asia", "name": "Nepal", "capital": "Kathmandu"},
            {"code": "NR", "continent": "Oceania", "name": "Nauru", "capital": "Yaren"},
            {"code": "NZ", "continent": "Oceania", "name": "New Zealand", "capital": "Wellington"},
            {"code": "OM", "continent": "Asia", "name": "Oman", "capital": "Muscat"},
            {"code": "PA", "continent": "North America", "name": "Panama", "capital": "Panama City"},
            {"code": "PE", "continent": "South America", "name": "Peru", "capital": "Lima"},
            {"code": "PG", "continent": "Oceania", "name": "Papua New Guinea", "capital": "Port Moresby"},
            {"code": "PH", "continent": "Asia", "name": "Philippines", "capital": "Manila"},
            {"code": "PK", "continent": "Asia", "name": "Pakistan", "capital": "Islamabad"},
            {"code": "PL", "continent": "Europe", "name": "Poland", "capital": "Warsaw"},
            {"code": "PT", "continent": "Europe", "name": "Portugal", "capital": "Lisbon"},
            {"code": "PW", "continent": "Oceania", "name": "Palau", "capital": "Ngerulmud"},
            {"code": "PY", "continent": "South America", "name": "Paraguay"},
            {"code": "QA", "continent": "Asia", "name": "Qatar", "capital": "Doha"},
            {"code": "RO", "continent": "Europe", "name": "Romania", "capital": "Bucharest"},
            {"code": "RU", "continent": "Europe", "name": "Russia", "capital": "Moscow"},
            {"code": "RU", "continent": "Europe", "name": "Russian Federation", "capital": "Moscow"},
            {"code": "RW", "continent": "Africa", "name": "Rwanda", "capital": "Kigali"},
            {"code": "SA", "continent": "Asia", "name": "Saudi Arabia", "capital": "Riyadh"},
            {"code": "SB", "continent": "Oceania", "name": "Solomon Islands", "capital": "Honiara"},
            {"code": "SC", "continent": "Africa", "name": "Seychelles", "capital": "Victoria"},
            {"code": "SD", "continent": "Africa", "name": "Sudan", "capital": "Khartoum"},
            {"code": "SE", "continent": "Europe", "name": "Sweden", "capital": "Stockholm"},
            {"code": "SG", "continent": "Asia", "name": "Singapore", "capital": "Singapore"},
            {"code": "SI", "continent": "Europe", "name": "Slovenia", "capital": "Ljubljana"},
            {"code": "SK", "continent": "Europe", "name": "Slovakia", "capital": "Bratislava"},
            {"code": "SL", "continent": "Africa", "name": "Sierra Leone", "capital": "Freetown"},
            {"code": "SM", "continent": "Europe", "name": "San Marino", "capital": "San Marino"},
            {"code": "SN", "continent": "Africa", "name": "Senegal", "capital": "Dakar"},
            {"code": "SO", "continent": "Africa", "name": "Somalia", "capital": "Mogadishu"},
            {"code": "SR", "continent": "South America", "name": "Suriname", "capital": "Paramaribo"},
            {"code": "ST", "continent": "Africa", "name": u"República Democrática de São Tomé e Príncipe"},
            {"code": "SY", "continent": "Asia", "name": "Syria", "capital": "Damascus"},
            {"code": "TG", "continent": "Africa", "name": "Togo"},
            {"code": "TH", "continent": "Asia", "name": "Thailand", "capital": "Bangkok"},
            {"code": "TJ", "continent": "Asia", "name": "Tajikistan", "capital": "Dushanbe"},
            {"code": "TM", "continent": "Asia", "name": "Turkmenistan", "capital": "Ashgabat"},
            {"code": "TN", "continent": "Africa", "name": "Tunisia", "capital": "Tunis"},
            {"code": "TO", "continent": "Oceania", "name": "Tonga"},
            {"code": "TR", "continent": "Asia", "name": "Turkey", "capital": "Ankara"},
            {"code": "TT", "continent": "North America", "name": "Trinidad and Tobago", "capital": "Port of Spain"},
            {"code": "TV", "continent": "Oceania", "name": "Tuvalu", "capital": "Funafuti"},
            {"code": "TZ", "continent": "Africa", "name": "Tanzania", "capital": "Dodoma"},
            {"code": "UA", "continent": "Europe", "name": "Ukraine", "capital": "Kiev"},
            {"code": "UG", "continent": "Africa", "name": "Uganda", "capital": "Kampala"},
            {"code": "US", "continent": "North America", "name": "United States", "capital": "Washington, D.C."},
            {"code": "UY", "continent": "South America", "name": "Uruguay", "capital": "Montevideo"},
            {"code": "UZ", "continent": "Asia", "name": "Uzbekistan", "capital": "Tashkent"},
            {"code": "VA", "continent": "Europe", "name": "Vatican City", "capital": "Vatican City"},
            {"code": "VE", "continent": "South America", "name": "Venezuela", "capital": "Caracas"},
            {"code": "VN", "continent": "Asia", "name": "Vietnam", "capital": "Hanoi"},
            {"code": "VU", "continent": "Oceania", "name": "Vanuatu", "capital": "Port Vila"},
            {"code": "YE", "continent": "Asia", "name": "Yemen"},
            {"code": "ZM", "continent": "Africa", "name": "Zambia", "capital": "Lusaka"},
            {"code": "ZW", "continent": "Africa", "name": "Zimbabwe", "capital": "Harare"},
            {"code": "DZ", "continent": "Africa", "name": "Algeria", "capital": "Algiers"},
            {"code": "BA", "continent": "Europe", "name": "Bosnia and Herzegovina", "capital": "Sarajevo"},
            {"code": "KH", "continent": "Asia", "name": "Cambodia", "capital": "Phnom Penh"},
            {"code": "CF", "continent": "Africa", "name": "Central African Republic", "capital": "Bangui"},
            {"code": "TD", "continent": "Africa", "name": "Chad"},
            {"code": "KM", "continent": "Africa", "name": "Comoros", "capital": "Moroni"},
            {"code": "HR", "continent": "Europe", "name": "Croatia", "capital": "Zagreb"},
            {"code": "TL", "continent": "Asia", "name": "East Timor", "capital": "Dili"},
            {"code": "SV", "continent": "North America", "name": "El Salvador", "capital": "San Salvador"},
            {"code": "GQ", "continent": "Africa", "name": "Equatorial Guinea", "capital": "Malabo"},
            {"code": "GD", "continent": "North America", "name": "Grenada"},
            {"code": "KZ", "continent": "Asia", "name": "Kazakhstan", "capital": "Astana"},
            {"code": "LA", "continent": "Asia", "name": "Laos", "capital": "Vientiane"},
            {"code": "FM", "continent": "Oceania", "name": "Federated States of Micronesia", "capital": "Palikir"},
            {"code": "MD", "continent": "Europe", "name": "Moldova"},
            {"code": "MC", "continent": "Europe", "name": "Monaco", "capital": "Monaco"},
            {"code": "ME", "continent": "Europe", "name": "Montenegro", "capital": "Podgorica"},
            {"code": "MA", "continent": "Africa", "name": "Morocco", "capital": "Rabat"},
            {"code": "KN", "continent": "North America", "name": "Saint Kitts and Nevis", "capital": "Basseterre"},
            {"code": "LC", "continent": "North America", "name": "Saint Lucia", "capital": "Castries"},
            {"code": "VC", "continent": "North America", "name": "Saint Vincent and the Grenadines", "capital": "Kingstown"},
            {"code": "WS", "continent": "Oceania", "name": "Samoa", "capital": "Apia"},
            {"code": "RS", "continent": "Europe", "name": "Serbia", "capital": "Belgrade"},
            {"code": "ZA", "continent": "Africa", "name": "South Africa", "capital": "Pretoria"},
            {"code": "ES", "continent": "Europe", "name": "Spain", "capital": "Madrid"},
            {"code": "LK", "continent": "Asia", "name": "Sri Lanka", "capital": "Sri Jayewardenepura Kotte"},
            {"code": "SZ", "continent": "Africa", "name": "Swaziland", "capital": "Mbabane"},
            {"code": "CH", "continent": "Europe", "name": "Switzerland", "capital": "Bern"},
            {"code": "AE", "continent": "Asia", "name": "United Arab Emirates", "capital": "Abu Dhabi"},
            {"code": "GB", "continent": "Europe", "name": "United Kingdom", "capital": "London"},
            {"code": "TW", "continent": "Asia", "name": "Taiwan"},
            {"code": "AW", "continent": "North America", "name": "Aruba"},
            {"code": "FO", "continent": "Europe", "name": "Faroe Islands"},
            {"code": "GI", "continent": "Europe", "name": "Gibraltar"},
            {"code": "GU", "continent": "Oceania", "name": "Guam"},
            {"code": "HK", "continent": "Asia", "name": "Hong Kong"},
            {"code": "HT", "continent": "North America", "name": "Haiti"},
            {"code": "IM", "continent": "Europe", "name": "Isle of Man"},
            {"code": "JE", "continent": "Europe", "name": "Jersey"},
            {"code": "KY", "continent": "North America", "name": "Cayman Islands"},
            {"code": "MP", "continent": "Oceania", "name": "Northern Mariana Islands"},
            {"code": "NC", "continent": "Oceania", "name": "New Caledonia"},
            {"code": "PF", "continent": "Oceania", "name": "French Polynesia"},
            {"code": "PR", "continent": "South America", "name": "Puerto Rico"},
            {"code": "VI", "continent": "North America", "name": "US Virgin Islands"},
            {"code": "YT", "continent": "Africa", "name": "Mayotte"},
            ]
        strContinent = None
        if strCountryName != None:
            strCountryName = unicode(strCountryName.lower().strip())
        for country in countries:
            if strCountryName == unicode(country["name"].lower().strip()):
                strContinent = country["continent"]
        return strContinent