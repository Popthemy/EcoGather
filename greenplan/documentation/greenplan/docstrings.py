from drf_spectacular.utils import OpenApiExample

CLONE_TEMPLATE_DESCRIPTION= """
        The view retrieves the template using the ID, performs the cloning process,
        and returns the details of the cloned template. If any error occurs (e.g., invalid ID,
        missing custom fields), an appropriate error response is returned.

        Parameters:
            template_id (int): The ID of the template to be cloned, passed in the URL.

        Permission:
            - The view requires the user to be authenticated (`IsAuthenticated`).

"""

CLONE_TEMPLATE_400_BAD_REQUEST = OpenApiExample(
  "400_BAD_REQUEST",
  description='Cloning Failed',
  value={
    "data": {
                "status": "error",
                "message": " Templates cloned unsuccessfully",
                "data": "ID can't be negative or less than one or empty template"}
  },

  response_only=True,
  status_codes=['400']
)


CLONE_TEMPLATE_201_CREATED = OpenApiExample(
  "201_CREATED",
  description='Cloning Successful',
  value={
    "data": {
                "status": "success",
                "message": " Templates cloned successfully",
                "data": {'title':'the cloned template name + (cloned)',
                         'other':'other fields'} }
  },

  response_only=True,
  status_codes=['201']
)