from util import settings


class CommandBase:
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        self._allowed_users = settings.get_allowed_users()
        event_dispatcher.add_listener(self._get_target_event(), self.execute)

    def execute(self, **kwargs):
        user = kwargs.get('user')

        if self._is_user_allowed(user):
            self._execute_allowed(user)
        else:
            self._execute_restricted(user)

    def _is_user_allowed(self, user):
        return str(user) in self._allowed_users.keys()

    def _execute_allowed(self, user):
        pass

    def _execute_restricted(self, user):
        self._event_dispatcher.dispatch(
            'send_message',
            user=user,
            text="Access denied. Please, use /myID command to get your ID and contact bot administrator"
        )

    def _get_target_event(self):
        pass


class Help(CommandBase):
    def _get_target_event(self):
        return 'command_help'

    def _execute_allowed(self, user):
        self._event_dispatcher.dispatch(
            'send_message',
            user=user,
            text="Available commands are /myID and /subscribe"
        )


class Subscribe(CommandBase):
    def _get_target_event(self):
        return 'command_subscribe'

    def _execute_allowed(self, user):
        self._event_dispatcher.dispatch('subscribe_user', user=user)
        self._event_dispatcher.dispatch('send_message', user=user, text='subscription is done')


class MyId(CommandBase):
    def _get_target_event(self):
        return 'command_my_id'

    def _execute_restricted(self, user):
        self._execute_allowed(user)

    def _execute_allowed(self, user):
        self._event_dispatcher.dispatch('send_message', user=user, text=f'{user}')
