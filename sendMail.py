from mailsender.smtp import SendMail
import os , time

# SMTP Setting

class SettingSender(object):

    def __init__(self,starttime,thread,opentrackurl,sender,attach,subject,message,smtphost,smtpport,mailadress,mailpassword,*sendto):

        kwargs = {}
        kwargs['smtpt'] = smtphost
        kwargs['port'] = smtpport
        kwargs['mailhost'] = mailadress
        kwargs['passwd'] = mailpassword

        with open(os.getcwd() + '\\sleuth\\mailOpenList\\' + starttime + '.txt', 'x') as createopen:
            createopen.write("")


        SendMail(thread,starttime,opentrackurl,attach, sender, subject, message, *sendto, **kwargs)



if __name__ == '__main__':
    SettingSender()
