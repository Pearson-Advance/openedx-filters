"""
Tests for ``authentication`` subdomain filters.
"""
import unittest
from unittest.mock import Mock, patch

from openedx_filters.authentication.filters import (
    SessionJWTCreationRequested,
    StudentLogoutRequested,
    StudentRegistrationFormTermsOfServiceLabelRequested,
)
from openedx_filters.tooling import OpenEdxPublicFilter


class TestSessionJWTCreationRequested(unittest.TestCase):
    """
    Test class to verify standard behavior of the filters located in authentication.

    - SessionJWTCreationRequested
    """

    def test_session_jwt_creation_requested(self):
        """
        Test SessionJWTCreationRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter should return the payload and the user.
        """
        payload = {'key': 'value'}
        modified_payload = {'key': 'modified_value'}
        user = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            'run_pipeline',
            return_value={'payload': modified_payload, 'user': user},
        ) as mock_run_pipeline:
            payload_result, user_result = SessionJWTCreationRequested.run_filter(payload, user)

            mock_run_pipeline.assert_called_once_with(payload=payload, user=user)
            self.assertEqual(modified_payload, payload_result)
            self.assertEqual(user, user_result)

    def test_session_jwt_creation_requested_missing_payload(self):
        """
        Test SessionJWTCreationRequested filter behavior when the payload is missing.

        Expected behavior:
            - The filter should return an empty payload and the user.
        """
        user = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            'run_pipeline',
            return_value={'payload': {}, 'user': user},
        ) as mock_run_pipeline:
            payload_result, user_result = SessionJWTCreationRequested.run_filter(None, user)

            mock_run_pipeline.assert_called_once_with(payload=None, user=user)
            self.assertEqual({}, payload_result)
            self.assertEqual(user, user_result)


class TestStudentLogoutRequested(unittest.TestCase):
    """
    Test class to verify standard behavior of the filters located in learning.

    - StudentLogoutRequested
    """

    def test_student_logout_requested_returns_modified_request(self):
        """
        Test StudentLogoutRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter should return the request provided by the pipeline output.
        """
        request = Mock()
        modified_request = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={"request": modified_request},
        ) as mock_run_pipeline:
            request_result = StudentLogoutRequested.run_filter(request)

            mock_run_pipeline.assert_called_once_with(request=request)
            self.assertEqual(modified_request, request_result)

    def test_student_logout_requested_missing_request_in_pipeline_output(self):
        """
        Test StudentLogoutRequested behavior when the pipeline output does not include 'request'.

        Expected behavior:
            - The filter should return the original request.
        """
        request = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={},  # no "request" key
        ) as mock_run_pipeline:
            request_result = StudentLogoutRequested.run_filter(request)

            mock_run_pipeline.assert_called_once_with(request=request)
            self.assertEqual(request, request_result)

    def test_student_logout_requested_non_dict_pipeline_output(self):
        """
        Test StudentLogoutRequested behavior when the pipeline returns a non-dict value.

        Expected behavior:
            - The filter should return the original request.
        """
        request = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value="not-a-dict",
        ) as mock_run_pipeline:
            request_result = StudentLogoutRequested.run_filter(request)

            mock_run_pipeline.assert_called_once_with(request=request)
            self.assertEqual(request, request_result)


class TestStudentRegistrationFormTermsOfServiceLabelRequested(unittest.TestCase):
    """
    Test class to verify standard behavior of the registration form label filter.

    - StudentRegistrationFormTermsOfServiceLabelRequested
    """

    def test_terms_of_service_label_requested_returns_modified_label(self):
        """
        Test filter behavior under normal conditions.

        Expected behavior:
            - The filter returns the modified label from the pipeline output.
        """
        label = "default label"
        platform_name = "My Platform"
        modified_label = "modified label"

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={"label": modified_label},
        ) as mock_run_pipeline:
            result = StudentRegistrationFormTermsOfServiceLabelRequested.run_filter(
                label=label,
                platform_name=platform_name,
            )

            mock_run_pipeline.assert_called_once_with(label=label, platform_name=platform_name)
            self.assertEqual(modified_label, result)

    def test_terms_of_service_label_requested_missing_label_in_pipeline_output(self):
        """
        Test behavior when pipeline output does not contain 'label'.

        Expected behavior:
            - The filter returns the original label.
        """
        label = "default label"
        platform_name = "My Platform"

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={},  # no "label" key
        ) as mock_run_pipeline:
            result = StudentRegistrationFormTermsOfServiceLabelRequested.run_filter(
                label=label,
                platform_name=platform_name,
            )

            mock_run_pipeline.assert_called_once_with(label=label, platform_name=platform_name)
            self.assertEqual(label, result)

    def test_terms_of_service_label_requested_non_dict_pipeline_output(self):
        """
        Test behavior when the pipeline returns a non-dict.

        Expected behavior:
            - The filter returns the original label.
        """
        label = "default label"
        platform_name = "My Platform"

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value="not-a-dict",
        ) as mock_run_pipeline:
            result = StudentRegistrationFormTermsOfServiceLabelRequested.run_filter(
                label=label,
                platform_name=platform_name,
            )

            mock_run_pipeline.assert_called_once_with(label=label, platform_name=platform_name)
            self.assertEqual(label, result)

    def test_terms_of_service_label_requested_none_pipeline_output(self):
        """
        Test behavior when the pipeline returns None.

        Expected behavior:
            - The filter returns the original label.
        """
        label = "default label"
        platform_name = "My Platform"

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value=None,
        ) as mock_run_pipeline:
            result = StudentRegistrationFormTermsOfServiceLabelRequested.run_filter(
                label=label,
                platform_name=platform_name,
            )

            mock_run_pipeline.assert_called_once_with(label=label, platform_name=platform_name)
            self.assertEqual(label, result)
