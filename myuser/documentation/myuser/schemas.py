from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from myuser.serializers import UserSerializer,LoginSerializer
from myuser.documentation.myuser.docstrings import REGISTER_USER_DESCRIPTION,REGISTER_USER_BAD_REQUEST,REGISTER_USER_CREATED,LOGIN_VIEW_DESCRIPTION, \
  LOGIN_USER_200_OK,LOGIN_USER_401_UNAUTHORIZED



register_user_doc = extend_schema(
  methods=['POST'],
  summary='User registration endpoint.',
  description=REGISTER_USER_DESCRIPTION,
  request=UserSerializer,
  responses={
  201: OpenApiTypes.OBJECT,
  400: OpenApiTypes.OBJECT,
  },
  examples=[REGISTER_USER_BAD_REQUEST,REGISTER_USER_CREATED] ,
  tags=['Authentication']
)


login_user_doc = extend_schema(
  methods=['POST'],
  summary='User login endpoint.',
  description= LOGIN_VIEW_DESCRIPTION,
  request=LoginSerializer,
  responses={
    200:OpenApiTypes.OBJECT,
    401:OpenApiTypes.OBJECT
  },
  examples=[LOGIN_USER_200_OK,LOGIN_USER_401_UNAUTHORIZED],
  tags=['Authentication']

)
