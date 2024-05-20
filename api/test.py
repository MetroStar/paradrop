#!/usr/bin/env python3
# RUN BY 'python3 -m unittest discover' command when in paradrop directory
from importlib import reload
import logging
import time
import unittest
from asyncio import run
from flask_setup import app
from api_setup import add_resources
from test_config import URL, tests, auth_types, success_message, fail_message, test_count
import sys
sys.path.append(".")

# Setting testing to True
app.config['TESTING'] = True

# Running function to add api endpoints
run(add_resources())

# Setting up test logger
# Restarting logging module because otherwise it would
# use the default one from app and we want to have separate
# logger for testing
logging.shutdown()
reload(logging)

file_handler = logging.FileHandler(filename="test_log.log", mode="w")
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    handlers=handlers)
logger = logging.getLogger()


def check_auth_code(auth):
    """
    Function to check what expected status code is based on our current authorization
    """
    if auth == "UNAUTHORIZED":
        return "code_unauth"

    elif auth == "READ-ONLY":
        return "code_user"

    elif auth == "ADMIN":
        return "code_admin"


class FlaskTestCase(unittest.TestCase):

    def testLoop(self):
        """
        This test function loops through our predefined test cases
        3 times. First as a non-authorized user, Second as our
        user with read-only rights and third as an administrator with
        admin rights. We can also specify what test we want to run with
        what authorization. More on that in test_config.py file. There is
        explanation to all atributes of format that those tests use.
        """

        all_tests_count = 0
        failure_count = 0
        success_count = 0

        # Run tests for every auth type specified
        for type in auth_types:

            with app.test_client() as tester:
                with tester.session_transaction() as sess:
                    # Setting specified authorization
                    sess["email"] = type["email"]

                try:
                    # Running predefined tests
                    for test_data in tests:
                        # If test isn't made for current authorization, skip it
                        if type["auth_type"] not in test_data["for"] and "all" not in test_data["for"]:
                            continue

                        if test_data["method"] == "GET":
                            response = tester.get(
                                URL + test_data["url"], headers=test_data["headers"],)
                            response_message = response.__dict__["_status"]

                        elif test_data["method"] == "POST":
                            response = tester.post(
                                URL + test_data["url"], json=test_data["json"], headers=test_data["headers"],)
                            response_message = response.get_data(as_text=True)

                        elif test_data["method"] == "PUT":
                            response = tester.put(
                                URL + test_data["url"], json=test_data["json"], headers=test_data["headers"],)
                            response_message = response.get_data(as_text=True)

                        elif test_data["method"] == "DELETE":
                            response = tester.delete(
                                URL + test_data["url"], json=test_data["json"], headers=test_data["headers"],)
                            response_message = response.get_data(as_text=True)

                        status_code = response.status_code
                        expected_code = check_auth_code(type["auth_type"])

                        # Assert test to check if we got status code that we
                        # expected
                        self.assertEqual(status_code, test_data[expected_code])

                        # If test was succesful, add it into test_log file in
                        # predefined format
                        logger.info(
                            success_message.format(
                                type["auth_type"],
                                test_data["test_case"],
                                test_data["url"],
                                test_data["method"],
                                test_data[expected_code],
                                status_code,
                                response_message))

                        success_count += 1
                        all_tests_count += 1

                        # Some operations need some time to apply so If there
                        # is a pause time specified, testing will pause
                        if test_data["pause"]:
                            time.sleep(test_data["pause"])

                except AssertionError as e:
                    # If test failed, add it into test_log file in predefined
                    # format
                    logger.error(
                        fail_message.format(
                            type["auth_type"],
                            test_data["test_case"],
                            test_data["url"],
                            test_data["method"],
                            test_data[expected_code],
                            status_code,
                            response_message,
                            e))

                    failure_count += 1
                    all_tests_count += 1

        app.config['TESTING'] = False

        if failure_count > 0:
            print("Paradrop API Tests have FAILURES: " + str(failure_count))

        # Adding summary of how many tests we did and how many
        # failures/successes we got into test_log file
        logger.info(
            test_count.format(
                all_tests_count,
                success_count,
                failure_count))


if __name__ == "__main__":
    unittest.main(exit=False)
