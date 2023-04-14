from flask import Flask, request, abort, render_template, jsonify
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, date
#============================
from models.OriganizeForFun import *
from models.OriganizeForCompetition import *
from models.DisplayActivity import *
from models.AddToGroup import *
from models.CancelFromGroup import *
from models.DrawLots import *
#from models.test import *
#======MySQL的函數庫==========

app = Flask(__name__)
#######################################################
##app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
##app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{username}:{password}@localhost:3306/{database}?charset=utf8"
##db = SQLAlchemy(app)
#######################################################
exec(open("secret.py").read())
global group1
group1 = 'C1de13fe7df6a1421fc631c7bc9f379f9'
group2 = 'Cc978f60556f64edc516f4c648226754f'
group3 = 'Caf7add7528e34b5b746829d18a183bd9'


class Product(db.Model):
        __tablename__='TableAllDatas'
        pid = db.Column(db.Integer, primary_key=True)
        group_id = db.Column(db.String(50), unique=False, nullable=True)
        time = db.Column(db.DATE)
        description = db.Column(db.TEXT, nullable=True)
        participater = db.Column(db.TEXT, nullable=True)
        insert_time = db.Column(db.DateTime, default=datetime.now)
        update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

        def __init__(self, group_id, time, description, participater):
                self.group_id = group_id
                self.time = time
                self.description = description
                self.participater = participater

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
################################
# Channel Access Token
##line_bot_api = LineBotApi('')
# Channel Secret
##handler = WebhookHandler('')
################################

#監聽所有來自 /callback 的 Post Request
#######
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400, "Invalid signature. Please check your channel access token/channel secret.")
    return "OK" 

@app.route("/")
def hello():
    db.create_all()  
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    return "Hello Flask!"

#########
#處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    weekday_change ={0:"(一)", 1:"(二)", 2:"(三)", 3:"(四)", 4:"(五)", 5:"(六)",6:'(日)'} 
    db.create_all()
    msg = event.message.text
    part_list = ''
    act_info = ''
    if '!開團' in msg[:3]:
#        message = TextSendMessage(OgzFF1(event))#Organize For fun
        group_id = event.source.group_id
        msg = msg.split(";",3)
#        test1 = Product(group_id,"2023-4-13","Max")
        test1 = Product(group_id,msg[1],msg[2],f',{msg[3]},')
        db.session.add(test1)
        db.session.commit()
        message = TextSendMessage(text="開團成功")
        line_bot_api.reply_message(event.reply_token, message)#

    elif '!比賽' in msg[:3]:
        message = TextSendMessage(OgzFC(event))#Organize For Competition
#        message = TextSendMessage(text="設定成功")
        line_bot_api.reply_message(event.reply_token, message)#

    elif '!活動' in msg[:3]:
#        message = TextSendMessage(DspAtt(event))#Display Activity
#        values = Product.query.all()
        values = Product.query.filter(Product.time>=datetime.today(), Product.group_id == event.source.group_id)
        message = ''
        for item in values:
             item.participater = item.participater.split(",")
             item.description = item.description.split(",")
         
             item.participater =[z for z in item.participater if z!=""]
             for x in item.participater:
                  part_list = part_list + (f"{item.participater.index(x)+1}.{x}\n")
             for y in item.description :
                  act_info = act_info +(f"{y}\n")
             message = message + (f"{item.time} {weekday_change[item.time.weekday()]}\n{act_info}----------------------------- \n{part_list}\n")
             part_list = ''
             act_info = ''
        if message == '':
             message = "No 活動"
        message = TextSendMessage(message)
#        message = TextSendMessage(text="顯示成功")
        line_bot_api.reply_message(event.reply_token, message)#

    elif '!抽籤' in msg[0:3]:
        message = TextSendMessage(DL(event))#Add To Group
#        message = TextSendMessage(text="報名成功")
        line_bot_api.reply_message(event.reply_token, message)#
   
    elif '+' in msg[0]:
        tmp_list = ''
        check_list = ''
        check_item= ("1","")
#        message = TextSendMessage(ATG(event))#Add To Group
        values = Product.query.filter(Product.time>=datetime.today(), Product.group_id == event.source.group_id)
        for item in values:
             part_list = item.participater
#        message = TextSendMessage(part_list)
        if msg[1:] not in check_item:
            tmp_list = tmp_list + msg[1:]+","
        else: 
            uid = event.source.user_id
            gid = event.source.group_id
            profile = line_bot_api.get_group_member_profile(gid, uid)
            name = profile.display_name
            tmp_list = tmp_list +name +","
        if tmp_list in part_list:
            message = TextSendMessage(text="報名過了哦")
        else:
            part_list = part_list + tmp_list
            get_today = date.today()
            values = Product.query.filter(Product.time>=get_today, Product.group_id == event.source.group_id).update({'participater':part_list})
            db.session.commit()
            message = TextSendMessage(text="報名成功")
        line_bot_api.reply_message(event.reply_token, message)#
        part_list = ''
        tmp_list = ''
    elif '-' in msg[0]:
#        message = TextSendMessage(CFG(event))#cancel from Group
        tmp_list = ''
        del_list = ''
        check_list = ''
        check_item= ("1","")
        name = ''
#        message = TextSendMessage(ATG(event))#Add To Group
        values = Product.query.filter(Product.time>=datetime.today(), Product.group_id == event.source.group_id)
        for item in values:
             part_list = item.participater
#        message = TextSendMessage(part_list)
        if msg[1:] not in check_item:
            tmp_list = tmp_list+","+ msg[1:]+","
            del_list = del_list + msg[1:] + ","
            print(del_list) 
        else: 
            uid = event.source.user_id
            gid = event.source.group_id
            profile = line_bot_api.get_group_member_profile(gid, uid)
            name = profile.display_name
            tmp_list = tmp_list +","+ name+","
            del_list = del_list+  msg[1:] + ","
            print(del_list)  
#            if part_list.find(tmp_list) > 2:
#                tmp_list = tmp_list+"," + name 
#            else:
#                tmp_list =" "+ tmp_list+name+","
        if tmp_list not in part_list:
            message = TextSendMessage(text="你沒有報名哦")
        else:
            part_list = part_list.replace(del_list,"")
            get_today = date.today()
            values = Product.query.filter(Product.time>=get_today, Product.group_id == event.source.group_id).update({'participater':part_list})
            db.session.commit()
            message = TextSendMessage(text="取消成功")
        line_bot_api.reply_message(event.reply_token, message)#
        part_list = ''
        tmp_list = ''
#        message = TextSendMessage(text="取消成功")
        line_bot_api.reply_message(event.reply_token, message)#
###############        
    elif '&' in msg[0]:
        test3()
#        message = TextSendMessage(text="取消成功")
        line_bot_api.reply_message(event.reply_token, message)#
    if '~' in msg[0]:
        message = TextSendMessage(text=f'"!開團"可以開團中間用;分隔，範例如下：\n!開團;2023-4-13;時間1430,地點:台南高商,人數:上限27、未滿14流團;名字(可不輸入)\n\n使用"!活動"可以看開團的活動\n\n使用"+"、"+1"、"+人名"可以報名\n\n使用"-"、"-1"、"-人名"可以取消報名\n\n目前還沒處理的問題:\n1.兩個群組開同一團\n2.一個群組開兩團以上\n3.人數到達上限之後轉項目欄轉成候補')
        line_bot_api.reply_message(event.reply_token, message)#
    elif '#' in msg[0]:
        uid = event.source.user_id
        gid = event.source.group_id
#        profile = line_bot_api.get_profile(uid)
        profile = line_bot_api.get_group_member_profile(gid, uid)
        name = profile.display_name
#        message = TextSendMessage(text=f'{name}')
        message = TextSendMessage(text=f'{name}')
#        message = TextSendMessage(text=f'{event.source.group_id}')
        line_bot_api.reply_message(event.reply_token, message)#
#    elif '!' in msg[0]:
#        message = TextSendMessage(text=f'{event.message.text}')
#        line_bot_api.reply_message(event.reply_token, message)#

#    elif '$' in msg[0]:
#        uid = event.source.user_id
#        profile = line_bot_api.get_profile(uid)
        
#        name = profile.display_name
#        describution = event.message.text
#        test1 = Product(f'{name}', f'{describution}')
#        db.session.add(test1)
#        db.session.commit()
#        message = TextSendMessage(text=f'{name} input success')
#        line_bot_api.reply_message(event.reply_token, message)#
#    elif "^" in msg[0]:
#        values = Product.query.all()
#        printout = f''
#        for item in values:
#              printout = printout + (f'{item.pid} {item.name}{item.description}\n')
#        message = TextSendMessage(printout)
#        line_bot_api.reply_message(event.reply_token, message)#
    elif "DeleteAllDatasFromTable" in msg[:23]:
        db.drop_all()
        message = TextSendMessage("drop the table success")
        line_bot_api.reply_message(event.reply_token, message)#
    elif "DeleteDatasFromTableInThisGroup" in msg[:31]:
#        db.drop_all()
        Product.query.filter(Product.group_id == event.source.group_id).delete()
        db.session.commit()
        message = TextSendMessage("clean the talbe from this group success")
        line_bot_api.reply_message(event.reply_token, message)#
