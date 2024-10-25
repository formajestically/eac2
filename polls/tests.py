from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class MySeleniumTests(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		opts = Options()
		cls.selenium = WebDriver(options=opts)
		cls.selenium.implicitly_wait(5)

		# Creació de superusuari
		user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
		user.is_superuser = True
		user.is_staff = True
		user.save()

	@classmethod
	def tearDownClass(cls):
		cls.selenium.quit()
		super().tearDownClass()

	def test_create_staff_user_and_change_passwd_via_admin(self):
	#Test per crear un usuari amb permisos de staff i modificar la contrasenya
	#=========================================================================

		# 1. Accedir a la pàgina d'administració
		self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

		# 2. Comprovar que el títol de la pàgina és el que esperem
		self.assertEqual(self.selenium.title , "Log in | Django site admin")

		# 3. Iniciar sessió com a superusuari
		username_input = self.selenium.find_element(By.NAME, "username")
		username_input.send_keys("isard")
		password_input = self.selenium.find_element(By.NAME, "password")
		password_input.send_keys("pirineus")
		self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

		# 4. Testejar que hem entrat a l'admin panel comprovant el títol de la pàgina
		self.assertEqual(self.selenium.title , "Site administration | Django site admin")

		# 5. Accedir a la secció de gestió d'usuaris
		self.selenium.find_element(By.LINK_TEXT, "Users").click()

		# 6. Clicar en "+ Add user" per crear un nou usuari
		self.selenium.find_element(By.LINK_TEXT, "ADD USER").click()

		# 7. Omplir les dades del nou usuari
		username_input = self.selenium.find_element(By.NAME, "username")
		username_input.send_keys("jordi")
		password1_input = self.selenium.find_element(By.NAME, "password1")
		password1_input.send_keys("eac2-1234")
		password2_input = self.selenium.find_element(By.NAME, "password2")
		password2_input.send_keys("eac2-1234")
		self.selenium.find_element(By.XPATH, '//input[@value="Save and continue editing"]').click()

		# 8. Assignar permisos de staff a l'usuari
		staff_status_checkbox = self.selenium.find_element(By.XPATH,'//input[@type="checkbox" and @name="is_staff"]')
		if not staff_status_checkbox.is_selected():
			staff_status_checkbox.click()

		# 9. Desar l'usuari amb permisos de staff
		self.selenium.find_element(By.XPATH, '//input[@value="Save"]').click()

		# 10. Sortir del panell d'administració
		self.selenium.find_element(By.ID, 'logout-form').click()
		
		# 11. Tornar a la pàgina d'inici
		self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

		# 12. Comprovar que el títol de la pàgina és el que esperem
		self.assertEqual(self.selenium.title , "Log in | Django site admin")

		# 13. Iniciar sessió com a superusuari
		username_staff_input = self.selenium.find_element(By.NAME, "username")
		username_staff_input.send_keys("isard")
		password_staff_input = self.selenium.find_element(By.NAME, "password")
		password_staff_input.send_keys("pirineus")
		self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

		# 14. Testejar que hem entrat a l'admin panel comprovant el títol de la pàgina
		self.assertEqual(self.selenium.title, "Site administration | Django site admin")

		# 15. Accedir a la secció de gestió d'usuaris
		self.selenium.find_element(By.LINK_TEXT, "Users").click()

		# 16. Testejar que hem entrat a l'admin panel comprovant el títol de la pàgina
		self.assertEqual(self.selenium.title, "Select user to change | Django site admin")

		# 17. Comprovar que el nou usuari apareix a la llista d'usuaris
		#search_input = self.selenium.find_element(By.NAME, "q")
		#search_input.send_keys("jordi")
		#search_input.send_keys(Keys.RETURN)

		# 17. Comprovar que apareix el nom d'usuari 'jordi' en els resultats de la cerca
		self.assertIn("jordi", self.selenium.page_source)

		# 18. Entrar a l'usuari 'jordi'
		user_link = self.selenium.find_element(By.LINK_TEXT, "jordi")
		user_link.click()

		# 19. Testejar que hem entrat a l'usuari jordi comprovant el títol de la pàgina
		self.assertEqual(self.selenium.title, "jordi | Change user | Django site admin")

		# 20. Clicar en l'opció "Reset password"
		self.selenium.find_element(By.LINK_TEXT, "Reset password").click()

		# 21. Testejar que hem entrat al canvi de contrasenya de l'usuari jordi comprovant el títol de la pàgina
		self.assertEqual(self.selenium.title, "Change password: jordi | Django site admin")

		# 22. Omplir les dades de la nova contrasenya
		new_password1_input = self.selenium.find_element(By.NAME, "password1")
		new_password1_input.send_keys("eac206112024")
		new_password2_input = self.selenium.find_element(By.NAME, "password2")
		new_password2_input.send_keys("eac206112024")
		self.selenium.find_element(By.XPATH, '//input[@value="Change password"]').click()

		# 23. Comprovar que la contrasenya s'ha desat correctament (per exemple, amb un missatge de confirmació)
		self.assertIn("Password changed successfully", self.selenium.page_source)

		# 24. Testejar element que no existeix
		try:
			self.selenium.find_element(By.XPATH, "//a[text()='Answers']")
			assert False, "Trobat element que no hi ha de ser"
		except NoSuchElementException:
			pass