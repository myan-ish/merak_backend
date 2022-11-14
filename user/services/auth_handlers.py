import json
import logging
from typing import Tuple
from cryptography.fernet import Fernet, InvalidToken
from typing import Optional, Union
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMultiAlternatives

User = get_user_model()
logger = logging.getLogger(__name__)


def encrypt_data(data: dict, key: bytes) -> str:
    f = Fernet(key)
    json_string = json.dumps(data)
    encrypted_string = f.encrypt(bytes(json_string, encoding="utf-8"))
    return encrypted_string.decode("utf-8")


def decrypt_string(encrypted: Union[str, bytes], key: bytes) -> Optional[dict]:
    f = Fernet(key)
    if not isinstance(encrypted, bytes):
        encrypted = bytes(encrypted, encoding="utf-8")
    try:
        decrypted_string = f.decrypt(encrypted)
        return json.loads(decrypted_string)
    except InvalidToken:
        return


def create_verification_link(user: User) -> Tuple[str, str]:
    data = {"uid": user.pk}
    key = encrypt_data(data, settings.INVITES_KEY)
    verification_url = (
        f"{settings.FRONTEND_BASE_URL}verification-success?actionType=registration"
    )
    logger.info(f"Verification URL => {verification_url}&token={key}")
    return verification_url, key


def smtp(subject, message, recepient):
    send_mail(
        subject, message, settings.DEFAULT_FROM_EMAIL, [recepient], fail_silently=False
    )


def send_verification_email(self):
    verification_url, key = create_verification_link(self)
    recepient = self.email
    subject = "Welcome to Merak."
    message = (
        "Hello, "
        + " Please click on this link to activate your account: "
        + verification_url
        + "&token="
        + key
    )
    html_content = (
        '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Started</title>
    <style type="text/css">
        body {
            margin: 0;
            padding: 0;
            background-color: #EEEEEE;
        }
        table{
            border-spacing: 0;
        }
        td{
            padding: 0;
        }
        img {
            border: 0;
        }
        .wrapper {
            background-color: #EEEEEE;
            width: 100%;
            table-layout: fixed;
        }
        .webkit {
            max-width: 600px;
            padding-bottom: 1rem;
            background-color: #FFFFFF;
        }
        .outer {
            Margin: 0 auto;
            width: 100%;
            max-width: 600px;
            border-spacing: 0;
            font-family: 'Quicksand';
            color: #333333;
        }
        .columns{
            text-align: center;
            font-size: 0;
            line-height: 0;
            padding: 1.5rem 0;
        }
        .columns .column{
            width: 100%;
            max-width: 200px;
            display: inline-block;
            vertical-align: top;
        }
        .padding {
            padding: 0.75rem 1rem;
        }
        .columns .column .content{
            font-size: 1rem;
            line-height: 0.75rem;
        }
        @media screen and (max-width: 400px) {
            .services{
               width: 200px !important;
               height: 150px !important;
           }  
           .padding{
               padding-right: 0 !important;
               padding-left: 0 !important;
           }           
        }
    </style>
</head>
<body>
    <center class="wrapper">
        <div class="webkit">
            <table class="outer" style="margin: 0 auto">
                <!-- Header -->
                <tr>
                    <td>
                        <table width="100%" style="border-spacing: 0;">
                            <tr>
                                <td style="background-color: #FFFFFF; box-shadow: rgba(33, 35, 38, 0.1) 0px 10px 10px -10px; text-align: center;">
                                    <a href=""><img src="https://github.com/Nimesh-bot/HandleMyPaper/blob/main/HMP_logo.png?raw=true" alt="Logo" title="Logo" style="height: 5rem; width: 12rem; object-fit: contain;"></a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <!-- Body -->
                <tr>
                    <td>
                        <a href="#"><img src="https://images.unsplash.com/photo-1604153138516-28db213cf26b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1115&q=80" alt="banner" style="height: 200px; width: 100%; object-fit: cover;"></a>
                        <div style="text-align: center; padding: 0 3rem;">
                            <h3>Thank you for registering</h3>
                            <p style="font-size: 0.75rem; margin-top: -0.5rem;">
                                We are happy to extend our greetings to you and we wish to continue working with you.
                                Visit our website and make yourself known as an expert for paid jobs by sending us an 
                                application or
                                submit your assignment to us and we will ensure to handle your assignment with care and
                                satisfy you to the fullest.
                            </p>
                            <a href="'''
        + verification_url
        + "&token="
        + key
        + """"
                            <button style="padding: 0.5rem; border: none; background-color: #ab47bc; border-radius: 4px; color: white;">Get Started</button>
                        </div>
                    </td>
                </tr>
                <!-- Services -->
                <tr>
                    <td>
                        <table width="100%" style="border-spacing: 0;">
                            <tr>
                                <td class="columns">
                                    <!-- Expert -->
                                    <table class="column">
                                        <tr>
                                            <td class="padding">
                                                <table class="content">
                                                    <tr>
                                                        <td>
                                                            <a href="#"><img class="services" src="https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1172&q=80" alt="" width= "150" style="max-width: 150px; border-radius: 4px; object-fit: cover;"></a>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <h5>Be an Expert</h3>
                                                            <p style="font-size: 0.75rem;">Send us your C.V. to apply yourself as an expert and get tons of paid jobs that matches your specialization</p>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                    <!-- Help -->
                                    <table class="column">
                                        <tr>
                                            <td class="padding">
                                                <table class="content">
                                                    <tr>
                                                        <td>
                                                            <a href="#"><img class="services" src="https://images.unsplash.com/photo-1509475826633-fed577a2c71b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1171&q=80" 
                                                            alt="" width= "150" style="max-width: 150px; border-radius: 4px; object-fit: cover;"></a>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <h5>Find an Expert</h3>
                                                            <p style="font-size: 0.75rem;">
                                                                If you are currently in need of an expert to handle your assignment, submit us your assignment and get your task handled by an expert with care.    
                                                            </p>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <!-- Footer -->
                <tr>
                    <td>
                        <table width="100%" style="border-spacing: 0;">
                            <tr>
                                <td style="background-color: #FFFFFF; box-shadow: rgba(33, 35, 38, 0.1) 0px 10px 10px 10px; text-align: center;">
                                    <h5 style="color: #ab47bc;">Contact: <span style="color: #333333; font-weight: 100;">98XXXXXXXX</span></h5>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </div>
    </center>   
</body>
</html>
"""
    )

    msg = EmailMultiAlternatives(
        subject, message, settings.EMAIL_HOST_USER, [recepient]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print("success")
