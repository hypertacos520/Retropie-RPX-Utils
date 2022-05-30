import graphicOverlay as go
import sys

if (len(sys.argv) < 3 or len(sys.argv) > 3):
    print("Invalid Arugument Format! Format:\n\npython3 notification.py *NOTIFICATION_TYPE* *NOTIFICATION_TEXT*\n")
    exit()

go.send_system_notification(int(sys.argv[1]), sys.argv[2])