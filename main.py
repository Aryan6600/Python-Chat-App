import signal
import PyQt5.QtWidgets as qtw
import firebase_admin
import firebase_admin.db

cred_obj = firebase_admin.credentials.Certificate('python-chat-app-517c1-firebase-adminsdk-z8ubq-2164f3f907.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://python-chat-app-517c1-default-rtdb.firebaseio.com/'
})

ref = firebase_admin.db.reference("/msg")


data=ref.get()

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        self.setFixedSize(800,600)
        screen_layout = qtw.QVBoxLayout()
        screen_wrapper = qtw.QWidget()
        screen_wrapper.setStyleSheet("background:#4a4a4a;")
        screen_wrapper.setLayout(screen_layout)
        
        msg_scrolling_container = qtw.QScrollArea()
        msg_scrolling_container.setWidgetResizable(True)
        msg_container = qtw.QWidget()
        msg_layout = qtw.QVBoxLayout()
        msg_container.setLayout(msg_layout)
        
        msg_scrolling_container.setWidget(msg_container)
        
        bottom_bar = qtw.QWidget()
        bottom_bar_layout = qtw.QHBoxLayout()
        bottom_bar.setLayout(bottom_bar_layout)
        
        msg_edit = qtw.QLineEdit()
        msg_edit.setStyleSheet('color:white;padding:5px;border:1px solid white;border-radius:5px;outline:1px solid white;font-size:18px;line-height:1.2em;')
        send_btn = qtw.QPushButton("Send Message -> ",clicked=lambda:send_msg())
        send_btn.setStyleSheet("padding:8px;color:white;background:transparent;border-radius:5px;border:1px solid white;")
        bottom_bar_layout.addWidget(msg_edit)
        bottom_bar_layout.addWidget(send_btn)

        screen_layout.addWidget(msg_scrolling_container)
        screen_layout.addWidget(bottom_bar)
        
        self.setCentralWidget(screen_wrapper)
        
        if data!=None:
            for i in data:
                msg_layout.addWidget(Message(data[i]["from"],data[i]["to"],data[i]["msg"]))
            
        else:
            msg_layout.addWidget(Message("System","You","No Messages to Display ! \n Try Sending a Message..."))
            
        def listener(event):
            if event.event_type=="put" and event.data !="" and event.path !="/":
                print(event.data)
                data = event.data
                signal.signal(signal.SIGALRM,add_msg(data))
                signal.alarm(0)
                
        firebase_admin.db.reference("/msg").listen(listener)
        
        def add_msg(data):
            msg_layout.addWidget(Message(data["from"],data["to"],data["msg"]))
    
        
        def send_msg():
            msg = msg_edit.text()
            if msg!="":
                ref.push({"from":"Someone","to":"Someone","msg":msg,"date":2})
                msg_edit.setText("")
        
class Message(qtw.QWidget):
    def __init__(self,msg_from,msg_to,message):
        super(Message,self).__init__()
        from_label = qtw.QLabel(f"from {msg_from}")
        to_label = qtw.QLabel(f"to {msg_to}")
        layout = qtw.QHBoxLayout()
        v_layout = qtw.QVBoxLayout()
        self.setLayout(v_layout)
        wrapper = qtw.QWidget()
        wrapper.setLayout(layout)
        layout.addWidget(from_label)
        layout.addWidget(to_label)
        wrapper.setMaximumHeight(50)
        self.layout().addWidget(wrapper)
        msg = qtw.QLabel(message)
        msg.setWordWrap(True)
        msg.setStyleSheet("color:white;")
        to_label.setStyleSheet("color:white;")
        from_label.setStyleSheet("color:white;")
        
        msg_scroller = qtw.QScrollArea()
        msg_scroller.setWidgetResizable(True)
        msg_scroller_layout = qtw.QHBoxLayout()
        msg_scroller.setLayout(msg_scroller_layout)
        msg_scroller.setWidget(msg)
        
        self.layout().addWidget(msg_scroller)
        self.setStyleSheet('background:#1f1f1f;padding:5px;border-radius:5px;')

        self.setFixedWidth(400)
        self.setFixedHeight(200)
        

app = qtw.QApplication([])
mw = MainWindow()
app.exec_()