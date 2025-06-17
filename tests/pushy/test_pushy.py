import os

import pytest

from config import PushyConfig
from pkg.notification.pushy_api import NotificationService
from pkg.scopus import Article


def get_article() -> Article:
    data = {
        '@_fa': 'true',
        'link': [
            {
                '@_fa': 'true',
                '@ref': 'self',
                '@href': 'https://api.elsevier.com/content/abstract/scopus_id/105005016947'
            }, {
                '@_fa': 'true',
                '@ref': 'author-affiliation',
                '@href': 'https://api.elsevier.com/content/abstract/scopus_id/105005016947?field=author,affiliation'
            }, {
                '@_fa': 'true',
                '@ref': 'scopus',
                '@href': 'https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=105005016947&origin=inward'
            }, {
                '@_fa': 'true',
                '@ref': 'scopus-citedby',
                '@href': 'https://www.scopus.com/inward/citedby.uri?partnerID=HzOxMe3b&scp=105005016947&origin=inward'
            }, {
                '@_fa': 'true',
                '@ref': 'full-text',
                '@href': 'https://api.elsevier.com/content/article/eid/1-s2.0-S2666038520000122'
            }
        ],
        'prism:url': 'https://api.elsevier.com/content/abstract/scopus_id/105005016947',
        'dc:identifier': 'SCOPUS_ID:105005016947',
        'eid': '2-s2.0-105005016947',
        'dc:title': 'In the Case of Theme: Topic Identifiers in English and Norwegian Academic Texts',
        'dc:creator': 'Hasselgård H.',
        'prism:publicationName': 'Contrastive Pragmatics',
        'prism:issn': '26660385',
        'prism:eIssn': '26660393',
        'prism:volume': '1',
        'prism:issueIdentifier': '1',
        'prism:pageRange': '108-135',
        'prism:coverDate': '2020-01-01',
        'prism:coverDisplayDate': '2020',
        'prism:doi': '10.1163/26660393-12340001',
        'citedby-count': '0',
        'affiliation': [
            {
                '@_fa': 'true',
                'affilname': 'Universitetet i Oslo',
                'affiliation-city': 'Oslo',
                'affiliation-country': 'Norway'
            }
        ],
        'prism:aggregationType': 'Journal',
        'subtype': 'ar',
        'subtypeDescription': 'Article',
        'source-id': '21101077304',
        'openaccess': '1',
        'openaccessFlag': True,
        'freetoread': {
            'value': [
                {
                    '$': 'all'
                },
                {
                    '$': 'publisherfullgold'
                },
                {
                    '$': 'repository'
                },
                {
                    '$': 'repositoryvor'
                }
            ]
        },
        'freetoreadLabel': {
            'value': [
                {
                    '$': 'All Open Access'
                },
                {
                    '$': 'Gold'
                },
                {
                    '$': 'Green'
                }
            ]
        }
    }

    return Article.model_validate(data)


async def test_pushy_send():
    key = os.getenv("PUSHY_FEED")
    if not key:
        pytest.skip("PUSHY_FEED not set in environment")
    notification_service = NotificationService(config=PushyConfig(feed=key))
    await notification_service.send_notifications({"eng": [get_article()]})
