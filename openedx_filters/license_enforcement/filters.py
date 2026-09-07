"""
Package where filters related to the ``license_enforcement`` architectural subdomain are implemented.
"""
from __future__ import annotations

from openedx_filters.tooling import OpenEdxPublicFilter


class CourseLicensingEnabledRequested(OpenEdxPublicFilter):
    """
    Filter used to determine whether course licensing is enabled for the current site.

    Purpose:
        This filter is triggered when platform code needs to know whether course
        licensing enforcement should be applied. It allows external plugins to
        compute this value, typically based on site configuration.

    Filter Type:
        org.openedx.learning.course_licensing.enabled.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: common/djangoapps/student (or CCX integration layer)
        - Function or Method: CcxCourseTab.is_enabled (and other licensing checks)
    """

    filter_type = "org.openedx.learning.course_licensing.enabled.requested.v1"

    @classmethod
    def run_filter(cls, *, enabled: bool = False) -> bool:
        """
        Process the configured pipeline steps to determine whether course licensing
        is enabled.

        Arguments:
            enabled (bool): Default value used when no pipeline step overrides it.

        Returns:
            bool:
                True if course licensing is enabled; False otherwise.
        """
        data = super().run_pipeline(enabled=enabled)
        return bool(data.get("enabled", enabled))


class CcxEnrollmentLicenseEnforcementRequested(OpenEdxPublicFilter):
    """
    Filter used to determine whether enrollment or invitation into a CCX is allowed
    under licensing rules.

    Purpose:
        This filter is triggered when an enrollment or invitation action is requested
        for a CCX. It allows external plugins to enforce seat limits, license status,
        institutional rules, and enrollment privileges.

    Filter Type:
        org.openedx.learning.ccx.enrollment.license_enforcement.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: enrollment / CCX invitation workflows
        - Function or Method: enrollment or invitation validation logic
    """

    filter_type = "org.openedx.learning.ccx.enrollment.license_enforcement.requested.v1"

    @classmethod
    def run_filter(
        cls,
        *,
        course_key,
        email=None,
        student=None,
        request=None,
        user=None,
        allowed: bool = True,
    ) -> bool:
        """
        Process the configured pipeline steps to determine whether the enrollment
        or invitation is allowed.

        Arguments:
            course_key (CCXLocator): Identifier of the CCX.
            email (str, optional): Email of the user to be invited.
            student (User, optional): Existing platform user to be enrolled.
            request (HttpRequest, optional): HTTP request initiating the action.
            user (User, optional): User who initiated the enrollment.
            allowed (bool): Initial allowance value, used for composition.

        Returns:
            bool:
                True if enrollment/invitation is allowed; False otherwise.
        """
        data = super().run_pipeline(
            course_key=course_key,
            email=email,
            student=student,
            request=request,
            user=user,
            allowed=allowed,
        )
        return bool(data.get("allowed", allowed))


class CcxLicensedStatusRequested(OpenEdxPublicFilter):
    """
    Filter used to determine whether a CCX is covered by an active license.

    Purpose:
        This filter is triggered when platform code needs to know whether a CCX
        is licensed and therefore subject to licensing-based restrictions.

    Filter Type:
        org.openedx.learning.ccx.licensed_status.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: CCX access and visibility checks
        - Function or Method: CCX authorization helpers
    """

    filter_type = "org.openedx.learning.ccx.licensed_status.requested.v1"

    @classmethod
    def run_filter(cls, *, course_id, licensed: bool = False) -> bool:
        """
        Process the configured pipeline steps to determine whether the CCX
        is licensed.

        Arguments:
            course_id (CCXLocator): Identifier of the CCX.
            licensed (bool): Default licensing status.

        Returns:
            bool:
                True if the CCX is licensed; False otherwise.
        """
        data = super().run_pipeline(course_id=course_id, licensed=licensed)
        return bool(data.get("licensed", licensed))


class CcxCoachTabAccessRequested(OpenEdxPublicFilter):
    """
    Filter used to determine whether a user is allowed to access the CCX coach tab.

    Purpose:
        This filter is triggered when rendering CCX navigation elements and allows
        external plugins to restrict access to the CCX coach dashboard based on
        licensing and role-based rules.

    Filter Type:
        org.openedx.learning.ccx.coach_tab.access.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: xmodule / course tabs
        - Function or Method: CcxCourseTab.is_enabled
    """

    filter_type = "org.openedx.learning.ccx.coach_tab.access.requested.v1"

    @classmethod
    def run_filter(cls, *, user, ccx_id, allowed: bool = False) -> bool:
        """
        Process the configured pipeline steps to determine whether the user
        is allowed to access the CCX coach tab.

        Arguments:
            user (User): Django user requesting access.
            ccx_id (CCXLocator): Identifier of the CCX.
            allowed (bool): Default access decision.

        Returns:
            bool:
                True if the user may access the CCX coach tab; False otherwise.
        """
        data = super().run_pipeline(user=user, ccx_id=ccx_id, allowed=allowed)
        return bool(data.get("allowed", allowed))


class CcxCreationPermissionRequested(OpenEdxPublicFilter):
    """
    Filter used to determine whether a user is allowed to create a CCX from a master course.

    Purpose:
        This filter is triggered during CCX creation workflows to allow external
        plugins to enforce licensing and institutional constraints on who may
        create CCXs.

    Filter Type:
        org.openedx.learning.ccx.creation.permission.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: CCX creation views / APIs
        - Function or Method: CCX creation validation logic
    """

    filter_type = "org.openedx.learning.ccx.creation.permission.requested.v1"

    @classmethod
    def run_filter(cls, *, user, master_course, allowed: bool = True) -> bool:
        """
        Process the configured pipeline steps to determine whether the user
        is allowed to create a CCX.

        Arguments:
            user (User): Django user requesting CCX creation.
            master_course (CourseLocator): Master course identifier.
            allowed (bool): Initial permission value.

        Returns:
            bool:
                True if the user may create a CCX; False otherwise.
        """
        data = super().run_pipeline(
            user=user,
            master_course=master_course,
            allowed=allowed,
        )
        return bool(data.get("allowed", allowed))


class CcxPendingEnrollmentsRequested(OpenEdxPublicFilter):
    """
    Filter used to retrieve pending enrollments for a licensed CCX.

    Purpose:
        This filter is triggered when platform code needs to retrieve the list
        of users pending enrollment into a CCX, allowing external plugins to
        provide or modify the data source.

    Filter Type:
        org.openedx.learning.ccx.pending_enrollments.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: CCX administration views
        - Function or Method: pending enrollment retrieval logic
    """

    filter_type = "org.openedx.learning.ccx.pending_enrollments.requested.v1"

    @classmethod
    def run_filter(cls, *, ccx_id, pending_enrollments=None):
        """
        Process the configured pipeline steps to retrieve pending enrollments.

        Arguments:
            ccx_id (CCXLocator): Identifier of the CCX.
            pending_enrollments (QuerySet | None): Default pending enrollments.

        Returns:
            QuerySet:
                A queryset (or iterable) of pending enrollments.
        """
        data = super().run_pipeline(
            ccx_id=ccx_id,
            pending_enrollments=pending_enrollments,
        )
        return data.get("pending_enrollments", pending_enrollments)


class PreBadgeIssuanceFilter(OpenEdxPublicFilter):
    """
    Filter used to determine if a badge should be issued.

    Purpose:
        Triggered before issuing a Credly badge, allows plugins to intercept
        and determine whether the badge should be issued based on custom logic.

    Filter Type:
        org.openedx.learning.badges.pre_badge_issuance.v1

    Trigger:
        - Repository: Pearson-Advance/credentials
        - Path: credentials/apps/badges/signals/handlers.py
        - Function or Method: handle_badge_completion
    """

    filter_type = "org.openedx.learning.badges.pre_badge_issuance.v1"

    @classmethod
    def run_filter(cls, username, badge_template_id, course_key, **kwargs):
        """
        Process badge issuance decision through the pipeline.

        Arguments:
            username (str): Username of the user
            badge_template_id (str): ID of the badge template
            course_key (str): Course key where the requirement was fulfilled

        Returns:
            dict: {'allow': bool, 'username': str, 'badge_template_id': str, 'course_key': str}
        """
        data = super().run_pipeline(
            username=username,
            badge_template_id=badge_template_id,
            course_key=course_key,
        )
        return data
