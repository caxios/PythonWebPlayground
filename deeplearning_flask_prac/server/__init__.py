"""딥러닝 서비스 배포용 앱(웹서버)"""

from flask import Flask
import config

# 서버가 호출되면 __init__.py이 실행되며 웹앱을 초기화해주는 거임
def create_app()->Flask:
    '''서비스용 앱 생성'''
    app = Flask(__name__) # 플라스크 객체(앱의 백엔드) 생성
    app.config.from_object(config) # 플라스크 객체에 설정(configuration)파일 등록


    # 각각의 파일에서 만든 Blueprint 객체를 flask에 등록
    from .views import main_views
    app.register_blueprint(
        main_views.bp,
    )

    return app