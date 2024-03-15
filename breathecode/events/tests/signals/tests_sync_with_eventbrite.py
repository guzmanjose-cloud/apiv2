from unittest.mock import MagicMock, call, patch

from breathecode.tests.mixins.legacy import LegacyAPITestCase

from ...signals import event_saved
from ...tasks import async_export_event_to_eventbrite


class TestAcademyEvent(LegacyAPITestCase):
    """
    🔽🔽🔽 No sync, sync_status PENDING
    """

    @patch.object(event_saved, 'send', MagicMock())
    @patch.object(async_export_event_to_eventbrite, 'delay', MagicMock())
    def test_sync_with_eventbrite__no_sync__status_pending(self, enable_signals):
        enable_signals()

        event_kwargs = {
            'sync_with_eventbrite': False,
            'eventbrite_sync_status': 'PENDING',
        }
        model = self.generate_models(event=True, event_kwargs=event_kwargs)
        event_db = self.model_to_dict(model, 'event')

        self.assertEqual(event_saved.send.call_args_list,
                         [call(instance=model.event, created=True, sender=model.event.__class__)])

        self.assertEqual(async_export_event_to_eventbrite.delay.call_args_list, [])
        self.assertEqual(self.bc.database.list_of('events.Event'), [event_db])

    """
    🔽🔽🔽 Sync, sync_status PERSISTED
    """

    @patch.object(event_saved, 'send', MagicMock())
    @patch.object(async_export_event_to_eventbrite, 'delay', MagicMock())
    def test_sync_with_eventbrite__sync__status_persisted(self, enable_signals):
        enable_signals()

        event_kwargs = {
            'sync_with_eventbrite': True,
            'eventbrite_sync_status': 'PERSISTED',
        }
        model = self.generate_models(event=True, event_kwargs=event_kwargs)
        event_db = self.model_to_dict(model, 'event')

        self.assertEqual(event_saved.send.call_args_list,
                         [call(instance=model.event, created=True, sender=model.event.__class__)])

        self.assertEqual(async_export_event_to_eventbrite.delay.call_args_list, [])
        self.assertEqual(self.bc.database.list_of('events.Event'), [event_db])

    """
    🔽🔽🔽 Sync, sync_status ERROR
    """

    @patch.object(event_saved, 'send', MagicMock())
    @patch.object(async_export_event_to_eventbrite, 'delay', MagicMock())
    def test_sync_with_eventbrite__sync__status_error(self, enable_signals):
        enable_signals()

        event_kwargs = {
            'sync_with_eventbrite': True,
            'eventbrite_sync_status': 'ERROR',
        }
        model = self.generate_models(event=True, event_kwargs=event_kwargs)
        event_db = self.model_to_dict(model, 'event')

        self.assertEqual(event_saved.send.call_args_list,
                         [call(instance=model.event, created=True, sender=model.event.__class__)])

        self.assertEqual(async_export_event_to_eventbrite.delay.call_args_list, [])
        self.assertEqual(self.bc.database.list_of('events.Event'), [event_db])

    """
    🔽🔽🔽 Sync, sync_status WARNING
    """

    @patch.object(event_saved, 'send', MagicMock())
    @patch.object(async_export_event_to_eventbrite, 'delay', MagicMock())
    def test_sync_with_eventbrite__sync__status_warning(self, enable_signals):
        enable_signals()

        event_kwargs = {
            'sync_with_eventbrite': True,
            'eventbrite_sync_status': 'WARNING',
        }
        model = self.generate_models(event=True, event_kwargs=event_kwargs)
        event_db = self.model_to_dict(model, 'event')

        self.assertEqual(event_saved.send.call_args_list,
                         [call(instance=model.event, created=True, sender=model.event.__class__)])

        self.assertEqual(async_export_event_to_eventbrite.delay.call_args_list, [])
        self.assertEqual(self.bc.database.list_of('events.Event'), [event_db])

    """
    🔽🔽🔽 Sync, sync_status SYNCHED
    """

    @patch.object(event_saved, 'send', MagicMock())
    @patch.object(async_export_event_to_eventbrite, 'delay', MagicMock())
    def test_sync_with_eventbrite__sync__status_synched(self, enable_signals):
        enable_signals()

        event_kwargs = {
            'sync_with_eventbrite': True,
            'eventbrite_sync_status': 'SYNCHED',
        }
        model = self.generate_models(event=True, event_kwargs=event_kwargs)
        event_db = self.model_to_dict(model, 'event')

        self.assertEqual(event_saved.send.call_args_list,
                         [call(instance=model.event, created=True, sender=model.event.__class__)])

        self.assertEqual(async_export_event_to_eventbrite.delay.call_args_list, [])
        self.assertEqual(self.bc.database.list_of('events.Event'), [event_db])

    """
    🔽🔽🔽 Sync, sync_status PENDING, check signal call
    """

    @patch.object(event_saved, 'send', MagicMock())
    @patch.object(async_export_event_to_eventbrite, 'delay', MagicMock())
    def test_sync_with_eventbrite__sync__status_pending__check_signal_call(self, enable_signals):
        enable_signals()

        event_kwargs = {
            'sync_with_eventbrite': True,
            'eventbrite_sync_status': 'PENDING',
        }
        model = self.generate_models(event=True, event_kwargs=event_kwargs)
        event_db = self.model_to_dict(model, 'event')

        self.assertEqual(event_saved.send.call_args_list,
                         [call(instance=model.event, created=True, sender=model.event.__class__)])

        self.assertEqual(async_export_event_to_eventbrite.delay.call_args_list, [])
        self.assertEqual(self.bc.database.list_of('events.Event'), [event_db])

    """
    🔽🔽🔽 Sync, sync_status PENDING, check task call
    """

    @patch.object(async_export_event_to_eventbrite, 'delay', MagicMock())
    def test_sync_with_eventbrite__sync__status_pending__check_task_call(self, enable_signals):
        enable_signals()

        event_kwargs = {
            'sync_with_eventbrite': True,
            'eventbrite_sync_status': 'PENDING',
        }
        model = self.generate_models(event=True, event_kwargs=event_kwargs)
        event_db = self.model_to_dict(model, 'event')

        assert async_export_event_to_eventbrite.delay.call_args_list == [call(1)]
        self.assertEqual(self.bc.database.list_of('events.Event'), [event_db])
