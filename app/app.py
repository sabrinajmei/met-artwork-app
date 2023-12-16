# PACKAGE IMPORT

import os
import requests
import random
import sendgrid

from IPython.display import display, Image
from datetime import datetime

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# AUTHORIZATION & API ACCESS

all_objects = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
response_test = requests.get(all_objects)
api_test = response_test.json()

from dotenv import load_dotenv
load_dotenv()
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# COLLECTING USER INFO

def get_user_email():
    return input("Please enter your email address: ")

def get_user_name():
    return input("Please enter your name: ")

# USAGE

def get_random_object_id():
    return random.randint(1, 485596)

# Met API Endpoint for Objects
objects_endpoint = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

def get_artwork_summary(object_id):
    url = (
        f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    )
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if all(data.get(key) for key in ["primaryImage", "title", "artistDisplayName"]):
            summary = {
                "Title": data["title"],
                "Artist": data["artistDisplayName"],
                "Culture": data.get("culture", "N/A"),
                "Classification": data.get("classification", "N/A"),
                "Object URL": data.get("objectURL", "N/A"),
                "Primary Image URL": data["primaryImage"],
                "Medium": data.get("medium", "N/A"),
                "Dimensions": data.get("dimensions", "N/A"),
                "Date Created": data.get("objectDate", "N/A"),
                "Wikidata URL": data.get("objectWikidata_URL", "N/A"),
                "Artist URL": data.get("artistULAN_URL","N/A")
            }
            return summary
    return None


def create_artwork_paragraph(artwork_summary):
    paragraph = f"This image depicts {artwork_summary['Title']}, an artwork by {artwork_summary['Artist']}. "
    paragraph += f"For more information, visit [Met Museum source]({artwork_summary['Object URL']})"

    # Include Wikidata source if available
    if "Wikidata URL" in artwork_summary and artwork_summary["Wikidata URL"] != "N/A":
        paragraph += f" or [Wikidata source]({artwork_summary['Wikidata URL']})."
    else:
        paragraph += "."

    return paragraph


def display_artwork(artwork_summary, image_size=(300, 300)):
    print("Artwork Summary:")
    for key, value in artwork_summary.items():
        print(f"{key}: {value}")

    # Display the primary image with a specified size
    primary_image_url = artwork_summary.get("Primary Image URL", None)
    if primary_image_url:
        print("\nPrimary Image:")
        display(Image(url=primary_image_url, width=image_size[0], height=image_size[1]))
    else:
        print("\nPrimary Image: Image not available.")

# SENDING THE EMAIL

#formatting the current date
current_date = datetime.today().date()
formatted_date = current_date.strftime("%A, %B %d, %Y")

def send_email_with_artwork_and_buttons(
    artwork_summary,
    formatted_date,
    recipient_address="sjm189@georgetown.edu",
    subject="Snapshot of The Met: Check out this amazing artwork!",
):
    print("SENDING EMAIL TO:", recipient_address)
    print("SUBJECT:", subject)

    # Create HTML content for the email
    html_content = f"<p style='font-size: 24px;'><strong>{formatted_date}</strong>: <strong style='font-size: 24px;'>Snapshot of The Met</strong></p>"
    html_content += f"<p>Hello {get_user_name()}! </p>"
    html_content += f"<p>Check out this amazing artwork:</p>"
    html_content += f"<p>Title: {artwork_summary['Title']}</p>"
    html_content += f"<p>Artist: {artwork_summary['Artist']}</p>"
    html_content += f"<p>Culture: {artwork_summary['Culture']}</p>"
    html_content += f"<p>Classification: {artwork_summary['Classification']}</p>"
    html_content += f"<p>Medium: {artwork_summary['Medium']}</p>"
    html_content += f"<p>Date Created: {artwork_summary['Date Created']}</p>"

    # Include image in the email if available
    if artwork_summary["Primary Image URL"]:
        html_content += f"<p>Image:</p>"
        html_content += f'<img src="{artwork_summary["Primary Image URL"]}" alt="Artwork Image" style="max-width: 500px;">'

    # Include Met Museum link for ART button if available
    if artwork_summary["Object URL"] and artwork_summary["Object URL"] != "N/A":
        html_content += f'<div><a href="{artwork_summary["Object URL"]}" style="background-color: #eb0029; color: white; padding: 10px 15px; margin-bottom: 10px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Learn more about the artwork here.</a></div>'

    # Include ULAN link for ARTIST button if available
    if artwork_summary["Artist URL"] and artwork_summary["Artist URL"] != "N/A":
        html_content += f'<div><a href="{artwork_summary["Artist URL"]}" style="background-color: #eb0029; color: white; padding: 10px 15px; margin-top: 10px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Learn more about the artist here.</a></div>'

    # Use SendGrid to send the email
    message = Mail(
        from_email=SENDER_ADDRESS,
        to_emails=recipient_address,
        subject=subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("RESULT:", response.status_code)
        print("Email sent successfully!")
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return None

# Function to get user's choice on whether to input a department
def get_user_department_choice():
    choice = input("Do you want to filter by department? (yes/no): ").lower()
    return choice == "yes"

# Function to get the user's preferred department
def get_user_department():
    print("Choose a department:")
    departments = [
        {"departmentId": 1, "displayName": "American Decorative Arts"},
        {"departmentId": 2, "displayName": "Ancient Near Eastern Art"},
        {"departmentId": 3, "displayName": "Arms and Armor"},
        {"departmentId": 4, "displayName": "Arts of Africa, Oceania, and the Americas"},
        {"departmentId": 5, "displayName": "Asian Art"},
        {"departmentId": 6, "displayName": "The Cloisters"},
        {"departmentId": 7, "displayName": "The Costume Institute"},
        {"departmentId": 8, "displayName": "Drawings and Prints"},
        {"departmentId": 9, "displayName": "Egyptian Art"},
        {"departmentId": 10, "displayName": "European Paintings"},
        {"departmentId": 11, "displayName": "European Sculpture and Decorative Arts"},
        {"departmentId": 12, "displayName": "Greek and Roman Art"},
        {"departmentId": 13, "displayName": "Islamic Art"},
        {"departmentId": 14, "displayName": "The Robert Lehman Collection"},
        {"departmentId": 15, "displayName": "The Libraries"},
        {"departmentId": 16, "displayName": "Medieval Art"},
        {"departmentId": 17, "displayName": "Musical Instruments"},
        {"departmentId": 18, "displayName": "Photographs"},
        {"departmentId": 19, "displayName": "Modern Art"},
    ]

    for dept in departments:
        print(f"{dept['departmentId']}. {dept['displayName']}")

    department_choice = int(input("Enter the number corresponding to your preferred department: "))
    return next((dept for dept in departments if dept["departmentId"] == department_choice), None)

# Function to get a random object ID based on user preferences
def get_random_object_id_for_department(department_id):
    params = {"departmentIds": department_id, "hasImages": "true"}
    response = requests.get(objects_endpoint, params=params)
    data = response.json()

    if "objectIDs" in data:
        object_ids = data["objectIDs"]
        if object_ids:
            return random.choice(object_ids)
    return None

# While Loop
while True:
    user_wants_department = get_user_department_choice()

    if user_wants_department:
        user_department = get_user_department()

        while user_department:
            random_object_id = get_random_object_id_for_department(user_department["departmentId"])

            artwork_summary = get_artwork_summary(random_object_id)

            if artwork_summary:
                display_artwork(artwork_summary)
                paragraph = create_artwork_paragraph(artwork_summary)
                print("\nArtwork Description:")
                print(paragraph)

                # Prompt user for email address
                recipient_email = get_user_email()

                # Send email with artwork summary and buttons
                send_email_with_artwork_and_buttons(
                    artwork_summary,
                    formatted_date,
                    recipient_address=recipient_email,
                    subject="Snapshot of The Met: Check out this amazing artwork!",
                )
                break
            else:
                print(
                    f"Object ID {random_object_id} does not have complete information or an available image. Trying another one..."
                )

        # Ask the user if they want to search for another artwork
        another_search = input("Do you want to search for another artwork? (yes/no): ").lower()
        if another_search != "yes":
            break
    else:
        while True:
            random_object_id = get_random_object_id()

            artwork_summary = get_artwork_summary(random_object_id)

            if artwork_summary:
                display_artwork(artwork_summary)
                paragraph = create_artwork_paragraph(artwork_summary)
                print("\nArtwork Description:")
                print(paragraph)

                # Prompt user for email address
                recipient_email = get_user_email()

                # Send email with artwork summary and buttons
                send_email_with_artwork_and_buttons(
                    artwork_summary,
                    formatted_date,
                    recipient_address=recipient_email,
                    subject="Snapshot of The Met: Check out this amazing artwork!",
                )
                break
            else:
                print(
                    f"Object ID {random_object_id} does not have complete information or an available image. Trying another one..."
                )

        # Ask the user if they want to search for another artwork
        another_search = input("Do you want to search for another artwork? (yes/no): ").lower()
        if another_search != "yes":
            break