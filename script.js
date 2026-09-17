/* =====================================================
   STUDYMATE - MAIN JAVASCRIPT
   ===================================================== */


/* =====================================================
   AUTOMATIC TOPIC COMPLETION
   ===================================================== */

const topicMap = {

    /* ================= PYTHON ================= */

    "/python_basics": "python_basics",
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


    /* ================= WEB DEVELOPMENT ================= */

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


    /* ================= CYBERSECURITY ================= */

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


    /* ================= NETWORKING ================= */

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

};


/* =====================================================
   SAVE CURRENT TOPIC AUTOMATICALLY
   ===================================================== */

function automaticallyCompleteTopic() {

    const currentPath = window.location.pathname;

    const topicId = topicMap[currentPath];

    if (!topicId) {
        return;
    }


    let completedTopics = [];


    try {

        completedTopics = JSON.parse(
            localStorage.getItem(
                "studymateCompletedTopics"
            ) || "[]"
        );

    } catch (error) {

        completedTopics = [];

    }


    if (!completedTopics.includes(topicId)) {

        completedTopics.push(topicId);

        localStorage.setItem(
            "studymateCompletedTopics",
            JSON.stringify(completedTopics)
        );

        console.log(
            "StudyMate completed:",
            topicId
        );

    }

}


/* Run automatic completion */

automaticallyCompleteTopic();



/* =====================================================
   REGISTER
   ===================================================== */

const registerForm =
    document.getElementById("registerForm");


if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const name =
                document.getElementById("name")?.value.trim();

            const email =
                document.getElementById("registerEmail")?.value.trim();

            const password =
                document.getElementById("registerPassword")?.value;

            const confirmPassword =
                document.getElementById("confirmPassword")?.value;


            if (!name || !email || !password || !confirmPassword) {

                alert("Please fill all fields.");

                return;

            }


            if (password !== confirmPassword) {

                alert("Passwords do not match.");

                return;

            }


            try {

                const response =
                    await fetch("/api/register", {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            name: name,

                            email: email,

                            password: password

                        })

                    });


                const data =
                    await response.json();


                if (response.ok) {

                    alert(
                        data.message ||
                        "Registration successful!"
                    );

                    window.location.href =
                        "/login";

                }

                else {

                    alert(
                        data.message ||
                        "Registration failed."
                    );

                }

            }

            catch (error) {

                alert(
                    "Something went wrong. Please try again."
                );

                console.error(error);

            }

        }
    );

}



/* =====================================================
   LOGIN
   ===================================================== */

const loginForm =
    document.getElementById("loginForm");


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const email =
                document.getElementById("loginEmail")?.value.trim();

            const password =
                document.getElementById("loginPassword")?.value;


            if (!email || !password) {

                alert(
                    "Please enter email and password."
                );

                return;

            }


            try {

                const response =
                    await fetch("/api/login", {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            email: email,

                            password: password

                        })

                    });


                const data =
                    await response.json();


                if (response.ok) {

                    alert(
                        data.message ||
                        "Login successful!"
                    );

                    window.location.href =
                        "/";

                }

                else {

                    alert(
                        data.message ||
                        "Invalid email or password."
                    );

                }

            }

            catch (error) {

                alert(
                    "Unable to connect to server."
                );

                console.error(error);

            }

        }
    );

}



/* =====================================================
   PYTHON EDITOR
   ===================================================== */

const pythonEditor =
    document.getElementById("pythonEditor");

const runPythonButton =
    document.getElementById("runPythonButton");

const pythonOutput =
    document.getElementById("pythonOutput");


if (
    pythonEditor &&
    runPythonButton &&
    pythonOutput
) {

    runPythonButton.addEventListener(
        "click",
        function () {

            const code =
                pythonEditor.value.trim();


            if (!code) {

                pythonOutput.textContent =
                    "Please write some Python code.";

                return;

            }


            pythonOutput.textContent =
                "Python code submitted for practice.\n\n" +
                "Run this code in your Python environment.";

        }
    );

}