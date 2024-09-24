from uuid import uuid4
from django.contrib.auth import get_user_model
from greenplan.models import Event,Organizer, Template
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
# Generate sample seed data

User = get_user_model()
# User = Users.objects.all()
organizer_queryset = Organizer.objects.select_related('user')

Events = Event.objects.all()
Bulletin = Template.objects.all()

user_seed_data = [
    {
        "id": uuid4(),
        "email": "bayo.adesina@example.com",
        "first_name": "Bayo",
        "last_name": "Adesina",
        "password": make_password("password123"),
        "date_joined": datetime.now(),
    },
    {
        "id": uuid4(),
        "email": "amina.muhammad@example.com",
        "first_name": "Amina",
        "last_name": "Muhammad",
        "password": make_password("password123"),
        "date_joined": datetime.now(),
    },
    {
        "id": uuid4(),
        "email": "john.ekene@example.com",
        "first_name": "John",
        "last_name": "Ekene",
        "password": make_password("password123"),
        "date_joined": datetime.now(),
    },
    {
        "id": uuid4(),
        "email": "fatima.kane@example.com",
        "first_name": "Fatima",
        "last_name": "Kane",
        "password": make_password("password123"),
        "date_joined": datetime.now(),
    },
    {
        "id": uuid4(),
        "email": "kwame.owusu@example.com",
        "first_name": "Kwame",
        "last_name": "Owusu",
        "password": make_password("password123"),
        "date_joined": datetime.now(),
    },
    {
        "id": uuid4(),
        "email": "isaac@example.com",
        "first_name": "Isaac",
        "last_name": "Eli",
        "password": make_password("password123"),
        "date_joined": datetime.now(),
    }

]


program_seed_data = [
  {'title': 'Conference'},
  {'title': 'Summit'},
  {'title': 'Workshop'}
]


organizer_seed_data = [
  
    {   "user": User.objects.get(email=user_seed_data[0]['email']),
        "username": 'Bayo001',
        "email": "bayo.adesina@example.com",
        "first_name": "Bayo",
        "last_name": "Adesina",
        "phone_number":'000'
    },
    {
        "user": User.objects.get(email=user_seed_data[1]['email']),
        "username":'Amina001',
        "email": "amina.muhammad@example.com",
        "first_name": "Amina",
        "last_name": "Muhammad",
        "phone_number": "2092123"
    },
    {
        "user": User.objects.get(email=user_seed_data[2]['email']),
        'username': 'john001',
        "email" : "john.ekene@example.com",
        "first_name": "John",
        "last_name": "Ekene",
        "phone_number": "i092u81203"
    },
    {
        "user": User.objects.get(email=user_seed_data[3]['email']),
        'username':'fatima001',
        "email": "fatima.kane@example.com",
        "first_name": "Fatima",
        "last_name": "Kane",
        "phone_number": "2902901203"
    },
    {
        "user": User.objects.get(email=user_seed_data[4]['email']),
        "username": 'Kwame001',
        "email" : "kwame.owusu@example.com",
        "first_name": "Kwame",
        "last_name": "Owusu",
        "phone_number": "2000901203"
    },
    {
        "user": User.objects.get(email=user_seed_data[5]['email']),
        "email": "isaac@example.com",
        "first_name": "Isaac",
        "last_name": "Eli",
        "phone_number": "200000903"
    }

]



event_seed_data = [
    {
        "code": "DEVFEST2024",
        "title": "African Developer Tech Summit",
        "venue": 'Nairaobi',
        "city_or_state": "Nairobi, Kenya",
        "start_datetime": datetime.now() + timedelta(days=1),
        "end_datetime": datetime.now() + timedelta(days=1, hours=3),
        "organizer": organizer_queryset.get(email=user_seed_data[0]['email']),
        "slug": "african-developer-tech-summit-2024"
    },
    {
        "code": "FINA2025",
        "title": "Pan-African Financial Summit",
        "venue": 'Johannesburg',
        "city_or_state": "Johannesburg, South Africa",
        "start_datetime": datetime.now() + timedelta(days=30),
        "end_datetime": datetime.now() + timedelta(days=35),
        "organizer": organizer_queryset.get(email=user_seed_data[1]['email']),
    },
    {
        "code": "AGRI2024",
        "title": "African Agricultural Innovation Expo",
        "venue": 'lauxer',
        "city_or_state": "Accra, Ghana",
        "start_datetime": datetime.now() + timedelta(days=20),
        "end_datetime": datetime.now() + timedelta(days=25),
        "organizer": organizer_queryset.get(email=user_seed_data[1]['email']),
    },
    {
        "code": "LAGEDU2024",
        "title": "African Academic Summit 2024",
        "venue": 'UNILAG',
        "city_or_state": "Lagos, Nigeria",
        "start_datetime": datetime.now(),
        "end_datetime": datetime.now() + timedelta(hours=4),
        "organizer": organizer_queryset.get(email=user_seed_data[3]['email']),
        "slug": "african-lagos-academic-summit-2024"
    },
    {
        "code": "FINTECH2024",
        "title": "African Fintech Conference 2024",
        "venue": 'University of Ibadan',
        "city_or_state": "Oyo, Nigeria",
        "start_datetime": datetime.now() + timedelta(days=1),
        "end_datetime": datetime.now() + timedelta(days=1, hours=3),
        "organizer": organizer_queryset.get(email=user_seed_data[4]['email']),
        "slug": "african-fintech-conference-2024"
    },
    {
        "code": "AGRICON2024",
        "title": "Agricultural Innovations Summit",
        "venue": 'University of Nairaobi',
        "city_or_state":"Nairobi, Kenya",
        "start_datetime": datetime.now() + timedelta(days=2),
        "end_datetime": datetime.now() + timedelta(days=2, hours=5),
        "organizer": organizer_queryset.get(email=user_seed_data[4]['email']),
        "slug": "agricultural-innovations-summit"
    },
    {
        "code": "YOUTHFORUM2024",
        "title": "African Youth Forum 2024",
        "venue": 'University of South Africa',
        "city_or_state":"Johannesburg, South Africa",
        "start_datetime": datetime.now() + timedelta(days=3),
        "end_datetime": datetime.now() + timedelta(days=3, hours=4),
        "organizer": organizer_queryset.get(email=user_seed_data[3]['email']),
        "slug": "african-youth-forum-2024"
    },
    {
        "code": "GOOGLEDEV2024",
        "title": "Google Developers Summit Africa 2024",
        "venue": 'Lanscape House of Africa',
        "city_or_state":"Cape Town, South Africa",
        "start_datetime": datetime.now() + timedelta(days=4),
        "end_datetime": datetime.now() + timedelta(days=4, hours=6),
        "organizer": organizer_queryset.get(email=user_seed_data[2]['email']),
        "slug": "google-developers-summit-africa"
    }
]


template_seed_data = [

    {
        "code": "BUL001",
        "title": "Standard Event Bulletin",
        "event_name": Events.get(code=event_seed_data[4]['code']),
        "description": "A general-purpose bulletin template for events.",
    },
    {
        "code": "BUL002",
        "title": "Academic Conference Bulletin",
        "event_name": Events.get(code=event_seed_data[3]['code']),

        "description": "A template specifically designed for academic conferences.",
    },
    {
        "code": "BUL003",
        "title": "Financial Summit Bulletin",
        "event_name": Events.get(code=event_seed_data[1]['code']),

        "description": "A template tailored for financial summits.",
    },

    {
        "code": "BULLETIN-ACADA",
       "title": "Academic Summit Bulletin",
        "event_name": Events.get(code=event_seed_data[3]['code']),  # Assume this refers to the first event "African Academic Summit 2024"

        "description": "The official bulletin for African Academic Summit 2024."
    },
    {
        "code": "BULLETIN-FINTECH",
        "title": "Fintech Conference Bulletin",
        "event_name":Events.get(code=event_seed_data[4]['code']) ,  # "African Fintech Conference 2024"
        "description": "The official bulletin for African Fintech Conference 2024."
    },
    {
        "code": "BULLETIN-AGRICON",
        "title": "Agricultural Summit Bulletin",
        "event_name":Events.get(code=event_seed_data[4]['code']),  # "Agricultural Innovations Summit"
        "slug": "agricultural-summit-bulletin",
        "description": "The official bulletin for Agricultural Innovations Summit."
    }
]


custom_field_seed_data = [
  
    {
        # Assume this refers to the first bulletin "Academic Summit Bulletin"
        "template": Bulletin.get(title=template_seed_data[1]['title']) ,
        "label": "Welcome Address",
        "content": "Welcome speech by the event host.",
        "start_time": "09:00",
        "end_time": "09:30"
    },
    {
        # Assume this refers to the second bulletin "Fintech Conference Bulletin"
        "template": Bulletin.get(title=template_seed_data[2]['title']),
        "label": "Keynote Address",
        "content": "Keynote speech by industry expert.",
        "start_time": "10:00",
        "end_time": "10:45"
    },
     {
        # Assume this refers to the first bulletin "Academic Summit Bulletin"
        "template": Bulletin.get(title=template_seed_data[2]['title']) ,
        "label": "Welcome Address",
        "content": "Welcome speech by the event host.",
        "start_time": "09:00",
        "end_time": "09:30"
    },
    {
        # Assume this refers to the second bulletin "Fintech Conference Bulletin"
        "template": Bulletin.get(title=template_seed_data[1]['title']) ,
        "label": "Keynote Address",
        "content": "Keynote speech by industry expert.",
        "start_time": "10:00",
        "end_time": "10:45"
    },
     {
        # Assume this refers to the first bulletin "Academic Summit Bulletin"
        "template": Bulletin.get(title=template_seed_data[3]['title']) ,
        "label": "Welcome Address",
        "content": "Welcome speech by the event host.",
        "start_time": "09:00",
        "end_time": "09:30"
    },
    {
        # Assume this refers to the second bulletin "Fintech Conference Bulletin"
        "template": Bulletin.get(title=template_seed_data[3]['title']),
        "label": "Keynote Address",
        "content": "Keynote speech by industry expert.",
        "start_time": "10:00",
        "end_time": "10:45"
    },
     {
        # Assume this refers to the first bulletin "Academic Summit Bulletin"
        "template":Bulletin.get(title=template_seed_data[4]['title']),
        "label": "Welcome Address",
        "content": "Welcome speech by the event host.",
        "start_time": "09:00",
        "end_time": "09:30"
    },
    {
        # Assume this refers to the second bulletin "Fintech Conference Bulletin"
        "template": Bulletin.get(title=template_seed_data[4]['title']),
        "label": "Keynote Address",
        "content": "Keynote speech by industry expert.",
        "start_time": "10:00",
        "end_time": "10:45"
    },
     {
        # Assume this refers to the first bulletin "Academic Summit Bulletin"
        "template":Bulletin.get(title=template_seed_data[1]['title']),
        "label": "Welcome Address",
        "content": "Welcome speech by the event host.",
        "start_time": "09:00",
        "end_time": "09:30"
    },
    {
        # Assume this refers to the second bulletin "Fintech Conference Bulletin"
        "template": Bulletin.get(title=template_seed_data[1]['title']),
        "label": "Keynote Address",
        "content": "Keynote speech by industry expert.",
        "start_time": "10:00",
        "end_time": "10:45"
    },
    {
        # Assume this refers to the third bulletin "Agricultural Summit Bulletin"
        "template":Bulletin.get(title=template_seed_data[3]['title']),
        "label": "Panel Discussion",
        "content": "Discussion on latest agricultural technologies.",
        "start_time": "11:00",
        "end_time": "12:00"
    },
    {
        "template":Bulletin.get(title=template_seed_data[3]['title']),
        "label": "Keynote Speaker",
        "content": "Dr. Amina J. Mohammed",
    },
    {
        "template": Bulletin.get(title=template_seed_data[1]['title']),
        "label": "Session Topics",
        "content": "Sustainable Development, Gender Equality, Technology in Education",
    },
    {
        "template":Bulletin.get(title=template_seed_data[2]['title']),
        "label": "Featured Speakers",
        "content": "Ngozi Okonjo-Iweala, Akinwumi Adesina",
    },
]



sponsors_seed_data = [
    {
        "name": "Tech Innovations Ltd.",
        "description": "Leading provider of innovative tech solutions and services.",
        "email": "contact@techinnovations.com"
    },
    {
        "name": "Green Earth Organization",
        "description": "Committed to promoting sustainability and environmental stewardship.",
        "email": "info@greenearth.org"
    },
    {
        "name": "HealthFirst Inc.",
        "description": "A healthcare company focused on improving patient care and outcomes.",
        "email": "support@healthfirst.com"
    },
    {
        "name": "Culinary Creations",
        "description": "Delivering gourmet meals with a focus on local ingredients.",
        "email": "hello@culinarycreations.com"
    },
    {
        "name": "Adventure Outdoors",
        "description": "Your partner for unforgettable outdoor adventures and experiences.",
        "email": "info@adventureoutdoors.com"
    }
]
