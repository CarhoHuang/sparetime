import os
from flask import render_template, current_app, url_for
from threading import Thread
from flask_mail import Message
from app import mail

basedir = os.path.abspath(os.path.dirname(__file__))


class EmailSender:
    def send_async_mail(self, app, msg, **kwargs):
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

    def send_picture_mail(self, to, subject, template, **kwargs):
        application = current_app._get_current_object()
        msg = Message(current_app.config['STFU_MAIL_SUBJECT_PREFIX'] + subject,
                      sender=current_app.config['MAIL_SENDER'], recipients=[to])

        # 邮件附上图片发送，有点卡，算了，不发了
        # with application.open_resource(basedir + url_for('static', filename='images/bg_1.jpg')) as fp:
        #     msg.attach('bg_1.jpg', "image/*", fp.read(), 'inline', headers=[('Content-ID', 'bg_1.jpg')])
        # with application.open_resource(basedir + url_for('static', filename='images/work-1.jpg')) as fp:
        #     msg.attach('work-1.jpg', "image/*", fp.read(), 'inline', headers=[('Content-ID', 'work-1.jpg')])
        # with application.open_resource(basedir + url_for('static', filename='images/work-2.jpg')) as fp:
        #     msg.attach('work-2.jpg', "image/*", fp.read(), 'inline', headers=[('Content-ID', 'work-2.jpg')])

        msg.body = render_template(template + '.txt', **kwargs)
        # msg.html = render_template(template + '.html', img_1='cid:bg_1.jpg', img_2='cid:work-1.jpg',
        #                            img_3='cid:work-2.jpg', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)

        thr = Thread(target=self.send_async_mail, args=[application, msg])
        thr.start()
        return thr
