"""
Email Sender
------------
Sends the HTML newsletter via Gmail SMTP.

SMTP = Simple Mail Transfer Protocol
It's the standard protocol for sending email.
Gmail lets you use it with an "App Password" for security.

Key concept: smtplib is Python's built-in email library.
We use SSL (port 465) for an encrypted connection.
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config.settings import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL


def wrap_in_template(newsletter_html: str) -> str:
    """
    Load the HTML email template and inject the newsletter content.
    
    We use simple string replacement instead of Jinja2 for clarity.
    """
    try:
        with open("delivery/templates/newsletter.html", "r") as f:
            template = f.read()
        return template.replace("{{ newsletter_content }}", newsletter_html)
    except FileNotFoundError:
        # Fallback: just return the content without a wrapper template
        return f"""<html><body>{newsletter_html}</body></html>"""


def send_newsletter(newsletter_html: str) -> bool:
    """
    Send the newsletter via Gmail SMTP.
    
    Returns True if successful, False if there was an error.
    """
    today = datetime.now().strftime("%A, %B %d, %Y")
    subject = f"📊 Finance Brief - {today}"
    
    # Wrap in HTML template
    full_html = wrap_in_template(newsletter_html)
    
    # Build the email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    
    # Attach the HTML body
    html_part = MIMEText(full_html, "html")
    msg.attach(html_part)
    
    print(f"Sending email to {RECIPIENT_EMAIL}...")
    
    # Connect to Gmail's SMTP server and send
    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        
        print(f"✓ Email sent successfully!")
        return True
    
    except smtplib.SMTPAuthenticationError:
        print("✗ Email failed: Authentication error.")
        print("  Check your Gmail address and App Password in .env")
        return False
    
    except Exception as e:
        print(f"✗ Email failed: {e}")
        return False
