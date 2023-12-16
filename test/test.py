from datetime import datetime

from app.app import (
    get_random_object_id,
    get_artwork_summary,
    create_artwork_paragraph,
    send_email_with_artwork_and_buttons,
)


def test_get_random_object_id():
    result = get_random_object_id()
    assert isinstance(result, int)
    assert 1 <= result <= 485596


def test_get_artwork_summary_empty():
    result = get_artwork_summary(1)
    assert result is None


def test_get_artwork_summary():
    result = get_artwork_summary(51749)
    assert result is not None
    assert isinstance(result, dict)


def test_create_artwork_paragraph():
    artwork_summary = {
        "Title": "Test Artwork",
        "Artist": "Test Artist",
        "Object URL": "http://testobject.com",
        "Primary Image URL": "http://testimage.com",
        "Wikidata URL": "test.com",
    }
    result = create_artwork_paragraph(artwork_summary)
    assert "Test Artwork" in result
    assert "Test Artist" in result
    assert "http://testobject.com" in result


def test_send_email_with_artwork_and_buttons():
    current_date = datetime.today().date()

    assert (
        send_email_with_artwork_and_buttons(
            get_artwork_summary(51749), current_date.strftime("%A, %B %d, %Y")
        )
        == 202
    )