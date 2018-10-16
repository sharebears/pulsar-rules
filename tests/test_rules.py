from conftest import add_permissions, check_json_response
from core import cache
from rules import RulePermissions


def test_get_sections(app, authed_client):
    add_permissions(app, RulePermissions.VIEW)
    response = authed_client.get('/rules').get_json()
    assert 'golden' in {d['id'] for d in response['response']}
    assert isinstance(response['response'], list)


def test_get_rules(app, authed_client):
    add_permissions(app, RulePermissions.VIEW)
    response = authed_client.get('/rules/golden').get_json()
    assert isinstance(response['response'], dict)
    assert 'id' in response['response']
    assert response['response']['rules'][0]['rules'][0]['number'] == '1.1'


def test_get_rules_nonexistent(app, authed_client):
    add_permissions(app, RulePermissions.VIEW)
    response = authed_client.get('/rules/nonexistent')
    check_json_response(response, 'nonexistent is not a valid section of the rules.')


def test_get_rules_cache(app, authed_client, monkeypatch):
    add_permissions(app, RulePermissions.VIEW)
    authed_client.get('/rules/golden')  # cache
    monkeypatch.setattr('rules.os', None)
    response = authed_client.get('/rules/golden').get_json()
    assert isinstance(response['response'], dict)
    assert 'id' in response['response']
    assert response['response']['rules'][0]['rules'][0]['number'] == '1.1'
    assert cache.get('rules_golden')
    assert cache.ttl('rules_golden') is None
