import smtplib
import time
import requests
from datetime import datetime

MY_LAT = 44.656610
MY_LONG = -63.624070

MY_EMAIL = "projectcodeworks@gmail.com"  # Corrected email
MY_PASS = "kste cqjy jjjo vlwe"
HET = "jivanihet142004@gmail.com"

def is_iss_overhead():
    try:
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()

        iss_longitude = float(data["iss_position"]["longitude"])
        iss_latitude = float(data["iss_position"]["latitude"])

        if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
            return True
        return False
    except requests.RequestException as e:
        print(f"Error fetching ISS data: {e}")
        return False

def is_nighttime():
    try:
        parameters = {
            "lat": MY_LAT,
            "lng": MY_LONG,
            "formatted": 0,
        }
        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()
        data = response.json()
        sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

        time_now = datetime.now().hour

        if time_now >= sunset or time_now <= sunrise:
            return True
        return False
    except requests.RequestException as e:
        print(f"Error fetching sunrise/sunset data: {e}")
        return False

while True:
    time.sleep(60)
    if is_iss_overhead() and is_nighttime():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:  # Added port number
                        connection.starttls()
                        connection.login(user=MY_EMAIL, password=MY_PASS)
                        connection.sendmail(
                            from_addr=MY_EMAIL,
                            to_addrs=[MY_EMAIL,HET],
                            msg="Subject: ISS Overhead Alert: Time to Look Up!\n\n"
                                "Hello,\n\n"
                                "This is an automated notification from ISS Tracking System.\n"
                                "\nThe International Space Station (ISS) is currently overhead and it is nighttime.\n\n"
                                "This email was sent by a Python program created by Anand Lo. My purpose is to monitor the ISS's position"
                                " and notify you whenever it is directly above your location during the night.\n\n"
                                "Best regards,\n"
                                "\nISS Tracking System"
                        )

