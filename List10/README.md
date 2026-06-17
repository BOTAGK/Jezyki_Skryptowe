# JS Lab 10 - SQLite + SQLAlchemy ORM

Rozwiazanie rozszerzone do laboratorium 10. Projekt uzywa SQLite oraz SQLAlchemy ORM, a kod jest podzielony na warstwy:

- `timetable/models` - modele ORM i relacje,
- `timetable/repositories` - zapytania do bazy,
- `timetable/services` - logika tworzenia bazy, importu GTFS i analiz,
- `timetable/schemas` - proste struktury danych zwracane przez serwisy,
- `timetable/utils` - funkcje pomocnicze,
- `create_database.py`, `load_data.py`, `analyze_stop.py`, `web_app.py` - skrypty uruchomieniowe.

## Instalacja

```bash
python -m pip install -r requirements.txt
```

## Utworzenie pustej bazy

```bash
python create_database.py my_timetable
```

Powstanie plik `my_timetable.sqlite3`. Skrypt przyjmuje tez pelna sciezke, np. `data/wroclaw.sqlite3`.

## Import paczki GTFS

```bash
python load_data.py OtwartyWroclaw_rozklad_jazdy_GTFS_28052026.zip my_timetable
```

Opcjonalnie mozna wyczyscic poprzednie dane przed importem:

```bash
python load_data.py OtwartyWroclaw_rozklad_jazdy_GTFS_28052026.zip my_timetable --replace
```

## Analiza przystanku w konsoli

```bash
python analyze_stop.py my_timetable
```

Mozna tez podac przystanek bez interaktywnego wyboru:

```bash
python analyze_stop.py my_timetable --stop-id 12345
```

Skrypt pokazuje:

- liczbe roznych linii zatrzymujacych sie na przystanku,
- liczbe odjazdow,
- najwczesniejszy i najpozniejszy odjazd,
- najczestsze kierunki,
- nietrywialne zapytanie agregujace: najbardziej obciazone godziny z liczba odjazdow i liczba roznych linii.

## Webowy interfejs uzytkownika

```bash
python web_app.py my_timetable --port 8000
```

Nastepnie otworz:

```text
http://127.0.0.1:8000
```

## DDL SQL

Plik `schema.sql` zawiera recznie zapisane polecenia DDL dla SQLite. Wlasciwa aplikacja tworzy te sama strukture z poziomu modeli SQLAlchemy.
