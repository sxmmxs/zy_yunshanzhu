from django import http
from django.db import DatabaseError
from django.views import View
from django_redis import get_redis_connection

from apps.user.models import User
from utils.response_code import RETCODE


class UserView(View):
    """提交"""

    def post(self, request):
        # 获取数据
        username = request.POST.get("username")
        mobile = request.POST.get("mobile")
        sms = request.POST.get("sms")
        company = request.POST.get("company")
        consulting = request.POST.get("consulting")
        print(username, mobile, sms)
        # 判断数据是否完整
        if not all([username, mobile, sms]):
            print("*" * 30)
            return http.JsonResponse({'code': RETCODE.MissingData, 'errmsg': '缺少数据'})
        # 链接redis数据库
        redis_conn = get_redis_connection('code')
        sms_code_saved = redis_conn.get('sms_%s' % mobile)
        # 判断验证码是否过期
        if sms_code_saved is None:
            return http.JsonResponse({'code': RETCODE.CaptchaNotExist, 'errmsg': '验证码已过期'})
        # 判断验证码是否有误
        if sms != sms_code_saved.decode():
            return http.JsonResponse({'code': RETCODE.VerificationError, 'errmsg': '你输入的短信验证码有误，请重新输入'})
        # 保存数据
        try:
            user = User.objects.create(username=username, mobile=mobile, company=company, consulting=consulting)
        except DatabaseError:
            return http.JsonResponse({'code': RETCODE.SubmitFailure, 'errmsg': '提交失败，请重试'})
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '提交成功'})
