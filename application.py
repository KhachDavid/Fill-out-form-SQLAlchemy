from flask import Flask, render_template, request
from participant import db, Participant
from flask_mail import Mail, Message

app = Flask(__name__)

db.init_app(app)

app.config.from_pyfile('config.cfg')
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://serob:Txa_1234@serob.mysql.pythonanywhere-services.com/serob$participants'
mail = Mail(app)

app.secret_key = 'b11223344AaadD$$r.,IIr]]tP[tu@urr'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        alert = ""
        return render_template('index.html', alert=alert)

    name = request.form.get("name")
    surname = request.form.get("surname")
    email = request.form.get("email")
    passport = request.form.get("passport")
    address = request.form.get("address")
    profession = request.form.get("profession")
    participant = Participant(firstname=name, lastname=surname, email=email, passport=passport,
                             address=address, profession=profession)
    db.session.add(participant)
    db.session.commit()
    alert = f"Դուք Գրանցված եք!! Ստուգեք ձեր էլեկտրոնային հասցեն {email}"

    msg = Message('Confirm Email', sender='esdavitnem@gmail.com', recipients=[email])
    msg.body = f"Հարգելի {name}, \n\nՁեր հայտը ընդունված է: \nԽնդրում եմ ստորև ստուգեք ձեր տվյալները;\n\nԱնձնագիր- {passport}\nՀասցե- {address} \n\nՎճարում կատարելու համար 1 օրվա ընթացքում կատարել փոխանցում հետևյալ հաշվեհամարին՝ Հայէկոնոմբանկ Սպանդարյանի մասնաճյուղ, 163048123489, Անհատ ձեռնարկատեր Սերոբ Խաչատրյան։ Վճարման նպատակը՝ դասընթացի մասնակցության մուտքավճար։\n\nԼավագnւյն Մաղթանքներով,\nՍերոբ"
    mail.send(msg)

    return render_template('index.html', alert=alert)


if __name__ == "__main__":
    app.run()
