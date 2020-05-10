from rest_framework.throttling import SimpleRateThrottle

class SMSRateThrottle(SimpleRateThrottle):
    scope = 'sms'

    #只对提交手机号的get方法进行限制
    def get_cache_key(self, request, view):
        mobile = request.query_params.get('mobile')
        #没有手机号就不做频率限制
        if not mobile:
            return None
        #返回的信息可以用手机号动态变化，且不易重复的字符串，作为缓存的key
        return 'throttle_%(scope)s_%(ident)s' % {'scope': self.scope, 'ident': mobile}