import mysql.connector as mysql

# Connect to the database
db = mysql.connect(
    host="localhost",
    user="root",
    passwd="user",
    database="project"
)

class Record:
    def __init__(self, individual_id, individual_name, entry_time):
        self.individual_id = individual_id
        self.individual_name = individual_name
        self.entry_time = entry_time
        self.exit_time = None

class BorderControlSystem:
    def __init__(self):
        self.records = {}

    def create_entry(self, individual_id, individual_name, entry_time):
        record = Record(individual_id, individual_name, entry_time)
        self.records[individual_id] = record
        self.save_to_db(record)
        return record

    def read_entry(self, individual_id):
        return self.records.get(individual_id)

    def update_exit(self, individual_id, exit_time):
        record = self.read_entry(individual_id)
        if record:
            record.exit_time = exit_time
            self.update_exit_time_in_db(individual_id, exit_time)

    def delete_entry(self, individual_id):
        if individual_id in self.records:
            del self.records[individual_id]
            self.delete_from_db(individual_id)

    def analyze_traffic_patterns(self):
        patterns = {}
        for record in self.records.values():
            patterns[record.individual_name] = patterns.get(record.individual_name, 0) + 1
        return patterns

    def save_to_db(self, record):
        cursor = db.cursor()
        query = "INSERT INTO record (individual_id, individual_name, entry_time) VALUES (%s, %s, %s)"
        cursor.execute(query, (record.individual_id, record.individual_name, record.entry_time))
        db.commit()

    def update_exit_time_in_db(self, individual_id, exit_time):
        cursor = db.cursor()
        query = "UPDATE record SET exit_time = %s WHERE individual_id = %s"
        cursor.execute(query, (exit_time, individual_id))
        db.commit()

    def delete_from_db(self, individual_id):
        cursor = db.cursor()
        query = "DELETE FROM record WHERE individual_id = %s"
        cursor.execute(query, (individual_id,))
        db.commit()

class Country:
    def __init__(self, name):
        self.name = name
        self.border_control_system = BorderControlSystem()

    def get_border_control_system(self):
        return self.border_control_system

class BorderControl:
    def __init__(self):
        self.countries = {}

    def add_country(self, country_name):
        if country_name not in self.countries:
            country = Country(country_name)
            self.countries[country_name] = country
            return country
        return None

    def get_country(self, country_name):
        return self.countries.get(country_name)

border_control = BorderControl()
country = border_control.add_country("Kashmir")
border_system = country.get_border_control_system()


#record = border_system.create_entry(55, 'mahesh', '2020-04-05')
#record = border_system.create_entry(51, 'kai', '2020-04-07')


border_system.update_exit(55, '05-04-2020')
#border_system.update_exit(45, '07-04-2020')


#order_system.delete_from_db(44)


patterns = border_system.analyze_traffic_patterns()
print(patterns) 