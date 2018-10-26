import json
import flask
from flask import (
    Flask,
    request
)
import traceback
import logging
from http.client import responses
from flask.logging import default_handler
from .util import epoch_ms
from .config import get_config
from .auth import (
    validate_service_token,
    validate_user_token
)
from .exceptions import (
    MissingTokenError,
    InvalidTokenError,
    TokenLookupError,
    IllegalParameterError,
    MissingParameterError
)
from feeds.managers.notification_manager import NotificationManager
from feeds.activity.notification import Notification
from feeds.feeds.notification.notification_feed import NotificationFeed

VERSION = "0.0.1"


def _initialize_logging():
    root = logging.getLogger()
    root.addHandler(default_handler)
    root.setLevel('INFO')


def _log(msg, *args, level=logging.INFO):
    logging.getLogger(__name__).log(level, msg, *args)


def _log_error(error):
    formatted_error = ''.join(
        traceback.format_exception(
            etype=type(error),
            value=error,
            tb=error.__traceback__)
        )
    _log("Exception: " + formatted_error, level=logging.ERROR)


def _get_auth_token(request, required=True):
    token = request.headers.get('Authorization')
    if not token and required:
        raise MissingTokenError()
    return token


def _make_error(error, msg, status_code):
    _log("%s %s", status_code, msg)
    err_response = {
        "http_code": status_code,
        "http_status": responses[status_code],
        "message": msg,
        "time": epoch_ms()
    }
    return (flask.jsonify({'error': err_response}), status_code)


def _get_notification_params(params):
    """
    Parses and verifies all the notification params are present.
    Raises a MissingParameter error otherwise.
    """
    # * `actor` - a user or org id.
    # * `type` - one of the type keywords (see below, TBD (as of 10/8))
    # * `target` - optional, a user or org id. - always receives this notification
    # * `object` - object of the notice. For invitations, the group to be invited to.
    #   For narratives, the narrative UPA.
    # * `level` - alert, error, warning, or request.
    # * `content` - optional, content of the notification, otherwise it'll be
    #   autogenerated from the info above.
    # * `global` - true or false. If true, gets added to the global notification feed
    #   and everyone gets a copy.

    if not isinstance(params, dict):
        raise IllegalParameterError('Expected a JSON object as an input.')
    required_list = ['actor', 'verb', 'target', 'object', 'level']
    missing = [r for r in required_list if r not in params]
    if missing:
        raise MissingParameterError("Missing parameter{} - {}".format(
            "s" if len(missing) > 1 else '',
            ", ".join(missing)
        ))
    # TODO - add more checks
    return params


def create_app(test_config=None):
    _initialize_logging()
    cfg = get_config()

    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.before_request
    def preprocess_request():
        _log('%s %s', request.method, request.path)
        pass

    @app.after_request
    def postprocess_request(response):
        _log('%s %s %s %s', request.method, request.path, response.status_code,
             request.headers.get('User-Agent'))
        return response

    @app.route('/', methods=['GET'])
    def root():
        return flask.jsonify({
            "service": "Notification Feeds Service",
            "version": VERSION,
            "servertime": epoch_ms()
        })

    @app.route('/api/V1/notifications', methods=['GET'])
    def get_notifications():
        # TODO: add filtering
        """
        General flow should be:
        1. validate/authenticate user
        2. make user feed object
        3. query user feed for most recent, based on params
        """
        # dummy code below
        max_notes = request.args.get('n', default=10, type=int)
        rev_sort = request.args.get('rev', default=0, type=int)
        rev_sort = False if rev_sort == 0 else True
        # level_filter = request.args.get('f', default=None, type=str)
        include_seen = request.args.get('seen', default=1, type=int)
        include_seen = False if include_seen == 0 else True
        # return json.dumps({
        #     "max_notes": max_notes,
        #     "rev_sort": rev_sort,
        #     "level_filter": level_filter,
        #     "include_seen": include_seen
        # })
        user_id = validate_user_token(_get_auth_token(request))
        _log('Getting feed for {}'.format(user_id))
        feed = NotificationFeed(user_id)
        notes = feed.get_notifications(count=max_notes)
        return_list = list()
        for note in notes:
            return_list.append(note.user_view())
        return (flask.jsonify(return_list), 200)

    @app.route('/api/V1/notification/<note_id>', methods=['GET'])
    def get_single_notification(note_id):
        raise NotImplementedError()

    @app.route('/api/V1/notifications/unsee', methods=['POST'])
    def mark_notifications_unseen():
        """Form data should have a list of notification ids to mark as unseen"""
        raise NotImplementedError()

    @app.route('/api/V1/notifications/see', methods=['POST'])
    def mark_notifications_seen():
        """Form data should have a list of notifications to mark as seen"""
        raise NotImplementedError()

    @app.route('/api/V1/notification', methods=['POST', 'PUT'])
    def add_notification():
        """
        Adds a new notification for other users to see.
        Form data requires the following:
        * `actor` - a user or org id.
        * `type` - one of the type keywords (see below, TBD (as of 10/8))
        * `target` - optional, a user or org id. - always receives this notification
        * `object` - object of the notice. For invitations, the group to be invited to.
            For narratives, the narrative UPA.
        * `level` - alert, error, warning, or request.
        * `content` - optional, content of the notification, otherwise it'll be
            autogenerated from the info above.
        * `global` - true or false. If true, gets added to the global notification
            feed and everyone gets a copy.

        This also requires a service token as an Authorization header.
        Once validated, will be used as the Source of the notification,
        and used in logic to determine which feeds get notified.
        """
        if not cfg.debug:
            token = _get_auth_token(request)
            service = validate_service_token(token)  # can also be an admin user
            if not service:
                raise InvalidTokenError("Token must come from a service, not a user!")
        params = _get_notification_params(json.loads(request.get_data()))
        # create a Notification from params.
        new_note = Notification(
            params.get('actor'),
            params.get('verb'),
            params.get('object'),
            params.get('source'),
            params.get('level'),
            target=params.get('target'),
            context=params.get('context')
        )
        # pass it to the NotificationManager to dole out to its audience feeds.
        manager = NotificationManager()
        manager.add_notification(new_note)
        # on success, return the notification id and info.
        return (flask.jsonify({'id': new_note.id}), 200)

    @app.errorhandler(IllegalParameterError)
    @app.errorhandler(json.JSONDecodeError)
    def handle_illegal_parameter(err):
        _log_error(err)
        return _make_error(err, "Incorrect data format", 400)

    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token(err):
        _log_error(err)
        return _make_error(err, "Invalid token", 401)

    @app.errorhandler(MissingTokenError)
    def handle_missing_token(err):
        _log_error(err)
        return _make_error(err, "Authentication token required", 403)

    @app.errorhandler(404)
    def not_found(err):
        return _make_error(err, "Path {} not found.".format(request.path), 404)

    @app.errorhandler(405)
    def handle_not_allowed(err):
        _log_error(err)
        return _make_error(err, "Method not allowed", 405)

    @app.errorhandler(MissingParameterError)
    def handle_missing_params(err):
        _log_error(err)
        return _make_error(err, str(err), 422)

    @app.errorhandler(TokenLookupError)
    def handle_auth_service_error(err):
        _log_error(err)
        return _make_error(err, "Unable to fetch authentication information", 500)

    @app.errorhandler(Exception)
    def general_error(err):
        _log_error(err)
        return _make_error(err, str(err), 500)

    return app


app = create_app()
