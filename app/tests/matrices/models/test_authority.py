import pytest
from django.contrib.auth.models import User
from matrices.models.authority import Authority, AUTHORITY_NONE, AUTHORITY_EDITOR, AUTHORITY_VIEWER, AUTHORITY_OWNER, AUTHORITY_ADMIN


@pytest.mark.django_db
def test_create_authority():
    user = User.objects.create(username='testuser')
    authority = Authority.create(name=AUTHORITY_EDITOR, owner=user)
    #authority.save()

    assert authority.name == AUTHORITY_EDITOR
    assert authority.owner == user


@pytest.mark.django_db
def test_authority_str():
    user = User.objects.create(username='testuser')
    authority = Authority.create(name=AUTHORITY_EDITOR, owner=user)
    #authority.save()

    assert str(authority) == AUTHORITY_EDITOR


@pytest.mark.django_db
def test_authority_repr():
    user = User.objects.create(username='testuser')
    authority = Authority.create(name=AUTHORITY_EDITOR, owner=user)
    #authority.save()

    assert repr(authority) == f"{authority.id}, {AUTHORITY_EDITOR}, {user.id}"


@pytest.mark.django_db
def test_is_owned_by():
    user = User.objects.create(username='testuser')
    another_user = User.objects.create(username='anotheruser')
    authority = Authority.create(name=AUTHORITY_EDITOR, owner=user)
    #authority.save()

    assert authority.is_owned_by(user) is True
    assert authority.is_owned_by(another_user) is False


@pytest.mark.django_db
def test_set_owner():
    user = User.objects.create(username='testuser')
    another_user = User.objects.create(username='anotheruser')
    authority = Authority.create(name=AUTHORITY_EDITOR, owner=user)
    #authority.save()

    authority.set_owner(another_user)
    assert authority.owner == another_user


@pytest.mark.django_db
def test_set_authority_levels():
    user = User.objects.create(username='testuser')
    authority = Authority.create(name=AUTHORITY_NONE, owner=user)
   # authority.save()

    authority.set_as_editor()
    assert authority.name == AUTHORITY_EDITOR

    authority.set_as_viewer()
    assert authority.name == AUTHORITY_VIEWER

    authority.set_as_owner()
    assert authority.name == AUTHORITY_OWNER

    authority.set_as_admin()
    assert authority.name == AUTHORITY_ADMIN


@pytest.mark.django_db
def test_is_authority_levels():
    user = User.objects.create(username='testuser')
    authority = Authority.create(name=AUTHORITY_NONE, owner=user)
    #authority.save()

    assert authority.is_none() is True
    assert authority.is_editor() is False
    assert authority.is_viewer() is False
    assert authority.is_owner() is False
    assert authority.is_admin() is False

    authority.set_as_editor()
    assert authority.is_editor() is True

    authority.set_as_viewer()
    assert authority.is_viewer() is True

    authority.set_as_owner()
    assert authority.is_owner() is True

    authority.set_as_admin()
    assert authority.is_admin() is True