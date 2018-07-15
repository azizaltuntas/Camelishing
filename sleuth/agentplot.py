import matplotlib.pyplot as plt
import os

class BasicReport(object):

        def __init__(self,send,open,starttime,sendtxt,opentxt,savedir):

            func = 100*open
            itachi = func/send


            labels = sendtxt+str(send),opentxt+str(open)
            sizes = [100-itachi,itachi]
            explode = (0, 0.09)

            color = ['palegreen','paleturquoise']

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, autopct='%1.1f%%',
                    shadow=True, startangle=100, colors=color)

            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)

            ax1.axis('equal')

            plt.legend(labels,loc="best")
            plt.tight_layout()
            plt.savefig(os.getcwd()+"\\sleuth\\"+savedir+"\\Report\\"+starttime+".png")
            plt.show()