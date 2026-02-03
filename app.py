from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>BLACKHEX</title>
<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>

<style>
body{
  margin:0;
  background:black;
  color:red;
  font-family:monospace;
  overflow:hidden;
  cursor:crosshair;
}
#particles-js{
  position:fixed;
  width:100%;
  height:100%;
  z-index:-1;
}
.container{
  text-align:center;
  margin-top:8%;
}
h1{
  font-size:60px;
  text-shadow:0 0 25px red;
}
button,input{
  padding:12px 25px;
  background:black;
  border:2px solid red;
  color:red;
  margin:6px;
  font-size:16px;
}
button:hover{
  background:red;
  color:black;
}
.section{display:none;}
pre{
  text-align:left;
  display:inline-block;
  margin-top:15px;
  white-space:pre-wrap;
  word-break:break-all;
}
.footer{
  position:fixed;
  bottom:10px;
  width:100%;
  text-align:center;
  font-size:12px;
  opacity:0.7;
}
#copyBtn{
  display:none;
  margin-top:10px;
}
</style>
</head>

<body>
<div id="particles-js"></div>
<audio id="glitch" src="https://assets.mixkit.co/sfx/preview/mixkit-glitchy-click-1114.mp3"></audio>

<div class="container">
<h1>BLACKHEX</h1>

<div id="home">
  <button onclick="show('tool')">Link Tool</button>
</div>

<div id="tool" class="section">
  <div>
    <button onclick="modo='perfil'">PERFIL</button>
    <button onclick="modo='server'">SERVER</button>
    <button onclick="modo='grupo'">GRUPO</button>
  </div>
  <br>
  <input id="url" placeholder="Pega el link aquí" style="width:80%;">
  <br>
  <button onclick="procesar()">CAMUFLAR + ACORTAR</button>
  <pre id="log"></pre>
  <pre id="resultado"></pre>
  <button id="copyBtn" onclick="copiar()">COPIAR LINK</button>
  <br>
  <button onclick="back()">Volver</button>
</div>
</div>

<div class="footer">
BLACKHEX — Link Manipulation Tool<br>
No logs. No warnings. No mercy.
</div>

<script>
let modo="";

function show(id){
  document.getElementById("home").style.display="none";
  document.getElementById(id).style.display="block";
}
function back(){
  document.getElementById("home").style.display="block";
  document.getElementById("tool").style.display="none";
}

// detección automática
function detectar(url){
  if(url.includes("/users/")) return "perfil";
  if(url.includes("/communities/")) return "grupo";
  if(url.includes("/games/")) return "server";
  return "";
}

function logtxt(t){
  document.getElementById("log").innerText += "> " + t + "\\n";
}

async function procesar(){
  let u = document.getElementById("url").value;
  document.getElementById("log").innerText="";
  document.getElementById("resultado").innerText="";
  document.getElementById("copyBtn").style.display="none";
  document.getElementById("glitch").play();

  logtxt("analizando enlace...");
  let tipo = modo || detectar(u);
  if(!tipo){
    logtxt("no se pudo detectar tipo");
    return;
  }

  logtxt("inyectando camuflaje...");
  const r = await fetch("/acortar",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({url:u})
  }).then(r=>r.json());

  let base="";
  if(tipo=="perfil")
    base="[https:__//__www.roblox.com/users/252441668279/profile]";
  if(tipo=="server")
    base="[https:__//__www.roblox.com/games/2753915549/profile]";
  if(tipo=="grupo")
    base="[https:__//__www.roblox.com/communities/2753915549/profile]";

  logtxt("LINK INYECTADO ✔");
  document.getElementById("resultado").innerText = base + "(" + r.short + ")";
  document.getElementById("copyBtn").style.display = "inline-block";
}

function copiar(){
  const text = document.getElementById("resultado").innerText;
  if(!text) return;

  navigator.clipboard.writeText(text).then(()=>{
    alert("Link copiado 📋");
  }).catch(()=>{
    const temp = document.createElement("textarea");
    temp.value = text;
    document.body.appendChild(temp);
    temp.select();
    document.execCommand("copy");
    document.body.removeChild(temp);
    alert("Link copiado 📋");
  });
}

particlesJS("particles-js",{
  particles:{
    number:{value:260},
    size:{value:1},
    color:{value:"#ff0000"},
    line_linked:{enable:true,color:"#ff0000",opacity:0.4},
    move:{speed:1}
  }
});
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/acortar", methods=["POST"])
def acortar():
    url = request.json.get("url")
    r = requests.get(
        "https://is.gd/create.php",
        params={"format":"simple","url":url},
        timeout=10
    )
    return jsonify({"short": r.text})

if __name__ == "__main__":
    app.run()
