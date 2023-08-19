# NetWatch

NetWatch is a Python script that helps you monitor the status of network services and receive email notifications when services go down. It offers the following features:

- **Flexible Monitoring**: NetWatch allows you to monitor multiple network services running on different hosts. You can specify the services you want to monitor, including their hostnames and ports.

- **Email Notifications**: When a monitored service becomes unavailable, NetWatch sends an email notification to a specified recipient. This feature ensures that you are promptly informed of any service disruptions.

- **Customizable Monitoring Interval**: You can configure the monitoring interval, which determines how often the script checks the status of the services. This flexibility allows you to tailor the tool to your specific needs.

- **Logging**: NetWatch logs service status information to a file named `monitoring.log`. This log file helps you keep a historical record of service uptime and downtime.

- **Database Storage**: The tool uses SQLite to store service status information in a database file named `monitoring.db`. You can use SQLite tools to query and analyze the data as needed.

## Prerequisites

Before you begin, make sure you have the following:

- Python 3 installed on your system.
- SMTP server credentials (for sending email notifications).
- Recipient email address to receive notifications.
- SQLite database support (included in Python's standard library).


  ## Usage

1. Run the NetWatch script:

           ```bash
        python NetWatch.py

2. The script will prompt you for the following information:
      -  Number of services to monitor.
      - Hostname and port for each service.
       - Monitoring interval in seconds (how often to check the service status).

3.  The script will continuously monitor the specified services and log the status in the monitoring.log file. If a service becomes unavailable, it will send an email notification and print a message to the console.

4. To stop monitoring, press Ctrl + C.
