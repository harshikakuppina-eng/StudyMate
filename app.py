from flask import Flask, request, jsonify, send_from_directory, session, redirect
import sqlite3
import uuid

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


app = Flask(__name__)

# =====================================================
# FLASK SETTINGS
# =====================================================

app.secret_key = "studymate-secret-key-2026"

DATABASE = "studymate.db"


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_db():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


# =====================================================
# DATABASE CREATION
# =====================================================

def create_database():

    connection = get_db()


    # USERS TABLE

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)


    # PROGRESS TABLE

    connection.execute("""
        CREATE TABLE IF NOT EXISTS progress (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            visitor_id TEXT NOT NULL,

            topic_id TEXT NOT NULL,

            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(visitor_id, topic_id)

        )
    """)

    # =====================================================
    # USER PROGRESS TABLE
    # =====================================================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            topic_id TEXT NOT NULL,

            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(user_id, topic_id)
        )
    """)

    connection.commit()

    connection.close()



# =====================================================
# TOPIC MAP
# =====================================================

TOPIC_MAP = {

    # ================= PYTHON =================

    "/python-basics": "python_basics",
    "/conditions": "conditions",
    "/loops": "loops",
    "/functions": "functions",
    "/lists": "lists",
    "/input": "input",
    "/dictionaries": "dictionaries",
    "/tuples": "tuples",
    "/sets": "sets",
    "/strings": "strings",
    "/oop": "oop",
    "/exception": "exception",
    "/file-handling": "file_handling",
    "/modules": "modules",
    "/mini-project": "mini_project",


    # ================= WEB =================

    "/html": "html",
    "/text": "text",
    "/links-images": "links_images",
    "/lists-tables": "lists_tables",
    "/forms": "forms",

    "/css-basics": "css_basics",
    "/colors-fonts": "colors_fonts",
    "/box-model": "box_model",
    "/flexbox": "flexbox",
    "/responsive-design": "responsive_design",

    "/javascript-basics": "javascript_basics",
    "/variables-data-types": "variables_data_types",
    "/js-conditions-loops": "js_conditions_loops",
    "/js-functions-events": "js_functions_events",
    "/dom-mini-project": "dom_mini_project",


    # ================= CYBERSECURITY =================

    "/cybersecurity-basics": "cybersecurity_basics",
    "/networking-fundamentals": "networking_fundamentals",
    "/osint": "osint",
    "/reconnaissance": "reconnaissance",
    "/vulnerabilities": "vulnerabilities",
    "/linux-basics": "linux_basics",
    "/kali-linux-tools": "kali_linux_tools",
    "/wireshark": "wireshark",
    "/burp-suite": "burp_suite",
    "/authentication": "authentication",
    "/malware-basics": "malware_basics",
    "/phishing-social-engineering": "phishing_social_engineering",
    "/firewalls-ids-ips": "firewalls_ids_ips",
    "/digital-forensics": "digital_forensics",
    "/cybersecurity-mini-project": "cybersecurity_mini_project",


    # ================= NETWORKING =================

    "/networking-intro": "networking_intro",
    "/networking-ip-mac": "networking_ip_mac",
    "/networking-ipv4-ipv6": "networking_ipv4_ipv6",
    "/networking-devices": "networking_devices",
    "/networking-osi": "networking_osi",
    "/networking-tcp-ip": "networking_tcp_ip",
    "/networking-ports-protocols": "networking_ports_protocols",
    "/networking-dns-dhcp": "networking_dns_dhcp",
    "/networking-arp-rarp": "networking_arp_rarp",
    "/networking-routing": "networking_routing",
    "/networking-wifi": "networking_wifi",
    "/networking-security": "networking_security",
    "/networking-troubleshooting": "networking_troubleshooting",
    "/networking-wireshark": "networking_wireshark",
    "/networking-mini-project": "networking_mini_project"

}


# =====================================================
# AUTOMATIC TOPIC TRACKING
# =====================================================

@app.before_request
def track_topic():

    current_path = request.path

    topic_id = TOPIC_MAP.get(current_path)

    if not topic_id:
        return


    # Track progress for logged-in user
    if "user_id" not in session:
        return

    user_id = session["user_id"]

    connection = get_db()

    connection.execute(
        """
        INSERT OR IGNORE INTO user_progress
        (user_id, topic_id)
        VALUES (?, ?)
        """,
        (user_id, topic_id)
    )

    connection.commit()
    connection.close()



# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    return send_from_directory(".", "index.html")



# =====================================================
# LOGIN
# =====================================================

@app.route("/login")
def login_page():

    return send_from_directory(".", "login.html")



# =====================================================
# REGISTER
# =====================================================

@app.route("/register")
def register_page():

    return send_from_directory(".", "register.html")



# =====================================================
# LEARN
# =====================================================

@app.route("/learn")
def learn_page():

    if "user_id" not in session:
        return redirect("/login")

    return send_from_directory(".", "learn.html")



# =====================================================
# WEB DEVELOPMENT
# =====================================================

@app.route("/html")
def html_page():

    return send_from_directory(".", "html.html")


@app.route("/text")
def text_page():

    return send_from_directory(".", "text.html")


@app.route("/links-images")
def links_images_page():

    return send_from_directory(".", "links_images.html")


@app.route("/lists-tables")
def lists_tables_page():

    return send_from_directory(".", "lists_tables.html")


@app.route("/forms")
def forms_page():

    return send_from_directory(".", "forms.html")


@app.route("/css-basics")
def css_basics_page():

    return send_from_directory(".", "css_basics.html")


@app.route("/colors-fonts")
def colors_fonts_page():

    return send_from_directory(".", "colors_fonts.html")


@app.route("/box-model")
def box_model_page():

    return send_from_directory(".", "box_model.html")


@app.route("/flexbox")
def flexbox_page():

    return send_from_directory(".", "flexbox.html")


@app.route("/responsive-design")
def responsive_design_page():

    return send_from_directory(".", "responsive_design.html")


@app.route("/javascript-basics")
def javascript_basics_page():

    return send_from_directory(".", "javascript_basics.html")


@app.route("/variables-data-types")
def variables_data_types_page():

    return send_from_directory(".", "variables_data_types.html")


@app.route("/js-conditions-loops")
def js_conditions_loops_page():

    return send_from_directory(".", "js_conditions_loops.html")


@app.route("/js-functions-events")
def js_functions_events_page():

    return send_from_directory(".", "js_functions_events.html")


@app.route("/dom-mini-project")
def dom_mini_project_page():

    return send_from_directory(".", "dom_mini_project.html")



# =====================================================
# CYBERSECURITY
# =====================================================

@app.route("/cybersecurity")
def cybersecurity_page():

    return send_from_directory(".", "cybersecurity.html")


@app.route("/cybersecurity-basics")
def cybersecurity_basics_page():

    return send_from_directory(".", "cybersecurity_basics.html")


@app.route("/networking-fundamentals")
def networking_fundamentals_page():

    return send_from_directory(".", "networking_fundamentals.html")


@app.route("/osint")
def osint_page():

    return send_from_directory(".", "osint.html")


@app.route("/reconnaissance")
def reconnaissance_page():

    return send_from_directory(".", "reconnaissance.html")


@app.route("/vulnerabilities")
def vulnerabilities_page():

    return send_from_directory(".", "vulnerabilities.html")


@app.route("/linux-basics")
def linux_basics_page():

    return send_from_directory(".", "linux_basics.html")


@app.route("/kali-linux-tools")
def kali_linux_tools_page():

    return send_from_directory(".", "kali_linux_tools.html")


@app.route("/wireshark")
def wireshark_page():

    return send_from_directory(".", "wireshark.html")


@app.route("/burp-suite")
def burp_suite_page():

    return send_from_directory(".", "burp_suite.html")


@app.route("/authentication")
def authentication_page():

    return send_from_directory(".", "authentication.html")


@app.route("/malware-basics")
def malware_basics_page():

    return send_from_directory(".", "malware_basics.html")


@app.route("/phishing-social-engineering")
def phishing_social_engineering_page():

    return send_from_directory(
        ".",
        "phishing_social_engineering.html"
    )


@app.route("/firewalls-ids-ips")
def firewalls_ids_ips_page():

    return send_from_directory(
        ".",
        "firewalls_ids_ips.html"
    )


@app.route("/digital-forensics")
def digital_forensics_page():

    return send_from_directory(
        ".",
        "digital_forensics.html"
    )


@app.route("/cybersecurity-mini-project")
def cybersecurity_mini_project_page():

    return send_from_directory(
        ".",
        "cybersecurity_mini_project.html"
    )



# =====================================================
# NETWORKING
# =====================================================

@app.route("/networking")
def networking_page():

    return send_from_directory(
        ".",
        "networking.html"
    )


@app.route("/networking-intro")
def networking_intro_page():

    return send_from_directory(
        ".",
        "networking_intro.html"
    )


@app.route("/networking-ip-mac")
def networking_ip_mac_page():

    return send_from_directory(
        ".",
        "networking_ip_mac.html"
    )


@app.route("/networking-ipv4-ipv6")
def networking_ipv4_ipv6_page():

    return send_from_directory(
        ".",
        "networking_ipv4_ipv6.html"
    )


@app.route("/networking-devices")
def networking_devices_page():

    return send_from_directory(
        ".",
        "networking_devices.html"
    )


@app.route("/networking-osi")
def networking_osi_page():

    return send_from_directory(
        ".",
        "networking_osi.html"
    )


@app.route("/networking-tcp-ip")
def networking_tcp_ip_page():

    return send_from_directory(
        ".",
        "networking_tcp_ip.html"
    )


@app.route("/networking-ports-protocols")
def networking_ports_protocols_page():

    return send_from_directory(
        ".",
        "networking_ports_protocols.html"
    )


@app.route("/networking-dns-dhcp")
def networking_dns_dhcp_page():

    return send_from_directory(
        ".",
        "networking_dns_dhcp.html"
    )


@app.route("/networking-arp-rarp")
def networking_arp_rarp_page():

    return send_from_directory(
        ".",
        "networking_arp_rarp.html"
    )


@app.route("/networking-routing")
def networking_routing_page():

    return send_from_directory(
        ".",
        "networking_routing.html"
    )


@app.route("/networking-wifi")
def networking_wifi_page():

    return send_from_directory(
        ".",
        "networking_wifi.html"
    )


@app.route("/networking-security")
def networking_security_page():

    return send_from_directory(
        ".",
        "networking_security.html"
    )


@app.route("/networking-troubleshooting")
def networking_troubleshooting_page():

    return send_from_directory(
        ".",
        "networking_troubleshooting.html"
    )


@app.route("/networking-wireshark")
def networking_wireshark_page():

    return send_from_directory(
        ".",
        "networking_wireshark.html"
    )


@app.route("/networking-mini-project")
def networking_mini_project_page():

    return send_from_directory(
        ".",
        "networking_mini_project.html"
    )



# =====================================================
# PLANNER
# =====================================================

@app.route("/planner")
def planner_page():

    return send_from_directory(
        ".",
        "planner.html"
    )



# =====================================================
# QUIZ
# =====================================================

@app.route("/quiz")
def quiz_page():

    return send_from_directory(
        ".",
        "quiz.html"
    )



# =====================================================
# PROGRESS PAGE
# =====================================================

@app.route("/progress")
def progress_page():

    return send_from_directory(
        ".",
        "progress.html"
    )

# =====================================================
# CERTIFICATE
# =====================================================

@app.route("/certificate")
def certificate_page():

    return send_from_directory(
        ".",
        "certificate.html"
    )


# =====================================================
# PYTHON
# =====================================================

@app.route("/python")
def python_page():

    return send_from_directory(
        ".",
        "python.html"
    )


@app.route("/python-basics")
def python_basics_page():

    return send_from_directory(
        ".",
        "python_basics.html"
    )


@app.route("/conditions")
def conditions_page():

    return send_from_directory(
        ".",
        "conditions.html"
    )


@app.route("/loops")
def loops_page():

    return send_from_directory(
        ".",
        "loops.html"
    )


@app.route("/functions")
def functions_page():

    return send_from_directory(
        ".",
        "functions.html"
    )


@app.route("/lists")
def lists_page():

    return send_from_directory(
        ".",
        "lists.html"
    )


@app.route("/input")
def input_page():

    return send_from_directory(
        ".",
        "input.html"
    )


@app.route("/dictionaries")
def dictionaries_page():

    return send_from_directory(
        ".",
        "dictionaries.html"
    )


@app.route("/tuples")
def tuples_page():

    return send_from_directory(
        ".",
        "tuples.html"
    )


@app.route("/sets")
def sets_page():

    return send_from_directory(
        ".",
        "sets.html"
    )


@app.route("/strings")
def strings_page():

    return send_from_directory(
        ".",
        "strings.html"
    )


@app.route("/oop")
def oop_page():

    return send_from_directory(
        ".",
        "oop.html"
    )


@app.route("/exception")
def exception_page():

    return send_from_directory(
        ".",
        "exception.html"
    )


@app.route("/file-handling")
def file_handling_page():

    return send_from_directory(
        ".",
        "file_handling.html"
    )


@app.route("/modules")
def modules_page():

    return send_from_directory(
        ".",
        "modules.html"
    )


@app.route("/mini-project")
def mini_project_page():

    return send_from_directory(
        ".",
        "mini_project.html"
    )



# =====================================================
# CSS
# =====================================================

@app.route("/style.css")
def style():

    return send_from_directory(
        ".",
        "style.css"
    )



# =====================================================
# JAVASCRIPT
# =====================================================

@app.route("/script.js")
def script():

    return send_from_directory(
        ".",
        "script.js"
    )



# =====================================================
# REGISTER API
# =====================================================

@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()


    name = data.get("name")

    email = data.get("email")

    password = data.get("password")


    if not name or not email or not password:

        return jsonify({

            "success": False,

            "message": "All fields are required."

        }), 400


    connection = get_db()


    existing_user = connection.execute(

        "SELECT * FROM users WHERE email = ?",

        (email,)

    ).fetchone()


    if existing_user:

        connection.close()


        return jsonify({

            "success": False,

            "message": "Email already registered."

        }), 409


    hashed_password = generate_password_hash(
        password
    )


    connection.execute(

        """
        INSERT INTO users
        (name, email, password)

        VALUES (?, ?, ?)
        """,

        (
            name,
            email,
            hashed_password
        )

    )


    connection.commit()

    connection.close()


    return jsonify({

        "success": True,

        "message": "Account created successfully!"

    })



# =====================================================
# LOGIN API
# =====================================================

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()


    email = data.get("email")

    password = data.get("password")


    connection = get_db()


    user = connection.execute(

        "SELECT * FROM users WHERE email = ?",

        (email,)

    ).fetchone()


    connection.close()


    if user and check_password_hash(
        user["password"],
        password
    ):

        session["visitor_id"] = session.get(
            "visitor_id",
            str(uuid.uuid4())
        )


        session["user_id"] = user["id"]


        return jsonify({

            "success": True,

            "message":
                f"Login successful! Welcome {user['name']} ❤️",

            "name": user["name"]

        })


    return jsonify({

        "success": False,

        "message": "Invalid email or password."

    }), 401



# =====================================================
# PROGRESS API
# =====================================================

@app.route("/api/progress")
def get_progress():

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401


    user_id = session["user_id"]


    connection = get_db()


    rows = connection.execute(

        """
        SELECT topic_id

FROM user_progress

WHERE user_id = ?

ORDER BY id
        """,

        (user_id,)

    ).fetchall()


    connection.close()


    completed_topics = [

        row["topic_id"]

        for row in rows

    ]


    return jsonify({

        "success": True,

        "completed_topics":
            completed_topics,

        "topics_learned":
            len(completed_topics)

    })



# =====================================================
# START SERVER
# =====================================================

if __name__ == "__main__":

    create_database()

    app.run(debug=True)