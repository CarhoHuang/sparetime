from flask import render_template, current_app
from threading import Thread
from flask_mail import Message
from app import mail


class EmailSender:
    def send_async_mail(self, app, msg):
        print('开始异步发送')
        with app.app_context():
            mail.send(msg)
        print('发送成功')

    def send_mail(self, to, subject, template, **kwargs):
        msg = Message(current_app.config['STFU_MAIL_SUBJECT_PREFIX'] + subject,
                      sender=current_app.config['MAIL_SENDER'], recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        thr = Thread(target=self.send_async_mail, args=[current_app._get_current_object(), msg])
        thr.start()
        return thr
