from flask import *
import sqlite3
from flask import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/add_student")
def add_student():
    return render_template("add_student.html")

@app.route("/saverecord",methods = ["POST","GET"])
def saveRecord():
    msg = "msg"
    if request.method == "POST":
        try:
            photo = request.form["phnum"]
            name = request.form["name"]
            email = request.form["mail"]
            file = request.form["file"]

            with sqlite3.connect("Photons.db") as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT into Photons (photo, name, email, file) values (?,?,?,?)",(photo, name, email, file))
                connection.commit()
                msg = "Student detials successfully Added"
        except:
            connection.rollback()
            msg = "We can not add Student detials to the database"
        finally:
            return render_template("success_record.html",msg = msg)
            connection.close()



@app.route("/delete_student")
def delete_student():
    return render_template("delete_student.html")



@app.route("/student_info")
def student_info():
    connection = sqlite3.connect("Photons.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select * from Photons")
    rows = cursor.fetchall()
    return render_template("student_info.html",rows = rows)



@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("Photons.db") as connection:

        cursor = connection.cursor()
        cursor.execute("select * from Photons where photo=?", (id,))
        rows = cursor.fetchall()
        if not rows == []:
            cursor.execute("delete from Photons where photo = ?",(id,))
            msg = "Student detial successfully deleted"
            return render_template("delete_record.html", msg=msg)
        else:
            msg = "can't be deleted"
            return render_template("delete_record.html", msg=msg)

@app.route("/send_image")
def sendpic():
    return render_template("send_image.html")

@app.route("/send",methods = ["POST"])
def sendimage():
    id = request.form["id"]
    connection = sqlite3.connect("Photons.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select * from Photons where photo =?",(id,))
    rows = cursor.fetchall()
    return render_template("image_found.html", rows=rows)

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        mail = request.form['fmail']
        f = request.files['file']
        f.save(f.filename)

        fromaddr = "dhanvenkat07@gmail.com"
        toaddr = mail

        # instance of MIMEMultipart
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Andromeda 2022"
        body = "Hi,\nWe have attached the image that you took on the Photo Expo\n\nWith Regards,\nPhotons"
        msg.attach(MIMEText(body, 'plain'))
        filename = f.filename;
        attachment = open(f.filename, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "sevendhoni")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()

        return render_template("success.html", name=f.filename)

if __name__ == "__main__":
    app.run(debug = True)  
