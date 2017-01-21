'''
Created on Jan 5, 2017

@author: taoprajjwal

If data not matched from database,, LoginFail().open()
'''
 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen,ScreenManager
import sqlite3
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.pagelayout import PageLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty


Builder.load_file('Main.kv')

class LoginFail(Popup):
    pass
class Home(Screen):
    def LogIn(self,username,password):
        passw=password.encode('utf-8')
        conn=sqlite3.connect('users.db')
        c=conn.cursor()
        c.execute('SELECT * FROM USERS WHERE Username=?',(username.encode('utf-8'),))
        enterpass=c.fetchone()
        conn.close()
        print(enterpass)
        if enterpass[2]==passw:
            s=Scre(enterpass[3])
            UserScreen.scre=s
            App.get_running_app().stop()
            UserScreen().run()
        else:
            LoginFail().open()
    
class MainApp(App):
    def build(self):
        return ScreenManage()
    def onstop(self):
        print('stopped')
        UserScreen().run()

class UserScreen(App):
    scre=ObjectProperty(None)
    def build(self):
        return self.scre
class ScreenManage(ScreenManager):
    def LogInSetup(self,blood):
        NextPage=Scre(blood)
        NextPage.name='lol'
        self.switch_to(NextPage)
class SignUp(Screen):
    def signup(self,username,password,age,btype,location):
        conn=sqlite3.connect('users.db')
        c=conn.cursor()
        c.execute('INSERT INTO USERS(Username,Password,BloodType,Location,Age) VALUES (?,?,?,?,?)',(username,password,btype,location,age))
        conn.commit()
        conn.close()
        print("LogIn Successful")
class Window(RelativeLayout):
    Pers_UID=StringProperty()
    Location=StringProperty()
    def __init__(self,name,loc,**kwargs):
        super(Window,self).__init__(**kwargs)
        self.Pers_UID=str(name)
        self.Location=str(loc)
class Paa(PageLayout):
    def __init__(self,BType,**kwargs):
        super(Paa,self).__init__(**kwargs)
        conn=sqlite3.connect('users.db')
        c=conn.cursor()
        c.execute('SELECT UID,Blood.BloodType,Blood.Location FROM Blood INNER JOIN USERS ON USERS.UserID=Blood.UID WHERE Blood.BloodType=?',(BType.encode('utf-8'),))
        d=c.fetchall()
        conn.close()
        for x in range(0,len(d)):
            self.add_widget(Window(d[x][0],d[x][2]))
class Scre(Screen):
    def __init__(self,Btype,**kwargs):
        super(Scre,self).__init__(**kwargs)
        self.add_widget(Paa(Btype))
                    
MainApp().run()
