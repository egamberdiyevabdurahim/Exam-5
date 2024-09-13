import smtplib

from database_config.config import EMAIL_CONFIG


class EmailSender:
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG.get('host')
        self.smtp_port = EMAIL_CONFIG.get("port")
        self.smtp_sender = EMAIL_CONFIG.get('sender')
        self.smtp_password = EMAIL_CONFIG.get('password')
        self.server = None

    def __enter__(self):
        # Set up the SMTP server connection
        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.server.starttls()  # Secure the connection
        self.server.login(self.smtp_sender, self.smtp_password)
        return self  # Return the instance itself for calling `send_email`

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure the server connection is closed
        if self.server:
            self.server.quit()

    def send_email(self, subject: str, message: str, to_user: str):
        email = f"Subject: {subject}\n\n{message}"
        self.server.sendmail(self.smtp_sender, to_user, email)


def send_email(subject: str, message: str, to_user: str):
    with EmailSender() as email_sender:
        email_sender.send_email(subject, message, to_user)
