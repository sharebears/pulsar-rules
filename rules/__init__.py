import json
import os

import flask

from core import APIException, cache
from core.permissions import PermissionsEnum
from core.utils import require_permission

bp = flask.Blueprint('rules', __name__)


class RulePermissions(PermissionsEnum):
    VIEW = 'rules_view'


SECTIONS = [
    {
        'id': 'golden',
        'name': 'Golden Rules',
        'description': 'These are the big rules. Break them and suffer.',
    }
]

SECTION_NAMES = {d['id'] for d in SECTIONS}


def init_app(app):
    app.register_blueprint(bp)


def get_rules(section: str) -> dict:
    if section not in SECTION_NAMES:
        raise APIException(f'{section} is not a valid section of the rules.')
    rules = cache.get(f'rules_{section}')
    if not rules:
        filename = os.path.join(os.path.dirname(__file__), f'{section}.json')
        with open(filename, 'r') as f:
            rules = json.load(f)
        cache.set(f'rules_{section}', rules, 0)
    return rules


@bp.route('/rules', methods=['GET'])
@require_permission(RulePermissions.VIEW)
def rules_view_overview() -> flask.Response:
    """
    View a list of rule sections. Requires the ``rules_view`` permission.

    .. :quickref: Rules; Get rule sections.

    **Example request**:

    .. parsed-literal::

       GET /rules HTTP/1.1
       Host: pul.sar
       Accept: application/json

    **Example response**:

    .. parsed-literal::

       HTTP/1.1 200 OK
       Vary: Accept
       Content-Type: application/json

       {
         "status": "success",
         "response": [
            "golden",
            "upload"
         ]
       }

    :>json list response: The list of rule sections

    :statuscode 200: Rules returned
    :statuscode 403: User does not have permission
    """
    return flask.jsonify(SECTIONS)


@bp.route('/rules/<section>', methods=['GET'])
@require_permission(RulePermissions.VIEW)
def rules_view(section: str) -> flask.Response:
    """
    View a section of rules. Requires the ``rules_view`` permission.

    .. :quickref: Rules; Get a rule section.

    **Example request**:

    .. parsed-literal::

       GET /rules/golden HTTP/1.1
       Host: pul.sar
       Accept: application/json

    **Example response**:

    .. parsed-literal::

       HTTP/1.1 200 OK
       Vary: Accept
       Content-Type: application/json

       {
         "status": "success",
         "response": {
           "1": {
             "1": {
               "main": "Do not create more than one account.",
               "more": "Users are allowed one account per lifetime."
             },
             "2": {
               "main": "Do not trade, sell, give away, or offer accounts.",
               "more": "If you no longer wish to use your account, send a Staff PM."
             },
           },
           "2": {
             "1": {
               "main": "Do not invite bad users.",
               "more": "You are responsible for your invitees."
             }
           }
         }
       }

    :>json dict response: The dictionary representation of the rules

    :statuscode 200: Rule section returned
    :statuscode 403: User does not have permission
    """
    return flask.jsonify(get_rules(section))
