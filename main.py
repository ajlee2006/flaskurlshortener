import requests, os
from github import Github
from urllib.parse import urlparse, ParseResult
from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<body>

<h1>Flask URL Shortener</h1>
<p>Warning: this is very lousy and extremely unsecure (all URLs are stored <a href="https://github.com/ajlee2006/flaskurlshortener">publicly</a>), use this at your own risk</p>
<input type='text' placeholder='Enter URL...' id='myText'>
<button onclick='myFunction()'>Go</button>
<script>
function myFunction() {
s = document.getElementById("myText").value;
s = s.split('');
for(var i=0; i<s.length;i++) s[i] = parseInt(s[i].charCodeAt(0));
  window.location.replace("shorten/"+s);
}
</script>

</body>
</html>
'''

@app.route('/shorten/<textf>')
def badtranslate(textf):
    s = ''.join([chr(int(i)) for i in textf.split(',')])
    print(s)

    p = urlparse(s, 'https')
    netloc = p.netloc or p.path
    path = p.path if p.netloc else ''
    if netloc.startswith('www.'):
        netloc = netloc[4:]

    p = ParseResult('https', netloc, path, *p[3:])
    s = p.geturl()

    l = eval(requests.get("https://raw.githubusercontent.com/ajlee2006/flaskurlshortener/main/list.txt").text)

    if s not in l:
        l.append(s)
        push("list.txt", "Add " + s, str(l), "main", update=True)

    i = l.index(s)
    
    return "<a href=" + s + ">" + s + "</a> has been shortened to <a href=/" + str(i) + ">https://flaskurlshortener.ajlee.repl.co/" + str(i) + "</a>. <a href='/'>Back to home</a>"

def push(path, message, content, branch, update=False):
    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_repo("ajlee2006/flaskurlshortener")
    if update:  # If file already exists, update it
        contents = repo.get_contents(path, ref=branch)
        repo.update_file(contents.path, message, content, contents.sha, branch=branch)
    else:  # If file doesn't exist, create it
        repo.create_file(path, message, content, branch=branch)

@app.route('/<int:n>')
def redirect(n):
    l = eval(requests.get("https://raw.githubusercontent.com/ajlee2006/flaskurlshortener/main/list.txt").text)
    return "Redirecting to <a href=" + l[n] + ">" + l[n] + "</a>...<meta http-equiv='Refresh' content='0; url=" + l[n] + "'>"

if __name__ == '__main__':
  app.run(host='0.0.0.0')
