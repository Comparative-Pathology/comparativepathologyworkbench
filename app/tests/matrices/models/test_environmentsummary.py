import pytest
from matrices.models.environmentsummary import ENVIRONMENT_NAME_CPW, EnvironmentSummary


@pytest.mark.django_db
def test_environment_name_cpw():
    assert ENVIRONMENT_NAME_CPW == 'CPW'

@pytest.mark.django_db
def test_environment_summary_str():
    env_summary = EnvironmentSummary(
        environment_id=1,
        environment_name='Test Environment',
        environment_location='Test Location',
        environment_colour='FFFFFF',
        environment_wordpress_active=True,
        environment_background_processing=True,
        environment_window_refresh_time_milliseconds=1000
    )
    assert str(env_summary) == '1, Test Environment, Test Location'

@pytest.mark.django_db
def test_environment_summary_is_cpw():
    env_summary = EnvironmentSummary(
        environment_id=1,
        environment_name='CPW',
        environment_location='Test Location',
        environment_colour='FFFFFF',
        environment_wordpress_active=True,
        environment_background_processing=True,
        environment_window_refresh_time_milliseconds=1000
    )
    assert env_summary.is_cpw() is True

@pytest.mark.django_db
def test_environment_summary_is_not_cpw():
    env_summary = EnvironmentSummary(
        environment_id=1,
        environment_name='Not CPW',
        environment_location='Test Location',
        environment_colour='FFFFFF',
        environment_wordpress_active=True,
        environment_background_processing=True,
        environment_window_refresh_time_milliseconds=1000
    )
    assert env_summary.is_cpw() is False

@pytest.mark.django_db
def test_environment_summary_is_wordpress_active():
    env_summary = EnvironmentSummary(
        environment_id=1,
        environment_name='Test Environment',
        environment_location='Test Location',
        environment_colour='FFFFFF',
        environment_wordpress_active=True,
        environment_background_processing=True,
        environment_window_refresh_time_milliseconds=1000
    )
    assert env_summary.is_wordpress_active() is True

@pytest.mark.django_db
def test_environment_summary_is_not_wordpress_active():
    env_summary = EnvironmentSummary(
        environment_id=1,
        environment_name='Test Environment',
        environment_location='Test Location',
        environment_colour='FFFFFF',
        environment_wordpress_active=False,
        environment_background_processing=True,
        environment_window_refresh_time_milliseconds=1000
    )
    assert env_summary.is_wordpress_active() is False