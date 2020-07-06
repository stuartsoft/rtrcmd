import unittest

from gpiozero.pins.mock import MockFactory

from constants import Constants
from steeringwheel import SteeringWheel


class SteeringWheelTest(unittest.TestCase):

    SOME_PIN_ID = 13

    def setUp(self) -> None:
        self.mock_servo = MockFactory(pin_class="mockpwmpin").pin(SteeringWheelTest.SOME_PIN_ID)
        self.test_obj = SteeringWheel(self.mock_servo)

    def test_can_construct(self):

        self.assertIs(self.test_obj.servo_ref, self.mock_servo)
        self.assertEqual(Constants.SERVO_CENTER_PWM_VALUE, self.test_obj.servo_ref.value)

    def test_can_map_direction_to_servo_value(self):

        self.test_obj.set_heading('N000')

        self.assertEqual(Constants.SERVO_CENTER_PWM_VALUE, self.test_obj.servo_ref.value)

        self.test_obj.set_heading('L100')

        self.assertEqual(1, self.test_obj.servo_ref.value)

        self.test_obj.set_heading('R100')

        self.assertEqual(-1, self.test_obj.servo_ref.value)

    def test_can_interpolate_values_based_on_configured_servo_center(self):

        self.test_obj.set_heading('L050')
        expected_value = (1 - Constants.SERVO_CENTER_PWM_VALUE)/2 + Constants.SERVO_CENTER_PWM_VALUE
        self.assertEqual(expected_value, self.test_obj.servo_ref.value)

        self.test_obj.set_heading('R025')
        expected_value = (-1 - Constants.SERVO_CENTER_PWM_VALUE)/4 + Constants.SERVO_CENTER_PWM_VALUE
        self.assertEqual(expected_value, self.test_obj.servo_ref.value)

    def test_should_set_to_center_if_neutral(self):

        self.test_obj.set_heading('N100')
        self.assertEqual(Constants.SERVO_CENTER_PWM_VALUE, self.test_obj.servo_ref.value)