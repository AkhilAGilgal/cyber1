# CSRF Vulnerability Scanner and Proof of Concept

## Project Overview

This project addresses the requirements of a cybersecurity assignment focused on Cross-Site Request Forgery (CSRF). It includes three main components:
1.  **Research:** A summary of CSRF middleware and protection mechanisms.
2.  **CSRF Scanner:** A Python-based crawler (`csrf_scanner.py`) that scans web applications for forms lacking CSRF token protection.
3.  **Proof of Concept (PoC):** An HTML page (`poc.html`) that demonstrates a successful CSRF attack against a sample vulnerable application.

---

## 1. Research: CSRF Middleware and Protections

Cross-Site Request Forgery (CSRF) is an attack that tricks a user into submitting a malicious request. It leverages the user's existing session/authentication with a web application to perform unauthorized actions (e.g., changing an email, transferring funds, deleting an account).

### How CSRF Protections Work

Modern web frameworks use CSRF middleware to protect against these attacks. The most common method is the **Synchronizer (CSRF) Token Pattern**.

1.  **Token Generation:** When a user requests a page with a form, the server generates a unique, unpredictable token.
2.  **Token Embedding:** This token is embedded as a hidden input field in the form.
3.  **Token Validation:** When the user submits the form, the server-side middleware checks if the submitted token matches the one stored in the user's session.
    *   **If tokens match:** The request is considered legitimate and is processed.
    *   **If tokens do not match (or the token is missing):** The request is rejected as potentially malicious.

This works because an attacker, hosting the malicious form on a different domain, cannot guess or access the correct token required by the application.

Other protections include:
*   **SameSite Cookies:** This attribute tells the browser whether to send cookies with cross-site requests. Setting it to `Strict` or `Lax` provides strong protection against CSRF.
*   **Checking the Referer/Origin Header:** The server can check if the request originated from its own domain, but this is less reliable as headers can sometimes be spoofed or stripped.

---

## 2. The CSRF Vulnerability Scanner

The `csrf_scanner.py` script is a crawler designed to identify forms that are potentially vulnerable to CSRF attacks by checking for the absence of CSRF tokens.

### How it Works

1.  **Initialization:** The scanner takes a starting URL as input.
2.  **Crawling:** It uses `requests` to fetch the page content and `BeautifulSoup` to parse the HTML. It identifies all internal links on the page to scan them recursively.
3.  **Form Analysis:** For each page, it finds all `<form>` elements.
4.  **Token Check:** Within each form, it looks for an `<input>` field with common CSRF token names (e.g., `csrf_token`, `csrfmiddlewaretoken`, `_token`).
5.  **Reporting:** If a form is found without a recognizable CSRF token, it is flagged as potentially vulnerable and its URL and action attribute are printed to the console.

### Usage

1.  Install the required libraries:
    ```bash
    pip install requests beautifulsoup4
    ```
2.  Run the scanner from the command line:
    ```bash
    python csrf_scanner.py <your-target-url>
    ```
    *Example:*
    ```bash
    python csrf_scanner.py http://127.0.0.1:5000
    ```

### Scanner in Action (Screenshot)

*(You will add your screenshot here)*

![Scanner Output](images/scanner_output.png)

---

## 3. Proof of Concept (PoC) Attack

To demonstrate the impact of a missing CSRF token, we created a sample vulnerable application and an HTML PoC to exploit it.

### The Vulnerable Application

A simple Flask application (`vulnerable_app.py`) was created with a form to change a user's email. **This form intentionally lacks a CSRF token.**

*   **Vulnerable Endpoint:** `POST /change-email`
*   **Action:** Changes the user's email to the one provided in the `email` parameter.
*   **Vulnerability:** It does not validate any CSRF token, so it will process any valid POST request from any source as long as the user is logged in.

![Vulnerable App Code](images/vulnerable_app_code.png)

### The Attack Scenario

1.  A victim is logged into the vulnerable application (`http://127.0.0.1:5000`).
2.  The victim visits a malicious website controlled by an attacker.
3.  This malicious website contains our `poc.html` page.
4.  The `poc.html` page contains a hidden form that targets the vulnerable `/change-email` endpoint. The form is pre-filled with the attacker's email address.
5.  JavaScript on the page automatically submits this form as soon as the page loads.
6.  Because the victim is logged in, their browser automatically attaches their session cookie to the request. The vulnerable server sees a valid session and processes the request, changing the victim's email to the attacker's email without the victim's knowledge.

### The PoC HTML (`poc.html`)

This HTML page performs the attack. It tells the user it's a "fun cat website" to trick them, while the hidden form submits in the background.

![PoC Code](images/poc_code.png)

### Demonstration of the Attack

1.  The user is logged in and their email is `user@example.com`.
![Vulnerable App Before Attack](images/app_before_attack.png)

2.  The user visits the attacker's `poc.html` page. The page auto-submits.
![PoC Page](images/poc_page.png)

3.  The user's email on the vulnerable application is now changed to `attacker@malicious.com`. The attack was successful.
![Vulnerable App After Attack](images/app_after_attack.png)
