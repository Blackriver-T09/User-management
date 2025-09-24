import unittest
from flask import Flask

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app  # 确保从你的应用模块中导入 Flask 实例

class TestCheckCreditsAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.url = '/api/Check-credits'
        self.token = '3*gh$mgbvsx1#tky*@b#s8rxedh?#o'  # 移到这里来定义

    # 测试没有提供 token 的情况
    def test_missing_token(self):
        response = self.client.post(self.url, json={'credits': 100})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'logic': False, 'message': 'please offer token'})


    # 测试没有提供 credits 的情况
    def test_missing_credits(self):
        response = self.client.post(self.url, json={'token': self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'logic': False, 'message': 'please offer credits'})

    # 测试 credits 不足的情况
    def test_insufficient_credits(self):
        response = self.client.post(self.url, json={'token': self.token, 'credits': 500})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'logic': False, 'message': 'Insufficient remaining credits'})

    # 测试 credits 足够的情况
    def test_successful_credit_check(self):
        response = self.client.post(self.url, json={'token': self.token, 'credits': 50})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'logic': True, 'message': None})

    # # 测试数据库错误
    # def test_database_error(self):
    #     response = self.client.post(self.url, json={'token': self.token, 'credits': 100})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json, {'logic': False, 'message': "An internal error occurred. Please try again."})

    # # 测试意外错误
    # def test_unexpected_error(self):
    #     response = self.client.post(self.url, json={'token': 'wrong_token', 'credits': 100})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json, {'logic': False, 'message': "An unexpected error occurred. Please try again."})

if __name__ == '__main__':
    unittest.main()
