import win32com.client
import xlsxwriter
import time
import os, sys
from macro.extractMacro import extractMacro


class CreateMacro(object):
    def __init__(self,macro,savemacroformatfile,mfile,saveas,url,text,textloc,buttontex,buttonloc,imgpath,imgloc,asfile):

        try:

            if os.path.isfile(macro):

                with open(macro, "r") as myfile:
                    mac = myfile.read()
                    newmacro = mac.replace('http://localhost/', url)
                    print(newmacro)

                    excel = win32com.client.Dispatch("Excel.Application")
                    wb = excel.Workbooks.Add()
                    wb.SaveAs(asfile, FileFormat=savemacroformatfile)
                    excel.Visible = False

                    if os.path.isfile(mfile):

                        workbooktwo = excel.Workbooks.Open(Filename=mfile)
                        module = workbooktwo.VBProject.VBComponents.Add(1)
                        module.CodeModule.AddFromString(newmacro)
                        excel.Workbooks(1).Close(SaveChanges=1)
                        excel.Application.Quit()

                        extractMacro(mfile, saveas, url, text, textloc, buttontex, buttonloc, imgpath, imgloc)

                    else:
                        excel.Workbooks(1).Close(SaveChanges=0)
                        excel.Application.Quit()
                        sys.stderr.write("No File")
                        sys.stderr.flush()

            else:
                sys.stderr.write("No Macro")
                sys.stderr.flush()
                sys.exit()


        except Exception as f:

            t, o, tb = sys.exc_info()
            print(f, tb.tb_lineno)
