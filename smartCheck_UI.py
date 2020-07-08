# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 12:08:36 2020

@author: grimr
"""
def prolo(toInput,dictHold):
    import pyswip
    prolog = pyswip.Prolog()
    prolog.assertz("approve(PNA,TM,AVG,BUD,TIME,HAZ,ENS,ON,CAN,EX) :- constraints(PNA,TM,AVG,BUD,TIME), content(PNA,HAZ,ENS), valid(X,ON,CAN,EX)")
    prolog.assertz("constraints(PNA,TM,AVG,BUD,TIME) :- stAMS(TM, AVG), bgt(BUD, TIME), write('this is Constraints')")
    prolog.assertz("stAMS('n4', 'l75l')")
    prolog.assertz("stAMS('n5', 'l75l')")
    prolog.assertz("stAMS('n2', 'u75u')")
    prolog.assertz("stAMS('n3', 'u75u')")
    prolog.assertz("bgt('l250l', 'mo1')")
    prolog.assertz("bgt('l250l', 'mo2')")
    prolog.assertz("bgt('l400l', 'mo0.5')")
    prolog.assertz("bgt('l400l', 'mo1')")
    prolog.assertz("content(PNA,HAZ,ENS) :- safe(HAZ,ENS)")
    #self.prolog.assertz("part(_,_,'u75u')")
    prolog.assertz("safe(no, no)")
    prolog.assertz("safe(fire, engi)")
    prolog.assertz("safe(lab, med)")
    prolog.assertz("valid(PNA,ON,CAN,EX) :- intime(ON,CAN,EX), write('this is valid')")
    prolog.assertz("intime(yes,_,_)")
    prolog.assertz("intime(no,yes,_)")
    prolog.assertz("intime(no,no,a)")
    prolog.assertz("intime(no,no,b)")
    
    for i in prolog.query(toInput):
            if i['X'] == dictHold['Excuses']:
                return True
    return False
##########################################################
from flask import Flask, render_template, redirect, url_for, request

def webRun():
    dictHold = {}
    ##### Website Running
    app = Flask(__name__)
    approval = "Approved"
    
    @app.route("/home",methods=["POST","GET"])
    def home():
        if request.method == "POST":
            return redirect(url_for("question1"))
        else:
            return render_template("home.html")
    
    @app.route("/question1",methods=["POST","GET"])
    def question1():
        if request.method == "POST":
            dictHold["Project_name"] = request.form["project_name"]
            return redirect(url_for("question2"))
            
        return render_template("q1.html")
        
    @app.route("/question2",methods=["POST","GET"])
    def question2():
        if request.method == "POST":
            dictHold["Team_member"] = request.form["team_num"]
            return redirect(url_for("question3"))
        return render_template("q2.html")
        
    @app.route("/question3",methods=["POST","GET"])
    def question3():
        if request.method == "POST":
            dictHold["Avg_Mid"] = request.form["avg_score"]
            return redirect(url_for("question4"))
        return render_template("q3.html")
    
    @app.route("/question4",methods=["POST","GET"])
    def question4():
        if request.method == "POST":
            dictHold["Budget"] = request.form["budget"]
            return redirect(url_for("question5"))
        return render_template("q4.html")
    
    @app.route("/question5",methods=["POST","GET"])
    def question5():
        if request.method == "POST":
            dictHold["Time"] = request.form["time_span"]
            return redirect(url_for("question6"))
        return render_template("q5.html")
        
    @app.route("/question6",methods=["POST","GET"])
    def question6():
        if request.method == "POST":
            dictHold["Hazard"] = request.form["hazard"]
            if dictHold["Hazard"] == "no":
                dictHold["Ensure"] = "null"
                return redirect(url_for("question7"))
            else:
                return redirect(url_for("question6a"))
        return render_template("q6.html")
    
    @app.route("/question6a",methods=["POST","GET"])
    def question6a():
        if request.method == "POST":
            dictHold["Ensure"] = request.form["ensure"]
            return redirect(url_for("question7"))
        return render_template("q6a.html")
        
    @app.route("/question7",methods=["POST","GET"])
    def question7():
        if request.method == "POST":
            dictHold["On_time"] = request.form["on_time"]
            if dictHold["On_time"] == "yes":
                dictHold["Canvas"] = "null"
                dictHold["Excuses"] = "null"
                #calculate()
                return redirect(url_for("result"))
            else:
                return redirect(url_for("question7a"))
        return render_template("q7.html")
        
    @app.route("/question7a",methods=["POST","GET"])
    def question7a():
        if request.method == "POST":
            dictHold["Canvas"] = request.form["canvas"]
            if dictHold["Canvas"] == "yes":
                dictHold["Excuses"] = "null"
                #calculate()
                return redirect(url_for("result"))
            else:
                return redirect(url_for("question7b"))
        return render_template("q7a.html")
        
    @app.route("/question7b",methods=["POST","GET"])
    def question7b():
        if request.method == "POST":
            dictHold["Excuses"] = request.form["excuse"]
            #calculate()
            return redirect(url_for("result"))
        return render_template("q7b.html")
        
    @app.route("/result",methods=["POST","GET"])
    def result():
        if request.method == "POST":
            return redirect(url_for("home"))
        #approval = calculate()
        return render_template("result.html",approval=approval,
                               name=dictHold['Project_name'],
                               num=dictHold['Team_member'],
                               score=dictHold['Avg_Mid'],
                               budget=dictHold['Budget'],
                               duration=dictHold['Time'],
                               hazard=dictHold['Hazard'],
                               ensure=dictHold['Ensure'],
                               on_time=dictHold['On_time'],
                               canvas=dictHold['Canvas'],
                               excuse=dictHold['Excuses'])
    #############################################################
    def calculate():
        approve = ""
        toInput = 'approve({},{},{},{},{},{},{},{},{},{})'.format(dictHold['Project_name'],
                          dictHold['Team_member'],
                          dictHold['Avg_Mid'],
                          dictHold['Budget'],
                          dictHold['Time'],
                          dictHold['Hazard'],
                          dictHold['Ensure'],
                          dictHold['On_time'],
                          dictHold['Canvas'],'X')
        
        approve = prolo(toInput,dictHold)
        
        if approve == dictHold['Excuses']:
            return 'The project is approvable'
        else:
            return 'The project is not approvable'            
    ###########################################################
    if __name__ == "__main__":
        app.run()
#########################################################################
webRun()