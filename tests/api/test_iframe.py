import unittest

from selenium.common.exceptions import StaleElementReferenceException
from helium import find_all, S, Text, get_driver
from tests.api import BrowserAT

class IframeTest(BrowserAT):
	def get_page(self):
		return "test_iframe/main.html"
	def test_test_text_in_iframe_exists(self):
		self.assertTrue(Text("This text is inside an iframe.").exists())
	def test_text_in_nested_iframe_exists(self):
		self.assertTrue(Text("This text is inside a nested iframe.").exists())
	def test_finds_element_in_parent_iframe(self):
		self.test_text_in_nested_iframe_exists()
		# Now we're "focused" on the nested IFrame. Check that we can still
		# find the element an the parent IFrame:
		self.test_test_text_in_iframe_exists()
	def test_access_attributes_across_iframes(self):
		text = Text("This text is inside an iframe.")
		self.assertEqual("This text is inside an iframe.", text.value)
		get_driver().switch_to.default_content()
		self.assertEqual("This text is inside an iframe.", text.value)
	#@unittest.skip("breaks other tests?? TODO FIXME")
	def test_iframe_text_web_element_attributes(self):
		found_elements = find_all(Text('This text is inside an iframe.'))
		self.assertEqual(len(found_elements), 1)
		for elem in found_elements:
			self.assertEqual(elem.value, 'This text is inside an iframe.')
			self.assertEqual(elem.web_element.text, 'This text is inside an iframe.')
			self.assertEqual(elem.web_element.tag_name, 'body')
	#@unittest.skip("breaks other tests?? TODO FIXME")
	def test_s_iframe_web_element_properties_in_default_content(self):
		found_elements = find_all(S('iframe'))
		self.assertEqual(len(found_elements), 2)
		caughtExceptionCount = 0
		for elem in found_elements:
			try:
				# can't access selenium WebElement properties in the wrong frame context
				get_driver().switch_to.default_content()
				self.assertEqual(elem.web_element.tag_name, 'iframe')
			except StaleElementReferenceException:
				caughtExceptionCount += 1
		self.assertEqual(caughtExceptionCount, 1)
	#@unittest.skip("breaks other tests?? TODO FIXME")
	def test_s_iframe_web_element_properties_checking_target_frame(self):
		found_elements = find_all(S('iframe'))
		self.assertEqual(len(found_elements), 2)
		for elem in found_elements:
			# can't access selenium WebElement properties in the wrong frame context
			get_driver().switch_to.default_content()
			if not elem.target_frame:
				self.assertEqual(elem.web_element.tag_name, 'iframe')
			elif elem.target_frame:
				with self.assertRaises(StaleElementReferenceException):
					self.assertEqual(elem.web_element.tag_name, 'iframe')
	#@unittest.skip("breaks other tests?? TODO FIXME")
	def test_s_iframe_web_element_properties_switch_to_target_frame(self):
		found_elements = find_all(S('iframe'))
		self.assertEqual(len(found_elements), 2)
		for elem in found_elements:
			elem.switch_to_target_frame()
			self.assertEqual(elem.web_element.tag_name, 'iframe')
			iframe_src = elem.web_element.get_attribute('src')
			self.assertTrue(iframe_src.endswith('iframe.html'))
	#@unittest.skip("breaks other tests?? TODO FIXME")
	def test_s_body_web_element_properties_across_frames(self):
		found_elements = find_all(S('body'))
		self.assertEqual(len(found_elements), 3) # main page and 2 iframes
		get_driver().switch_to.default_content()
		try:
			caughtExceptionCount = 0
			for elem in found_elements:
				try:
					# can't access selenium WebElement properties in the wrong frame context
					self.assertEqual(elem.web_element.tag_name, 'body')
				except StaleElementReferenceException:
					caughtExceptionCount += 1
			self.assertEqual(caughtExceptionCount, 2)
			for elem in found_elements:
				elem.switch_to_target_frame()
				self.assertEqual(elem.web_element.tag_name, 'body')
				if elem.web_element.text:
					self.assertTrue(elem.web_element.text.startswith('This text is inside a'))
		finally:
			get_driver().switch_to.default_content()
