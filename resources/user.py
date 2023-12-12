from flask import request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restful import Resource
from mysql.connector import Error
import datetime
from email_validator import validate_email, EmailNotValidError
from mysql_connection import get_connection
from utils import check_password, hash_password

class UserRegisterResource(Resource) :
    def post(self) :

        #1. 클라이언트가 보낸 데이터를 받는다.
        data = request.get_json()

        #{
            #"username" : "홍길동",
            #"email" : "abc@naver.com",
            #"password":"1234"
        #}

        # 2. 이메일 주소형식이 올바른지 확인한다.
        try :
            validate_email(data['email'])
        except EmailNotValidError as e :
            print(3)
            return {'error': str(e)}, 400
        #3. 비밀번호 길이가 유효한지 체크한다.
        #만약, 비번은 4자리 이상 14자리 이하라고 한다면
        #이런것을 여기서 체크한다.

        if len(data['password']) < 4 or len(data['password']) > 14 :
            return {'error':'비번길이가 올바르지 않습니다.'} , 400
        
        #4. 비밀번호를 암호화한다.
        password = hash_password(data['password'])
        
        print(password)
    
        #5. DB의 user 테이블에 저장
        try :
            connection = get_connection()

            query ='''insert into user
                    (email, password, nickname, gender)
                    values
                    (%s, %s,%s,%s);'''
            
            record = (data['email'],
                      password,
                      data['nickname'],
                      data['gender']
                      )
            
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            ### 테이블에 방금 insert한 데이터의 아이디를 가져오는 방법
            user_id = cursor.lastrowid
            
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)}, 500
        #6. user 테이블의 id로
        # JWT 토큰을 만들어야 한다.
        access_token = create_access_token(user_id)

        #7. 토큰을 클라이언트에게 준다. response
        return {'result' : 'success',
                'access_token' : access_token}, 200
    
class UserLoginResource(Resource) :
    
    def post(self) :
        data = request.get_json()

        try : 
            connection = get_connection()

            query = '''select *
                    from user
                    where email = %s;'''
            record = (data['email'], )

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)}, 500
        
        if len(result_list) == 0 :
            return{'error' : '회원가입 먼저 하십시오.'}, 400
        
        check = check_password(data['password'], result_list[0]['password'])

        if check == False:
            return {'error' :'비번이 틀립니다.'}, 400
        
        access_token = create_access_token(result_list[0]['id'])

        
        return {'result' :'success',
                'accessToken' : access_token}, 200
    
jwt_blocklist = set()
class UserLogoutResource(Resource) :

    @jwt_required()
    def delete(self) :

        jti = get_jwt()['jti']
        print(jti)
        
        jwt_blocklist.add(jti)

        return {"result" : "success"}, 200