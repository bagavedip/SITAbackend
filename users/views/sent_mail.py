import logging
import smtplib

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import datetime
from cryptography.fernet import Fernet

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from users.models import User
from users.serializers.user import UserUpdateSerializer

from users.services.user import UserService

class UserSentMail(mixins.CreateModelMixin, viewsets.GenericViewSet):

    def sent_mail(self, request):
        reciever = request.data['email']
        query = User.objects.all().filter(email__iexact = reciever)
        key = Fernet.generate_key()
        fernet = Fernet(key)
        nowtime = datetime.datetime.now()
        strnowtime = nowtime.strftime('%m/%d/%y %H:%M')
        encMessage = fernet.encrypt(strnowtime.encode())
        if query:
            User.objects.all().filter(email__iexact=reciever).update(key=key)
            key = User.objects.filter(email__iexact=reciever).values('key')
            print(key)
            for q in query:
                id = q.id
                first_name = q.first_name
            subject = "Forget Password Link"
            message = (f"http://20.127.195.117:3000/forget_password/{id}@{encMessage}")
            email_from = settings.EMAIL_HOST_USER
            email_reciever = [reciever]
            # messages = (f"Hi,Please click this link http://20.127.195.117:3000/forget_password/{query.id}@{encMessage} to reset your password. Thanks, Shashi")
            # email_from = settings.FROM
            # email_reciever = [reciever]
            # message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\
            #     %s
            #     """ % (email_from, ", ".join(email_reciever), subject, messages)
            # server = smtplib.SMTP(settings.SERVER)
            # server.login(email_from, "bcDv%dfter5243")
            # server.sendmail(email_from, email_reciever, message)
            # server.quit()
            html_message = render_to_string("email_template.html", {'link': message, "name":first_name})
            text_content = strip_tags(html_message)

            # server = smtplib.SMTP('smtp.office365.com', 587)
            # server.ehlo()
            # server.starttls()
            # server.login(user, pwd)
            # server.sendmail(FROM, TO, message)
            # server.close()
            send_mail(subject,
                text_content,
                email_from,
                email_reciever,
                html_message=html_message)
            data={
                "Status": "SUCCESS",
                "link" : message,
                "Message" : "Mail Successfully sent"
            }
        else:
            data={
                "Status" : "FAILED",
                "Message" : "User Not exist!"
            }
        return Response(
            {
            "Data":data
            }
        )

    def decrypt_hashcode(self, request):
        requesttoken = request.data['token']
        id=requesttoken.split("@")[0]
        token=requesttoken.split("@")[1]
        new = token.split("'")[1]
        bytetoken = new.encode('utf-8')
        user=User.objects.all().filter(id=id)
        data={
            "Status" : "FAILED",
            "Message" : "Session Timeout!!"
        }
        for q in user:
            user_key = q.key
            user.key = ""
            user.update()
            print(user_key)
        if user_key :
            key = user_key
            user.key = ""
            user.save()
            fernet = Fernet(key)
            decMessage = fernet.decrypt(bytetoken).decode()
            newdatetime=datetime.datetime.strptime(decMessage, format('%m/%d/%y %H:%M'))
            current_time= datetime.datetime.now()
            backcurrenttime = current_time - datetime.timedelta(minutes=30)
            if newdatetime > backcurrenttime:
                data={
                    "Status": "SUCCESS",
                    "Message" : "Success"
                }
            else:
                data={
                    "Status" : "FAILED",
                    "Message" : "Session Timeout!!"
                }
        else:
            data={
                    "Status" : "FAILED",
                    "Message" : "Session Timeout!!"
                }
        return Response(
            {
            "Data":data
            }
        )
