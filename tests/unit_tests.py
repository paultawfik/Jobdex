"""
Unit tests UserApp, CardApp, and DocumentsApp.
"""

import unittest
import sys
import models

class TestUser(unittest.TestCase):
    """
    Unit tests for the User class (part of UserApp)
    """
    users = models.User()

    ####################
    ##                ##
    ##  USER SIGN UP  ##
    ##                ##
    ####################

    def testSignUp(self):
        """
        Test that signing up a user works.
        """
        self.assertEqual(models.SUCCESS, self.users.sign_up("userA", "myPassword", "myPassword", "userA@gmail.com"))

    def testSignUpDatabaseUpdates(self):
        """
        Test that the database reflects the newly signed up users.
        """
        models.User.objects.all().delete() # first delete all rows in database
        self.assertEqual(len(models.User.objects.all()), 0)
        self.users.sign_up("george", "myPassword", "myPassword", "george@berkeley.edu")
        self.assertEqual(len(models.User.objects.all()), 1)
        self.users.sign_up("necula", "myPassword", "myPassword", "necula@berkeley.edu")
        self.assertEqual(len(models.User.objects.all()), 2)

    def testSignUpEmptyUsername(self):
        """
        Test that signing up with an empty username fails.
        """
        self.assertEqual(models.FAILURE, self.users.sign_up("", "myPassword", "myPassword", "userA@gmail.com"))

    def testSignUpNoneUsername(self):
        """
        Test that signing up with a None object as the username fails.
        """
        self.assertEqual(models.FAILURE, self.users.sign_up(None, "myPassword", "myPassword", "userA@gmail.com"))

    def testSignUpLongUsername(self):
        """
        Test that signing up with a username that exceeds 128 characters fails.
        """
        original_username = "this_will_be_long"
        long_username = original_username*10
        self.assertEqual(models.FAILURE, self.users.sign_up(None, long_username, long_username, "userA@gmail.com"))

    def testSignUpEmptyPassword(self):
        """
        Test that signing up with an empty password fails.
        """
        self.assertEqual(models.FAILURE, self.users.sign_up("userB", "", "", "userB@gmail.com"))

    def testSignUpNonePassword(self):
        """
        Test that signing up with None as the password fails.
        """
        self.assertEqual(models.FAILURE, self.users.sign_up("userC", None, None, "userC@gmail.com"))

    def testSignUpLongPassword(self):
        """
        Test that signing up with a password that exceeds 128 characters fails.
        """
        original_password = "this_will_be_long"
        long_password = original_password*10
        self.assertEqual(models.FAILURE, self.users.sign_up("userD", long_password, long_password, "userD@gmail.com"))

    def testSignUpUnmatchingPasswords(self):
        """
        Test that signing up with a password that doesn't match the password_confirm field fails.
        """
        self.assertEqual(models.FAILURE, self.users.sign_up("userE", "ilovebears", "ihatebears", "userE@gmail.com"))

    def testSignUpInvalidEmail1(self):
        """
        Test that signing up with an invalid email address format (i.e. missing @ symbol) fails.
        """
        self.assertEqual(models.FAILURE, self.users.sign_up("userF", "myPassword", "myPassword", "userFgmail.com"))

    def testSignUpInvalidEmail2(self):
        """
        Test that signing up with an invalid email address format (i.e. missing a period) fails.
        """
        self.assertEqual(models.FAILURE, self.users.sign_up("userG", "myPassword", "myPassword", "userG@gmailcom"))

    def testSignUpInvalidEmail3(self):
        """
        Test that signing up with an invalid email address format (i.e. missing @ symbol and a period) fails.
        """
        self.assertEquals(models.FAILURE, self.users.sign_up("userH", "myPassword", "myPassword", "blahblahblah"))

    def testSignUpEmptyEmail(self):
        """
        Test that signing up with an empty email address fails.
        """
        self.assertEqual(models.FAILURE, self.users.sign_up("userI", "myPassword", "myPassword", ""))

    def testSignUpNoneEmail(self):
        """
        Test that signing up with email address as None fails.
        """
        self.assertEqual(models.FAILURE, self.users.sign_up("userJ", "myPassword", "myPassword", None))

    def testSignUpUserExists(self):
        """
        Tests that signing up with a username that already exists in the database fails.
        """
        self.assertEqual(models.SUCCESS, self.users.sign_up("userK", "myPassword", "myPassword", "userK@gmail.com"))
        self.assertEqual(models.FAILURE, self.users.sign_up("userK", "myPassword", "myPassword", "userK@gmail.com"))

    def testSignUpConsecutively(self):
        """
        Tests that signing up two users consecutively works.
        """
        self.assertEqual(models.SUCCESS, self.users.sign_up("userL", "myPassword", "myPassword", "userL@gmail.com"))
        self.assertEqual(models.SUCCESS, self.users.sign_up("userM", "myPassword", "myPassword", "userM@gmail.com"))

    def testSignUpNoneUsernameAndPassword(self):
        """
        Tests that signing up with both username AND password as None fails
        """
        self.assertEqual(models.FAILURE, self.users.sign_up(None, None, None, "both_none@gmail.com"))

    def testSignUpBlankUsernameAndPassword(self):
        """
        Tests that signing up with both a blank username AND password fails
        """
        self.assertEqual(models.FAILURE, self.users.sign_up("", "", "", "both_blank@gmail.com"))

    def testSignUpLongUsernameAndPassword(self):
        """
        Tests that signing up with both a long username AND long password fails
        """
        original_username = "this_will_be_long"
        long_username = original_username*10
        original_password = "this_will_also_be_long"
        long_password = original_password*10
        self.assertEqual(models.FAILURE, self.users.sign_up(long_username, long_password, long_password,
                                                            "both_long@gmail.com"))

    ###################
    ##               ##
    ##  USER LOG IN  ##
    ##               ##
    ###################

    def testLogin(self):
        """
        Tests that user login works for a valid username and password.
        """
        self.assertEqual(models.SUCCESS, self.users.sign_up("userN", "myPassword", "myPassword", "userN@gmail.com"))
        self.assertEqual(models.SUCCESS, self.users.login("userN", "myPassword"))

    def testLoginUserNonExistent(self):
        """
        Tests that user login fails with a username that doesn't exist in the database.
        """
        self.assertEqual(models.FAILURE, self.users.login("this_user_doesnt_exist", "myPassword"))

    def testLoginBadPassword(self):
        """
        Tests that user login fails with an existing username whose input password doesn't match the one in the database.
        """
        self.assertEqual(models.SUCCESS, self.users.sign_up("userO", "password", "password", "userO@gmail.com"))
        self.assertEqual(models.FAILURE, self.users.login("userO", "passw0rd"))

    def testLoginEmptyUsername(self):
        """
        Tests that user login fails with an empty username.
        """
        self.assertEqual(models.FAILURE, self.users.login("", "password"))

    def testLoginEmptyPassword(self):
        """
        Tests that user login fails with an empty password.
        """
        self.assertEqual(models.SUCCESS, self.users.sign_up("userP", "password", "password", "userP@gmail.com"))
        self.assertEqual(models.FAILURE, self.users.login("userP", ""))

    def testLoginNoneUsername(self):
        """
        Tests that user login fails with a None username.
        """
        self.assertEqual(models.FAILURE, self.users.login(None, "password"))

    def testLoginNonePassword(self):
        """
        Tests that user login fails with a None password.
        """
        self.assertEqual(models.SUCCESS, self.users.sign_up("userQ", "password", "password", "userQ@gmail.com"))
        self.assertEqual(models.FAILURE, self.users.login("userQ", None))

    def testLoginLongUsername(self):
        """
        Tests that user login fails with a username that exceeds 128 characters.
        """
        original_username = "this_will_be_long"
        long_username = original_username*10
        self.assertEqual(models.FAILURE, self.users.login(long_username, "password"))

    def testLoginLongPassword(self):
        """
        Tests that user login fails with a password that exceeds 128 characters.
        """
        original_password = "this_will_be_long"
        long_password = original_password*10
        self.assertEqual(models.FAILURE, self.users.login("userR", long_password))

    ####################
    ##                ##
    ##  USER LOG OUT  ##
    ##                ##
    ####################

    def testLogout(self):
        """
        Tests that user logout works.
        """
        self.assertEqual(models.SUCCESS, self.users.sign_up("paulina", "myPassword", "myPassword", "paulina@gmail.com"))
        self.assertEqual(models.SUCCESS, self.users.login("paulina", "myPassword"))
        self.assertEqual(models.SUCCESS, self.users.logout())

###############################################################################################################

class TestCard(unittest.TestCase):
    """
    Unit tests for the Card class (part of CardApp)
    """
    cards = models.Card()

    ###################
    ##               ##
    ##  CREATE CARD  ##
    ##               ##
    ###################

    def testCreateCard(self):
        """
        Tests that a card can be created.
        """
        self.assertEqual(models.SUCCESS, self.cards.create_card("Amazon", "Software Engineer", 2))

    def testCreateCardLongCompanyName(self):
        """
        Tests that creating a card with a company name that exceeds 128 characters fails.
        """
        long_name = "LongCompanyName"*10
        self.assertEqual(models.FAILURE, self.cards.create_card(long_name, "Software Engineer", 2))

    def testCreateCardEmptyCompanyName(self):
        """
        Tests that creating a card with an empty company name fails.
        """
        self.assertEqual(models.FAILURE, self.cards.create_card("", "Software Engineer", 2))

    def testCreateCardNoneCompanyName(self):
        """
        Tests that creating a card with a None company name fails.
        """
        self.assertEqual(models.FAILURE, self.cards.create_card(None, "Software Engineer", 2))

    def testCreateCardLongJobTitle(self):
        """
        Tests that creating a card with a job title that exceeds 128 characters fails.
        """
        long_title = "LongJobTitle"*10
        self.assertEqual(models.FAILURE, self.cards.create_card("Accenture", long_title, 2))

    def testCreateCardEmptyJobTitle(self):
        """
        Tests that creating a card with an empty job title fails.
        """
        self.assertEqual(models.FAILURE, self.cards.create_card("AirPR", "", 2))

    def testCreateCardNoneJobTitle(self):
        """
        Tests that creating a card with a None job title fails.
        """
        self.assertEqual(models.FAILURE, self.cards.create_card("Affirm", None, 2))

    def testCreateCardInvalidStatus(self):
        """
        Tests that creating a card with a status that is not 0, 1, or 2 fails.
        """
        self.assertEqual(models.FAILURE, self.cards.create_card("BrightRoll", "Software Engineer", 3))

    def testCreateCardsConsecutively(self):
        """
        Tests that consecutive cards of different statuses can be created.
        """
        self.assertEqual(models.SUCCESS, self.cards.create_card("Apple", "Software Engineer", 0))
        self.assertEqual(models.SUCCESS, self.cards.create_card("Airbnb", "Software Engineer", 1))
        self.assertEqual(models.SUCCESS, self.cards.create_card("Akamai", "Software Engineer", 2))

    ###################
    ##               ##
    ##  MODIFY CARD  ##
    ##               ##
    ###################

    def testModifyCard(self):
        """
        Tests that a card's status can be modified.
        """
        self.assertEqual(models.SUCCESS, self.cards.create_card("Boeing", "Mechanical Engineer", 1))
        card_id = models.Card.objects.get(name='Boeing').id
        self.assertEqual(models.SUCCESS, self.cards.modify_card_status(card_id, 0))

    def testModifyCardInvalidStatus(self):
        """
        Tests that a card's status can't be modified to an invalid status number.
        """
        self.assertEqual(models.SUCCESS, self.cards.create_card("Behance", "Web Developer", 1))
        card_id = models.Card.objects.get(name='Behance').id
        self.assertEqual(models.FAILURE, self.cards.modify_card_status(card_id, 3))

###############################################################################################################

class TestTag(unittest.TestCase):
    """
    Unit tests for the Tag class (part of CardApp)
    """
    tags = models.Tag()

    ###############
    ##           ##
    ##  ADD TAG  ##
    ##           ##
    ###############

    def testAddTag(self):
        """
        Tests that a tag between 1-128 characters can be added to an existing card.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("Capricity", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='Capricity').id
        self.assertEqual(models.SUCCESS, self.tags.add_tag(card_id, "tech"))

    def testAddTagLong(self):
        """
        Tests that adding a tag that exceeds 128 characters fails.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("CompanyA", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='CompanyA').id
        long_tag = "technologyrocksssss"*10
        self.assertEqual(models.FAILURE, self.tags.add_tag(card_id, long_tag))

    def testAddTagEmpty(self):
        """
        Tests that adding an empty tag fails.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("CompanyB", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='CompanyB').id
        self.assertEqual(models.FAILURE, self.tags.add_tag(card_id, ""))

    def testAddTagNone(self):
        """
        Tests that adding a None tag fails.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("CompanyC", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='CompanyC').id
        self.assertEqual(models.FAILURE, self.tags.add_tag(card_id, None))

    def testAddCardIDEmpty(self):
        """
        Tests that adding a tag to an empty card ID fails.
        """
        self.assertEqual(models.FAILURE, self.tags.add_tag("", "tech"))

    def testAddCardIDNone(self):
        """
        Tests that adding a tag to a None card ID fails.
        """
        self.assertEqual(models.FAILURE, self.tags.add_tag(None, "tech"))

    def testAddCardIDNonexistent(self):
        """
        Tests that adding a tag to a card that doesn't exist fails.
        """
        self.assertEqual(models.FAILURE, self.tags.add_tag(models.Card.objects.get(name='THIS_CARD_DOESNT_EXIST').id,
                                                           "tech"))

    ##################
    ##              ##
    ##  MODIFY TAG  ##
    ##              ##
    ##################

    def testModifyTag(self):
        """
        Tests that modifying a card's tag with a new tag between 1-128 characters succeeds.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("CompanyD", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='CompanyD').id
        self.assertEqual(models.SUCCESS, self.tags.add_tag(card_id, "tech"))
        self.assertEqual(models.SUCCESS, self.tags.modify_tag(card_id, "tech", "engineer"))

    def testModifyTagLong1(self):
        """
        Tests that modifying a card's tag with a new tag that exceeds 128 characters fails.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("CompanyE", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='CompanyE').id
        self.assertEqual(models.SUCCESS, self.tags.add_tag(card_id, "tech"))
        new_long_tag = "superlongtagahhhhhh"*10
        self.assertEqual(models.FAILURE, self.tags.modify_tag(card_id, "tech", new_long_tag))

    def testModifyTagLong2(self):
        """
        Tests that passing in a current_tag_name that is over 128 characters fails.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("CompanyF", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='CompanyF').id
        long_current_tag = "superlongtagahhhhhh"*10
        self.assertEqual(models.FAILURE, self.tags.modify_tag(card_id, long_current_tag, "shorter_tag"))

    def testModifyTagNonexistentCard(self):
        """
        Tests that modifying a tag on a card that doesn't exist fails.
        """
        self.assertEqual(models.FAILURE, self.tags.modify_tag(models.Card.objects.get(name='NONEXISTENT_COMPANY').id,
                                                              "hardware", "software"))

    def testModifyTagNonexistent(self):
        """
        Tests that passing in a current_tag_name that doesn't exist fails.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("CompanyG", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='CompanyG').id
        self.assertEqual(models.FAILURE, self.tags.modify_tag(card_id, "this_tag_doesnt_exist", "new_tag"))

    def testModifyTagDuplicate(self):
        """
        Tests that modifying a tag to one that already exists will fail.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("CompanyH", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='CompanyH').id
        self.assertEqual(models.SUCCESS, self.tags.add_tag(card_id, "tech"))
        self.assertEqual(models.SUCCESS, self.tags.add_tag(card_id, "engineer"))
        self.assertEqual(models.FAILURE, self.tags.modify_tag(card_id, "tech", "engineer"))

    ################
    ##            ##
    ##  GET TAGS  ##
    ##            ##
    ################

    def testGetTags(self):
        """
        Tests that it returns a list of tags associated with an existing card_id.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("CompanyI", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='CompanyI').id
        self.assertEqual(models.SUCCESS, self.tags.add_tag(card_id, "tech"))
        self.assertEqual(models.SUCCESS, self.tags.add_tag(card_id, "software"))
        self.assertEqual(models.SUCCESS, self.tags.add_tag(card_id, "engineer"))
        tags_list = ["tech", "software", "engineer"]
        self.assertEqual(tags_list, self.tags.get_tags(card_id))

    def testGetTagsInvalidCard(self):
        """
        Tests that it doesn't return a list of tags for a non-existent card id.
        """
        self.assertEqual(models.FAILURE, self.tags.get_tags("THIS_CARD_ID_DOESNT_EXIST"))

    ###################
    ##               ##
    ##  REMOVE TAGS  ##
    ##               ##
    ###################

    def testRemoveTagInvalidCard(self):
        """
        Tests that it fails to removes an existing tag from a non-existent card.
        """
        self.assertEqual(models.FAILURE, self.tags.remove_tag("THIS_CARD_ID_DOESNT_EXIST", "tech"))

    def testRemoveTagNonexistentTag(self):
        """
        Tests that it fails to removes a non-existent tag from an existing card.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("CompanyJ", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='CompanyJ').id
        self.assertEqual(models.SUCCESS, self.tags.add_tag(card_id, "software"))
        self.assertEqual(models.FAILURE, self.tags.remove_tag(card_id, "hardware"))

    def testRemoveTag(self):
        """
        Tests that it successfully removes an existing tag from an existing card.
        """
        self.assertEqual(models.SUCCESS, self.tags.create_card("CompanyK", "Software Engineer", 2))
        card_id = models.Card.objects.get(name='CompanyK').id
        self.assertEqual(models.SUCCESS, self.tags.add_tag(card_id, "tech"))
        self.assertEqual(models.SUCCESS, self.tags.remove_tag(card_id, "tech"))

###############################################################################################################

class TestDocuments(unittest.TestCase):
    """
    Unit tests for the Documents class (part of DocumentApp)
    """
    documents = models.Documents()

    ######################
    ##                  ##
    ##  REMOVE DOCUMENT ##
    ##                  ##
    ######################

    def testRemoveDocumentNonexistentID(self):
        """
        Tests that removing a document that doesn't exist will fail.
        """
        self.assertEqual(models.FAILURE, self.documents.remove_document("NONEXISTENT_DOCUMENT_ID"))

    def testRemoveDocumentNonexistentID(self):
        """
        Tests that removing a document id that
        """
        self.assertEqual(models.FAILURE, self.documents.remove_document("NONEXISTENT_DOCUMENT_ID"))

    ####################
    ##                ##
    ##  GET DOCUMENTS ##
    ##                ##
    ####################

    def testGetDocumentsNonexistentUser(self):
        """
        Tests that getting documents belonging to a non-existent user will fail.
        """
        self.assertEqual(models.FAILURE, self.documents.get_documents("NONEXISTENT_USER_ID"))

    def testGetDocumentsLongUsername(self):
        """
        Tests that passing in a user_id that exceeds 128 characters will fail.
        """
        long_user_id = "thisisasuperlonguserid"*10
        self.assertEqual(models.FAILURE, self.documents.get_documents(long_user_id))

###############################################################################################################

    ###############################
    ##                           ##
    ##  MISCELLANEOUS UNIT TESTS ##
    ##                           ##
    ###############################

    # def testResetFixture(self):
    #     """
    #     Test that resetting the database works
    #     """
    #     models.User.objects.all().delete()
    #     self.assertEqual(models.SUCCESS, self.users.sign_up("batman", "password", "password", "batman@gmail.com"))
    #     self.assertEqual(len(models.UsersModel.objects.all()), 1)
    #     models.User.objects.all().delete()
    #     self.assertEqual(len(models.UsersModel.objects.all()), 0)

# If this file is invoked as a Python script, run the tests in this module
if __name__ == "__main__":
    # Add a verbose argument
    sys.argv = [sys.argv[0]] + ["-v"] + sys.argv[1:]
    unittest.main()