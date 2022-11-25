INSERT INTO main_classrooms (id_classroom, name)
    VALUES (1, 'E105');

INSERT INTO main_person (id_person, firstname, surname, address, telephone, email, role)
    VALUES (1, 'Marina', 'Krav', 'Kolejni 2, 612 00 Brno', '99999999', 'abcd@mail.com', 'a');
INSERT INTO main_person (id_person, firstname, surname, address, telephone, email, role)
    VALUES (2, 'Tomas', 'Vojnar', 'Kolejni 2, 612 00 Brno', '99999998', 'jatomas@mail.com', 'g');


INSERT INTO main_course (id_course, abbrv, title, description, credits, max_persons, approved, type, id_person)
    VALUES (1, 'IOS', 'Operační systémy', 'Cílem je seznámit studenty s principy operačních systémů obecně a dále se základy operačního systému Unix.', 5, 100, 1, 's', 2);

INSERT INTO main_course (abbrv, title, description, credits, max_persons, approved, type, id_person)
    VALUES ('IIS', 'Informační systémy', 'Informační systém jako speciální případ systému. Druhy informačních systémů OLAP a OLTP. Historie informačních systémů.', 4, 100, 1, 'w', 4);

INSERT INTO main_termin (id_termin, id_course_id, id_classroom_id, name, repeted, time_start, time_end, date, weekday, max_points, description, type)
    VALUES (1, 1, 1, 'Lecture', 1, '14:00:00', '16:00:00', '2022-01-01', 'monday', 0, 'Lecture on the subject of IOS', 'l');

INSERT INTO main_termin (id_course_id, id_classroom_id, name, repeted, time_start, time_end, date, weekday, max_points, description, type)
    VALUES (2, 1, 'Project', 0, '00:00:00', '23:59:59', '2022-11-28', '', 25, 'Project on the subject of IIS', 'p');