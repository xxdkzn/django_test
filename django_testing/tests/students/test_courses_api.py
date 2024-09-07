import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def course():
    return baker.make('students.Course')

@pytest.mark.django_db
def test_retrieve_course(api_client, course):
    url = f'/api/v1/courses/{course.id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == course.id

@pytest.mark.django_db
def test_list_courses(api_client):
    courses = baker.make('students.Course', _quantity=5)
    url = '/api/v1/courses/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(courses)

@pytest.mark.django_db
def test_filter_courses_by_id(api_client):
    course1 = baker.make('students.Course')
    course2 = baker.make('students.Course')
    url = f'/api/v1/courses/?id={course1.id}'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == course1.id

@pytest.mark.django_db
def test_filter_courses_by_name(api_client):
    course1 = baker.make('students.Course', name='Test Course')
    baker.make('students.Course', name='Another Course')
    url = '/api/v1/courses/?name=Test Course'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Course'

@pytest.mark.django_db
def test_create_course(api_client):
    url = '/api/v1/courses/'
    data = {
        'name': 'New Course',
        'description': 'This is a new course.'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'New Course'

@pytest.mark.django_db
def test_update_course(api_client, course):
    url = f'/api/v1/courses/{course.id}/'
    data = {
        'name': 'Updated Course',
        'description': 'Updated description.'
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    course.refresh_from_db()
    assert course.name == 'Updated Course'

@pytest.mark.django_db
def test_delete_course(api_client, course):
    url = f'/api/v1/courses/{course.id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Course.objects.filter(id=course.id).count() == 0