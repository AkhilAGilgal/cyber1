# CSRF Vulnerability Scanner and Proof of Concept

## 📜 Project Overview

This project is designed to research and identify Cross-Site Request Forgery (CSRF) vulnerabilities in web applications. It includes a Python-based crawler to detect missing CSRF protections and an HTML-based Proof of Concept (PoC) to demonstrate the vulnerability.

---

## 📌 Part 1: Research on CSRF Middleware and Protections

### What is CSRF?

Cross-Site Request Forgery (CSRF) is an attack that tricks a user into submitting a malicious request. It inherits the identity and privileges of the victim to perform an undesired function on their behalf. For most sites, browser requests automatically include any credentials associated with the site, such as session cookies, IP addresses, and domain credentials. Therefore, if the user is authenticated to the site, the site cannot distinguish between a forged request and a legitimate one.

### How CSRF Protection Works

Modern web frameworks provide middleware to protect against CSRF attacks. The most common mitigation is the **Synchronizer Token Pattern**.

1.  **Token Generation**: When a user requests a page with a form, the server generates a unique, random token (the CSRF token).
2.  **Token Embedding**: This token is embedded within a hidden input field in the form.
3.  **Token Validation**: When the user submits the form, the token is sent back to the server. The server-side middleware then compares this token with the one it generated. If they match, the request is considered legitimate. If the token is missing or incorrect, the request is rejected.

---

## 🐍 Part 2: CSRF Crawler

This project includes a Python crawler designed to scan web applications for potential CSRF vulnerabilities.

### How it Works

The crawler (`crawler.py`) automatically discovers and analyzes forms within a web application. It checks each form for the presence of a CSRF token.

1.  **Crawling**: The script starts at a given URL and recursively follows all links on the same domain.
2.  **Form Detection**: For each page, it parses the HTML to find all `<form>` elements.
3.  **Token Verification**: It then checks if each form contains an `input` field with a name commonly used for CSRF tokens (e.g., `csrf_token`, `_csrf`, `authenticity_token`).
4.  **Reporting**: The crawler prints a report of all forms found and indicates whether they have a CSRF token.

### How to Use the Crawler

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AkhilAGilgal/cyber1.git
    cd cyber1
    ```
2.  **Install dependencies:**
    ```bash
    pip install requests beautifulsoup4
    ```
3.  **Run the script:**
    ```bash
    python crawler.py <URL_TO_SCAN>
    ```
    Replace `<URL_TO_SCAN>` with the URL of the web application you want to test.

*(Optional: Insert a screenshot of the crawler in action here. See instructions below on how to add images.)*

---

## 💥 Part 3: HTML Proof of Concept (PoC)

To demonstrate a successful CSRF attack, an HTML Proof of Concept (`poc.html`) is provided.

### How the PoC Works

The `poc.html` page contains a hidden form that mimics a legitimate form from the target application (e.g., a "change password" or "add to cart" form).

1.  **Malicious Page**: An attacker hosts this HTML page on a different server and tricks a logged-in user into visiting it.
2.  **Automatic Submission**: The page uses JavaScript to automatically submit the hidden form to the target application's endpoint.
3.  **Unauthorized Action**: Since the user is logged in, their browser automatically includes their session cookie with the request. The vulnerable application processes the request as if the user had made it themselves, leading to an unauthorized action.

*(Optional: Insert a screenshot of the PoC page or the result of the successful attack here.)*

---

## 🖼️ Supporting Images

Below are images that support the explanations above.

**Image 1: Example of a form with a CSRF token.**
*(You will insert your image here)*

**Image 2: The crawler identifying a vulnerable form.**
*(You will insert your image here)*

**Image 3: The result of the successful PoC attack.**
*(You will insert your image here)*
