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
worksheet.insert_chart("D20",allChart)
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
worksheet.insert_chart("N2",pChart)
pChart.add_series({'values':["Data Summary",1,12,406,12], 'categories':["Data Summary",1,11,406,11]})
###

###Dif between avg and perfect
worksheet.write('V1',"Dif avg and per X")
worksheet.write('W1',"Dif avg and per Y")
for row in range(1,403):
    worksheet.write_formula(row,21,'=ABS(A%d-L%d)'%(row+1,row+1))
    worksheet.write_formula(row,22,'=ABS(B%d-M%d)'%(row+1,row+1))
dChart = workbook.add_chart({'type': 'column'})

dChart.set_title({'name':'Difference Run X'})
worksheet.insert_chart("Y2",dChart)
dChart.add_series({'values':["Data Summary",1,21,406,21]})

d2Chart = workbook.add_chart({'type': 'column'})
d2Chart.set_title({'name':'Difference Run Y'})
worksheet.insert_chart("Y20",d2Chart)
d2Chart.add_series({'values':["Data Summary",1,22,406,22]})

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
worksheet.insert_chart("N20",tChart)
firstTen=True
index=0

###

for f in filenames:
        print(f)
        df = pd.read_csv(f)
        averageDataX=pd.concat([averageDataX,df[['X']]],axis=1)
        averageDataY=pd.concat([averageDataY,df[['Y']]],axis=1)
        sheetName=os.path.basename(f)[:31]        
        allChart.add_series({'values' : [sheetName,2,3,404,3], 'categories':[sheetName,2,2,404,2],'name':sheetName})
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
        tempChart.add_series({'values' : [sheetName,2,3,404,3], 'categories':[sheetName,2,2,404,2],'name':sheetName})
        ###FirstTen
        index=index+1
        if(index<11):
            tChart.add_series({'values' : [sheetName,2,3,404,3], 'categories':[sheetName,2,2,404,2], 'name':sheetName})
            
        
###Data Table
worksheet.write('D35',"Average Dif in X")
worksheet.write('E35',"Average Dif in Y")
worksheet.write('F35',"Max Dif in X")
worksheet.write('G35',"Max Dif in Y")
worksheet.write('H35',"Min Dif in X")
worksheet.write('I35',"Min Dif in Y")
worksheet.write_formula('D36',"=AVERAGE(V2:V402)")
worksheet.write_formula('E36',"=AVERAGE(W2:W402)")
worksheet.write_formula('F36',"=MAX(V2:V402)")
worksheet.write_formula('G36',"=MAX(W2:W402)")
worksheet.write_formula('H36',"=MIN(V2:V402)")
worksheet.write_formula('I36',"=MIN(W2:W402)")



###
worksheet.write_column('A2', averageDataX.mean(axis=1,skipna=True,numeric_only=True))
worksheet.write_column('B2', averageDataY.mean(axis=1,skipna=True,numeric_only=True))
chart.add_series({'values':["Data Summary",1,1,403,1], 'categories':["Data Summary",1,0,403,0]})
writer.save()
