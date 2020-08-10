import json
import random

import requests
from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from libs.captcha.captcha import captcha
from utils import constants
from utils.response_code import RETCODE


class ImageCodeView(View):
    """图形验证码"""

    def get(self, request):
        # 生成图片验证码
        _, text, image = captcha.generate_captcha()
        # print(text)
        url = 'https://oss.crowncrystalhotel.com/resource/image_temporary/upload'
        files = {'attach': ('text.png', image)}
        r = requests.post(url, files=files)
        print(type(r.json()))
        image_url = r.json()["complete"]

        context = {
            'code': 200,
            'data': {
                'text': text,  # 分页后数据
                'image_url': image_url
            }
        }
        return http.HttpResponse(json.dumps(context))


class SMSCodeView(View):
    """短信验证码"""

    def get(self, reqeust, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        # 创建连接到redis的对象
        redis_conn = get_redis_connection('code')
        # 获取redis中的数据
        send_sms_flag = redis_conn.get('sms2_%s' % mobile)
        # 判断redis中是否有数据，60秒倒计时
        if send_sms_flag:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '发送短信过于频繁'})

        # 生成短信验证码：生成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # 发送短信验证码
        url = 'http://sms.crowncrystalhotel.com/v1/authentication/ht/sms/send_auth_code/'
        headers = {
            "content-type": "application/json"
        }
        request_data = {
            "phone_number": mobile,
            "code": sms_code
        }
        r = requests.post(url, headers=headers,
                          data=json.dumps(request_data))

        # 保存短信验证码
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        redis_conn.setex('sms2_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES2, sms_code)

        print(">>>>短信验证码>>>>>>", sms_code)

        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})
