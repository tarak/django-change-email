.. _api-views:

Views
=====

All of the following documented views are:

* only accessible to logged in users.
* Class based generic views. These are further documented in the Django
  documentation.

.. automodule:: change_email.views

.. view:: EmailChangeConfirmView

``EmailChangeConfirmView``
--------------------------

.. autoclass:: change_email.views.EmailChangeConfirmView
   :members: object, template_name, dispatch, get_context_data, save
   :show-inheritance:

.. view:: EmailChangeCreateView

``EmailChangeCreateView``
-------------------------

.. autoclass:: change_email.views.EmailChangeCreateView
   :members: form_class, model, dispatch, form_valid
   :show-inheritance:

.. view:: EmailChangeDeleteView

``EmailChangeDeleteView``
-------------------------

.. autoclass:: change_email.views.EmailChangeDeleteView
   :members: model, dispatch, get_success_url
   :show-inheritance:

.. view:: EmailChangeDetailView

``EmailChangeDetailView``
-------------------------

.. autoclass:: change_email.views.EmailChangeDetailView
   :members: model, dispatch
   :show-inheritance:

.. view:: EmailChangeIndexView

``EmailChangeIndexView``
-------------------------

.. autoclass:: change_email.views.EmailChangeIndexView
   :members: permanent, dispatch, get_redirect_url
   :show-inheritance:
