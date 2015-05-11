# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import random
from tests.ggrc import TestCase
from freezegun import freeze_time
from datetime import datetime
from mock import patch

import os
from ggrc import notification
from ggrc.models import NotificationConfig, Notification, Person
from tests.ggrc_workflows.generator import WorkflowsGenerator
from tests.ggrc.api_helper import Api
from tests.ggrc.generator import GgrcGenerator


if os.environ.get('TRAVIS', False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestEnableAndDisableNotifications(TestCase):

  """ This class contains simple one time workflow tests that are not
  in the gsheet test grid
  """

  def setUp(self):
    TestCase.setUp(self)
    self.api = Api()
    self.wf_generator = WorkflowsGenerator()
    self.ggrc_generator = GgrcGenerator()
    Notification.query.delete()

    self.random_objects = self.ggrc_generator.generate_random_objects(2)
    _, self.user = self.ggrc_generator.generate_person(user_role="gGRC Admin")
    _, self.user2 = self.ggrc_generator.generate_person(user_role="gGRC Admin")
    self.create_test_cases()

    def init_decorator(init):
      def new_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        if hasattr(self, "created_at"):
          self.created_at = datetime.now()
      return new_init

    Notification.__init__ = init_decorator(Notification.__init__)

  @patch("ggrc.notification.email.send_email")
  def test_disabled_notifications(self, mock_mail):

    with freeze_time("2015-02-01 13:39:20"):
      _, wf = self.wf_generator.generate_workflow(self.quarterly_wf)
      response, wf = self.wf_generator.activate_workflow(wf)

      self.assert200(response)

      user = Person.query.get(self.user.id)

    with freeze_time("2015-01-01 13:39:20"):
      _, notif_data = notification.get_todays_notifications()
      self.assertNotIn(user.email, notif_data)

    with freeze_time("2015-01-29 13:39:20"):
      _, notif_data = notification.get_todays_notifications()
      self.assertNotIn(user.email, notif_data)

  @patch("ggrc.notification.email.send_email")
  def test_enabled_notifications(self, mock_mail):

    with freeze_time("2015-02-01 13:39:20"):
      _, wf = self.wf_generator.generate_workflow(self.quarterly_wf)
      response, wf = self.wf_generator.activate_workflow(wf)

      self.assert200(response)

      user = Person.query.get(self.user.id)

    with freeze_time("2015-01-29 13:39:20"):
      _, notif_data = notification.get_todays_notifications()
      self.assertNotIn(user.email, notif_data)


      data = {
          "notification_config": {
              "person_id": user.id,
              "notif_type": "Email_Digest",
              "enable_flag": True,
              "context": None,
              "type": "NotificationConfig",
          }
      }
      response = self.ggrc_generator.api.post(NotificationConfig, data)

      user = Person.query.get(self.user.id)
      _, notif_data = notification.get_todays_notifications()
      self.assertIn(user.email, notif_data)

  @patch("ggrc.notification.email.send_email")
  def test_forced_notifications(self, mock_mail):

    with freeze_time("2015-02-01 13:39:20"):
      _, wf = self.wf_generator.generate_workflow(self.quarterly_wf_forced)
      response, wf = self.wf_generator.activate_workflow(wf)

      self.assert200(response)

      user = Person.query.get(self.user.id)

    with freeze_time("2015-01-29 13:39:20"):
      _, notif_data = notification.get_todays_notifications()
      self.assertIn(user.email, notif_data)

      data = {
          "notification_config": {
              "person_id": user.id,
              "notif_type": "Email_Digest",
              "enable_flag": True,
              "context": None,
              "type": "NotificationConfig",
          }
      }
      response = self.ggrc_generator.api.post(NotificationConfig, data)

      user = Person.query.get(self.user.id)
      _, notif_data = notification.get_todays_notifications()
      self.assertIn(user.email, notif_data)

  @patch("ggrc.notification.email.send_email")
  def test_force_one_wf_notifications(self, mock_mail):

    with freeze_time("2015-02-01 13:39:20"):
      _, wf_forced = self.wf_generator.generate_workflow(self.quarterly_wf_forced)
      response, wf_forced = self.wf_generator.activate_workflow(wf_forced)
      _, wf = self.wf_generator.generate_workflow(self.quarterly_wf)
      response, wf = self.wf_generator.activate_workflow(wf)

      self.assert200(response)

      user = Person.query.get(self.user.id)

    with freeze_time("2015-01-29 13:39:20"):
      _, notif_data = notification.get_todays_notifications()
      self.assertIn(user.email, notif_data)
      self.assertIn("cycle_starts_in", notif_data[user.email])
      self.assertIn(wf_forced.id, notif_data[user.email]["cycle_starts_in"])
      self.assertNotIn(wf.id, notif_data[user.email]["cycle_starts_in"])

      data = {
          "notification_config": {
              "person_id": user.id,
              "notif_type": "Email_Digest",
              "enable_flag": True,
              "context": None,
              "type": "NotificationConfig",
          }
      }
      response = self.ggrc_generator.api.post(NotificationConfig, data)

      user = Person.query.get(self.user.id)
      _, notif_data = notification.get_todays_notifications()
      self.assertIn(user.email, notif_data)
      self.assertIn("cycle_starts_in", notif_data[user.email])
      self.assertIn(wf_forced.id, notif_data[user.email]["cycle_starts_in"])
      self.assertIn(wf.id, notif_data[user.email]["cycle_starts_in"])

  @patch("ggrc.notification.email.send_email")
  def test_user_task_bleed(self, mock_mail):
    def enable_notifications(user):
      data = {
          "notification_config": {
              "person_id": user.id,
              "notif_type": "Email_Digest",
              "enable_flag": True,
              "context": None,
              "type": "NotificationConfig",
          }
      }
      response = self.ggrc_generator.api.post(NotificationConfig, data)

    with freeze_time("2015-02-01 13:39:20"):
      _, wf = self.wf_generator.generate_workflow(self.quarterly_wf_two_users)
      response, wf = self.wf_generator.activate_workflow(wf)

      self.assert200(response)

      user1 = Person.query.get(self.user.id)
      user2 = Person.query.get(self.user2.id)

    with freeze_time("2015-02-01 13:39:20"):
      enable_notifications(user1)
      enable_notifications(user2)

      notifications, notif_data = notification.get_todays_notifications()

      print notif_data

      self.assertIn(user1.email, notif_data)
      self.assertIn(user2.email, notif_data)

      # check that user1 my_tasks include only "task 1"
      # check that user2 my_tasks include only "task 2"

  def create_test_cases(self):
    def person_dict(person_id):
      return {
          "href": "/api/people/%d" % person_id,
          "id": person_id,
          "type": "Person"
      }

    self.quarterly_wf_forced = {
        "title": "quarterly wf forced notification",
        "notify_on_change": True,
        "description": "",
        "owners": [person_dict(self.user.id)],
        "frequency": "quarterly",
        "task_groups": [{
            "title": "tg_1",
            "contact": person_dict(self.user.id),
            "task_group_tasks": [{
                "contact": person_dict(self.user.id),
                "description": self.wf_generator.random_str(100),
                "relative_start_day": 5,
                "relative_start_month": 2,
                "relative_end_day": 25,
                "relative_end_month": 2,
            },
            ],
        },
        ]
    }

    self.quarterly_wf = {
        "title": "quarterly wf 1",
        "description": "",
        "owners": [person_dict(self.user.id)],
        "frequency": "quarterly",
        "task_groups": [{
            "title": "tg_1",
            "contact": person_dict(self.user.id),
            "task_group_tasks": [{
                "contact": person_dict(self.user.id),
                "description": self.wf_generator.random_str(100),
                "relative_start_day": 5,
                "relative_start_month": 2,
                "relative_end_day": 25,
                "relative_end_month": 2,
            },
            ],
        },
        ]
    }

    self.quarterly_wf_two_users = {
      "title": "quarterfly wf 2",
      "description": "",
      "owners": [person_dict(self.user.id)],
      "frequency": "quarterly",
      "task_groups": [{
        "title": "tg_1",
        "contact": person_dict(self.user.id),
        "task_group_tasks": [{
            "contact": person_dict(self.user.id),
            "description": "task 1",
            "relative_start_day": 5,
            "relative_start_month": 2,
            "relative_end_day": 25,
            "relative_end_month": 2
          },
          {
            "contact": person_dict(self.user2.id),
            "description": "task 2",
            "relative_start_day": 5,
            "relative_start_month": 2,
            "relative_end_day": 25,
            "relative_end_month": 2
          }
        ],
      }]
    }