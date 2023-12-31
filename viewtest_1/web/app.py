from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

db = SQLAlchemy()

#先設好Flask
#static_folder設置告訴Flask在哪裡查找靜態資源文件。
#static_url_path設置預設路徑
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)

# 主頁
@app.route("/")
def reserve():
    return render_template("reserve.html")

# 查看預約
@app.route("/view")
def view():
    return render_template("view.html")

# 變更預約
@app.route("/modify")
def modify():
    return render_template("modify.html")

# 即時狀況
@app.route("/now")
def now():
    return render_template("now.html")

# 處理預約資料
@app.route("/rdata", methods=["POST"])
def rdata():
    c_id = request.form.get("c_id")
    room = request.form.get("meetroom")
    start_year = request.form.get("start_year")
    start_month = request.form.get("start_month")
    start_date = request.form.get("start_date")
    start_hour = request.form.get("start_hour")
    start_minute = request.form.get("start_minute")
    end_year = request.form.get("end_year")
    end_month = request.form.get("end_month")
    end_date = request.form.get("end_date")
    end_hour = request.form.get("end_hour")
    end_minute = request.form.get("end_minute")

    print(f"c_id: {c_id}")
    print(f"room: {room}")
    print(f"r_start: {start_year,start_month,start_date,start_hour,start_minute}")
    print(f"r_end: {end_year,end_month,end_date,end_hour,end_minute}")

    # 建立回應資料
    response_data = {
        "c_id": c_id,
        "room": room,
        "r_start": start_year + "-" + start_month + "-" + start_date + " " + start_hour + ":" + start_minute,
        "r_end": end_year + "-" + end_month + "-" + end_date + " " + end_hour + ":" + end_minute
    }
    
    #將資料傳送到連接資料庫的文件
    from connect_database import check
    message1 = check(response_data)
    print(message1)
    
    return message1

@app.route("/vdata", methods=["POST"])
def vdata():
    viewYear = request.form.get("viewYear")
    viewMonth = request.form.get("viewMonth")
    viewDate = request.form.get("viewDate")

    print(f"viewYear: {viewYear}")
    print(f"viewMonth: {viewMonth}")
    print(f"viewDate: {viewDate}")

    response_data = {
        "viewTime": viewYear + "-" + viewMonth + "-" + viewDate
    }
    from connect_database import view
    message2 = view(response_data)

    if not message2:
        return "當日無預約資料"  # 如果沒有資料，返回相應的消息
    
    return jsonify(message2)

    # table = "<table border='1'>"
    # table += "<tr><th>預約開始時間</th><th>預約結束時間</th><th>員工號碼</th><th>會議室</th></tr>"

    # for index, item in enumerate(message2):
    #     row_class = "even" if index % 2 == 0 else "odd"
    #     table += f"<tr class='{row_class}'>"
    #     table += f"<td>{item['r_start']}</td><td>{item['r_end']}</td><td>{item['c_id']}</td><td>{item['room_no']}</td>"
    #     table += "</tr>"

    # table += "</table>"

    # return table

@app.route("/mdata", methods=["POST"])
def mdata():
    m_id = request.form.get("m_id")
    print(f"m_id: {m_id}")
    
    response_data = {"m_id": m_id}
    from connect_database import modify
    message3 = modify(response_data)
            
    if not message3:
        return "查無該ID的預約資料"  # 如果沒有資料，返回相應的消息
    
    table = "<table border='1'>"
    table += "<tr><th>預約開始時間</th><th>預約結束時間</th><th>會議室</th><th>操作</th></tr>"

    for item in message3:   
        table += f"<tr><td>{item['r_start']}</td><td>{item['r_end']}</td><td>{item['room_no']}</td>"
        table += f"<td><form id='dForm' action='/delete' method='POST'><input type='hidden' name='r_no' value='{item['r_no']}'><button type='submit'>删除</button></form></td></tr>"
            
    table += "</table>"
    return table

@app.route('/delete', methods=['POST'])
def delete():
    r_no = request.form.get("r_no")
    print(f"r_no: {r_no}")
    
    response_data = {"r_no": r_no}
    from connect_database import delete
    message4 = delete(response_data)
    return message4



@app.route("/ndata", methods=["POST"])
def ndata():
    return

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000)
    
