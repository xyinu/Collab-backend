from dotenv import load_dotenv
import os
from azure.communication.email import EmailClient

load_dotenv()
connection_string = os.getenv('CONNECTION_STRING')
email_client = EmailClient.from_connection_string(connection_string)
url = 'https://gray-desert-02bb59f00.4.azurestaticapps.net' if os.getenv('ENVIRONMENT') == 'Production' else 'http://localhost:8000'

def send_ticket(title,TA,student,category,severity,details,email):
    try:
        message = {
            "content": {
                "subject": f"Ticket Created: {title} by {TA}",
                "html": f"<html><p>Title: {title}</p> <p>From: {TA}</p> <p>Student: {student}</p><p>Category: {category}</p><p>Severity: {severity}</p> <p>Details: {details}</p></html>"
            },
            "recipients": {
                "to": [
                    {
                        "address": f"{email}",
                    }
                ]
            },
            "senderAddress": "DoNotReply@f1307582-508c-4a39-ac6f-36a7a59039bb.azurecomm.net"
        }

        poller = email_client.begin_send(message)
        result = poller.result()
    except Exception as ex:
        print(ex)

def send_ticket_approve(title,TA,student,category,severity,details,email):
    try:
        message = {
            "content": {
                "subject": f"Ticket Created: {title} by {TA}",
                "html": f"<html><p>Title: {title}</p> <p>From: {TA}</p> <p>Student: {student}</p><p>Category: {category}</p><p>Severity: {severity}</p> <p>Details: {details}</p><p>You can click on approve or reject link below for action. Or you can go on the website to ask more about the ticket at <a href='{url}'>Link</a></p></html>"
            },
            "recipients": {
                "to": [
                    {
                        "address": f"{email}",
                    }
                ]
            },
            "senderAddress": "DoNotReply@f1307582-508c-4a39-ac6f-36a7a59039bb.azurecomm.net"
        }

        poller = email_client.begin_send(message)
        result = poller.result()
    except Exception as ex:
        print(ex)

def send_completed_ticket(title,TA,student,category,severity,details,email,Prof,comment):
    try:
        message = {
            "content": {
                "subject": f"Ticket Closed: {title}",
                "html": f"<html><p>Title: {title}</p> <p>From: {TA}</p> <p>Student: {student}</p><p>Category: {category}</p><p>Severity: {severity}</p> <p>Details: {details}</p><h4>Final Comment: {comment}</h4><p>This ticket has been closed by {Prof}</p></html>"
            },
            "recipients": {
                "to": [
                    {
                        "address": f"{email}",
                    }
                ]
            },
            "senderAddress": "DoNotReply@f1307582-508c-4a39-ac6f-36a7a59039bb.azurecomm.net"
        }

        poller = email_client.begin_send(message)
        result = poller.result()
    except Exception as ex:
        print(ex)

def send_reopen_ticket(title,TA,student,category,severity,details,email,Prof,comment):
    try:
        message = {
            "content": {
                "subject": f"Ticket Reopned: {title}",
                "html": f"<html><h4>Reopen Comment: {comment}</h4><p>Title: {title}</p> <p>From: {TA}</p> <p>Student: {student}</p><p>Category: {category}</p><p>Severity: {severity}</p> <p>Details: {details}</p><p>This ticket has been reopened by {Prof}</p></html>"
            },
            "recipients": {
                "to": [
                    {
                        "address": f"{email}",
                    }
                ]
            },
            "senderAddress": "DoNotReply@f1307582-508c-4a39-ac6f-36a7a59039bb.azurecomm.net"
        }

        poller = email_client.begin_send(message)
        result = poller.result()
    except Exception as ex:
        print(ex)

def send_task(title,Prof,details,dueDate,email):
    try:
        message = {
            "content": {
                "subject": f"Task Created: {title} by {Prof}",
                "html": f"<html><p>Title: {title}</p> <p>From: {Prof}</p><p>Due Date: {dueDate}</p><p>Details: {details}</p></html>"
            },
            "recipients": {
                "to": [
                    {
                        "address": f"{email}",
                    }
                ]
            },
            "senderAddress": "DoNotReply@f1307582-508c-4a39-ac6f-36a7a59039bb.azurecomm.net"
        }

        poller = email_client.begin_send(message)
        result = poller.result()
    except Exception as ex:
        print(ex)

def send_completed_task(title,Prof,details,dueDate,email,TA):
    try:
        message = {
            "content": {
                "subject": f"Task Completed: {title} completed by {TA}",
                "html": f"<html><p>Title: {title}</p> <p>From: {Prof}</p><p>Due Date: {dueDate}</p><p>Details: {details}</p> <p>Task has been completed by {TA}</html>"
            },
            "recipients": {
                "to": [
                    {
                        "address": f"{email}",
                    }
                ]
            },
            "senderAddress": "DoNotReply@f1307582-508c-4a39-ac6f-36a7a59039bb.azurecomm.net"
        }

        poller = email_client.begin_send(message)
        result = poller.result()
    except Exception as ex:
        print(ex)

def send_thread(by,ticket,details,email):
    try:
        message = {
            "content": {
                "subject": f"Comment Created by {by} for {ticket}",
                "html": f"<html><p>Ticket Title:{ticket}</p> <p>From: {by}</p><p>Comment: {details}</p></html>"
            },
            "recipients": {
                "to": [
                    {
                        "address": f"{email}",
                    }
                ]
            },
            "senderAddress": "DoNotReply@f1307582-508c-4a39-ac6f-36a7a59039bb.azurecomm.net"
        }

        poller = email_client.begin_send(message)
        result = poller.result()
    except Exception as ex:
        print(ex)

def send_task_thread(by,ticket,details,email):
    try:
        message = {
            "content": {
                "subject": f"Comment Created by {by} for {ticket}",
                "html": f"<html><p>Task Title:{ticket}</p> <p>From: {by}</p><p>Comment: {details}</p></html>"
            },
            "recipients": {
                "to": [
                    {
                        "address": f"{email}",
                    }
                ]
            },
            "senderAddress": "DoNotReply@f1307582-508c-4a39-ac6f-36a7a59039bb.azurecomm.net"
        }

        poller = email_client.begin_send(message)
        result = poller.result()
    except Exception as ex:
        print(ex)

def send_access(name,email):
    try:
        message = {
            "content": {
                "subject": "Joining of collaboration tool",
                "html": f"<html><p>Hello,</p> <p>You have been invited by {name} to use the collaboration tool, please click on the link below to authenticate your account using your NTU email. Thank you.</p><a href='{url}'>Link</a></html>"
            },
            "recipients": {
                "to": [
                    {
                        "address": f"{email}",
                    }
                ]
            },
            "senderAddress": "DoNotReply@f1307582-508c-4a39-ac6f-36a7a59039bb.azurecomm.net"
        }

        poller = email_client.begin_send(message)
        result = poller.result()
    except Exception as ex:
        print(ex)