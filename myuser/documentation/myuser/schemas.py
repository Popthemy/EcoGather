from drf_spectacular.utils import extend_schema,extend_schema_view
from drf_spectacular.types import OpenApiTypes
from myuser.serializers import UserSerializer,LoginSerializer,LogoutSerializer
from myuser.documentation.myuser.docstrings import REGISTER_USER_DESCRIPTION,REGISTER_USER_BAD_REQUEST,REGISTER_USER_CREATED,LOGIN_VIEW_DESCRIPTION, \
  LOGIN_USER_200_OK,LOGIN_USER_401_UNAUTHORIZED,LOGOUT_USER_DESCRIPTION,LOGOUT_USER_200_OK,LOGOUT_USER_400_BAD_REQUEST, TOKEN_REFRESH_DESCRIPTION,TOKEN_REFRESH_200_OK,TOKEN_REFRESH_400_BAD_REQUEST



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


logout_user_doc =extend_schema(
  methods=['POST'],
  summary='User logout endpoint.',
  description=LOGOUT_USER_DESCRIPTION,
  request=LogoutSerializer,
  responses={
    200:OpenApiTypes.OBJECT,
    400:OpenApiTypes.OBJECT
  },
  examples=[LOGOUT_USER_200_OK,LOGOUT_USER_400_BAD_REQUEST],
  tags=['Authentication']

)


refresh_token_doc = extend_schema_view(
  post= extend_schema(
  methods=['POST'],
  summary='Token refresh endpoint.',
  description=TOKEN_REFRESH_DESCRIPTION,
  request=LogoutSerializer,
  responses={
    200:OpenApiTypes.OBJECT,
    400:OpenApiTypes.OBJECT
  },
  examples=[TOKEN_REFRESH_200_OK,TOKEN_REFRESH_400_BAD_REQUEST],
  tags=['Token']
)
)