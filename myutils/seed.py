import uuid
from datetime import datetime, timedelta
from greenplan.models import BulletinTemplate
# Generate sample seed data

event_seed_data = [
    {
        "code": "DEVFEST2024",
        "title": "African Tech Summit",
        "location": "Nairobi, Kenya",
        "start_time": datetime.now() + timedelta(days=1),
        "end_time": datetime.now() + timedelta(days=1, hours=3),
        "organizer": uuid.uuid4(),
        "slug": "african-tech-summit-2024"
    },
    {
        "code": "FINA2025",
        "title": "Pan-African Financial Summit",
        "location": "Johannesburg, South Africa",
        "start_time": datetime.now() + timedelta(days=30),
        "end_time": datetime.now() + timedelta(days=35),
        "organizer": uuid.uuid4(),
    },
    {
        "code": "AGRI2024",
        "title": "African Agricultural Innovation Expo",
        "location": "Accra, Ghana",
        "start_time": datetime.now() + timedelta(days=20),
        "end_time": datetime.now() + timedelta(days=25),
        "organizer": uuid.uuid4(),  # Assuming you have a User model with ID 3
    },
    {
        "code": "HALE2024",
        "title": "African Academic Summit 2024",
        "location": "Lagos, Nigeria",
        "start_time": datetime.now(),
        "end_time": datetime.now() + timedelta(hours=4),
        "organizer": uuid.uuid4(),
        "slug": "african-academic-summit-2024"
    },
    {
        "code": "FINTECH2024",
        "title": "African Fintech Conference 2024",
        "location": "Accra, Ghana",
        "start_time": datetime.now() + timedelta(days=1),
        "end_time": datetime.now() + timedelta(days=1, hours=3),
        "organizer": uuid.uuid4(),
        "slug": "african-fintech-conference-2024"
    },
    {
        "code": "AGRICON2024",
        "title": "Agricultural Innovations Summit",
        "location": "Nairobi, Kenya",
        "start_time": datetime.now() + timedelta(days=2),
        "end_time": datetime.now() + timedelta(days=2, hours=5),
        "organizer": uuid.uuid4(),
        "slug": "agricultural-innovations-summit"
    },
    {
        "code": "YOUTHFORUM2024",
        "title": "African Youth Forum 2024",
        "location": "Johannesburg, South Africa",
        "start_time": datetime.now() + timedelta(days=3),
        "end_time": datetime.now() + timedelta(days=3, hours=4),
        "organizer": uuid.uuid4(),
        "slug": "african-youth-forum-2024"
    },
    {
        "code": "GOOGLEDEV2024",
        "title": "Google Developers Summit Africa 2024",
        "location": "Cape Town, South Africa",
        "start_time": datetime.now() + timedelta(days=4),
        "end_time": datetime.now() + timedelta(days=4, hours=6),
        "organizer": uuid.uuid4(),
        "slug": "google-developers-summit-africa"
    }
]


bulletin_template_seed_data = [
  
  {
        "code": "BUL001",
        "title": "Standard Event Bulletin",
        "description": "A general-purpose bulletin template for events.",
    },
    {
        "code": "BUL002",
        "title": "Academic Conference Bulletin",
        "description": "A template specifically designed for academic conferences.",
    },
    {
        "code": "BUL003",
        "title": "Financial Summit Bulletin",
        "description": "A template tailored for financial summits.",
    },

    {
        "code": "BULLETIN-ACADA",
        "title": "Academic Summit Bulletin",
        "event_name": 1,  # Assume this refers to the first event "African Academic Summit 2024"
        "slug": "academic-summit-bulletin",
        "description": "The official bulletin for African Academic Summit 2024."
    },
    {
        "code": "BULLETIN-FINTECH",
        "title": "Fintech Conference Bulletin",
        "event_name": 2,  # "African Fintech Conference 2024"
        "slug": "fintech-conference-bulletin",
        "description": "The official bulletin for African Fintech Conference 2024."
    },
    {
        "code": "BULLETIN-AGRICON",
        "title": "Agricultural Summit Bulletin",
        "event_name": 3,  # "Agricultural Innovations Summit"
        "slug": "agricultural-summit-bulletin",
        "description": "The official bulletin for Agricultural Innovations Summit."
    }
]

custom_field_seed_data = [
    {
        # Assume this refers to the first bulletin "Academic Summit Bulletin"
        "bulletin_template": 1,
        "label": "Welcome Address",
        "content": "Welcome speech by the event host.",
        "start_time": "09:00",
        "end_time": "09:30"
    },
    {
        # Assume this refers to the second bulletin "Fintech Conference Bulletin"
        "bulletin_template": 2,
        "label": "Keynote Address",
        "content": "Keynote speech by industry expert.",
        "start_time": "10:00",
        "end_time": "10:45"
    },
    {
        # Assume this refers to the third bulletin "Agricultural Summit Bulletin"
        "bulletin_template": 3,
        "label": "Panel Discussion",
        "content": "Discussion on latest agricultural technologies.",
        "start_time": "11:00",
        "end_time": "12:00"
    },
    {
        "bulletin_template": 4,
        "label": "Keynote Speaker",
        "content": "Dr. Amina J. Mohammed",
    },
    {
        "bulletin_template": 5,
        "label": "Session Topics",
        "content": "Sustainable Development, Gender Equality, Technology in Education",
    },
    {
        "bulletin_template":6,
        "label": "Featured Speakers",
        "content": "Ngozi Okonjo-Iweala, Akinwumi Adesina",
    },
]

# event_seed_data, bulletin_template_seed_data, custom_field_seed_data
