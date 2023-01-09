# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 13:35:48 2023

@author: jkern
"""

from BillingFuns import *

mcheck = 0

uploaded_filem = st.file_uploader("Upload Monthly Billing CSV")
if uploaded_filem is not None:
    mcheck = 1
    #read xls or xlsx
    monthlydf=pd.read_csv(uploaded_filem, skiprows=3)
    monthlydf = getFactorize(monthlydf)
    
else:
    st.warning("Monthly Bill From Geotab")



### Enter Year, and Month name
year = 0
month = ''

yearcheck = 0
moncheck = 'nono'
while yearcheck == 0:
    year = st.text_input('Year', '2023')
    #year = input("Please type the year we are billing: ")
    try:
        year = int(year)
        yearcheck = getYear(year)
    except ValueError:
        print("Please enter a number.\n")

        
while moncheck == 'nono':
    month = st.text_input('Month (The one it currently is)', 'February')
    #month = input("Please type the month we are billing: ")
    moncheck = getMonth(month)
    
month = moncheck
year = yearcheck

# ---------------------------------------------------------------------------



# Set our unit prices
monthlydf = editProductPrice(monthlydf)


## Edit cost
monthlydf = setCost(monthlydf)


## Get the number of companies to bill this month
lng = len(monthlydf['Database'].unique())


## Create Database for each company (These will turn into excel spreadsheets)
d = {}
for i in range(lng):
    tdf = monthlydf.loc[monthlydf['id'] == i]
    tdf = tdf.reset_index(drop=True)
    d[i] = tdf


## Deals with termination of GO7 Devices and alters the billing days accordingly
d = setQuantity(d, month, year)

zipObj = ZipFile("MonthlyBillBreakdown.zip", "w")



if mcheck == 1:
    for i in range(lng):
    
        # Write each company billing to a separate excel spreadsheet
        tempdf, tempfile = writeToCsv(d, lng, i)
        CSV = convert_df(tempdf, tempfile)
        zipObj.write(CSV)
        

# close the Zip File
zipObj.close()

ZipfileDotZip = "MonthlyBillBreakdown.zip"

with open(ZipfileDotZip, "rb") as f:
    bytes = f.read()
    b64 = base64.b64encode(bytes).decode()
    href = f"<a href=\"data:file/zip;base64,{b64}\" download='{ZipfileDotZip}.zip'>\
        Click last model weights\
    </a>"
st.sidebar.markdown(href, unsafe_allow_html=True)






