.. _Existing Filters:

Filters
#######

This is the list of Open edX Filters found in this repository.

.. note::
    Filters can be created in other projects and plugins as well, but these default filters are guaranteed to exist.

Learning Subdomain
********************

.. automodule:: openedx_filters.learning.filters
   :members:

Learner dashboard course order
=============================

``LearnerDashboardCoursesRendered`` receives the complete ``serialized_courses``
list from ``LearnerDashboardSerializer.get_courses``. Each item is a serialized
course card. Unfulfilled entitlement cards have ``courseRun=None``.
The optional ``sort_by`` argument contains the API request's ``sort`` value.
It is ``None`` when the request has no sort parameter. Each pipeline step decides
which sort modes it supports.

To replace or reorder the list, a pipeline step returns
``{"serialized_courses": updated_cards}``. Configure the step under
``org.openedx.learning.home.courses.rendered.v1`` in ``OPEN_EDX_FILTERS_CONFIG``.
Without a configured pipeline, the filter returns the original list.

Course Authoring Subdomain
***************************

.. automodule:: openedx_filters.course_authoring.filters
   :members:

**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Reviewer                      |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-13    | Maria Grimaldi                |  Sumac         |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+
