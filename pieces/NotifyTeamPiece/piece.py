from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

class NotifyTeamPiece(BasePiece):
    
    def send_email(self, metrics: dict):

        # Email configuration from environment variables
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL", "energy-team@company.com")
        
        if not sender_email or not sender_password:
            print("[WARNING] Email credentials not configured. Skipping email.")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"✅ Solar XGBoost Model Trained - MAE: {metrics['MAE_kW']} kW"
        
        body = f"""
        Hello Team,
        
        The daily XGBoost training has completed successfully.
        
        Performance Metrics:
        - MAE: {metrics['MAE_kW']} kW
        - R²: {metrics['R2']}
        - Samples: {metrics['samples']:,}
        
        Model registered in Domino.
        
        Best regards,
        SoMES Pipeline
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            print(f"[SUCCESS] Email sent to {recipient_email}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
            return False

    def send_slack(self, metrics: dict, webhook_url: str) -> bool:
        payload = {
            "text": f"*Solar XGBoost pipeline completed*\n"
                    f"> *MAE*: {metrics['MAE_kW']} kW\n"
                    f"> *R²*: {metrics['R2']}\n"
                    f"> *Samples*: {metrics['samples']:,}\n"
                    f"> <{os.getenv('DOMINO_PROJECT_URL', '#')}|View model in Domino>"
        }
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            print("[SUCCESS] Slack notification sent")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send Slack notification: {e}")
            return False

    def piece_function(self, input_data: InputModel):
        print(f"[INFO] Sending notifications...")
        
        # Load metrics
        with open(input_data.metrics_path) as f:
            metrics = json.load(f)
        
        # Send email
        email_sent = self.send_email(metrics)
        
        # Send Slack notification if webhook provided
        slack_sent = False
        if input_data.webhook_url:
            slack_sent = self.send_slack(metrics, input_data.webhook_url)
        
        notification_sent = email_sent or slack_sent
        recipients = "email" if email_sent else ""
        if slack_sent:
            recipients += ", slack" if recipients else "slack"
        
        print("[SUCCESS] Notifications completed")
        
        return OutputModel(
            message=f"Notifications sent successfully",
            notification_sent=notification_sent,
            recipients=recipients if recipients else "none"
        )
  

# import json
# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import requests
# from models import InputModel, OutputModel

# def send_email(metrics: dict) -> bool:
#     # Email configuration from environment variables
#     smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
#     smtp_port = int(os.getenv("SMTP_PORT", "587"))
#     sender_email = os.getenv("SENDER_EMAIL")
#     sender_password = os.getenv("SENDER_PASSWORD")
#     recipient_email = os.getenv("RECIPIENT_EMAIL", "energy-team@company.com")
    
#     if not sender_email or not sender_password:
#         print("[WARNING] Email credentials not configured. Skipping email.")
#         return False
    
#     # Create message
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = recipient_email
#     msg['Subject'] = f"✅ Solar XGBoost Model Trained - MAE: {metrics['MAE_kW']} kW"
    
#     body = f"""
#     Hello Team,
    
#     The daily XGBoost training has completed successfully.
    
#     Performance Metrics:
#     - MAE: {metrics['MAE_kW']} kW
#     - R²: {metrics['R2']}
#     - Samples: {metrics['samples']:,}
    
#     Model registered in Domino.
    
#     Best regards,
#     SoMES Pipeline
#     """
    
#     msg.attach(MIMEText(body, 'plain'))
    
#     # Send email
#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         text = msg.as_string()
#         server.sendmail(sender_email, recipient_email, text)
#         server.quit()
#         print(f"[SUCCESS] Email sent to {recipient_email}")
#         return True
#     except Exception as e:
#         print(f"[ERROR] Failed to send email: {e}")
#         return False

# def send_slack(metrics: dict, webhook_url: str) -> bool:
#     payload = {
#         "text": f"*Solar XGBoost pipeline completed*\n"
#                 f"> *MAE*: {metrics['MAE_kW']} kW\n"
#                 f"> *R²*: {metrics['R2']}\n"
#                 f"> *Samples*: {metrics['samples']:,}\n"
#                 f"> <{os.getenv('DOMINO_PROJECT_URL', '#')}|View model in Domino>"
#     }
    
#     try:
#         response = requests.post(webhook_url, json=payload)
#         response.raise_for_status()
#         print("[SUCCESS] Slack notification sent")
#         return True
#     except Exception as e:
#         print(f"[ERROR] Failed to send Slack notification: {e}")
#         return False

# def main(input_model: InputModel) -> OutputModel:
#     print(f"[INFO] Sending notifications...")
    
#     # Load metrics
#     with open(input_model.metrics_path) as f:
#         metrics = json.load(f)
    
#     # Send email
#     email_sent = send_email(metrics)
    
#     # Send Slack notification if webhook provided
#     slack_sent = False
#     if input_model.webhook_url:
#         slack_sent = send_slack(metrics, input_model.webhook_url)
    
#     notification_sent = email_sent or slack_sent
#     recipients = "email" if email_sent else ""
#     if slack_sent:
#         recipients += ", slack" if recipients else "slack"
    
#     print("[SUCCESS] Notifications completed")
    
#     return OutputModel(
#         message=f"Notifications sent successfully",
#         notification_sent=notification_sent,
#         recipients=recipients if recipients else "none"
#     )

# if __name__ == "__main__":
#     # For testing purposes
#     input_data = InputModel(
#         metrics_path="/mnt/artifacts/metrics.json",
#         webhook_url="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
#     )
#     result = main(input_data)
#     print(result)