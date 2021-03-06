import imp

from django.test import SimpleTestCase
from django.test.utils import override_settings
from django.template import Template, Context

import thumborize
from thumborize import ThumborURL


class ThumborizeTests(SimpleTestCase):

    def test_should_accept_filters_as_string(self):
        thumborized = thumborize.url("image.png",
                                     width=300,
                                     height=500,
                                     filters="quality(80):grayscale()")
        self.assertIn("quality(80)", thumborized)
        self.assertIn("grayscale()", thumborized)

    @override_settings(THUMBOR_DEFAULT_FILTERS={"brightness": "(40)"})
    def test_default_filters_should_be_applied(self):
        imp.reload(thumborize.conf)
        thumborized = thumborize.url("image.png")
        self.assertIn("brightness(40)", thumborized)

    @override_settings(THUMBOR_DEFAULT_FILTERS={"rgb": "(20,-20,40)", "round_corner": "(20,255,255,255)"})
    def test_default_filters_should_be_overridden_by_given_filters(self):
        imp.reload(thumborize.conf)
        thumborized = thumborize.url("image.png", filters="rbg(10,10,10)")
        self.assertNotIn("rbg(20,-20,40)", thumborized)
        self.assertIn("rbg(10,10,10)", thumborized)
        self.assertIn("round_corner(20,255,255,255)", thumborized)

    @override_settings(THUMBOR_DEFAULT_FILTERS={"grayscale": "()"})
    def test_resetting_default_filters_should_be_possible(self):
        imp.reload(thumborize.conf)
        thumborized = thumborize.url("image.png", reset_filters=True, filters="quality(80)")
        self.assertNotIn("grayscale()", thumborized)
        self.assertIn("quality(80)", thumborized)

    def test_should_be_able_to_add_filters_as_string(self):
        imp.reload(thumborize.conf)
        thumbor_url = ThumborURL("image.png")
        thumbor_url.add_filters("grayscale()")
        thumborized = thumbor_url.generate()
        self.assertIn("grayscale()", thumborized)

    def test_should_be_able_to_remove_filters_as_string(self):
        thumbor_url = ThumborURL("image.png", filters=["grayscale()", "quality(80)"])
        thumbor_url.remove_filters("grayscale")
        thumborized = thumbor_url.generate()
        self.assertNotIn("grayscale()", thumborized)
        self.assertIn("quality(80)", thumborized)

    def test_should_be_able_to_add_filters_as_kwargs(self):
        thumbor_url = ThumborURL("image.png")
        thumbor_url.add_filters(quality="(80)")
        thumborized = thumbor_url.generate()
        self.assertIn("quality(80)", thumborized)

    def test_thumbor_url_should_render_as_string_on_templates(self):
        thumbor_url = ThumborURL("image.png", width=400)
        template = Template("{{ url }}")
        context = Context({"url": thumbor_url})
        rendered = template.render(context)
        self.assertEqual(rendered, thumbor_url.generate())

    def test_should_be_able_to_apply_filters_by_method_calling(self):
        thumbor_url = ThumborURL("image.png")
        gray_image = thumbor_url.grayscale()
        self.assertIn("grayscale()", gray_image.generate())
        low_quality_image = thumbor_url.quality(30)
        self.assertIn("quality(30)", low_quality_image.generate())

    def test_apply_filters_by_method_calling_should_be_chainable(self):
        thumbor_url = ThumborURL("image.png")
        new_image = thumbor_url.grayscale().quality(30)
        self.assertIn("grayscale()", new_image.generate())
        self.assertIn("quality(30)", new_image.generate())

    def test_resizing_should_keep_not_overriden_dimensions(self):
        thumbor_url = ThumborURL("image.png", width=300, height=150)
        resized_image = thumbor_url.resize(width=150)
        self.assertEqual(resized_image.options["width"], 150)
        self.assertEqual(resized_image.options["height"], 150)
