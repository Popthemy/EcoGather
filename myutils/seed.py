from uuid import uuid4
from django.contrib.auth import get_user_model
from greenplan.models import Event, BulletinTemplate
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
# Generate sample seed data

Users = get_user_model()
User = Users.objects.all()

Events = Event.objects.all()
Bulletin = BulletinTemplate.objects.all()


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


event_seed_data = [
    {
        "code": "DEVFEST2024",
        "title": "African Tech Summit",
        "location": "Nairobi, Kenya",
        "start_time": datetime.now() + timedelta(days=1),
        "end_time": datetime.now() + timedelta(days=1, hours=3),
        "organizer": User.get(email=user_seed_data[0]['email']),
        "slug": "african-tech-summit-2024"
    },
    {
        "code": "FINA2025",
        "title": "Pan-African Financial Summit",
        "location": "Johannesburg, South Africa",
        "start_time": datetime.now() + timedelta(days=30),
        "end_time": datetime.now() + timedelta(days=35),
        "organizer": User.get(email=user_seed_data[2]['email']),
    },
    {
        "code": "AGRI2024",
        "title": "African Agricultural Innovation Expo",
        "location": "Accra, Ghana",
        "start_time": datetime.now() + timedelta(days=20),
        "end_time": datetime.now() + timedelta(days=25),
        # Assuming you have a User model with ID 3
        "organizer": User.get(email=user_seed_data[1]['email']),
    },
    {
        "code": "HALE2024",
        "title": "African Academic Summit 2024",
        "location": "Lagos, Nigeria",
        "start_time": datetime.now(),
        "end_time": datetime.now() + timedelta(hours=4),
        "organizer": User.get(email=user_seed_data[3]['email']),
        "slug": "african-academic-summit-2024"
    },
    {
        "code": "FINTECH2024",
        "title": "African Fintech Conference 2024",
        "location": "Accra, Ghana",
        "start_time": datetime.now() + timedelta(days=1),
        "end_time": datetime.now() + timedelta(days=1, hours=3),
        "organizer":User.get(email=user_seed_data[4]['email']),
        "slug": "african-fintech-conference-2024"
    },
    {
        "code": "AGRICON2024",
        "title": "Agricultural Innovations Summit",
        "location": "Nairobi, Kenya",
        "start_time": datetime.now() + timedelta(days=2),
        "end_time": datetime.now() + timedelta(days=2, hours=5),
        "organizer": User.get(email=user_seed_data[4]['email']),
        "slug": "agricultural-innovations-summit"
    },
    {
        "code": "YOUTHFORUM2024",
        "title": "African Youth Forum 2024",
        "location": "Johannesburg, South Africa",
        "start_time": datetime.now() + timedelta(days=3),
        "end_time": datetime.now() + timedelta(days=3, hours=4),
        "organizer": User.get(email=user_seed_data[3]['email']),
        "slug": "african-youth-forum-2024"
    },
    {
        "code": "GOOGLEDEV2024",
        "title": "Google Developers Summit Africa 2024",
        "location": "Cape Town, South Africa",
        "start_time": datetime.now() + timedelta(days=4),
        "end_time": datetime.now() + timedelta(days=4, hours=6),
        "organizer":User.get(email=user_seed_data[2]['email']),
        "slug": "google-developers-summit-africa"
    }
]


bulletin_template_seed_data = [

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
        "bulletin_template": Bulletin.get(title=bulletin_template_seed_data[1]['title']) ,
        "label": "Welcome Address",
        "content": "Welcome speech by the event host.",
        "start_time": "09:00",
        "end_time": "09:30"
    },
    {
        # Assume this refers to the second bulletin "Fintech Conference Bulletin"
        "bulletin_template": Bulletin.get(title=bulletin_template_seed_data[2]['title']),
        "label": "Keynote Address",
        "content": "Keynote speech by industry expert.",
        "start_time": "10:00",
        "end_time": "10:45"
    },
     {
        # Assume this refers to the first bulletin "Academic Summit Bulletin"
        "bulletin_template": Bulletin.get(title=bulletin_template_seed_data[2]['title']) ,
        "label": "Welcome Address",
        "content": "Welcome speech by the event host.",
        "start_time": "09:00",
        "end_time": "09:30"
    },
    {
        # Assume this refers to the second bulletin "Fintech Conference Bulletin"
        "bulletin_template": Bulletin.get(title=bulletin_template_seed_data[1]['title']) ,
        "label": "Keynote Address",
        "content": "Keynote speech by industry expert.",
        "start_time": "10:00",
        "end_time": "10:45"
    },
     {
        # Assume this refers to the first bulletin "Academic Summit Bulletin"
        "bulletin_template": Bulletin.get(title=bulletin_template_seed_data[3]['title']) ,
        "label": "Welcome Address",
        "content": "Welcome speech by the event host.",
        "start_time": "09:00",
        "end_time": "09:30"
    },
    {
        # Assume this refers to the second bulletin "Fintech Conference Bulletin"
        "bulletin_template": Bulletin.get(title=bulletin_template_seed_data[3]['title']),
        "label": "Keynote Address",
        "content": "Keynote speech by industry expert.",
        "start_time": "10:00",
        "end_time": "10:45"
    },
     {
        # Assume this refers to the first bulletin "Academic Summit Bulletin"
        "bulletin_template":Bulletin.get(title=bulletin_template_seed_data[4]['title']),
        "label": "Welcome Address",
        "content": "Welcome speech by the event host.",
        "start_time": "09:00",
        "end_time": "09:30"
    },
    {
        # Assume this refers to the second bulletin "Fintech Conference Bulletin"
        "bulletin_template": Bulletin.get(title=bulletin_template_seed_data[4]['title']),
        "label": "Keynote Address",
        "content": "Keynote speech by industry expert.",
        "start_time": "10:00",
        "end_time": "10:45"
    },
     {
        # Assume this refers to the first bulletin "Academic Summit Bulletin"
        "bulletin_template":Bulletin.get(title=bulletin_template_seed_data[5]['title']),
        "label": "Welcome Address",
        "content": "Welcome speech by the event host.",
        "start_time": "09:00",
        "end_time": "09:30"
    },
    {
        # Assume this refers to the second bulletin "Fintech Conference Bulletin"
        "bulletin_template": Bulletin.get(title=bulletin_template_seed_data[5]['title']),
        "label": "Keynote Address",
        "content": "Keynote speech by industry expert.",
        "start_time": "10:00",
        "end_time": "10:45"
    },
    {
        # Assume this refers to the third bulletin "Agricultural Summit Bulletin"
        "bulletin_template":Bulletin.get(title=bulletin_template_seed_data[5]['title']),
        "label": "Panel Discussion",
        "content": "Discussion on latest agricultural technologies.",
        "start_time": "11:00",
        "end_time": "12:00"
    },
    {
        "bulletin_template":Bulletin.get(title=bulletin_template_seed_data[3]['title']),
        "label": "Keynote Speaker",
        "content": "Dr. Amina J. Mohammed",
    },
    {
        "bulletin_template": Bulletin.get(title=bulletin_template_seed_data[5]['title']),
        "label": "Session Topics",
        "content": "Sustainable Development, Gender Equality, Technology in Education",
    },
    {
        "bulletin_template":Bulletin.get(title=bulletin_template_seed_data[2]['title']),
        "label": "Featured Speakers",
        "content": "Ngozi Okonjo-Iweala, Akinwumi Adesina",
    },
]

