import unittest
from app import create_app, db
from flask import json

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        # 创建一个测试客户端
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
        
        # 创建数据库和表
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # 清理数据库
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        # 测试用户注册
        response = self.client.post('/register', json={
            'fullname': 'testuser',
            'email': 'test@example.com',
            'institution': 'TestInstitute',
            'password': 'testpassword123',
            'confirm-password': 'testpassword123'
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['result'])

    def test_login_user(self):
        # 先注册一个用户
        self.client.post('/register', json={
            'fullname': 'testuser',
            'email': 'test@example.com',
            'institution': 'TestInstitute',
            'password': 'testpassword123',
            'confirm-password': 'testpassword123'
        })
        
        # 测试用户登录
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword123'
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['result'])
        self.assertIsNotNone(data.get('tokenTmp'))

if __name__ == '__main__':
    unittest.main()
