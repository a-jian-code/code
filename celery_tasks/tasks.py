import os
import time

from django.template import loader
from django_redis import get_redis_connection
from goods.models import GoodsType, IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from celery import Celery
from dailyfresh import settings
from django.core.mail import send_mail

# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE","dailyfresh.settings")
# django.setup()

#创建一个Celery类的实例对象
app=Celery('celery_tasks.tasks',broker='redis://172.16.16.113:6379/8')

@app.task
def send_register_active_email(to_email,token):
    subject = '天天生鲜欢迎信息'
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>尊敬的用户您好，您已成功注册天天生鲜账户，请于24小时之内点击以下链接激活您的账户<h1><br><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
    token, token)
    send_mail(subject=subject, message='', from_email=sender, recipient_list=receiver, html_message=html_message)
    time.sleep(5)

@app.task
def generate_static_index_html():
    # 获取商品的种类信息
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    for type in types:  # GoodsType
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners



    # 组织模板上下文
    context = {'type': types,
               'goods_banners': goods_banners,
               'promotion_banners': promotion_banners,
               }

    # 使用模板
    # 1.加载模板文件,返回模板对象
    temp = loader.get_template('static_index.html')
    # 2.定义模板上下文
    # context = RequestContext(request, context)
    # 3.模板渲染
    static_index_html = temp.render(context)

    # 生成首页对应的静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')

    with open(save_path, 'w') as f:
        f.write(static_index_html)