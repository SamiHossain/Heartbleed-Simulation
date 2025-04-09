#  Heartbleed Vulnerability Simulation

This project simulates the infamous **Heartbleed** vulnerability (CVE-2014-0160) in the TLS heartbeat extension. It demonstrates how improper bounds checking in a TLS heartbeat request can result in unintended memory leakage from a vulnerable server.

##  Project Overview

- A **vulnerable TLS server** is created using `pyOpenSSL`, which accepts heartbeat requests but lacks proper validation.
- An **attacker client** connects to the server, sends a malformed heartbeat request, and captures the leaked memory data.

This project is for educational purposes only.

---

##  How to Run the Simulation

1. Clone the Repository

You may need to delete the current server.crt and server.key and generate your own

2. Install Dependencies
Ensure you have Python 3.x installed. Then install the required libraries:

in bash type:
pip install pyOpenSSL

3. Generate TLS Certificate
Use openssl to generate a self-signed certificate and private key:

in bash type:
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt

## Running the Simulation

Step 1: Start the Vulnerable Server

in a terminal type:
python vulnerable_server.py

Step 2: Run the Attacker Client

In a new terminal, run:
python attacker_client.py

