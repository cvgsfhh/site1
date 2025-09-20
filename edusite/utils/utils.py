import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kavenegar import *
template="verify"

def send_email(to, subject, body):
   #ایجاد حساب کاربری
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    emali_user = 'farzadfgh34@gmail.com'
    password = 'fopx hbsi rhqw dcbm'

    to_email= to
    subject = subject
    body = body

    msg = MIMEMultipart()
    msg['From'] = emali_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    try:

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(emali_user, password)
        server.sendmail(emali_user, to_email, msg.as_string())
        print(f'Email sent to successfully.')
    except Exception as e:
        print(f'Error sending email: {e}')
    finally:
        server.quit()


def html_body(random_code):
    html = f'''
    <div>
         <img style="width:300px;height:300px;margin:top"  src="https://s5.uupload.ir/files/dastyar/mysite/mysite_files/python_danekar_t1.jpg" />   
    </div>
    <hr/>
    <h2 style="text-align: center">سلام به آموزشگاه آنلاین ما خوش آمدید کد فعال سازی را وارد کنید</h2>
    <hr/>
    <h2 style="text-align: center;">{random_code}</h2>
    
        '''
    return html

def send_sms(to,code):
    try:
        api = KavenegarAPI('7A4C7933687139336A675564644E6E327057622F6D575148546765536845754E6D364A41653377506479453D')
        params = {
            'receptor': to,
            'template': template,
            'token': code,
            'token2': '',
            'token3': '',
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
