# Kongtapp Veerawattananun 6210546374
import unittest
import requests
from decouple import config

class ApiTest(unittest.TestCase):
    """ test for World Class Government API. """

    def setUp(self):
        self.url = config('URL')
        self.ryn_id = "1010278345143"

        # create test citizen
        self.create_registration("1010278345143", "Ryn", "Akaldia", "28/01/2000", "student", "0951153666", "False", "South Continent jirhadt", "[Astra]")

    def create_registration(self, citizen_id, name, surname, birth_date, phone_num, is_risk,occupation, address, vaccine_taken):
        """
        use args to create registration_url for registration
        """
        params = f"/registration?citizen_id={citizen_id}&name={name}" \
                 f"&surname={surname}&birth_date={birth_date}" \
                 f"&occupation={occupation}&phone_number={phone_num}&is_risk={is_risk}" \
                 f"&address={address}&vaccine_taken={vaccine_taken}"
        return requests.post(self.url + params)

    def test_get_registration(self):
        """ fetch the citizen personal data from citizen_id """
        response = requests.get(self.url + f"/registration/{self.ryn_id}")
        self.assertEqual(self.ryn_id, response.json()["citizen_id"])

    def test_delete_citizen(self):
        """ delete specific citizen personal data from citizen_id"""
        response = requests.delete(self.url + f"/citizen?citizen_id={self.ryn_id}")
        self.assertEqual(404, response.status_code)

    def test_get_invalid_citizen(self):
        """ try to fetch specific citizen personal data by invalid citizen_id"""
        response = requests.get(self.url + f"/citizen/string")
        self.assertNotEqual(200, response.status_code)

    def test_post_registration(self):
        """ registration for a user """
        response = self.create_registration("1010278345145", "Tetris", "Spinner", "09/01/2000", "0850592059", "False","Gamer", "Wine Cellar", "[]")
        self.assertEqual("registration success!", response.json()["feedback"])

    def test_registration_empty_id(self):
        """ try register a user data with empty citizen_id """
        response = self.create_registration("", "Dyluze", "Akaldia", "13/09/1997", "0881113333", "False","Warrior", "South Continent jirhadt", "[]")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_registration_id_array(self):
        """ try register a user data with citizen_id as a array """
        response = self.create_registration(["1234567890123", "2345678901234"], "str", "sentence", "04/04/2004", "0883331111", "True", "student", "ionia", "[]")
        self.assertEqual("registration failed: invalid citizen ID", response.json()["feedback"])

    def test_registration_id_string(self):
        """ try to register a user data with string as a citizen_id """
        response = self.create_registration("string", "str", "sentence", "04/04/2004", "0882223333", "False","student", "ionia", "[]")
        self.assertEqual("registration failed: invalid citizen ID", response.json()["feedback"])

    def test_registration_empty_first_name(self):
        """ try register a user data with empty first name """
        response = self.create_registration("1109864231798", "", "Akaldia", "12/09/1997", "0882223333", "False","Warrior",
                                            "South Continent jirhadt", "[]")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_registration_empty_last_name(self):
        """ try register a user data with empty last name """
        response = self.create_registration("1109864231798", "Dyluze", "", "03/09/1997", "0882223333", "False","Warrior",
                                            "South Continent jirhadt", "[]")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_registration_name_array(self):
        """ try register a user data with name as a array """
        response = self.create_registration("1110278345543", ["str", "ings"], ["Hello"], "04/04/2004", "0882223333", "False","student",
                                            "demacia", "[]")
        self.assertEqual("registration failed: invalid name format", response.json()["feedback"])

    def test_registration_empty_birth_date(self):
        """ try register a user data with empty birth_date """
        response = self.create_registration("1109864231798", "Dyluze", "Akaldia", "", "0882223333", "False","Warrior",
                                            "South Continent jirhadt", "[]")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_registration_invalid_date(self):
        """ try register a user data with invalid date """
        response = self.create_registration("1110278345144", "master", "yi", "60/01/2000", "0882223333", "False","wuju master",
                                            "ionia", "[]")
        self.assertEqual("registration failed: invalid birth date format", response.json()["feedback"])

    def test_registration_future_date(self):
        """ try register a user data by using future date """
        response = self.create_registration("1106587451355", "Neotica", "Balm", "04/04/2044", "0882223333", "False","student",
                                            "Neo-Thailand-Hospital", "[]")
        self.assertEqual("registration failed: not archived minimum age", response.json()["feedback"])

    def test_registration_1000_years_ago(self):
        """ try register a user data by using over 1000 years in the past """
        response = self.create_registration("1000000000002", "Old", "Boi", "04/04/1000", "0882223333", "False","corpse",
                                            "Graveyard", "[]")
        self.assertEqual("registration failed: too old", response.json()["feedback"])

    def test_registration_empty_occupation(self):
        """ try register a user data with empty occupation """
        response = self.create_registration("1109864231798", "Dyluze", "Akaldia", "02/09/1997", "0882223333", "True","",
                                            "South Continent jirhadt", "[]")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_registration_occupation_array(self):
        """ try register a user data with multiple occupation """
        response = self.create_registration("1000012340005", "Little", "Boi", "03/05/2000", "0882223333", "False",
                                            ["Killer", "Murderer", "Teacher", "4444"], "Jail", "[]")
        self.assertEqual("registration success!", response.json()["feedback"])

    def test_registration_empty_address(self):
        """ try register a user data with empty address """
        response = self.create_registration("1109864231798", "Dyluze", "Akaldia", "02/09/1997", "0882223333", "False", "Warrior", "", "[]")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_registration_address_array(self):
        """ try register a user data with multiple address as array """
        response = self.create_registration("1109861834798", "Die", "Addrie", "02/02/1997", "0882323333", "False", "Student", ["99/302", "99/303"], "[]")
        self.assertEqual("registration success!", response.json()["feedback"])


if __name__ == '__main__':
    unittest.main()
