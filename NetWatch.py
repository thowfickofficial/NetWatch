import socket
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Configure logging
logging.basicConfig(filename='monitoring.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Email notification configuration (Add your email configuration here)
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@example.com'
SMTP_PASSWORD = 'your_email_password'

# Initialize email server and login
email_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
email_server.starttls()
email_server.login(SMTP_USERNAME, SMTP_PASSWORD)

# Database configuration (SQLite for simplicity)
import sqlite3

def create_database():
    conn = sqlite3.connect('monitoring.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host TEXT,
            port INTEGER,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_port_open(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((host, port))
        sock.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def send_email(subject, message):
    from_email = SMTP_USERNAME
    to_email = 'recipient@example.com'
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    email_server.sendmail(from_email, to_email, msg.as_string())

def main():
    create_database()
    
    num_services = int(input("Enter the number of services to monitor: "))
    services = []

    for i in range(num_services):
        host = input(f"Enter host for service {i + 1}: ")
        port = int(input(f"Enter port for service {i + 1}: "))
        services.append((host, port))

    interval = int(input("Enter the monitoring interval in seconds: "))

    print(f"Monitoring {num_services} services every {interval} seconds...")

    threshold = 3

    while True:
        for host, port in services:
            open_count = 0
            for _ in range(threshold):
                if is_port_open(host, port):
                    open_count += 1
            if open_count >= threshold:
                status = "OPEN"
                logging.info(f"Port {port} is OPEN on {host}")
            else:
                status = "CLOSED"
                logging.info(f"Port {port} is CLOSED on {host}")
                send_email(f"Port {port} on {host} is DOWN", f"Port {port} is not responding.")
                print(f"Port {port} on {host} is DOWN")  # Console notification
            conn = sqlite3.connect('monitoring.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO service_status (host, port, status) VALUES (?, ?, ?)
            ''', (host, port, status))
            conn.commit()
            conn.close()
        time.sleep(interval)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Monitoring stopped.")
    finally:
        email_server.quit()  # Close the email server when done
