import datetime
import re
from flask import Flask
from flask import render_template
from flask import request

def in_time(date,regular):
    regular_split = regular.split(",")
    for i in regular_split:
        if "-" in i:
            rang = i.split("-")
            if int(rang[0]) <= date <= int(rang[1]):
                return True
        else:
            if date == int(i):
                return True
    else:
        return False
    
def classTable():
    date = datetime.date.today() - datetime.date(2020,8,23)
    week = date.days//7
    class_table=[]
    with open("class.html", "r", encoding="utf-8") as f:
        html_class = f.read()
    class_form = re.search('<table id="KebiaoTable1" cellpadding="0" style="border-collapse: collapse" border="1" bordercolor="#000000">.*?</table>', html_class, re.DOTALL).group(0).replace(" ", "").replace("\n", "")
    class_tr = re.findall('<tr>(.*?)</tr>', class_form)
    class_time =re.findall("<td.*?>(.*?)</td>", class_tr[1])
    class_table.append(class_time)
    for i in range(2,len(class_tr)):
        class_table.append([])
        class_td = re.findall('<tdclass="style1.*?">(.*?)</td>', class_tr[i])
        for j in class_td:
            class_dl = re.findall("<dl>(.*?)</dl>", j)
            if class_dl:
                for k in class_dl:
                    class_dd = re.findall("<dd>(.*?)</dd>", k)
                    class_week = re.match(r"(.*?)\(", class_dd[1])
                    if in_time(week, class_week.group(1)):
                        class_name = re.search("<ahref=.*?>(.*?)</a>", k).group(1)
                        class_teacher = class_dd[0]
                        class_room = re.search("<b>(.*?)</b>", class_dd[1]).group(1)
                        class_info=f"{class_name}@{class_teacher}@{class_room}"
                        class_table[-1].append(class_info)
            else:
                class_table[-1].append("")
    return class_table

if __name__ == "__main__":
    app = Flask(__name__)

    @app.route("/")
    def index():
        classtable=classTable()
        return render_template("index.html", classtable=classtable, n=len(classtable[0]))

    @app.route("/upload", methods=['POST'])
    def upload():
        f = request.files['file']
        f.save('class.html')
        return "OK"
    app.run(port=5001)