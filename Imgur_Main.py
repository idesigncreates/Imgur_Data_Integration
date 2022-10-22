import requests
import json
import pyodbc

def establish_connection():
    server = 'SCALEUPLAPTOP25\SQLEXPRESS'
    database= 'Imgur'
    # u_id = 'BCX_Tarsem'
    # password = 'tarsem123'
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=' + server + ';'
                          'Database=' + database + ';'
                          'Trusted_Connection=Yes;')
    return conn


# conn = establish_connection()
# print(conn)

def access_t():
    try:
        conn = establish_connection()
        cursor = conn.cursor()
        cursor.execute('select accessT from access_imgur')
        # conn.close()  
        for row in cursor:
            row_to_list = [elem for elem in row]
        return(row_to_list)
    except:
        cursor.rollback()
    finally:
        print('Got '+ row_to_list[0] + ' as Access Token from DB')
        cursor.close()
        conn.close()
        print('Connection Closed')

# d = access_k
# print(d)
def refresh_t():
    try:
        conn = establish_connection()
        cursor = conn.cursor()
        cursor.execute('select refreshT from access_imgur')
        # conn.close()
        for row in cursor:
            row_to_list = [elem for elem in row]
        return(row_to_list)
    except:
        cursor.rollback()
    finally:
        print('Got '+ row_to_list[0]+ ' as Refresh Token from DB')
        cursor.close()
        conn.close()
        print('Connection Closed')
    
access_T = access_t()
refresh_T = refresh_t()
# print(access_T)
# print(refresh_T)
# # for row in cursor:
# #     print('row = %r' % (row,))
# print(refresh_T[0])



url = "https://api.imgur.com/oauth2/token"
payload={'refresh_token': refresh_T[0] ,
'client_id': '029e3e62a6377a6',
'client_secret': '2a913961cf4866d44dd3393f902a4dfb8eefc875',
'grant_type': 'refresh_token'}
files=[]
headers = {
  'Authorization': 'Bearer '+ access_T[0]  
}

# response = requests.request("POST", url, headers=headers, data=payload, files=files)


def get_access(url,headers,payload,files):
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    access=json.loads(response.text)
    return access


# test = get_access(url,headers,payload,files)
# print(access_T)
# print(refresh_T)
# print(test)


def update_tokens():
    try:
        cred = get_access(url,headers,payload,files)
        # print(cred)
        new_access_token = list(cred.values())[0]
        new_refresh_token = list(cred.values())[4]

        type(new_access_token)
        # print(new_refresh_token)
        conn = establish_connection()
        cursor = conn.cursor()
        query = "update access_imgur set accessT = ?, refreshT = ?, created_at = getdate()"
        cursor.execute(query,(new_access_token,new_refresh_token))  #token update
        conn.commit()
    except:
        cursor.rollback()
    finally:
        print('Updated Access Token is ' + new_access_token+ ' and Refresh Token is ' + new_refresh_token)
        cursor.close()
        conn.close()
        print('Connection Closed')
    
update_tokens()
        
