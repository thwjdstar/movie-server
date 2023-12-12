from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

class MovieListResource(Resource):
  
    def get(self) :

        #1. 클라이언트로부터 데이터를 받아온다.
        # 없다.

        #2. 디비에 저장된 데이터를 가져온다.
        try :
            connection = get_connection()
            query = '''select * 
                        from movie;'''
            # 중요!!!
            # select문에서!!! 커서를 만들때에는 
            # 파라미터 dictionary = True로 해준다.
            # 왜? 리스트와 딕셔너리 형태로 가져오기 때문에
            # 클라이언트에게 json 형식으로 보내줄수 있다.

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)

            result_list = cursor.fetchall()

            print(result_list)

            #datetime은 파이썬에서 사용하는 데이터타입이므로
            #JSON형식이 아니다. 따라서 JSON은 문자열이나 숫자만 가능하므로
            #datetime을 문자열로 바꿔줘야한다.
            
            i=0
            for row in result_list :
               result_list[i]['year'] = row['year'].isoformat()
               result_list[i]['createAt'] = row['createAt'].isoformat()
               i = i+1
            
            print()
            print(result_list)
            print()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            #클라이언트에게 에러라고 보내줘야 한다.
            return{"result":"fail","error":str(e)},500
        

        return {"result" : "success", 
                "items" : result_list, 
                "count" : len(result_list) }, 200