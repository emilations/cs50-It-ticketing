import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///itsolutions.db")

@app.after_request
def after_request(response):
	"""Ensure responses aren't cached"""
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response

# INDEX
@app.route("/")
@login_required
def index():
	return redirect("/tickets")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		# Ensure username was submitted
		username = request.form.get("username")
		password = (request.form.get("password")).lower()
		if not username or not password:
			error = "Please provide a username and password"
			return render_template("login.html", error=error)
		# Query database for username
		rows = db.execute("SELECT employee_id, username, password FROM employees WHERE username = ?", request.form.get("username"))
		# Ensure username exists and password is correct
		if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
			error = "Please enter a valid username and password"
			return render_template("login.html", error=error)
		# Remember which user has logged in
		session["user_id"] = rows[0]["employee_id"]
		flash("You are logged in")
		# Redirect user to home page
		return redirect("/")
	else:
		return render_template("login.html")

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "POST":
		# initiate the inputs given from the user
		error = None
		firstName = (request.form.get("firstName")).lower()
		lastName = (request.form.get("lastName")).lower()
		password = request.form.get("password")
		confirmation = request.form.get("confirmation")
		code = (request.form.get("code")).lower()
		name = firstName.title() + " " + lastName.title()
		# no input should be empty
		if not firstName or not lastName or not password or not confirmation or not code:
			error = "Please make sure all fields are submitted"
		# password and password confirmation should be identical
		if not password == confirmation and not error:
			error = "Passwords not matching"
		# generate hash and assemble username variable
		hash = generate_password_hash(password)
		username = firstName + "." + lastName
		email = username + "@itsolutions.com"
		# validate that  user does not exist in database
		exists = db.execute("SELECT employee_id FROM employees WHERE username = ?", username)
		if exists and not error:
			error = "User already exists in database"
		# retreive the HR code and check if correct input from user
		codeHR = db.execute("SELECT hr_code FROM human_resources")[0]["hr_code"]
		if code != codeHR and not error:
			error = "Invalid HR code"
		# validate if user has permission and then execute data in database
		if code == codeHR and not error:
			db.execute("INSERT INTO employees (firstName, lastName, email, username, password, name) VALUES(?, ?, ?, ?, ?, ?)", firstName, lastName, email, username, hash, name)
			userId = db.execute("SELECT employee_id FROM employees WHERE username = ?", username)
			session["user_id"] = userId[0]["employee_id"]
			flash("Registration successfull - You are logged in")
			return redirect("/")
		return render_template("register.html", error=error)
	else:
		return render_template("register.html")

# LOGOUT
@app.route("/logout")
def logout():
	"""Log user out"""

	# Forget any user_id
	session.clear()
	flash("You are logged out")
	# Redirect user to login form
	return redirect("/")

# SUBMIT TICKET
@app.route("/submit", methods=["GET", "POST"])
def submit():
	error = None
	if request.method == "POST":
		ticket = fetchTicket()
		if not ticket["createdBy"] or not ticket["email"] or not ticket["assetTag"] or not ticket["serviceType"] or not ticket["subject"]:
			error = "Please make sure all fields are filled before submitting"
		if not error:
			ticket["status"] = "Open"
			db.execute("INSERT INTO tickets (created_by, email, asset_tag, service_type, subject, description, status) VALUES(?, ?, ?, ?, ?, ?, ?)", ticket["createdBy"], ticket["email"], ticket["assetTag"], ticket["serviceType"], ticket["subject"], ticket["description"], ticket["status"])
			flash("Ticket submitted successfully")
		assets = db.execute("SELECT asset_tag FROM assets ORDER BY asset_tag DESC")
		return render_template("submit.html", assets=assets, error=error)
	else:
		assets = db.execute("SELECT asset_tag FROM assets ORDER BY asset_tag DESC")
		return render_template("submit.html", assets=assets)

# TICKETS
@app.route("/tickets", methods=["GET", "POST"])
@login_required
def tickets():
	tickets, assets, agents = fetchDatabase()
	error = None
	if request.method == "POST":
		postType = request.form.get("postType")
		# New ticket
		if postType == "new":
			ticket = fetchTicket()
			ticket["status"] = "Open"
			ticket["agentName"] = "None"
			# Check if input submit ticket are empty
			if not ticket["createdBy"] or not ticket["email"] or not ticket["assetTag"] or not ticket["serviceType"] or not ticket["subject"]:
				error = "Try again: please make sure all fields are submitted"
				tickets, assets, agents = fetchDatabase()
				return render_template("tickets.html", tickets=tickets, assets=assets, agents=agents, error=error)
			db.execute("INSERT INTO tickets (created_by, email, asset_tag, service_type, subject, description, status) VALUES(?, ?, ?, ?, ?, ?, ?)",
				ticket["createdBy"], ticket["email"], ticket["assetTag"], ticket["serviceType"], ticket["subject"], ticket["description"], ticket["status"])
			flash("Ticket submitted successfully")
			return redirect("/tickets")
		# Modify ticket
		if postType == "edit":
			ticket = fetchTicket()
			if not ticket["createdBy"] or not ticket["email"] or not ticket["subject"]:
				error = "Please make sure fields Subject, Created by, Email are not empty"
				return render_template("tickets.html", tickets=tickets, assets=assets, agents=agents, error=error)
			# Conditions to print the timestamp for closing and opening tickets
			previousStatus = db.execute("SELECT status FROM tickets WHERE ticket_id = ?", ticket["ticketId"])
			if ticket["status"] == "Closed" and previousStatus[0]["status"] == "Open":
				db.execute("UPDATE tickets SET status = ?, service_type = ?, subject = ?, description = ?, asset_tag = ?, created_by = ?, email = ?, agent_name = ?, time_closed = CURRENT_TIMESTAMP WHERE ticket_id = ?;",
					ticket["status"], ticket["serviceType"], ticket["subject"], ticket["description"], ticket["assetTag"], ticket["createdBy"], ticket["email"], ticket["agentName"], ticket["ticketId"])
			elif ticket["status"] == "Open" and previousStatus[0]["status"] == "Closed":
				db.execute("UPDATE tickets SET status = ?, service_type = ?, subject = ?, description = ?, asset_tag = ?, created_by = ?, email = ?, agent_name = ?, time_closed = NULL WHERE ticket_id = ?;",
					ticket["status"], ticket["serviceType"], ticket["subject"], ticket["description"], ticket["assetTag"], ticket["createdBy"], ticket["email"], ticket["agentName"], ticket["ticketId"])
			else:
				db.execute("UPDATE tickets SET status = ?, service_type = ?, subject = ?, description = ?, asset_tag = ?, created_by = ?, email = ?, agent_name = ? WHERE ticket_id = ?;",
					ticket["status"], ticket["serviceType"], ticket["subject"], ticket["description"], ticket["assetTag"], ticket["createdBy"], ticket["email"], ticket["agentName"], ticket["ticketId"])
			flash("Ticket modifed successfully")
			return redirect("/tickets")
		# Delete ticket
		if postType == "delete":
			ticket = fetchTicket()
			db.execute("DELETE FROM tickets WHERE ticket_id = ?", ticket["ticketId"])
			message = "Ticket " + ticket["ticketId"] + " deleted successfully"
			flash(message)
			return redirect("/tickets")
	else:
		tickets, assets, agents = fetchDatabase()
		return render_template("tickets.html", tickets=tickets, assets=assets, agents=agents)

# ASSETS
@app.route("/assets", methods=["GET", "POST"])
@login_required
def assets():
	error = None
	if request.method == "POST":
		postType = request.form.get("postType")
		# New asset
		if postType == "new":
			assets = fetchAsset()
			# Handles errors if fields are empty
			if not assets["assetTag"] or not assets["deviceType"] or not assets["brand"] or not assets["model"] or not assets["serialNumber"] or not assets["dateInService"] or not assets["warrantyStart"]:
				error = "Make sure all fields are filled"
				assets = db.execute("SELECT * FROM assets ORDER BY asset_id DESC")
				return render_template("assets.html", assets=assets, error=error)
			db.execute("INSERT INTO assets (asset_tag, device_type, brand, model, serial_number, date_in_service, warranty_start, warranty_end, asset_status) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
				assets["assetTag"], assets["deviceType"], assets["brand"], assets["model"], assets["serialNumber"], assets["dateInService"], assets["warrantyStart"], assets["warrantyEnd"], "In service")
			flash("The asset was created successfully")
			return redirect("/assets")
		# Modify asset
		if postType == "edit":
			assets = fetchAsset()
			# Handles errors if fields are empty
			if not assets["assetTag"] or not assets["deviceType"] or not assets["brand"] or not assets["model"] or not assets["serialNumber"] or not assets["dateInService"] or not assets["warrantyStart"]:
				error = "Make sure all fields are filled"
				assets = db.execute("SELECT * FROM assets ORDER BY asset_id DESC")
				return render_template("assets.html", assets=assets, error=error)
			db.execute("UPDATE assets SET asset_tag = ?, device_type = ?, brand = ?, model = ?, serial_number = ?, date_in_service = ?, warranty_start = ?, warranty_end = ?, asset_status = ? WHERE asset_id = ?",
				assets["assetTag"], assets["deviceType"], assets["brand"], assets["model"], assets["serialNumber"], assets["dateInService"], assets["warrantyStart"], assets["warrantyEnd"], assets["assetStatus"], assets["assetId"])
			flash("The asset was modified successfully")
			return redirect("/assets")
		# Delete asset
		if postType == "delete":
			assets = fetchAsset()
			db.execute("DELETE FROM assets WHERE asset_id = ?", assets["assetId"])
			message = "The asset " + assets["assetTag"] + " was deleted successfully"
			flash(message)
			return redirect("/assets")
	else:
		assets = db.execute("SELECT * FROM assets ORDER BY asset_id DESC")
		return render_template("assets.html", assets=assets, error=error)

# AGENTS
@app.route("/agents", methods=["GET", "POST"])
@login_required
def agents():
	# initiate the inputs given from the user
	error = None
	if request.method == "POST":
		codeHR = request.form.get("codeHR")
		if not codeHR:
			error = "The field cannot be blank"
			agents = db.execute("SELECT * FROM employees")
			codeHR = db.execute("SELECT hr_code FROM human_resources")[0]["hr_code"]
			return render_template("agents.html", agents=agents, codeHR=codeHR, error=error)
		db.execute("UPDATE human_resources SET hr_code = ?", codeHR)
		flash("Successfull - HR code updated")
		return redirect("/agents")
	else:
		agents = db.execute("SELECT * FROM employees")
		codeHR = db.execute("SELECT hr_code FROM human_resources")[0]["hr_code"]
		for row in agents:
			row["firstName"] = row["firstName"].title()
			row["lastName"] = row["lastName"].title()
		return render_template("agents.html", agents=agents, codeHR=codeHR)

# SEARCH TICKETS JS Sync
@app.route("/searchTickets", methods=["GET"])
@login_required
def searchTickets():
	q = request.args.get("q")
	if q:
		tickets = db.execute("SELECT * FROM tickets WHERE subject LIKE ? ORDER BY ticket_id DESC", "%" + q + "%")
	else:
		tickets = db.execute("SELECT * FROM tickets ORDER BY ticket_id DESC")
	return render_template("searchTickets.html", tickets=tickets)

# SEARCH ASSETS JS Sync
@app.route("/searchAssets", methods=["GET"])
@login_required
def searchAssets():
	q = request.args.get("q")
	if q:
		assets = db.execute("SELECT * FROM assets WHERE asset_tag LIKE ? ORDER BY asset_id DESC", "%" + q + "%")
	else:
		assets = db.execute("SELECT * FROM assets ORDER BY asset_id DESC")
	return render_template("searchAssets.html", assets=assets)

# FETCH TICKET FORM REQUEST INPUTS
def fetchTicket():
	ticket = {}
	ticket["ticketId"] = request.form.get("ticketId")
	ticket["status"] = request.form.get("status")
	ticket["serviceType"] = request.form.get("serviceType")
	ticket["subject"] = request.form.get("subject")
	ticket["description"] = request.form.get("description")
	ticket["assetTag"] = request.form.get("assetTag")
	ticket["createdBy"] = request.form.get("createdBy")
	ticket["email"] = request.form.get("email")
	ticket["agentName"] = request.form.get("agentName")
	ticket["timeCreated"] = request.form.get("timeCreated")
	ticket["timeClosed"] = request.form.get("timeClosed")
	return ticket

# FETCH ASSET FORM REQUEST INPUTS
def fetchAsset():
	assets = {}
	assets["assetId"] = request.form.get("assetId")
	assets["assetTag"] = request.form.get("assetTag")
	assets["deviceType"] = request.form.get("deviceType")
	assets["brand"] = request.form.get("brand")
	assets["model"] = request.form.get("model")
	assets["serialNumber"] = request.form.get("serialNumber")
	assets["dateInService"] = request.form.get("dateInService")
	assets["warrantyStart"] = request.form.get("warrantyStart")
	assets["warrantyEnd"] = request.form.get("warrantyEnd")
	assets["assetStatus"] = request.form.get("assetStatus")
	return assets

# FETCH DATABASE BEFORE RENDERING TICKETS.HTML
def fetchDatabase():
	tickets = db.execute("SELECT * FROM tickets ORDER BY ticket_id DESC")
	assets = db.execute("SELECT * FROM assets ORDER BY asset_tag DESC")
	agents = db.execute("SELECT * FROM employees ORDER BY username DESC")
	return tickets, assets, agents