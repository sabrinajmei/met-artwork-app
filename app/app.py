# Package Import

import requests
import random
import os
from IPython.display import display, Image
from datetime import datetime

# Authorization and API Access

all_objects = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
response_test = requests.get(all_objects)
api_test = response_test.json()

# Collecting User Info

def get_user_email():
    return input("Please enter your email address: ")

def get_user_name():
    return input("Please enter your name: ")

# Usage

from dotenv import load_dotenv
load_dotenv()
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def get_random_object_id():
    return random.randint(1, 485596)


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
    if artwork_summary["Wikidata URL"] and artwork_summary["Wikidata URL"] != "N/A":
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

# Sending the Email

#formatting the current date
current_date = datetime.today().date()
formatted_date = current_date.strftime("%A, %B %d, %Y")

def send_email_with_artwork_and_buttons(
    artwork_summary,
    recipient_address="adw94@georgetown.edu",
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

    try:
        request_url = "https://api.sendgrid.com/v3/mail/send"
        message_data = {
            "personalizations": [{"to": [{"email": recipient_address}]}],
            "from": {"email": SENDER_ADDRESS},
            "subject": subject,
            "content": [{"type": "text/html", "value": html_content}],
        }
        headers = {"Authorization": f"Bearer {SENDGRID_API_KEY}"}
        response = requests.post(request_url, headers=headers, json=message_data)
        print("RESULT:", response.status_code)
        response.raise_for_status()
        print("Email sent successfully!")
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error sending email: {str(e)}")
        return None

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
        send_email_with_artwork_and_buttons(artwork_summary, recipient_address=recipient_email)
        break
    else:
        print(
            f"Object ID {random_object_id} does not have complete information or an available image. Trying another one..."
        )