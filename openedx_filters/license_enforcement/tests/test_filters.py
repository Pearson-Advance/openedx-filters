"""
Tests for ``license_enforcement`` subdomain filters.
"""
import unittest
from unittest.mock import Mock, patch

from openedx_filters.license_enforcement.filters import (
    CcxCoachTabAccessRequested,
    CcxCreationPermissionRequested,
    CcxEnrollmentLicenseEnforcementRequested,
    CcxLicensedStatusRequested,
    CcxPendingEnrollmentsRequested,
    CourseLicensingEnabledRequested,
)
from openedx_filters.tooling import OpenEdxPublicFilter


class TestCourseLicensingEnabledRequested(unittest.TestCase):
    """
    Test class to verify standard behavior of the filters located in license_enforcement.

    - CourseLicensingEnabledRequested
    """

    def test_filter_type(self):
        """Verify the filter type remains stable."""
        self.assertEqual(
            "org.openedx.learning.course_licensing.enabled.requested.v1",
            CourseLicensingEnabledRequested.filter_type,
        )

    def test_course_licensing_enabled_requested(self):
        """
        Test CourseLicensingEnabledRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter should return the 'enabled' value from the pipeline.
        """
        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={"enabled": True},
        ) as mock_run_pipeline:
            result = CourseLicensingEnabledRequested.run_filter(enabled=False)

            mock_run_pipeline.assert_called_once_with(enabled=False)
            self.assertTrue(result)

    def test_course_licensing_enabled_requested_missing_enabled(self):
        """
        Test CourseLicensingEnabledRequested filter behavior when 'enabled' is missing.

        Expected behavior:
            - The filter should return the default 'enabled' value passed to run_filter.
        """
        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={},
        ) as mock_run_pipeline:
            result = CourseLicensingEnabledRequested.run_filter(enabled=True)

            mock_run_pipeline.assert_called_once_with(enabled=True)
            self.assertTrue(result)


class TestCcxEnrollmentLicenseEnforcementRequested(unittest.TestCase):
    """
    Test class to verify standard behavior of the filters located in license_enforcement.

    - CcxEnrollmentLicenseEnforcementRequested
    """

    def test_filter_type(self):
        """Verify the filter type remains stable."""
        self.assertEqual(
            "org.openedx.learning.ccx.enrollment.license_enforcement.requested.v1",
            CcxEnrollmentLicenseEnforcementRequested.filter_type,
        )

    def test_ccx_enrollment_license_enforcement_requested(self):
        """
        Test CcxEnrollmentLicenseEnforcementRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter should return the 'allowed' value from the pipeline.
        """
        course_key = Mock()
        email = "learner@example.com"
        student = Mock()
        request = Mock()
        user = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={"allowed": False},
        ) as mock_run_pipeline:
            result = CcxEnrollmentLicenseEnforcementRequested.run_filter(
                course_key=course_key,
                email=email,
                student=student,
                request=request,
                user=user,
                allowed=True,
            )

            mock_run_pipeline.assert_called_once_with(
                course_key=course_key,
                email=email,
                student=student,
                request=request,
                user=user,
                allowed=True,
            )
            self.assertFalse(result)

    def test_ccx_enrollment_license_enforcement_requested_missing_allowed(self):
        """
        Test CcxEnrollmentLicenseEnforcementRequested filter behavior when 'allowed' is missing.

        Expected behavior:
            - The filter should return the default 'allowed' value passed to run_filter.
        """
        course_key = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={},
        ) as mock_run_pipeline:
            result = CcxEnrollmentLicenseEnforcementRequested.run_filter(
                course_key=course_key,
                allowed=False,
            )

            mock_run_pipeline.assert_called_once_with(
                course_key=course_key,
                email=None,
                student=None,
                request=None,
                user=None,
                allowed=False,
            )
            self.assertFalse(result)


class TestCcxLicensedStatusRequested(unittest.TestCase):
    """
    Test class to verify standard behavior of the filters located in license_enforcement.

    - CcxLicensedStatusRequested
    """

    def test_filter_type(self):
        """Verify the filter type remains stable."""
        self.assertEqual(
            "org.openedx.learning.ccx.licensed_status.requested.v1",
            CcxLicensedStatusRequested.filter_type,
        )

    def test_ccx_licensed_status_requested(self):
        """
        Test CcxLicensedStatusRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter should return the 'licensed' value from the pipeline.
        """
        course_id = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={"licensed": True},
        ) as mock_run_pipeline:
            result = CcxLicensedStatusRequested.run_filter(course_id=course_id, licensed=False)

            mock_run_pipeline.assert_called_once_with(course_id=course_id, licensed=False)
            self.assertTrue(result)

    def test_ccx_licensed_status_requested_missing_licensed(self):
        """
        Test CcxLicensedStatusRequested filter behavior when 'licensed' is missing.

        Expected behavior:
            - The filter should return the default 'licensed' value passed to run_filter.
        """
        course_id = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={},
        ) as mock_run_pipeline:
            result = CcxLicensedStatusRequested.run_filter(course_id=course_id, licensed=True)

            mock_run_pipeline.assert_called_once_with(course_id=course_id, licensed=True)
            self.assertTrue(result)


class TestCcxCoachTabAccessRequested(unittest.TestCase):
    """
    Test class to verify standard behavior of the filters located in license_enforcement.

    - CcxCoachTabAccessRequested
    """

    def test_filter_type(self):
        """Verify the filter type remains stable."""
        self.assertEqual(
            "org.openedx.learning.ccx.coach_tab.access.requested.v1",
            CcxCoachTabAccessRequested.filter_type,
        )

    def test_ccx_coach_tab_access_requested(self):
        """
        Test CcxCoachTabAccessRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter should return the 'allowed' value from the pipeline.
        """
        user = Mock()
        ccx_id = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={"allowed": True},
        ) as mock_run_pipeline:
            result = CcxCoachTabAccessRequested.run_filter(user=user, ccx_id=ccx_id, allowed=False)

            mock_run_pipeline.assert_called_once_with(user=user, ccx_id=ccx_id, allowed=False)
            self.assertTrue(result)

    def test_ccx_coach_tab_access_requested_missing_allowed(self):
        """
        Test CcxCoachTabAccessRequested filter behavior when 'allowed' is missing.

        Expected behavior:
            - The filter should return the default 'allowed' value passed to run_filter.
        """
        user = Mock()
        ccx_id = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={},
        ) as mock_run_pipeline:
            result = CcxCoachTabAccessRequested.run_filter(user=user, ccx_id=ccx_id, allowed=False)

            mock_run_pipeline.assert_called_once_with(user=user, ccx_id=ccx_id, allowed=False)
            self.assertFalse(result)


class TestCcxCreationPermissionRequested(unittest.TestCase):
    """
    Test class to verify standard behavior of the filters located in license_enforcement.

    - CcxCreationPermissionRequested
    """

    def test_filter_type(self):
        """Verify the filter type remains stable."""
        self.assertEqual(
            "org.openedx.learning.ccx.creation.permission.requested.v1",
            CcxCreationPermissionRequested.filter_type,
        )

    def test_ccx_creation_permission_requested(self):
        """
        Test CcxCreationPermissionRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter should return the 'allowed' value from the pipeline.
        """
        user = Mock()
        master_course = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={"allowed": False},
        ) as mock_run_pipeline:
            result = CcxCreationPermissionRequested.run_filter(
                user=user,
                master_course=master_course,
                allowed=True,
            )

            mock_run_pipeline.assert_called_once_with(
                user=user,
                master_course=master_course,
                allowed=True,
            )
            self.assertFalse(result)

    def test_ccx_creation_permission_requested_missing_allowed(self):
        """
        Test CcxCreationPermissionRequested filter behavior when 'allowed' is missing.

        Expected behavior:
            - The filter should return the default 'allowed' value passed to run_filter.
        """
        user = Mock()
        master_course = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={},
        ) as mock_run_pipeline:
            result = CcxCreationPermissionRequested.run_filter(
                user=user,
                master_course=master_course,
                allowed=False,
            )

            mock_run_pipeline.assert_called_once_with(
                user=user,
                master_course=master_course,
                allowed=False,
            )
            self.assertFalse(result)


class TestCcxPendingEnrollmentsRequested(unittest.TestCase):
    """
    Test class to verify standard behavior of the filters located in license_enforcement.

    - CcxPendingEnrollmentsRequested
    """

    def test_filter_type(self):
        """Verify the filter type remains stable."""
        self.assertEqual(
            "org.openedx.learning.ccx.pending_enrollments.requested.v1",
            CcxPendingEnrollmentsRequested.filter_type,
        )

    def test_ccx_pending_enrollments_requested(self):
        """
        Test CcxPendingEnrollmentsRequested filter behavior under normal conditions.

        Expected behavior:
            - The filter should return the 'pending_enrollments' from the pipeline.
        """
        ccx_id = Mock()
        pending_enrollments = Mock()  # could be a QuerySet in real code

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={"pending_enrollments": pending_enrollments},
        ) as mock_run_pipeline:
            result = CcxPendingEnrollmentsRequested.run_filter(
                ccx_id=ccx_id,
                pending_enrollments=None,
            )

            mock_run_pipeline.assert_called_once_with(
                ccx_id=ccx_id,
                pending_enrollments=None,
            )
            self.assertEqual(pending_enrollments, result)

    def test_ccx_pending_enrollments_requested_missing_pending_enrollments(self):
        """
        Test CcxPendingEnrollmentsRequested filter behavior when 'pending_enrollments' is missing.

        Expected behavior:
            - The filter should return the default pending_enrollments passed to run_filter.
        """
        ccx_id = Mock()
        default_pending = Mock()

        with patch.object(
            OpenEdxPublicFilter,
            "run_pipeline",
            return_value={},
        ) as mock_run_pipeline:
            result = CcxPendingEnrollmentsRequested.run_filter(
                ccx_id=ccx_id,
                pending_enrollments=default_pending,
            )

            mock_run_pipeline.assert_called_once_with(
                ccx_id=ccx_id,
                pending_enrollments=default_pending,
            )
            self.assertEqual(default_pending, result)
