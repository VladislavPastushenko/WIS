INSERT INTO main_classrooms (id_classroom, name)
    VALUES (1, 'E105');

INSERT INTO main_person (id_person, firstname, surname, address, telephone, email, role)
    VALUES (1, 'Marina', 'Krav', 'Kolejni 2, 612 00 Brno', '99999999', 'abcd@mail.com', 'a');
INSERT INTO main_person (id_person, firstname, surname, address, telephone, email, role)
    VALUES (2, 'Tomas', 'Vojnar', 'Kolejni 2, 612 00 Brno', '99999998', 'jatomas@mail.com', 'g');


INSERT INTO main_course (id_course, abbrv, title, description, credits, max_persons, approved, type)
    VALUES (1, 'IOS', 'Operační systémy', 'Cílem je seznámit studenty s principy operačních systémů obecně a dále se základy operačního systému Unix.', 5, 100, TRUE, 's');


INSERT INTO main_termin (id_termin, name, type, id_classroom, id_course)
    VALUES (1, 'lecture', 'l', 1, 1);