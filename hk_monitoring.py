from flask import  Flask, render_template, request, redirect, url_for, session, flash
from flaskext.mysql import MySQL
import datetime


app = Flask(__name__)
app.secret_key = "i love you cute"
mysql = MySQL()

#setter kung ano nga db gamiton
app.config["MYSQL_DATABASE_USER"]="root"
app.config["MYSQL_DATABSE_PASSWORD"]=""
app.config["MYSQL_DATABASE_DB"]="hkscholar"
app.config["MYSQLI_DATABASE_HOST"]="localhost"

#connection mo ni sa db kag sa python aka conn
mysql.init_app(app)
conn = mysql.connect()
qury = conn.cursor()

#--------------------------log in data dont tandog--------------------------------

qury.execute("SELECT `email` FROM `hk_users`")
userEmail = qury.fetchall()
usremail = []
for i in userEmail:
    usremail.append(i[0])
print(usremail)

qury.execute("SELECT `password` FROM `hk_users`")
userPassword = qury.fetchall()
usrpass = []
for i in userPassword:
    usrpass.append(i[0])
print(usrpass)

#portanti ni sa log in
credintials = []
index = 0
for i in usremail:
    credintials.append(i +" "+ usrpass[index])
    index+=1
print(credintials)

#----student id numbers---
qury.execute("SELECT `idnum` FROM `hk_users`")
idnumberStdnt = qury.fetchall()
stdntIdNumberAvilable =[]
for k in idnumberStdnt:
    stdntIdNumberAvilable.append(k[0])
print(stdntIdNumberAvilable)



#------------------------admin side request data--------------------------------

qury.execute("SELECT `email`, `date`, `timeIn`, `timeOut`, `id` FROM `request` WHERE 1 ")
reqdata = qury.fetchall()

reqdataList = []
for i in reqdata:
    reqdataList.append(i)
print(reqdataList)



#storage for admin usernames dont delete this
adminls = []
#------------admin data---------------------


qury.execute("SELECT `userName` FROM `admin` ")
adminUsername = qury.fetchall()

adminusernamels=[]
for k in adminUsername:
    adminusernamels.append(k[0])
print(adminusernamels)

qury.execute("SELECT `passWord` FROM `admin` ")
adminpass = qury.fetchall()

adminuserpassWord=[]
for k in adminpass:
    adminuserpassWord.append(k[0])
print(adminuserpassWord)

admin_cridentials = []
indexadmin = 0
for i in adminusernamels:
    admin_cridentials.append(i +" "+ adminuserpassWord[indexadmin])
    indexadmin+=1
print(admin_cridentials)


#-----------------operations Datas-------------------------------------------

qury.execute("SELECT `Faculty_Id_Number` FROM `operations_data`")
Faculty_Id_Number = qury.fetchall()

faculty_id = []
for k in Faculty_Id_Number:
    faculty_id.append(k[0])
print(faculty_id)

qury.execute("SELECT `Faculty_Password`FROM `operations_data`")
Faculty_PassWord = qury.fetchall()

faculty_psw = []
for k in Faculty_PassWord:
    faculty_psw.append(k[0])
print(faculty_psw)

#faculty credintials
faculty_credintials =[]
faculty_counter = 0

for k in faculty_id:
    compress = (k+" "+faculty_psw[faculty_counter])
    faculty_credintials.append(compress)
    faculty_counter+=1
print(faculty_credintials)

#------------------------data table for Duty_assignment------------------------
qury.execute("SELECT * FROM `operation_request`")
operation_request_DB = qury.fetchall()
operation_request = []
for k in operation_request_DB:
    operation_request.append(k)


table_Assigment_Page_Admin =[]
for k in range(len(operation_request)):
    process = {"DESIGNATION": operation_request[k][0],"REQ": operation_request[k][1],"REPORT DAY/S": operation_request[k][2], "SUPERVISOR":operation_request[k][5],	"DEPT":operation_request[k][4], "REQST":operation_request[k][3]}
    table_Assigment_Page_Admin.append(process)
print(table_Assigment_Page_Admin)




#checker if ang student naka sign in or wala pa
list_of_sign_in = []
#stroage for time in Time to use in formulation
timeInList =[]
# stroage for time in Time to use in formulation

#----------------------main code------------------------------



#-----------------------landing page----------------------------------------------

@app.route("/")
def landing_page():

    return render_template("ScholarTracker/unaindex.php")

@app.route("/sts_Page")
def sts_Page():

    return render_template("ScholarTracker/index1caps.php")





#--------------------------------------register------------------------------------------------

@app.route("/register")
def reg_render():

    return render_template('register.html')
@app.route("/reg", methods=["POST"])
def indexprocess():
    try:

        gmail = request.form["email"]
        password = request.form["psw"]
        repPaswrd = request.form['cnfrpsw']
        idnum = request.form['idnum']
        fname = request.form['fname']
        lname = request.form['lname']
        mname = request.form['Mname']
        phone = request.form['phone']
        Position = request.form['Position']
        dept = request.form['dept']


        if password == repPaswrd:

            faculty_credintials.append(idnum+" "+password)
            qury.execute("INSERT INTO `operations_data`(`Faculty_Lname`, `Faculty_Fname`, `Faculty_Password`, `Faculty_Id_Number`, `Operation_Dept`,"
                         " `Operations_Mname`, `Operation_phone_Number`, `Operation_Designation-Position`, `Operations_Email`)"
                         " VALUES ('"+lname+"','"+fname+"','"+password+"','"+idnum+"','"+dept+"','"+mname+"','"+phone+"','"+Position+"','"+gmail+"')")
            conn.commit()
            return '<script>alert("Registered Complete");window.location="/register"</script>'
        else:
            return '<script>alert("wrong pass");window.location="/register"</script>'

    except:

        return '<script>alert("Email already used");window.location="/register"</script>'


#---------------------------------log in-----------------------------------------------------


@app.route("/Sign in")
def signInPAge():
    return render_template("SignIn.html")


@app.route("/signed in", methods= ["POST"])
def signInprocess():

    idNum = request.form['email']
    password = request.form['psw']
    logindata = idNum+" "+password
    session["user"]=idNum

    if logindata in faculty_credintials:

        # faculty usr namea
        qury.execute("SELECT `Faculty_Fname` FROM `operations_data` WHERE `Faculty_Id_Number` = '"+idNum+"'")
        fname = qury.fetchall()[0][0]

        qury.execute("SELECT `Faculty_Lname` FROM `operations_data` WHERE `Faculty_Id_Number` = '"+idNum+"'")
        lname = qury.fetchall()[0][0]

        session["fname"] = fname
        session["lname"] = lname

        username = (fname+" "+lname).upper()
        session['username']=username


        return '<script>alert("Log in");window.location="/Dash board"</script>'

    else:

        flash("Wrong Email or Password", "info")
        return '<script>alert("Wrong ssword or Email");window.location="/Sign in"</script>'


#------------------------------------log out----------------------------------------------
@app.route("/Logout", methods=['POST'])
def logOut():
    session.pop("user",None)
    session.pop("username",None)
    session.pop("lname",None)
    session.pop("fname", None)



    return '<script>alert("Log Out");window.location="/"</script>'

#-------------------------------dash board-----------------------------------------
@app.route("/Dash board")
def Dashboard():

    if "user" in session:

        return render_template("dashboard operations/OpartionsDashBoard.html",logUser = session['username'])

    else:
        return redirect(url_for("signInPAge"))
#-----------------------------------------request-----------------------------------------------------

@app.route("/Request and Scholar Management")
def request_Scholar():

    print(session['username'])

    qury.execute("SELECT `hk_ID`FROM `hk_assignd_teaecher` WHERE `operatikon_ID` = '"+session["lname"]+"'")
    mYStudent_Db_Id = qury.fetchall()
    print("my student",mYStudent_Db_Id)

    listahan = []
    for k in mYStudent_Db_Id:
        print(k[0])
        qury.execute("SELECT `idnum`,`lname`, `fname`, `id_totalHours`,  `remaningDuty`, `remDutyMins`,`statsForRenewal` FROM `hk_users` WHERE `idnum`= '"+k[0]+"'")
        listahan.append(qury.fetchall()[0])
    print(listahan)

    student_underMe=[]
    for k in range(len(listahan)):
        tables = {"STUDENT ID":listahan[k][0],"SCHOLAR NAME":listahan[k][1]+" "+listahan[k][2],"COMPLETED HOURS":listahan[k][3],"REMAINING HOURS":listahan[k][4]+"h "+str(listahan[k][5]).split(".")[0]+"m","STATUS":listahan[k][6]}
        student_underMe.append(tables)
    return render_template("dashboard operations/requestmanage.html",logUser = session['username'], student_underMe =student_underMe)




@app.route("/Profile")
def Profile_Operations():

    return render_template("dashboard operations/profile.html",logUser = session['username'])


@app.route("/Modal_request_process", methods=['POST'])
def Modal_request_process():
    Designation = request.form['Designation']
    Requirements = request.form['Requirements']
    Report_Days = request.form['Report Day/s']
    Request = request.form['Request']

    qury.execute("SELECT `Operation_Dept` FROM `operations_data` WHERE `Faculty_Id_Number` = '"+str(session["user"])+"' ")
    dept = qury.fetchall()
    print(dept[0][0])


    qury.execute("INSERT INTO `operation_request`(`Designation`, `Requirements`, `Report Day/s`, `Request`, `DEPT`, `SUPERVISOR`) VALUES ('"+Designation+"','"+Requirements+"','"+Report_Days+"','"+Request+"', '"+dept[0][0]+"', '"+session['lname']+"') ")
    conn.commit()

    process = {"DESIGNATION": Designation, "REQ": Requirements,
               "REPORT DAY/S": Report_Days, "SUPERVISOR": session["lname"],
               "DEPT":dept[0][0] , "REQST":Request }
    table_Assigment_Page_Admin.append(process)

    return '<script>alert("Request Sent!!");window.location="/Request and Scholar Management"</script>'




#-------------------------------------show total duty hours-----------------------------------------------
@app.route("/showDutyProcess", methods=['POST'])
def showDutyHours():
#for formulation data time
    qury.execute("SELECT `totaldutyHours` FROM `dutyhourformulationdata` WHERE `email`='"+session["user"]+"' ")
    dtymData = qury.fetchall()
    totalDutyHours= (dtymData[0][0])
    convertToHours = int(totalDutyHours) / 60
    splitedHM = str(convertToHours).split(".")
    hour = splitedHM[0]
    session["hours"] = hour
    minutes = float("0."+splitedHM[1])*60
    session["minutes"] = minutes
    timeToDisplay = ("Total Working Hours: '"+str(hour)+"' Hours and '"+str(int(minutes))+"' Minutes")
    print(timeToDisplay)
    session["duty"]=timeToDisplay
    print(session["duty"])
#this is for remaining duty hours
    target = 10800
    H = int(session["hours"]) * 60
    remM = target - H
    dataTime = str(remM / 60).split(".")
    Hour = dataTime[0]
    Minutes = str(int((float("0." + dataTime[1]) * 60)))
    reamining = str(Hour) + ":" + Minutes
    session["reamining"] =reamining
    print(dataTime)
#this is for records time date display
    qury.execute("SELECT * FROM `timeintimeout` WHERE `TinToutgmail` = '" + session["user"] + "'")
    userTimeRecords = qury.fetchall()


    return render_template("dashboard operations/OpartionsDashBoard.html", logUser=session['username'],duty = session["duty"], remduty = session["reamining"], rec = userTimeRecords)



#-------------------------------------request end-------------------------------------





#-------------------------------------Profile-------------------------------------------------------
@app.route("/Profile")
def profile():
    return render_template("Profile.html",lname=session["lname"],fname=session["fname"])

@app.route("/Profile process", methods=['POST'])
def ProfileProcess():

    newFname = request.form['fnameNew']
    newLname = request.form['lnameNew']
    oldpsw = request.form['OldPassword']
    newpsw = request.form['NewPassword']
    qury.execute("SELECT`password`FROM `hk_users` WHERE `email`='"+session["user"]+"' ")
    pswcon = qury.fetchall()
    print(pswcon)


    if oldpsw == str(pswcon[0][0]) :
        print("true")
        qury.execute("UPDATE `hk_users` SET `fname`='"+newFname+"',`lname`='"+newLname+"',`password`='"+newpsw+"'WHERE `email` ='"+session["user"]+"'")
        conn.commit()

        flash("Update sucess!! pls Re-login to see changes", "info")

    else:

        flash("wrong old password", "info")

    return redirect(url_for("profile"))

@app.route("/Acc del")
def accDel():

    return render_template("deleteAccount.html")
@app.route("/delProcess", methods=['POST'])
def delProccess():

    qury.execute("DELETE FROM `hk_users` WHERE `email` = '"+session['user']+"'")
    conn.commit()

    qury.execute("DELETE FROM `dutyhourformulationdata` WHERE `email` = '" + session['user'] + "'")
    conn.commit()
    session.pop("user",None)

    flash("Account Deleted!")
    return redirect(url_for("indexpage"))
#-------------------------------------end Profile---------------------------------------------------

#------------------------------------scholar info searching--------------------------------------------------
@app.route("/search_PAge")
def searchPage():
    return render_template("scholar.html")


@app.route("/scholars",methods=['POST'])
def scholarSearch():

    searchInputIdNum = request.form['search']
    if searchInputIdNum in stdntIdNumberAvilable:
        qury.execute("SELECT * FROM `hk_users` WHERE `idnum` = '"+searchInputIdNum+"'")
        hkdetails = qury.fetchall()#len of 17
        #details to show in profile of the student searched
        idnum=hkdetails[0][0]#idnum
        Lname=hkdetails[0][2]#Lname
        Fname=hkdetails[0][3]#Fname
        totalDuty=hkdetails[0][5]#totalDuty
        course_Program=hkdetails[0][6]#course_Program
        department=hkdetails[0][7]#department
        yearLvl=hkdetails[0][8]#yearLvl
        scholarship=hkdetails[0][9]#scholarship
        DUTY_DESIGNATION=hkdetails[0][10]#DUTY_DESIGNATION
        DUTY_SUPERVISOR=hkdetails[0][11]#DUTY_SUPERVISOR
        reqiredDuty=hkdetails[0][12]#reqiredDuty
        remaningDuty=hkdetails[0][13]#remaningDuty
        remDutyMin = str(float(hkdetails[0][14])).split(".")  # remDutyMin
        statsuForRenewal=hkdetails[0][15]#statsuForRenewal
        Schoolyr=hkdetails[0][16]#Schoolyr
        semister=hkdetails[0][17]#semister

        return render_template("details.html",idnum=idnum,Lname=Lname,Fname=Fname,totalDuty=totalDuty,
        course_Program=course_Program,department=department,yearLvl=yearLvl,scholarship=scholarship,
        DUTY_DESIGNATION=DUTY_DESIGNATION,DUTY_SUPERVISOR=DUTY_SUPERVISOR,reqiredDuty=reqiredDuty,
        remaningDuty=remaningDuty,statsuForRenewal=statsuForRenewal,Schoolyr=Schoolyr,semister=semister, remDutyMin=remDutyMin[0])

    else:
        return render_template("norecords.html")


#---------- end of scholar info page -------------------









#------------------admin side------------------------------
@app.route("/adminLanding")
def admin():
    return render_template("admin.html")

@app.route("/adminLog", methods=['POST'])
def adminLog():

    useraAdmin = request.form['email']
    pswAdmin = request.form['pass']
    session["adminUser"] = useraAdmin


    check = useraAdmin+" "+pswAdmin
    if check in admin_cridentials:
        return '<script>alert("Welcome");window.location="admindashBoard"</script>'
    else:
        return  '<script>alert("Wrong Cridentials!");window.location="/adminLanding"</script>'

@app.route("/admindashBoard")
def admindashBoard():

#to check if the user is still log in
    if "adminUser" in session:

        return render_template('dashboard admin/dashboardAdminFinal.html', logUser=session["adminUser"])
    else:
        return redirect(url_for("admin"))

# to log out the admin log and clear all session
@app.route("/LogoutAdmin", methods=['POST'])
def logOutAmin():
    session.pop("adminUser",None)
    return '<script>alert("Log Out");window.location="/"</script>'
   #-----------------------end of admin dash board----------------------

#----------------------------ADMIN SIDE BARS----------------------------

@app.route("/compliance")
def compliance():
    # -------------student informations---------------------
    qury.execute("SELECT * FROM `hk_users`")
    student_Info_FromDb = qury.fetchall()

    student_info = []
    for k in student_Info_FromDb:
        student_info.append(k)
    print(len(student_info))

    table_OfStudent_Info = []
    counter_Table1 = 0
    # details to show in profile of the student searched #
    for k in student_info:
        std_fullNmae = str(student_info[counter_Table1][3]) + " " + str(student_info[counter_Table1][2])
        dataProcess = {"STUDENT ID": student_info[counter_Table1][0], "SCHOLAR NAME": std_fullNmae,
                       "COMPLETED HOURS": student_info[counter_Table1][5]+"m",
                       "REMAINING HOURS": student_info[counter_Table1][13]+"h "+str(student_info[counter_Table1][14]).split(".")[0]+"m", "STATUS": student_info[counter_Table1][15]}
        table_OfStudent_Info.append(dataProcess)
        counter_Table1 += 1

    print(table_OfStudent_Info)


    return render_template("dashboard admin/compliance.html",logUser=session["adminUser"], table_OfStudent_Info = table_OfStudent_Info)

#----------------------Hk 25, 50, 75, 100-----------------------------
@app.route("/compliance_hk_25")
def compliance_Hk_25():

    #Qeury Student with 25% hk

    qury.execute("SELECT * FROM `hk_users` WHERE `scholarship` = 'HK25' " )
    student_Info_FromDb_25 = qury.fetchall()

    student_info_25 = []
    for k in student_Info_FromDb_25:
        student_info_25.append(k)

    table_OfStudent_Info_25 = []
    counter_Table1 = 0
    # details to show in profile of the student searched #
    for k in student_info_25:
        std_fullNmae = str(student_info_25[counter_Table1][3]) + " " + str(student_info_25[counter_Table1][2])
        dataProcess = {"STUDENT ID": student_info_25[counter_Table1][0], "SCHOLAR NAME": std_fullNmae,
                       "COMPLETED HOURS": student_info_25[counter_Table1][5],
                       "REMAINING HOURS": student_info_25[counter_Table1][13], "STATUS": student_info_25[counter_Table1][14]}
        table_OfStudent_Info_25.append(dataProcess)
        counter_Table1 += 1


    return render_template("dashboard admin/compliance_Hk_25.html",logUser=session["adminUser"], table_OfStudent_Info = table_OfStudent_Info_25)

@app.route("/compliance_hk_50")
def compliance_Hk_50():
    # Qeury Student with 50% hk

    qury.execute("SELECT * FROM `hk_users` WHERE `scholarship` = 'HK50' ")
    student_Info_FromDb_50 = qury.fetchall()

    student_info_50 = []
    for k in student_Info_FromDb_50:
        student_info_50.append(k)

    table_OfStudent_Info_50 = []
    counter_Table1 = 0
    # details to show in profile of the student searched #
    for k in student_info_50:
        std_fullNmae = str(student_info_50[counter_Table1][3]) + " " + str(student_info_50[counter_Table1][2])
        dataProcess = {"STUDENT ID": student_info_50[counter_Table1][0], "SCHOLAR NAME": std_fullNmae,
                       "COMPLETED HOURS": student_info_50[counter_Table1][5],
                       "REMAINING HOURS": student_info_50[counter_Table1][13],
                       "STATUS": student_info_50[counter_Table1][14]}
        table_OfStudent_Info_50.append(dataProcess)
        counter_Table1 += 1

    return render_template("dashboard admin/compliance_Hk_50.html",logUser=session["adminUser"], table_OfStudent_Info = table_OfStudent_Info_50)

@app.route("/compliance_hk_75")
def compliance_Hk_75():
    # Qeury Student with 75% hk

    qury.execute("SELECT * FROM `hk_users` WHERE `scholarship` = 'HK75' ")
    student_Info_FromDb_75 = qury.fetchall()

    student_info_75 = []
    for k in student_Info_FromDb_75:
        student_info_75.append(k)

    table_OfStudent_Info_75 = []
    counter_Table1 = 0
    # details to show in profile of the student searched #
    for k in student_info_75:
        std_fullNmae = str(student_info_75[counter_Table1][3]) + " " + str(student_info_75[counter_Table1][2])
        dataProcess = {"STUDENT ID": student_info_75[counter_Table1][0], "SCHOLAR NAME": std_fullNmae,
                       "COMPLETED HOURS": student_info_75[counter_Table1][5],
                       "REMAINING HOURS": student_info_75[counter_Table1][13],
                       "STATUS": student_info_75[counter_Table1][14]}
        table_OfStudent_Info_75.append(dataProcess)
        counter_Table1 += 1

    return render_template("dashboard admin/compliance_Hk_75.html",logUser=session["adminUser"], table_OfStudent_Info = table_OfStudent_Info_75)

@app.route("/compliance_hk_100")
def compliance_Hk_100():
    # Qeury Student with 100% hk

    qury.execute("SELECT * FROM `hk_users` WHERE `scholarship` = 'HK100' ")
    student_Info_FromDb_100 = qury.fetchall()

    student_info_100 = []
    for k in student_Info_FromDb_100:
        student_info_100.append(k)

    table_OfStudent_Info_100 = []
    counter_Table1 = 0
    # details to show in profile of the student searched #
    for k in student_info_100:
        std_fullNmae = str(student_info_100[counter_Table1][3]) + " " + str(student_info_100[counter_Table1][2])
        dataProcess = {"STUDENT ID": student_info_100[counter_Table1][0], "SCHOLAR NAME": std_fullNmae,
                       "COMPLETED HOURS": student_info_100[counter_Table1][5],
                       "REMAINING HOURS": student_info_100[counter_Table1][13],
                       "STATUS": student_info_100[counter_Table1][14]}
        table_OfStudent_Info_100.append(dataProcess)
        counter_Table1 += 1

    return render_template("dashboard admin/compliance_Hk_100.html",logUser=session["adminUser"], table_OfStudent_Info = table_OfStudent_Info_100)






@app.route("/Duty Assignment And Management")
def DutyAssig():
    # messages = request.args['h'] mag pass value halin sa url_for
    return render_template("dashboard admin/assignment.html",logUser=session["adminUser"],table_Assigment_Page_Admin = table_Assigment_Page_Admin  )


#to assign a studen to a faculty
techer =[]
@app.route("/Duty Assignment", methods=['POST'])
def DutyAssig_process():
    # messages = request.args['h'] mag pass value halin sa url_for
    qury.execute("SELECT `idnum`, `lname`, `fname`,`program_course`, `department`, `yrLvL` FROM `hk_users` WHERE `Status_avail` = 'av'")
    student_db_data = qury.fetchall()

    supervi = request.form['operations_Id_Selected']
    techer.append(supervi)

    avil_std_list = []
    for k in student_db_data:
        avil_std_list.append(k)
    print(avil_std_list)

    table_avil_std =[]
    for k in range (len(avil_std_list)):
        table = {"STUDENT ID":avil_std_list[k][0],"SCHOLAR NAME":avil_std_list[k][1]+" "+avil_std_list[k][2],"YEAR LVL":avil_std_list[k][3],"PROGRAM":avil_std_list[k][4], "DEPARTMENT":avil_std_list[k][5]}
        table_avil_std.append(table)

    return render_template("dashboard admin/assignment.html", logUser=session["adminUser"],table_Assigment_Page_Admin=table_Assigment_Page_Admin,table_avil_std=table_avil_std )

@app.route("/Assigment_modal_process", methods =['POST'])
def Assigment_modal_process():

    checkList = request.form.getlist("selected_std")
    print(checkList)
    tc_selected = techer[len(techer)-1]

    for k in checkList:
        print(k)
        qury.execute("INSERT INTO `hk_assignd_teaecher`(`operatikon_ID`, `hk_ID`) VALUES ('"+tc_selected+"','"+k+"')")
        conn.commit()

        qury.execute("UPDATE `hk_users` SET `Status_avail`='Na' WHERE `idnum` = '"+k+"' ")
        conn.commit()

    techer.clear()


    return redirect(url_for("DutyAssig"))
#-----------------------------------------------------------------------------------------------------------------------




@app.route("/User Management")
def UserManagement():
    return render_template("dashboard admin/UserManagement.html",logUser=session["adminUser"])

@app.route("/Scholar Information")
def scholarinfor():
    return render_template("dashboard admin/scholarinfo.html",logUser=session["adminUser"])

@app.route("/Reports And Analytics")
def analytics():
    return render_template("dashboard admin/analytics.html",logUser=session["adminUser"])

@app.route("/Export to Excel")
def Excel():
    return render_template("dashboard admin/Excel.html",logUser=session["adminUser"])

@app.route("/Setting and Configurations")
def Setting():
    return render_template("dashboard admin/Setting.html",logUser=session["adminUser"])

@app.route("/System Health Logs")
def Systemhealth():
    return render_template("dashboard admin/Systemhealth.html",logUser=session["adminUser"])

@app.route("/Feedback and Improvements")
def Feedback():
    return render_template("dashboard admin/Feedback.html",logUser=session["adminUser"])

@app.route("/assigment")
def assiment():

    return  render_template("dashboard admin/assignment.html",logUser=session["adminUser"])
@app.route("/student_records")
def student_records():

    return render_template("dashboard admin/ScholarRecordAdmin.html")



@app.route("/student_rec_process", methods=['POST'])
def student_rec_process():
    if request.form.get('select') == 'select':
        print('selected')
        student_Id = request.form.get("Selected_Id")

        qury.execute("SELECT * FROM `hk_users` WHERE `idnum` = '" + str(student_Id) + "'")
        hkdetails = qury.fetchall()  # len of 17

        # details to show in profile of the student searched
        idnum = hkdetails[0][0]  # idnum
        Lname = hkdetails[0][2]  # Lname
        Fname = hkdetails[0][3]  # Fname
        totalDuty = hkdetails[0][5]  # totalDuty
        course_Program = hkdetails[0][6]  # course_Program
        department = hkdetails[0][7]  # department
        yearLvl = hkdetails[0][8]  # yearLvl
        scholarship = hkdetails[0][9]  # scholarship
        DUTY_DESIGNATION = hkdetails[0][10]  # DUTY_DESIGNATION
        DUTY_SUPERVISOR = hkdetails[0][11]  # DUTY_SUPERVISOR
        reqiredDuty = hkdetails[0][12]  # reqiredDuty
        remaningDuty = hkdetails[0][13]  # remaningDuty
        remDutyMin = str(float(hkdetails[0][14])).split(".")# remDutyMin
        statsuForRenewal = hkdetails[0][15]  # statsuForRenewal
        Schoolyr = hkdetails[0][16]  # Schoolyr
        semister = hkdetails[0][17]  # semister


    return render_template("dashboard admin/ScholarRecordAdmin.html",idnum=idnum,Lname=Lname,Fname=Fname,totalDuty=totalDuty,
        course_Program=course_Program,department=department,yearLvl=yearLvl,scholarship=scholarship,
        DUTY_DESIGNATION=DUTY_DESIGNATION,DUTY_SUPERVISOR=DUTY_SUPERVISOR,reqiredDuty=reqiredDuty,
        remaningDuty=remaningDuty,statsuForRenewal=statsuForRenewal,Schoolyr=Schoolyr,semister=semister, remDutyMin = remDutyMin[0])



@app.route("/Duty_Records", methods=['POST'])
def Duty_Records():
    DUTY_Id_Num = request.form.get('Duty_Id')

    qury.execute("SELECT * FROM `scholar_duty_records` WHERE `Student_id_Number` = '"+DUTY_Id_Num+"'")
    rec_list_Db = qury.fetchall()

    rec_list = []
    for k in rec_list_Db:
        rec_list.append(k)
    record_table = []
    time_in = ""
#----- solve the renderd duty hours in minutes format-----------
    total_duty = 0
    for k in range (len(rec_list)):

        if rec_list[k][5]=="IN":
            inh = rec_list[k][1]
            inm = rec_list[k][2]
            time_in =  f"{rec_list[k][1]:}:{rec_list[k][2]:02d}"

        elif rec_list[k][5] == "OUT":
            time_out = f"{rec_list[k][1]:}:{rec_list[k][2]:02d}"
            durationoH = int(rec_list[k][1]) - int(inh)
            durationm = int(rec_list[k][2]) - int(inm)
            HourTo_min = durationoH * 60
            totalduty_mins = HourTo_min + durationm
            total_duty +=totalduty_mins
            duration = f"{durationoH:}h {durationm:02d}m"
            rec_process = {"DATE": rec_list[k][0], "CHECK-IN TIME": time_in, "CHECK-OUT TIME": time_out, "DURATION": duration}
            record_table.append(rec_process)

            qury.execute("UPDATE `hk_users` SET `id_totalHours`='"+str(total_duty)+"' WHERE `idnum` = '" + DUTY_Id_Num + "' ")
            conn.commit()




    return render_template("dashboard admin/dutyrecords.html", DUTY_Id_Num =DUTY_Id_Num, record_table= record_table)

#-------------------------END OF ADMIN SIDE BARS------------------




#--------------------------Terminals----------------------


@app.route("/terminal")
def terminal():

    return render_template("Terminal/terminal.html")


@app.route("/StudentTimeIN_Out", methods=['POST'])
def StudentTimeIN_Out():
    # Get current date
    tday = datetime.date.today()
    # Get the current time
    current_time = datetime.datetime.now()
    current_date = datetime.date.today()
    # Extract the year, mont, day, hours, and minutes
    current_hour = current_time.hour
    current_minute = current_time.minute
    yr =current_date.year
    month = current_date.month
    date = current_date
    #checker if the id number had sign in or not





    time_In_Out = request.form.get('login')
    stdId = request.form['idstndt']
    total_duty = 0

    try:
        if  time_In_Out == "IN":
            # to check if the user already sign in and need to sign out
            if stdId in list_of_sign_in:
                errormess = "You already Sign in"
                return render_template("Terminal/terminal.html", errormess=errormess)
            # to check if the user already sign in and need to sign out


            else:
                #to insert the time in time
                timeInList.append(current_hour)# index 0
                timeInList.append(current_minute)# index 1
                list_of_sign_in.append(stdId)
                print(list_of_sign_in)
                qury.execute("INSERT INTO `scholar_duty_records`"
                             "(`date`,`Hours_In_Out`, "
                             "`Minutes_In_Out`, `Student_id_Number`, "
                             "`Type_of_Process`) VALUES "
                             "('" + str(date) + "','" + str(current_hour) + "','" + str(current_minute) + "','" + stdId + "','" + time_In_Out + "')")
                conn.commit()
                #to insert the time in time


                #to get the name who sing in and out
                qury.execute("SELECT `lname`, `fname` FROM `hk_users` WHERE `idnum` = '" + stdId + "' ")
                fullname = qury.fetchall()
                fname = fullname[0][1]
                lname = fullname[0][0]
                #to get the name who sing in and out


                return render_template("Terminal/terminal.html", tday=tday, hours=current_hour, mins=current_minute,time_In_Out=time_In_Out, stdId=stdId, fname=fname, lname=lname)
            return render_template("Terminal/terminal.html")





        elif time_In_Out =="OUT":
            list_of_sign_in.remove(stdId)

            qury.execute("SELECT * FROM `scholar_duty_records` WHERE `Student_id_Number` = '" + stdId + "'")
            rec_list_Db = qury.fetchall()

            rec_list = []
            for k in rec_list_Db:
                rec_list.append(k)

        # ----- solve the renderd duty hours in minutes format-----------
            record_table = []
            time_in = ""

            for k in range(0,int(len(rec_list))):

                if rec_list[k][5] == "IN":
                    inh = rec_list[k][1]
                    inm = rec_list[k][2]
                    time_in = f"{rec_list[k][1]:}:{rec_list[k][2]:02d}"

                elif rec_list[k][5] == "OUT":
                    time_out = f"{rec_list[k][1]:}:{rec_list[k][2]:02d}"
                    durationoH = int(rec_list[k][1]) - int(inh)
                    durationm = int(rec_list[k][2]) - int(inm)
                    HourTo_min = durationoH * 60
                    totalduty_mins = HourTo_min + durationm

                    print("ngaa",totalduty_mins)
                    total_duty += totalduty_mins
                    print(total_duty)
                    duration = f"{durationoH:}h {durationm:02d}m"
                    rec_process = {"DATE": rec_list[k][0], "CHECK-IN TIME": time_in, "CHECK-OUT TIME": time_out,
                                   "DURATION": duration}
                    record_table.append(rec_process)

                    #update the renderd duty-----
                    qury.execute("UPDATE `hk_users` SET `id_totalHours`='" + str(
                        total_duty) + "' WHERE `idnum` = '" + stdId + "' ")
                    conn.commit()
                    #update the renderd duty-----


            #----------------------formulation of reminin duty hours
            timInHour = (float(timeInList[0])*60)
            timeInMin = (float(timeInList[1])+timInHour)
            timeOutHours = (float(current_hour)*60)
            timeOutMin = (float(current_minute)+timeOutHours)
            renderedDutyToday = (timeOutMin - timeInMin)
            print("renderd today",renderedDutyToday)

            qury.execute("SELECT `remaningDuty`, `remDutyMins`FROM `hk_users` WHERE `idnum` = '" + stdId + "'")
            remdutyDb = qury.fetchall()
            remdutymins = (float(remdutyDb[0][1]))
            remduty = (float(remdutyDb[0][0])*60)+remdutymins

            print(remduty)


            remdutyMins = remduty - renderedDutyToday
            remdutyHoursConverstion = str(remdutyMins / 60).split(".")
            remdutyHours = remdutyHoursConverstion[0]
            remdutyMinscpnvertion = (float("0."+remdutyHoursConverstion[1])*60)

            print("remdutyMins",remdutyMins)
            print("remdutyHoursConverstion", remdutyHoursConverstion)
            print("remdutyHours", remdutyHours)
            print("remdutyMinscpnvertion", remdutyMinscpnvertion)
            qury.execute("UPDATE `hk_users` SET `remaningDuty`='"+str(remdutyHours)+"',`remDutyMins`='"+str(remdutyMinscpnvertion)+"' WHERE `idnum` = '"+stdId+"'")
            conn.commit()
            timeInList.clear()
            #------------------formulation of reminin duty hours



            qury.execute("INSERT INTO `scholar_duty_records`"
                         "(`date`,`Hours_In_Out`, "
                         "`Minutes_In_Out`, `Student_id_Number`, "
                         "`Type_of_Process`) VALUES "
                         "('" + str(date) + "','" + str(current_hour) + "','" + str(
                current_minute) + "','" + stdId + "','" + time_In_Out + "')")
            conn.commit()
            qury.execute("SELECT `lname`, `fname` FROM `hk_users` WHERE `idnum` = '" + stdId + "' ")
            fullname = qury.fetchall()
            fname = fullname[0][1]
            lname = fullname[0][0]



            return render_template("Terminal/terminal.html", tday=tday, hours=current_hour, mins=current_minute,time_In_Out=time_In_Out, stdId=stdId, fname=fname, lname=lname)


    except Exception:
        errormess = "..Sign in first.. "





    return render_template("Terminal/terminal.html", errormess =errormess  )






if __name__ == "__main__":
    app.run(debug=True)