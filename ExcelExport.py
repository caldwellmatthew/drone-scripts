from seaborn import relplot
import matplotlib.pyplot as plt
import xlsxwriter
import os
import glob
import pandas as pd
PATH="/home/bitcraze/Downloads/2-5-2020 Drone 1 Evening Test Flights/"
os.chdir(PATH)
writer=pd.ExcelWriter('CombinedDroneData.xlsx',engine='xlsxwriter')
extension = 'csv'
#All Files in folder
filenames = [i for i in glob.glob('*.{}'.format(extension))]
try:
    filenames.remove("checklist.csv")
except ValueError:
    print("No checklist file, are these tests from the latest version of the script")
dataPage=pd.DataFrame()
dataPage.to_excel(writer, sheet_name="Data Summary")
workbook  = writer.book
worksheet = writer.sheets['Data Summary']
chartsheet=workbook.add_chartsheet()
chartsheet2=workbook.add_chartsheet()
###Average Chart
chart = workbook.add_chart({'type': 'scatter'})
chart.set_x_axis({
    'name': 'X-Coordinate',
    'min':-.6,
    'max':.6
})
chart.set_y_axis({
    'name': 'Y-Coordinate',
    'min':-.6,
    'max':.6
})
chart.set_title({'name':'Average Run'})
worksheet.write('A1',"AverageX")
worksheet.write('B1',"AverageY")
worksheet.insert_chart('D2',chart)
d={'X':[0]}
d2={'Y':[0]}
averageDataX=pd.DataFrame(data=d)
averageDataY=pd.DataFrame(data=d2)
###
##All Runs Chart
allChart = workbook.add_chart({'type': 'scatter'})
allChart.set_x_axis({
    'name': 'X-Coordinate',
    'min':-.6,
    'max':.6
})
allChart.set_y_axis({
    'name': 'Y-Coordinate',
    'min':-.6,
    'max':.6
})
allChart.set_title({'name':'All Runs'})
#worksheet.insert_chart("D20",allChart)
chartsheet.set_chart(allChart)
chartsheet.activate()
###
###Perfect Data
worksheet.write('L1',"Perfect X")
worksheet.write('M1',"Perfect Y")
worksheet.write('L2',0)
worksheet.write('M2',0)
for row in range(2,201):
    worksheet.write_formula(row,11,'=L%d+(0.8*0.01*COS((180*((ROW()-1)*0.01))*(PI()/180)))'%(row))
    worksheet.write_formula(row,12,'=M%d+(-0.8*0.01*SIN((180*((ROW()-1)*0.01))*(PI()/180)))'%(row))
for row in range(201,402):
    worksheet.write_formula(row,11,'=L%d+(-0.8*0.01*COS((180*((ROW()-1)*0.01))*(PI()/180)))'%(row))
    worksheet.write_formula(row,12,'=M%d+(0.8*0.01*SIN((180*((ROW()-1)*0.01))*(PI()/180)))'%(row))
pChart = workbook.add_chart({'type': 'scatter'})
pChart.set_x_axis({
    'name': 'X-Coordinate',
    'min':-.6,
    'max':.6
})
pChart.set_y_axis({
    'name': 'Y-Coordinate',
    'min':-.6,
    'max':.6
})
pChart.set_title({'name':'Perfect Run'})
worksheet.insert_chart("D20",pChart)
pChart.add_series({'values':["Data Summary",1,12,406,12], 'categories':["Data Summary",1,11,406,11]})
###

###Dif between avg and perfect
worksheet.write('V1',"Dif avg and per X")
worksheet.write('W1',"Dif avg and per Y")
worksheet.write('X1',"Dif avg and per Dist")
for row in range(1,402):
    worksheet.write_formula(row,21,'=ABS(A%d-L%d)'%(row+1,row+1))
    worksheet.write_formula(row,22,'=ABS(B%d-M%d)'%(row+1,row+1))
dChart = workbook.add_chart({'type': 'column'})

dChart.set_title({'name':'Difference Run X'})
worksheet.insert_chart("N2",dChart)
dChart.add_series({'values':["Data Summary",1,21,402,21]})

d2Chart = workbook.add_chart({'type': 'column'})
d2Chart.set_title({'name':'Difference Run Y'})
worksheet.insert_chart("N20",d2Chart)
d2Chart.add_series({'values':["Data Summary",1,22,402,22]})

for row in range(1,402):
    worksheet.write_formula(row,23,'=SQRT(POWER(V%d,2) + POWER(W%d,2))'%(row+1,row+1))
    
d3Chart = workbook.add_chart({'type': 'column'})

d3Chart.set_title({'name':'Difference Run Combination'})
worksheet.insert_chart("N40",d3Chart)
d3Chart.add_series({'values':["Data Summary",1,23,406,23]})

###FirstTen
tChart = workbook.add_chart({'type': 'scatter'})
tChart.set_title({'name':'Ten Runs'})
tChart.set_x_axis({
    'name': 'X-Coordinate',
    'min':-.6,
    'max':.6
    })
tChart.set_y_axis({
    'name': 'Y-Coordinate',
    'min':-.6,
    'max':.6
    })
#worksheet.insert_chart("N20",tChart)
chartsheet2.set_chart(tChart)
chartsheet2.activate()
firstTen=True
index=0

###

for f in filenames:
        print(f)
        df = pd.read_csv(f)
        averageDataX=pd.concat([averageDataX,df[['X']]],axis=1)
        averageDataY=pd.concat([averageDataY,df[['Y']]],axis=1)
        sheetName=os.path.basename(f)[:31]        
        allChart.add_series({'values' : [sheetName,1,3,404,3], 'categories':[sheetName,1,2,404,2],'name':sheetName})
        df.to_excel(writer, sheet_name=sheetName)
        ##TempChart
        tempSheet=writer.sheets[sheetName]
        tempChart = workbook.add_chart({'type': 'scatter'})
        tempChart.set_x_axis({
            'name': 'X-Coordinate',
            'min':-.6,
            'max':.6
        })
        tempChart.set_y_axis({
            'name': 'Y-Coordinate',
            'min':-.6,
            'max':.6
        })
        tempChart.set_title({'name':'Current Run'})
        tempSheet.insert_chart("F2",tempChart)
        tempChart.add_series({'values' : [sheetName,1,3,404,3], 'categories':[sheetName,1,2,404,2],'name':sheetName})
        ###FirstTen
        index=index+1
        if(index<11):
            tChart.add_series({'values' : [sheetName,1,3,404,3], 'categories':[sheetName,1,2,404,2], 'name':sheetName})
        ###
        ### Error
        tempSheet.write('N1',"Perfect X")
        tempSheet.write('O1',"Perfect Y")
        tempSheet.write('N2',0)
        tempSheet.write('O2',0)
        for row in range(2,201):
            tempSheet.write_formula(row,13,'=N%d+(0.8*0.01*COS((180*((ROW()-1)*0.01))*(PI()/180)))'%(row))
            tempSheet.write_formula(row,14,'=O%d+(-0.8*0.01*SIN((180*((ROW()-1)*0.01))*(PI()/180)))'%(row))
        for row in range(201,402):
            tempSheet.write_formula(row,13,'=N%d+(-0.8*0.01*COS((180*((ROW()-1)*0.01))*(PI()/180)))'%(row))
            tempSheet.write_formula(row,14,'=O%d+(0.8*0.01*SIN((180*((ROW()-1)*0.01))*(PI()/180)))'%(row))
        tpChart = workbook.add_chart({'type': 'scatter'})
        tpChart.set_x_axis({
            'name': 'X-Coordinate',
            'min':-.6,
            'max':.6
        })
        tpChart.set_y_axis({
            'name': 'Y-Coordinate',
            'min':-.6,
            'max':.6
        })
        tpChart.set_title({'name':'Perfect Run'})
        tempSheet.insert_chart("F20",tpChart)
        tpChart.add_series({'values':[sheetName,1,14,406,14], 'categories':[sheetName,1,13,406,13]})


        tempSheet.write('Q1',"Dif from per X")
        tempSheet.write('R1',"Dif from per Y")
        tempSheet.write('S1',"Dif from per Dist")
        for row in range(1,402):
            tempSheet.write_formula(row,16,'=ABS(C%d-N%d)'%(row+1,row+1))
            tempSheet.write_formula(row,17,'=ABS(D%d-O%d)'%(row+1,row+1))
        tdChart = workbook.add_chart({'type': 'column'})

        tdChart.set_title({'name':'Difference Run X'})
        tempSheet.insert_chart("U2",tdChart)
        tdChart.add_series({'values':[sheetName,1,16,402,16]})

        td2Chart = workbook.add_chart({'type': 'column'})
        td2Chart.set_title({'name':'Difference Run Y'})
        tempSheet.insert_chart("U20",td2Chart)
        td2Chart.add_series({'values':[sheetName,1,17,402,17]})

        for row in range(1,402):
            tempSheet.write_formula(row,18,'=SQRT(POWER(Q%d,2) + POWER(R%d,2))'%(row+1,row+1))
            
        td3Chart = workbook.add_chart({'type': 'column'})

        td3Chart.set_title({'name':'Difference Run Combination'})
        tempSheet.insert_chart("U40",td3Chart)
        td3Chart.add_series({'values':[sheetName,1,18,402,18]})

        



        
        
###Data Table
worksheet.write('AA0',"Average Dif in X")
worksheet.write('AA1',"Average Dif in Y")
worksheet.write('AA2',"Max Dif in X")
worksheet.write('AA3',"Max Dif in Y")
worksheet.write('AA4',"Min Dif in X")
worksheet.write('AA5',"Min Dif in Y")
worksheet.write_formula('AB0',"=AVERAGE(V2:V402)")
worksheet.write_formula('AB1',"=AVERAGE(W2:W402)")
worksheet.write_formula('AB2',"=MAX(V2:V402)")
worksheet.write_formula('AB3',"=MAX(W2:W402)")
worksheet.write_formula('AB4',"=MIN(V2:V402)")
worksheet.write_formula('AB5',"=MIN(W2:W402)")



###
worksheet.write_column('A2', averageDataX.mean(axis=1,skipna=True,numeric_only=True))
worksheet.write_column('B2', averageDataY.mean(axis=1,skipna=True,numeric_only=True))
chart.add_series({'values':["Data Summary",1,1,403,1], 'categories':["Data Summary",1,0,403,0]})
writer.save()
