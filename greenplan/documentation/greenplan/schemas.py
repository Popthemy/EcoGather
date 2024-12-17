from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from greenplan.documentation.greenplan.docstrings import CLONE_TEMPLATE_DESCRIPTION, CLONE_TEMPLATE_400_BAD_REQUEST,CLONE_TEMPLATE_201_CREATED


clone_template_doc = extend_schema(
  methods=['GET'],
  summary= 'Clones a template based on the provided template ID in the URL.',
  description=CLONE_TEMPLATE_DESCRIPTION,
  responses={
    400:OpenApiTypes.OBJECT,
    201:OpenApiTypes.OBJECT
  },
  examples=[CLONE_TEMPLATE_400_BAD_REQUEST, CLONE_TEMPLATE_201_CREATED],
  tags =['Template']
)


"""
        
        Returns:
            Response: 
                - A successful response with status `201 Created` if the template is cloned.
                - A `400 Bad Request` response if the template ID is invalid or if an error occurs during cloning.
        """