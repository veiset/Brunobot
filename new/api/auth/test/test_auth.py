import unittest
import test.mock as mock
import api.auth.auth as auth

class AuthAPITEST(unittest.TestCase):
    
    def setUp(self):
        self.authAPI = auth.Auth(mock.Bot())
        self.WILDCARD = self.authAPI.WILDCARD
        self.ADMIN = self.authAPI.ADMIN

    def test_that_adding_an_user_adds_the_user_to_all_lists(self):
        self.authAPI.add('vz','~vz','veiset.org', self.authAPI.FOUNDER)
        assert 'vz' in self.authAPI.authNick
        assert len(self.authAPI.authNick['vz']) == 1
        assert '~vz' in self.authAPI.authIdent
        assert len(self.authAPI.authIdent['~vz']) == 1
        assert 'veiset.org' in self.authAPI.authHost
        assert len(self.authAPI.authHost['veiset.org']) == 1

    def test_that_wildcard_is_taken_as_wildcard(self):

        user1 = auth.AuthUser('vz', '~vz', 'veiset.org', self.ADMIN)

        user2 = auth.AuthUser(self.WILDCARD, '~vz', 'veiset.org', self.ADMIN)
        user3 = auth.AuthUser('vz', self.WILDCARD, 'veiset.org', self.ADMIN)
        user4 = auth.AuthUser('vz', '~vz', self.WILDCARD, self.ADMIN)

        user5 = auth.AuthUser(self.WILDCARD, self.WILDCARD, 'veiset.org', self.ADMIN)
        user6 = auth.AuthUser('vz', self.WILDCARD, self.WILDCARD, self.ADMIN)
        user7 = auth.AuthUser(self.WILDCARD, self.WILDCARD, self.WILDCARD, self.ADMIN)

        assert user1.equals(user1)
        assert user1.equals(user2)
        assert user1.equals(user3)
        assert user1.equals(user4)
        assert user1.equals(user5)
        assert user1.equals(user6)
        assert user1.equals(user7)

    def test_that_different_users_are_not_same(self):
        user1 = auth.AuthUser('vz', '~vz', 'host.org', self.ADMIN)
        user2 = auth.AuthUser(self.WILDCARD, '~vz', 'veiset.org', self.ADMIN)
        
        assert not user1.equals(user2)

    def test_that_removing_a_user_removes_it_from_all_lists(self):
        self.authAPI.add('vz','~vz','veiset.org', self.authAPI.FOUNDER)
        self.authAPI.remove('vz','~vz','veiset.org')
        assert len(self.authAPI.authNick['vz']) == 0
        assert len(self.authAPI.authIdent['~vz']) == 0
        assert len(self.authAPI.authHost['veiset.org']) == 0

    def test_that_same_user_with_different_user_level_is_different(self):
        user1 = auth.AuthUser('vz', '~vz', 'veiset.org', self.ADMIN)
        user2 = auth.AuthUser('vz', '~vz', 'veiset.org', self.authAPI.USER)

        assert user1.equals(user2)
        

    def test_that_auth_level(self):
        self.authAPI.add('vz','~vz','veiset.org', self.ADMIN)
        assert self.authAPI.isAuthed('vz','~vz','veiset.org', self.authAPI.ADMIN)
        assert self.authAPI.isAuthed('vz','~vz','veiset.org', self.authAPI.USER)
        assert not self.authAPI.isAuthed('vz','~vz','veiset.org', self.authAPI.FOUNDER)


    def test_wildcard_auth_level(self):
        self.authAPI.add('vz','~vz','veiset.org', self.ADMIN)
        self.authAPI.add('brbot','~vz','veiset.org', self.WILDCARD)

        assert self.authAPI.isAuthed('vz', self.WILDCARD, self.WILDCARD, self.ADMIN)
        assert not self.authAPI.isAuthed('nobody', self.WILDCARD, self.WILDCARD, self.ADMIN)
        assert self.authAPI.isAuthed('brbot', '~vz', 'veiset.org', self.ADMIN)

