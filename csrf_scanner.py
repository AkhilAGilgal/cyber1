import re
import requests

def scan_for_csrf(html_content):
 
    results = []
   
    form_regex = re.compile(r'<form(.*?)>(.*?)</form>', re.IGNORECASE | re.DOTALL)
   
    method_regex = re.compile(r'method\s*=\s*["\']post["\']', re.IGNORECASE)
    
   
    csrf_token_regex = re.compile(r'<input[^>]+type\s*=\s*["\']hidden["\'][^>]+name\s*=\s*["\'](\w*csrf\w*|\w*token\w*|authenticity_token)["\']', re.IGNORECASE)

    forms = form_regex.findall(html_content)
    
    if not forms:
        results.append("No forms found on the page.")
        return results

    form_count = 0
    for form_attributes, form_content in forms:
        form_count += 1
        full_form_html = f"<form{form_attributes}>{form_content}</form>"

      
        is_post_form = method_regex.search(form_attributes)
        
        if is_post_form:
            has_csrf_token = csrf_token_regex.search(form_content)
            
            if has_csrf_token:
                results.append(f"Form {form_count}: [SECURE] Found POST form with a potential CSRF token.")
            else:
                results.append(f"Form {form_count}: [VULNERABLE] Found POST form that appears to be missing a CSRF token.")
        else:
           
            results.append(f"Form {form_count}: [INFO] Found non-POST form. CSRF protection not typically required.")
            
    return results


if __name__ == "__main__":
 
    sample_html = """
    <!DOCTYPE html>
    <html>
    <body>

    <h2>Vulnerable Form (No CSRF Token)</h2>
    <p>This form changes user data using POST but has no CSRF token.</p>
    <form action="/change-email" method="post">
      Email: <input type="text" name="email"><br>
      <input type="submit" value="Submit">
    </form>

    <hr>

    <h2>Secure Form (Has CSRF Token)</h2>
    <p>This form is protected with a hidden CSRF token field.</p>
    <form action="/post-comment" method="post">
      Comment: <input type="text" name="comment"><br>
      <input type="hidden" name="csrf_token" value="xyz123abc987">
      <input type="submit" value="Submit">
    </form>
    
    <hr>
    
    <h2>GET Form (CSRF Not Applicable)</h2>
    <form action="/search" method="get">
      Search: <input type="text" name="q"><br>
      <input type="submit" value="Search">
    </form>

    </body>
    </html>
    """
    
    findings = scan_for_csrf(sample_html)
    for finding in findings:
        print(finding)
