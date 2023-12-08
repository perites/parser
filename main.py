from datetime import datetime

file_path = "C:/Users/nikit/Downloads/client_coaching_log.csv"


class Person:

    def __init__(self, name: str, mail: str, start_date_str: str, end_date_str: str, one_session_hours: float,
                 line_str: str):
        self.name = name
        self.mail = mail

        self.hours_overall = 0
        self.session_amount = 0

        self.line_str = line_str

        self.date_format = '%y.%m.%d %H:%M'
        self.one_session_hours = one_session_hours
        self.start_date = datetime.strptime(start_date_str, self.date_format)
        self.end_date = datetime.strptime(end_date_str, self.date_format)
        self.check_date(self.start_date, self.end_date, self.one_session_hours)

    def check_date(self, start_date: datetime, end_date: datetime, hours: float) -> None:
        if (end_date - start_date).total_seconds() / (60 * 60) != hours:
            raise WrongLine

        self.hours_overall += hours
        self.session_amount += 1

    def merge(self, person: 'Person'):
        self.hours_overall += person.hours_overall
        self.session_amount += person.session_amount

    def add_to_list(self) -> None:
        for added_person in PERSONS:
            if not added_person.name == self.name:
                continue

            added_person.merge(self)
            return

        PERSONS.append(self)


class WrongLine(Exception):
    pass


def wrong_line(line: str):
    print("add to error file this line:\n"
          f"{line}")


if __name__ == '__main__':

    PERSONS: list[Person] = []

    with open(file_path) as file:
        file_lines = file.readlines()

    for line_str in file_lines[2:-16]:
        line = line_str.split(";")

        try:
            person = Person(line[0],
                            line[1],
                            line[4],
                            line[5],
                            float(line[6].replace(",", ".")),
                            line_str)
        except Exception as e:
            wrong_line(line_str)
            continue

        person.add_to_list()

    for person in PERSONS:
        print(f"name : {person.name}\n"
              f"mail : {person.mail}\n"
              f"hours overall {person.hours_overall}\n"
              f"session amount: {person.session_amount}\n")
