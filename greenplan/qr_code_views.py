from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from qrcode_artistic import write_artistic
from PIL import Image
from io import BytesIO
import segno



@api_view(['GET'])
def generate_qr_code(request):
    link = str(request.GET.get('link', None))

    if not link:
        return Response({'error': 'No link! Try again'}, status=status.HTTP_400_BAD_REQUEST)

    # make qr code
    try:
      qr = segno.make(link)
    except Exception as e:
        return Response({'error': f'Error generating QR code: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    response = HttpResponse(content_type='image/png')
    qr.save(response, kind="png",scale=5)

    # set the status code
    response.status_code = status.HTTP_200_OK
    return response
