"""
Package where filters related to the ``authentication`` architectural subdomain are implemented.
"""
from typing import Any, Dict, Tuple

from openedx_filters.tooling import OpenEdxPublicFilter


class SessionJWTCreationRequested(OpenEdxPublicFilter):
    """
    Filter used to update the JWT token's payload by adding extra data when its creation is requested.

    Purpose:
        This filter is triggered when the JWT token's creation is requested, and grants the possibility to add new
        additional data to it.

    Filter Type:
        org.openedx.authentication.session.jwt.creation.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/oauth_dispatch/jwt.py
        - Function or Method: _create_jwt
    """

    filter_type = "org.openedx.authentication.session.jwt.creation.requested.v1"

    @classmethod
    def run_filter(cls, payload: Dict[str, Any], user: Any) -> Tuple[Dict[str, Any], Any]:
        """
        Process the inputs using the configured pipeline steps to modify the payload of the JWT token.

        Arguments:
            payload (str): the payload of JWT token to be modified.
            user (User): Django User related to the JWT token.

        Returns:
            tuple[dict, User]:
                - dict: the modified payload of the JWT token.
                - User: the user of the JWT token.
        """
        data = super().run_pipeline(payload=payload, user=user)
        return data.get('payload', {}), data.get('user')


class StudentLogoutRequested(OpenEdxPublicFilter):
    """
    Filter used to perform custom actions when a user logs out of the LMS.

    Purpose:
        This filter is triggered to propagate logout to external SSO/IdP, revoke 3rd-party sessions
        and audit/telemetry side effects.

    Filter Type:
        org.openedx.learning.student.logout.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_authn/views/logout.py
        - Function or Method: LogoutView.dispatch
    """

    filter_type = "org.openedx.learning.student.logout.requested.v1"

    @classmethod
    def run_filter(cls, request):
        """
        Execute the configured pipeline.

        Args:
            request: Django HttpRequest for the logout request.

        Returns:
            The (possibly modified) request. For most use-cases this is unchanged.
        """
        data: dict[str, Any] | Any = super().run_pipeline(request=request)

        if isinstance(data, dict):
            return data.get("request", request)

        return request


class StudentRegistrationFormTermsOfServiceLabelRequested(OpenEdxPublicFilter):
    """
    Filter used to modify the Terms of Service field label in the registration form description.

    Purpose:
        This filter allows extensions or plugins to customize or replace the
        Terms of Service label displayed on the registration form, for example
        to inject institution-specific wording, branding, or legal language
        based on the platform or site context.

    Filter Type:
        org.openedx.learning.student.registration.form.terms_of_service.label.requested.v1

    Trigger:
        - Repository: openedx/edx-platform
        - Path: openedx/core/djangoapps/user_authn/views/register.py
        - Function or Method: _add_terms_of_service_field
    """

    filter_type = "org.openedx.learning.student.registration.form.terms_of_service.label.requested.v1"

    @classmethod
    def run_filter(cls, label: Any, platform_name: str) -> Any:
        """
        Run the filter pipeline to optionally override the Terms of Service label
        shown on the registration form.

        Args:
            label (Any): Default Terms of Service label.
            platform_name (str): Current platform or site identifier.

        Returns:
            Any: The overridden label if provided by a filter, otherwise the original.
        """
        data: Any = super().run_pipeline(label=label, platform_name=platform_name)

        if isinstance(data, dict):
            return data.get("label", label)

        return label
