-- Inserting Programs (10)
INSERT INTO myapp_program (title, featured_event) VALUES
('Technology', NULL),
('Business', NULL),
('Education', NULL),
('Health', NULL),
('Music', NULL),
('Art & Culture', NULL),
('Sports', NULL),
('Finance', NULL),
('Science', NULL),
('Entrepreneurship', NULL);


-- Inserting Events (20)
INSERT INTO myapp_event (code, title, description, program_id, venue, city, start_datetime, end_datetime, contact_email, contact_phone_number, organizer_id, slug, is_private, created_at, updated_at) VALUES
('ACADA2024', 'ACADA 2024 Summit', 'A summit for students', 1, 'The Great Hall, Lautech', 'Ogbomoso', '2024-03-15 09:00:00', '2024-03-15 17:00:00', 'contact@acada.com', '08012345678', 1, 'acada2024-summit', false, '2023-11-10 00:00:00', '2023-11-10 00:00:00'),
('BUS2024', 'Business Innovation Conference', 'Conference on business innovations', 2, 'Business Center, Lagos', 'Lagos', '2024-04-01 10:00:00', '2024-04-01 18:00:00', 'contact@businessconf.com', '08023456789', 2, 'business-innovation-2024', false, '2023-11-11 00:00:00', '2023-11-11 00:00:00'),
('EDUC2024', 'Global Education Expo', 'Educational expo and workshop', 3, 'Expo Center, Abuja', 'Abuja', '2024-05-05 09:00:00', '2024-05-05 16:00:00', 'contact@eduexpo.com', '08034567890', 3, 'global-education-expo', true, '2023-11-12 00:00:00', '2023-11-12 00:00:00'),
('HEALTH2024', 'Health and Wellness Expo', 'Wellness and health conference', 4, 'Health Hall, Ibadan', 'Ibadan', '2024-06-10 10:00:00', '2024-06-10 17:00:00', 'contact@healthexpo.com', '08045678901', 4, 'health-wellness-expo', false, '2023-11-13 00:00:00', '2023-11-13 00:00:00'),
('MUSIC2024', 'Nigerian Music Festival', 'Annual music festival featuring top artists', 5, 'Music Arena, Lagos', 'Lagos', '2024-07-01 15:00:00', '2024-07-01 23:00:00', 'contact@musicfest.com', '08056789012', 5, 'nigerian-music-fest-2024', false, '2023-11-14 00:00:00', '2023-11-14 00:00:00'),
('ART2024', 'National Art Exhibition', 'Exhibition of national artists', 6, 'Art Gallery, Abuja', 'Abuja', '2024-08-01 09:00:00', '2024-08-01 17:00:00', 'contact@artexpo.com', '08067890123', 6, 'national-art-exhibit', true, '2023-11-15 00:00:00', '2023-11-15 00:00:00'),
('SPORTS2024', 'Sports Meet 2024', 'Annual sports event for students', 7, 'Sports Complex, Enugu', 'Enugu', '2024-09-05 08:00:00', '2024-09-05 18:00:00', 'contact@sportsmeet.com', '08078901234', 7, 'sports-meet-2024', false, '2023-11-16 00:00:00', '2023-11-16 00:00:00'),
('FINANCE2024', 'Financial Freedom Summit', 'Summit for entrepreneurs and investors', 8, 'Finance Hall, Port Harcourt', 'Port Harcourt', '2024-10-10 09:00:00', '2024-10-10 16:00:00', 'contact@finfreedom.com', '08089012345', 8, 'financial-freedom-summit', true, '2023-11-17 00:00:00', '2023-11-17 00:00:00'),
('SCIENCE2024', 'Science and Innovation Forum', 'Forum on scientific innovations and discoveries', 9, 'Science Arena, Kano', 'Kano', '2024-11-12 10:00:00', '2024-11-12 18:00:00', 'contact@scienceforum.com', '08090123456', 9, 'science-innovation-forum', false, '2023-11-18 00:00:00', '2023-11-18 00:00:00'),
('ENTREPRENEUR2024', 'Entrepreneurship Summit', 'Summit focused on entrepreneurship', 10, 'Entrepreneur Hall, Lagos', 'Lagos', '2024-12-20 08:00:00', '2024-12-20 16:00:00', 'contact@entresummit.com', '08001234567', 10, 'entrepreneurship-summit', true, '2023-11-19 00:00:00', '2023-11-19 00:00:00');



-- Inserting Templates (3 to 5 for each event)
INSERT INTO myapp_template (owner_id, code, title, event_id, slug, description, created_at, updated_at) VALUES
(1, 'TEMPLATE1', 'Registration Template', 1, 'registration-template', 'Template for event registration.', '2023-11-01 00:00:00', '2023-11-01 00:00:00'),
(1, 'TEMPLATE2', 'Event Agenda Template', 1, 'event-agenda-template', 'Template for event agenda.', '2023-11-02 00:00:00', '2023-11-02 00:00:00'),
(2, 'TEMPLATE1', 'Business Plan Template', 2, 'business-plan-template', 'Template for business presentations.', '2023-11-03 00:00:00', '2023-11-03 00:00:00'),
(2, 'TEMPLATE2', 'Investor Pitch Template', 2, 'investor-pitch-template', 'Template for investor pitch presentations.', '2023-11-04 00:00:00', '2023-11-04 00:00:00'),
(3, 'TEMPLATE1', 'Education Expo Flyer', 3, 'education-expo-flyer', 'Template for the event flyer.', '2023-11-05 00:00:00', '2023-11-05 00:00:00');



-- Inserting Custom Fields (7 for each template)
INSERT INTO myapp_customfield (template_id, label, content, start_time, end_time) VALUES
(1, 'Welcome Speech', 'Speech by the event organizer', '09:00:00', '09:30:00'),
(1, 'Keynote Address', 'Keynote speech by the CEO', '09:30:00', '10:00:00'),
(2, 'Workshop on Business Strategy', 'Interactive workshop on strategy building', '10:00:00', '11:30:00'),
(2, 'Pitch Session', 'Investor pitch session for selected businesses', '12:00:00', '13:00:00'),
(3, 'Exhibitor Introduction', 'Introduction to the exhibitors at the event', '14:00:00', '14:30:00'),
(3, 'Closing Remarks', 'Closing remarks and thank you note', '17:00:00', '17:30:00');


-- Inserting Templates for more events (3 to 5 for each event)
INSERT INTO myapp_template (owner_id, code, title, event_id, slug, description, created_at, updated_at) VALUES
(3, 'TEMPLATE1', 'School Expo Registration Template', 3, 'school-expo-registration', 'Template for event registration for the education expo.', '2023-11-06 00:00:00', '2023-11-06 00:00:00'),
(3, 'TEMPLATE2', 'Event Program Template', 3, 'education-event-program', 'Template for the event program for the education expo.', '2023-11-07 00:00:00', '2023-11-07 00:00:00'),
(4, 'TEMPLATE1', 'Health and Wellness Flyer', 4, 'health-wellness-flyer', 'Template for the wellness and health expo flyer.', '2023-11-08 00:00:00', '2023-11-08 00:00:00'),
(4, 'TEMPLATE2', 'Health Expo Agenda', 4, 'health-expo-agenda', 'Template for the agenda of the health and wellness expo.', '2023-11-09 00:00:00', '2023-11-09 00:00:00'),
(4, 'TEMPLATE3', 'Workshop Agenda', 4, 'wellness-workshop-agenda', 'Template for wellness workshops at the expo.', '2023-11-10 00:00:00', '2023-11-10 00:00:00'),
(5, 'TEMPLATE1', 'Music Festival Event Program', 5, 'music-festival-program', 'Template for the music festival event program.', '2023-11-11 00:00:00', '2023-11-11 00:00:00'),
(5, 'TEMPLATE2', 'Concert Schedule Template', 5, 'concert-schedule', 'Template for the concert schedule.', '2023-11-12 00:00:00', '2023-11-12 00:00:00'),
(5, 'TEMPLATE3', 'Artist List Template', 5, 'artist-list', 'Template for the artist list at the music festival.', '2023-11-13 00:00:00', '2023-11-13 00:00:00'),
(6, 'TEMPLATE1', 'Art Exhibition Program', 6, 'art-exhibition-program', 'Template for the art exhibition program.', '2023-11-14 00:00:00', '2023-11-14 00:00:00'),
(6, 'TEMPLATE2', 'Artists Presentation Template', 6, 'artists-presentation', 'Template for the artist presentations.', '2023-11-15 00:00:00', '2023-11-15 00:00:00'),
(6, 'TEMPLATE3', 'Exhibitor Details Template', 6, 'exhibitor-details', 'Template for exhibitor details at the exhibition.', '2023-11-16 00:00:00', '2023-11-16 00:00:00'),
(7, 'TEMPLATE1', 'Sports Meet Schedule', 7, 'sports-meet-schedule', 'Template for sports meet event schedule.', '2023-11-17 00:00:00', '2023-11-17 00:00:00'),
(7, 'TEMPLATE2', 'Athlete Registration Template', 7, 'athlete-registration', 'Template for athlete registration.', '2023-11-18 00:00:00', '2023-11-18 00:00:00'),
(8, 'TEMPLATE1', 'Financial Freedom Flyer', 8, 'financial-freedom-flyer', 'Template for the financial freedom summit flyer.', '2023-11-19 00:00:00', '2023-11-19 00:00:00'),
(8, 'TEMPLATE2', 'Investment Plan Template', 8, 'investment-plan', 'Template for the investment session at the summit.', '2023-11-20 00:00:00', '2023-11-20 00:00:00'),
(9, 'TEMPLATE1', 'Science Forum Brochure', 9, 'science-forum-brochure', 'Template for the science forum brochure.', '2023-11-21 00:00:00', '2023-11-21 00:00:00'),
(9, 'TEMPLATE2', 'Science Panel Template', 9, 'science-panel', 'Template for the science forum panel discussions.', '2023-11-22 00:00:00', '2023-11-22 00:00:00'),
(9, 'TEMPLATE3', 'Innovation Showcase Template', 9, 'innovation-showcase', 'Template for innovation showcases at the forum.', '2023-11-23 00:00:00', '2023-11-23 00:00:00'),
(10, 'TEMPLATE1', 'Entrepreneurship Summit Agenda', 10, 'entrepreneurship-summit-agenda', 'Template for the entrepreneurship summit agenda.', '2023-11-24 00:00:00', '2023-11-24 00:00:00'),
(10, 'TEMPLATE2', 'Startup Presentation Template', 10, 'startup-presentation', 'Template for the startup presentations at the summit.', '2023-11-25 00:00:00', '2023-11-25 00:00:00');



-- Inserting Custom Fields (7 for each template)
-- For Template 1 (Registration Template for ACADA2024)
INSERT INTO myapp_customfield (template_id, label, content, start_time, end_time) VALUES
(1, 'Welcome Speech', 'Speech by the event organizer', '09:00:00', '09:30:00'),
(1, 'Keynote Address', 'Keynote speech by the CEO', '09:30:00', '10:00:00'),
(1, 'Panel Discussion', 'Panel discussion on event topics', '10:30:00', '11:30:00'),
(1, 'Networking Session', 'Opportunities to network with other attendees', '12:00:00', '13:00:00'),
(1, 'Lunch Break', 'Lunch for all participants', '13:00:00', '14:00:00'),
(1, 'Afternoon Workshop', 'Interactive workshop on entrepreneurship', '14:30:00', '16:00:00'),
(1, 'Closing Remarks', 'Final remarks and event closing', '16:30:00', '17:00:00');

-- For Template 2 (Event Program for ACADA2024)
INSERT INTO myapp_customfield (template_id, label, content, start_time, end_time) VALUES
(2, 'Opening Ceremony', 'Formal opening of the event', '09:00:00', '09:30:00'),
(2, 'Introduction to Speakers', 'Introduction of keynote speakers', '09:30:00', '10:00:00'),
(2, 'Guest Speaker Presentation', 'Guest speaker will present on educational innovations', '10:00:00', '11:00:00'),
(2, 'Networking Break', 'Networking break and refreshments', '11:30:00', '12:00:00'),
(2, 'Workshops on Coding', 'Various workshops on coding and programming', '12:00:00', '14:00:00'),
(2, 'Keynote Speech', 'Keynote speech by invited experts', '14:30:00', '15:00:00'),
(2, 'Event Wrap-up', 'Summary and event closing remarks', '15:30:00', '16:00:00');

-- For Template 3 (Event Agenda for Health Expo)
INSERT INTO myapp_customfield (template_id, label, content, start_time, end_time) VALUES
(3, 'Opening Ceremony', 'Event opening with introduction to health expo', '09:00:00', '09:30:00'),
(3, 'Health Talk', 'A talk on the importance of healthy living', '09:30:00', '10:00:00'),
(3, 'Fitness Session', 'Live fitness and wellness session', '10:30:00', '11:30:00'),
(3, 'Healthy Cooking Class', 'Learn to cook healthy meals', '12:00:00', '13:00:00'),
(3, 'Lunch Break', 'Lunch for participants', '13:00:00', '14:00:00'),
(3, 'Interactive Health Check', 'Free health checkups for attendees', '14:00:00', '16:00:00'),
(3, 'Closing Remarks', 'Event conclusion and final words', '16:30:00', '17:00:00');

-- Continue adding similar custom fields for other templates as needed




-- Inserting Additional Programs (10)
INSERT INTO myapp_program (title, featured_event) VALUES
('Leadership', NULL),
('Tech & Innovation', NULL),
('Marketing', NULL),
('Web Development', NULL),
('Digital Transformation', NULL),
('Sustainability', NULL),
('AI & Machine Learning', NULL),
('E-commerce', NULL),
('Blockchain', NULL),
('Cybersecurity', NULL);


-- Inserting Additional Events (20)
INSERT INTO myapp_event (code, title, description, program_id, venue, city, start_datetime, end_datetime, contact_email, contact_phone_number, organizer_id, slug, is_private, created_at, updated_at) VALUES
('LEADERSHIP2024', 'Leadership Summit 2024', 'Leadership summit for aspiring leaders', 1, 'Grand Ballroom, Abuja', 'Abuja', '2024-02-20 09:00:00', '2024-02-20 17:00:00', 'contact@leadersummit.com', '08022334455', 1, 'leadership-summit-2024', false, '2023-11-01 00:00:00', '2023-11-01 00:00:00'),
('TECHINNO2024', 'Tech and Innovation Conference', 'A conference exploring cutting-edge technology and innovations', 2, 'Innovation Center, Lagos', 'Lagos', '2024-03-10 09:00:00', '2024-03-10 18:00:00', 'contact@techinnoconf.com', '08033445566', 2, 'tech-innovation-conference', true, '2023-11-02 00:00:00', '2023-11-02 00:00:00'),
('MARKETING2024', 'Digital Marketing Summit', 'Summit on digital marketing strategies', 3, 'Marketing Hub, Port Harcourt', 'Port Harcourt', '2024-04-05 09:00:00', '2024-04-05 17:00:00', 'contact@marketingsummit.com', '08044556677', 3, 'digital-marketing-summit', false, '2023-11-03 00:00:00', '2023-11-03 00:00:00'),
('WEBDEV2024', 'Web Development Bootcamp', 'Training bootcamp on modern web development techniques', 4, 'Tech Hub, Enugu', 'Enugu', '2024-05-12 08:00:00', '2024-05-12 17:00:00', 'contact@webdevbootcamp.com', '08055667788', 4, 'webdev-bootcamp-2024', true, '2023-11-04 00:00:00', '2023-11-04 00:00:00'),
('DIGITRANS2024', 'Digital Transformation Summit', 'Exploring digital transformation in businesses', 5, 'Business Hall, Abuja', 'Abuja', '2024-06-01 09:00:00', '2024-06-01 17:00:00', 'contact@digittransummit.com', '08066778899', 5, 'digital-transformation-summit', false, '2023-11-05 00:00:00', '2023-11-05 00:00:00'),
('SUSTAIN2024', 'Sustainability Conference', 'Conference on sustainability practices', 6, 'Sustainability Center, Lagos', 'Lagos', '2024-07-20 09:00:00', '2024-07-20 17:00:00', 'contact@sustainconf.com', '08077889900', 6, 'sustainability-conference-2024', true, '2023-11-06 00:00:00', '2023-11-06 00:00:00'),
('AIML2024', 'AI and Machine Learning Expo', 'An expo on AI and machine learning advancements', 7, 'AI Arena, Kano', 'Kano', '2024-08-15 10:00:00', '2024-08-15 18:00:00', 'contact@aimlexpo.com', '08088990011', 7, 'ai-machine-learning-expo', false, '2023-11-07 00:00:00', '2023-11-07 00:00:00'),
('ECOM2024', 'E-commerce Summit', 'Summit on modern e-commerce strategies', 8, 'E-commerce Plaza, Oyo', 'Oyo', '2024-09-05 09:00:00', '2024-09-05 17:00:00', 'contact@ecomsummit.com', '08099001122', 8, 'ecommerce-summit-2024', true, '2023-11-08 00:00:00', '2023-11-08 00:00:00'),
('BLOCKCHAIN2024', 'Blockchain Conference', 'A deep dive into blockchain technologies', 9, 'Tech Hub, Lagos', 'Lagos', '2024-10-01 09:00:00', '2024-10-01 17:00:00', 'contact@blockchainconf.com', '08012345678', 9, 'blockchain-conference-2024', false, '2023-11-09 00:00:00', '2023-11-09 00:00:00'),
('CYBERSEC2024', 'Cybersecurity Summit', 'Cybersecurity conference for tech professionals', 10, 'Cyber Hub, Ibadan', 'Ibadan', '2024-11-10 09:00:00', '2024-11-10 17:00:00', 'contact@cybersecsummit.com', '08023456789', 10, 'cybersecurity-summit-2024', true, '2023-11-10 00:00:00', '2023-11-10 00:00:00');



-- Inserting Templates for Additional Events (3 to 5 for each event)
INSERT INTO myapp_template (owner_id, code, title, event_id, slug, description, created_at, updated_at) VALUES
(1, 'TEMPLATE1', 'Leadership Registration Template', 11, 'leadership-registration', 'Template for registration at the Leadership Summit.', '2023-11-11 00:00:00', '2023-11-11 00:00:00'),
(1, 'TEMPLATE2', 'Event Program for Leadership Summit', 11, 'leadership-program', 'Program for the Leadership Summit event.', '2023-11-12 00:00:00', '2023-11-12 00:00:00'),
(2, 'TEMPLATE1', 'Tech & Innovation Conference Flyer', 12, 'tech-innovation-flyer', 'Flyer template for the Tech & Innovation Conference.', '2023-11-13 00:00:00', '2023-11-13 00:00:00'),
(2, 'TEMPLATE2', 'Innovation Expo Registration', 12, 'innovation-expo-registration', 'Registration template for the Innovation Expo.', '2023-11-14 00:00:00', '2023-11-14 00:00:00'),
(3, 'TEMPLATE1', 'Marketing Summit Registration', 13, 'marketing-summit-registration', 'Template for registration for the Digital Marketing Summit.', '2023-11-15 00:00:00', '2023-11-15 00:00:00'),
(3, 'TEMPLATE2', 'Summit Agenda', 13, 'marketing-summit-agenda', 'Agenda template for the Digital Marketing Summit.', '2023-11-16 00:00:00', '2023-11-16 00:00:00'),
(4, 'TEMPLATE1', 'Web Development Workshop Program', 14, 'webdev-workshop-program', 'Workshop program for the Web Development Bootcamp.', '2023-11-17 00:00:00', '2023-11-17 00:00:00'),
(4, 'TEMPLATE2', 'Web Developer Bootcamp Flyer', 14, 'webdev-flyer', 'Flyer for the Web Development Bootcamp event.', '2023-11-18 00:00:00', '2023-11-18 00:00:00'),
(5, 'TEMPLATE1', 'Digital Transformation Brochure', 15, 'digittrans-brochure', 'Brochure template for the Digital Transformation Summit.', '2023-11-19 00:00:00', '2023-11-19 00:00:00'),
(5, 'TEMPLATE2', 'Transformation Keynote Speech Program', 15, 'transformation-keynote', 'Keynote speech program for the Digital Transformation Summit.', '2023-11-20 00:00:00', '2023-11-20 00:00:00');


-- Inserting Custom Fields for Templates (7 per template)
-- For Leadership Summit
INSERT INTO myapp_customfield (template_id, label, content, start_time, end_time) VALUES
(1, 'Opening Speech', 'Welcome speech by the organizer', '09:00:00', '09:30:00'),
(1, 'Keynote Address', 'Keynote by renowned speaker', '09:30:00', '10:00:00'),
(1, 'Leadership Workshop', 'Interactive leadership training', '10:30:00', '12:00:00'),
(1, 'Networking Lunch', 'Lunch and networking session', '12:30:00', '13:30:00'),
(1, 'Panel Discussion', 'Panel discussion with experts', '14:00:00', '15:00:00'),
(1, 'Closing Remarks', 'Final remarks and event closure', '15:30:00', '16:00:00'),
(1, 'After Party', 'Event after party for networking', '17:00:00', '19:00:00');
