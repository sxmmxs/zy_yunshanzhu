class RETCODE:
    OK = "0"  # 成功
    VerificationError = "4001"  # 验证码错误
    THROTTLINGERR = "4002"  # 短信发送频繁
    MissingData = "4003"  # 缺少数据
    CaptchaNotExist = '4004'  # 验证码不存在
    SubmitFailure = '4005'  # 提交失败
