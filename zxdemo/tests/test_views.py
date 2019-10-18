from __future__ import absolute_import, unicode_literals

import unittest

from django.conf import settings
from django.test import TestCase

from demoscene.models import Releaser
from parties.models import Party
from platforms.models import Platform
from productions.models import Production


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestHome(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        pondlife = Production.objects.get(title='Pondlife')
        pondlife.screenshots.create(thumbnail_url='http://example.com/pondlife.thumb.png')

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestShowScreenshot(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        pondlife = Production.objects.get(title='Pondlife')
        screen = pondlife.screenshots.create(thumbnail_url='http://example.com/pondlife.thumb.png')

        response = self.client.get('/screens/%d/' % screen.id)
        self.assertEqual(response.status_code, 200)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestProductions(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        response = self.client.get('/productions/')
        self.assertEqual(response.status_code, 200)

    def test_get_noscreen(self):
        response = self.client.get('/productions/?noscreen=1')
        self.assertEqual(response.status_code, 200)

    def test_get_letter(self):
        response = self.client.get('/productions/?letter=Q')
        self.assertEqual(response.status_code, 200)

    def test_get_bad_count(self):
        response = self.client.get('/productions/?count=lots')
        self.assertEqual(response.status_code, 200)

    def test_get_empty_page(self):
        response = self.client.get('/productions/?page=9999')
        self.assertEqual(response.status_code, 200)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestReleasesRedirect(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get_music(self):
        response = self.client.get('/releases.php?filter=6')
        self.assertRedirects(response, '/productions/?music=', status_code=301)

    def test_get_demos(self):
        response = self.client.get('/releases.php?filter=5')
        self.assertRedirects(response, '/productions/?demos=', status_code=301)

    def test_get_gfx(self):
        response = self.client.get('/releases.php?filter=3')
        self.assertRedirects(response, '/productions/?graphics=', status_code=301)

    def test_invalid(self):
        response = self.client.get('/releases.php?filter=potato')
        self.assertRedirects(response, '/productions/?', status_code=301)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestProduction(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        pondlife = Production.objects.get(title='Pondlife')

        response = self.client.get('/productions/%d/' % pondlife.id)
        self.assertEqual(response.status_code, 200)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestProductionRedirect(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        pondlife = Production.objects.get(title='Pondlife')
        pondlife.links.create(link_class='ZxdemoItem', parameter='42')

        response = self.client.get('/item.php?id=42')
        self.assertRedirects(response, '/productions/%d/' % pondlife.id, status_code=301)

    def test_bad_id(self):
        response = self.client.get('/item.php?id=potato')
        self.assertEqual(response.status_code, 404)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestAuthors(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        response = self.client.get('/authors/')
        self.assertEqual(response.status_code, 200)

    def test_get_letter(self):
        response = self.client.get('/authors/?letter=Y')
        self.assertEqual(response.status_code, 200)

    def test_bad_count(self):
        response = self.client.get('/authors/?count=potato')
        self.assertEqual(response.status_code, 200)

    def test_bad_page(self):
        response = self.client.get('/authors/?page=potato')
        self.assertEqual(response.status_code, 200)

    def test_empty_page(self):
        response = self.client.get('/authors/?page=9999')
        self.assertEqual(response.status_code, 200)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestAuthor(TestCase):
    fixtures = ['tests/gasman.json']

    def setUp(self):
        self.gasman = Releaser.objects.get(name='Gasman')
        self.hprg = Releaser.objects.get(name='Hooy-Program')

    def test_get_scener(self):
        Production.objects.get(title='Madrielle').credits.create(
            nick=self.gasman.primary_nick, category='Code'
        )
        response = self.client.get('/authors/%d/' % self.gasman.id)
        self.assertEqual(response.status_code, 200)

    def test_get_group(self):
        response = self.client.get('/authors/%d/' % self.hprg.id)
        self.assertEqual(response.status_code, 200)

    def test_get_missing(self):
        response = self.client.get('/authors/999999/')
        self.assertEqual(response.status_code, 404)

    def test_get_noscreen(self):
        response = self.client.get('/authors/%d/?noscreen=1' % self.gasman.id)
        self.assertEqual(response.status_code, 200)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestAuthorRedirect(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        gasman = Releaser.objects.get(name='Gasman')
        gasman.external_links.create(link_class='ZxdemoAuthor', parameter='42')

        response = self.client.get('/author.php?id=42')
        self.assertRedirects(response, '/authors/%d/' % gasman.id, status_code=301)

    def test_bad_id(self):
        response = self.client.get('/author.php?id=potato')
        self.assertEqual(response.status_code, 404)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestParties(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        response = self.client.get('/parties/')
        self.assertEqual(response.status_code, 200)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestPartyYear(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        response = self.client.get('/parties/2000/')
        self.assertEqual(response.status_code, 200)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestPartyCalendarRedirect(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        response = self.client.get('/partycalendar.php')
        self.assertRedirects(response, '/parties/', status_code=301)

    def test_get_year(self):
        response = self.client.get('/partycalendar.php?year=2000')
        self.assertRedirects(response, '/parties/2000/', status_code=301)

    def test_bad_year(self):
        response = self.client.get('/partycalendar.php?year=patarty')
        self.assertRedirects(response, '/parties/', status_code=301)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestParty(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        forever = Party.objects.get(name='Forever 2e3')
        response = self.client.get('/party/%d/' % forever.id)
        self.assertEqual(response.status_code, 200)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestPartyRedirect(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        forever = Party.objects.get(name='Forever 2e3')
        forever.external_links.create(link_class='ZxdemoParty', parameter='123')
        response = self.client.get('/party.php?id=123')
        self.assertRedirects(response, '/party/%d/' % forever.id, status_code=301)

    def test_bad_id(self):
        response = self.client.get('/party.php?id=patarty')
        self.assertEqual(response.status_code, 404)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestRss(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        response = self.client.get('/rss/')
        self.assertEqual(response.status_code, 200)


@unittest.skipIf(settings.ROOT_URLCONF != 'zxdemo.urls', "not running zxdemo environment")
class TestSearch(TestCase):
    fixtures = ['tests/gasman.json']

    def test_get(self):
        response = self.client.get('/search/?search=gasman&demoskip=zzz&musicskip=zzz&gfxskip=zzz&scenerskip=zzz')
        self.assertEqual(response.status_code, 200)

    def test_demo_paging(self):
        zx = Platform.objects.get(name='ZX Spectrum')
        for i in range(1, 20):
            prod = Production.objects.create(title="Dupa Biskupa part %d" % i, supertype='production')
            prod.platforms.add(zx)

        response = self.client.get('/search/?search=dupa&demoskip=5')
        self.assertEqual(response.status_code, 200)

    def test_music_paging(self):
        zx = Platform.objects.get(name='ZX Spectrum')
        for i in range(1, 20):
            prod = Production.objects.create(title="Oxygene %d" % i, supertype='music')
            prod.platforms.add(zx)

        response = self.client.get('/search/?search=oxygene&musicskip=5')
        self.assertEqual(response.status_code, 200)

    def test_gfx_paging(self):
        zx = Platform.objects.get(name='ZX Spectrum')
        for i in range(1, 20):
            prod = Production.objects.create(title="Vallejo valkyrie chick %d" % i, supertype='graphics')
            prod.platforms.add(zx)

        response = self.client.get('/search/?search=vallejo&gfxskip=5')
        self.assertEqual(response.status_code, 200)

    def test_scener_paging(self):
        zx = Platform.objects.get(name='ZX Spectrum')
        for i in range(1, 20):
            prod = Production.objects.create(title="Dupa Biskupa part %d" % i, supertype='production')
            releaser = Releaser.objects.create(name="razor %d" % i, is_group=True)
            prod.platforms.add(zx)
            prod.author_nicks.add(releaser.primary_nick)

        response = self.client.get('/search/?search=razor&scenerskip=5')
        self.assertEqual(response.status_code, 200)