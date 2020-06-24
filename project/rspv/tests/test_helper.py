import unittest
from datetime import timezone, datetime

from project.rspv.helper import sign_with_jwt, build_payload


class TestBuildPayload(unittest.TestCase):
    user = "user1@example.com"

    def test_not_empty(self):
        """
        Check if Payload is empty or not
        :return:
        """
        payload = build_payload(self.user)

        self.assertTrue(payload)

    def test_payload_not_empty(self):
        """
        Check if Payloads actual payload is empty or not
        :return:
        """
        payload = build_payload(self.user)

        self.assertTrue(payload['payload'])

    def test_user_is_set(self):
        """
        Check if Payload holds same user value
        :return:
        """
        payload = build_payload(self.user)

        self.assertEqual(payload['payload']['user'], self.user)

    def test_payload_date_not_empty(self):
        """
        Check if Payloads date is empty or not
        :return:
        """
        payload = build_payload(self.user)

        self.assertTrue(payload['payload']['date'])

    def test_has_correct_date(self):
        """
        Check if Payload holds correct date
        :return:
        """
        payload = build_payload(self.user)
        expected_date = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')

        self.assertEqual(payload['payload']['date'], expected_date)

    def test_jti_length(self):
        """
        Check if jti is 32 bytes (64 hex chars)
        :return:
        """
        payload = build_payload(self.user)

        self.assertEqual(len(payload['jti']), 64)

    def test_jti_type(self):
        """
        Check if jti is string
        :return:
        """
        payload = build_payload(self.user)

        self.assertIs(type(payload['jti']), str)

    def test_iat_type(self):
        """
        Check if iat is int
        :return:
        """
        payload = build_payload(self.user)

        self.assertIs(type(payload['iat']), int)


class TestSignWithJWT(unittest.TestCase):
    payload = build_payload("user1@example.com")

    def test_not_empty(self):
        """
        Check if Token is created
        :return:
        """
        jwt_token = sign_with_jwt(self.payload)

        self.assertTrue(jwt_token)

    def test_type(self):
        """
        Check if we receive bytes
        :return:
        """
        jwt_token = sign_with_jwt(self.payload)

        self.assertIs(type(jwt_token), bytes)


if __name__ == '__main__':
    unittest.main()
