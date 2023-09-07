# Importing the required modules for testing
from django.forms import ValidationError
from django.test import TestCase
from univest.models import (
    Idea,
    IdeaStatus,
    Order,
)
from univest.constants import (
    OrderTypeChoices,
    OrderStatusChoices,
    IdeaStatusChoices,
)


class OrderModelTest(TestCase):
    def setUp(self):
        # Create an Idea and IdeaStatus instance for testing
        self.idea = Idea.objects.create(
            # populate the fields as per your Idea model
        )
        self.idea_status = IdeaStatus.objects.create(
            idea=self.idea, status=IdeaStatusChoices.NEW.name
        )

    def test_create_order_with_status_placed(self):
        """
        Test that a new order can only be created with status "PLACED".
        """

        order = Order.objects.create(
            idea_status=self.idea_status,
            order_type=OrderTypeChoices.BUY.name,
            status=OrderStatusChoices.EXECUTED.name,
            # other fields
        )
        self.assertRaises(ValidationError)

        order = Order.objects.create(
            idea_status=self.idea_status,
            order_type=OrderTypeChoices.BUY.name,
            status=OrderStatusChoices.PLACED.name,
            # other fields
        )
        self.assertEqual(order.status, OrderStatusChoices.PLACED.name)

    def test_change_order_status_from_placed_to_cancelled_or_executed(self):
        """
        Test changing the order status from "PLACED" to either "CANCELLED" or "EXECUTED".
        """
        order = Order.objects.create(
            idea_status=self.idea_status,
            order_type=OrderTypeChoices.BUY.name,
            status=OrderStatusChoices.PLACED.name,
            # other fields
        )
        order.status = OrderStatusChoices.CANCELLED.name
        order.save()
        self.assertEqual(order.status, OrderStatusChoices.CANCELLED.name)

        order.status = OrderStatusChoices.EXECUTED.name
        order.save()
        self.assertEqual(order.status, OrderStatusChoices.EXECUTED.name)

    def test_status_from_cancelled_or_executed_to_any_other_is_forbidden(self):
        """
        Test that status from "CANCELLED" or "EXECUTED" to any other states is forbidden.
        """
        order = Order.objects.create(
            idea_status=self.idea_status,
            order_type=OrderTypeChoices.BUY.name,
            status=OrderStatusChoices.CANCELLED.name,
            # other fields
        )
        with self.assertRaises(ValidationError):
            order.status = OrderStatusChoices.PLACED.name
            order.save()

    # Add more tests for other scenarios


# Run these tests by running `python manage.py test` in your terminal
