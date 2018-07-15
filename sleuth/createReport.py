from sleuth.agentplot import BasicReport

#Function sent to create report

class Report(object):

    def __init__(self,sending,open,starttime,sendtxt,opentxt,savedir):

        BasicReport(sending,open,starttime,sendtxt,opentxt,savedir)
