import os
from macro.mainmacro import CreateMacro
import sys

class Macro(object):
    def __init__(self,saveas,url,text,textloc,buttontex,buttonloc,imgpath,imgloc,fname):
        try:

            mfile = saveas+"\\"+fname+'.xlsm'
            macro = '%s'% os.getcwd()+"\\"+"macro"+"\\"+"createfile"+"\\"+'DownloadMacro.txt'
            asfile = saveas+"\\"+fname+'.xlsm'

            savemacroformatfile = 52



            filecontrol = os.listdir(saveas)

            for _ in filecontrol:
                file,extension = os.path.splitext(_)
                if ".bin" or ".xlsm" in _:
                    if ".bin"  in extension:
                        os.remove(saveas+"\\"+file+extension)
                    elif ".xlsm" in extension:
                        pass
                else:
                    pass

            CreateMacro(macro,savemacroformatfile,mfile,saveas,url,text,textloc,buttontex,buttonloc,imgpath,imgloc,asfile)
        except Exception as f:

            t, o, tb = sys.exc_info()
            print(f, tb.tb_lineno)

