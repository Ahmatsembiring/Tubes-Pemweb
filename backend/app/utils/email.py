import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'your-email@gmail.com')
    SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD', 'your-app-password')
    
    @staticmethod
    def generate_verification_token() -> str:
        """Generate random email verification token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def send_verification_email(recipient_email: str, token: str, frontend_url: str) -> bool:
        """Send email verification link"""
        try:
            verification_link = f"{frontend_url}/verify-email?token={token}"
            
            subject = "Verify Your Email - Job Portal System"
            body = f"""
            <html>
                <body>
                    <h2>Email Verification</h2>
                    <p>Thank you for registering on Job Portal System!</p>
                    <p>Please click the link below to verify your email:</p>
                    <a href="{verification_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Verify Email
                    </a>
                    <p>Or copy and paste this link: {verification_link}</p>
                    <p>This link will expire in 24 hours.</p>
                    <p>Best regards,<br/>Job Portal Team</p>
                </body>
            </html>
            """
            
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = EmailService.SENDER_EMAIL
            message['To'] = recipient_email
            message.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT) as server:
                server.starttls()
                server.login(EmailService.SENDER_EMAIL, EmailService.SENDER_PASSWORD)
                server.send_message(message)
            
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
