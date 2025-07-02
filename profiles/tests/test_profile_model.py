import pytest

from profiles.models import Profile


@pytest.mark.django_db
def test_profile_creation():
    """Test the creation of a Profile instance and its default fields."""
    profile = Profile.objects.create(
        tg_id=123456, nickname="testuser", first_name="Test", last_name="User"
    )

    assert profile.tg_id == 123456
    assert profile.nickname == "testuser"
    assert profile.first_name == "Test"
    assert profile.last_name == "User"
    assert profile.created_dt is not None
