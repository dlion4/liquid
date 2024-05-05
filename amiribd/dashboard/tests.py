from django.test import TestCase

# Create your tests here.

import pytest
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse
from amiribd.dashboard.kyc.views import (
    YourViewClass,
)  # Adjust the import according to your view class name


@pytest.mark.parametrize(
    "form_data, expected_url",
    [
        # Happy path tests
        (
            {"field1": "value1", "field2": "value2"},
            "/expected/success/url/",
            pytest.param(id="happy-path-1"),
        ),
        (
            {"field1": "differentValue", "field2": "anotherValue"},
            "/expected/success/url/",
            pytest.param(id="happy-path-2"),
        ),
        # Edge cases
        (
            {"field1": "", "field2": "value2"},
            "/expected/success/url/",
            pytest.param(id="edge-case-empty-field1"),
        ),
        (
            {"field1": "value1", "field2": ""},
            "/expected/success/url/",
            pytest.param(id="edge-case-empty-field2"),
        ),
        # Assuming your form validation handles these, otherwise adjust for actual error handling
        # Error cases
        ({}, "/error/url/", pytest.param(id="error-case-empty-form")),
        (
            {"field1": "invalidValue", "field2": "anotherInvalidValue"},
            "/error/url/",
            pytest.param(id="error-case-invalid-values"),
        ),
    ],
)
def test_form_valid(form_data, expected_url):
    # Arrange
    request = RequestFactory().post("/dummy/url/", data=form_data)
    view = YourViewClass()
    view.request = request
    view.success_url = expected_url
    form_class = view.get_form_class()
    form = form_class(data=form_data)

    # Act
    response = view.form_valid(form)

    # Assert
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == expected_url
