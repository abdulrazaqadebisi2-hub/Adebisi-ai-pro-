import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
You are Adebisi AI Pro.
Creator: Sulaiman Abdul Razaq Adebisi from Kwara State, Nigeria.
You were built by Sulaiman Abdul Razaq Adebisi.
If anyone asks who made you, who created you, your developer, owner, or origin, ALWAYS answer: Sulaiman Abdul Razaq Adebisi from Kwara State built me.
Never say Meta AI, Llama, Groq, or any other company. You are Adebisi AI Pro.
Speak like a smart Naija assistant. Helpful, fast, friendly.
"""

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adebisi AI Pro</title>
<style>
body{margin:0;font-family:system-ui;background:#0f172a;color:#fff;display:flex;flex-direction:column;height:100vh}
header{padding:15px;background:#1e293b;text-align:center;font-weight:bold;font-size:18px;border-bottom:1px solid #334155}
#chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:10px}
.msg{max-width:85%;padding:12px 15px;border-radius:15px;line-height:1.4}
.user{align-self:flex-end;background:#2563eb}
.ai{align-self:flex-start;background:#1e293b;border:1px solid #334155}
#inputArea{display:flex;padding:12px;background:#1e293b;gap:8px}
input{flex:1;padding:12px;border-radius:25px;border:none;background:#0f172a;color:#fff;outline:none}
button{padding:12px 20px;border-radius:25px;border:none;background:#2563eb;color:#fff;font-weight:bold}
.ad-box{text-align:center;padding:8px;background:#020617;font-size:12px;color:#94a3b8}
</style>
</head>
<body>
<header>ADEBISI AI PRO - Built by Sulaiman Abdul Razaq Adebisi</header>
<div class="ad-box">
  Ad space - Monetag / HilltopAds banner here
  <!-- PASTE YOUR MONETAG BANNER CODE BELOW THIS LINE -->
  
  <!-- PASTE ABOVE THIS LINE -->
</div>
<div id="chat"><div class="msg ai">Salama Alaikum! I am Adebisi AI Pro, built by Sulaiman Abdul Razaq Adebisi from Kwara. How can I help you today?</div></div>
<div id="inputArea">
<input id="q" placeholder="Ask anything...">
<button onclick="send()">Send</button>
</div>

<script>
async function send(){
 let input=document.getElementById('q');
 let text=input.value.trim();
 if(!text)return;
 let chat=document.getElementById('chat');
 chat.innerHTML+=`<div class="msg user">${text}</div>`;
 input.value='';
 chat.scrollTop=chat.scrollHeight;
 let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});
 let data=await res.json();
 chat.innerHTML+=`<div class="msg ai">${data.reply}</div>`;
 chat.scrollTop=chat.scrollHeight;
 // Trigger direct link ad on every 3rd message
 if(window.msgCount===undefined)window.msgCount=0;
 window.msgCount++;
 if(window.msgCount%3===0){
   window.open('YOUR_MONETAG_DIRECT_LINK','_blank');
 }
}
document.getElementById('q').addEventListener('keydown',e=>{if(e.key==='Enter')send()})
</script>

<!-- PASTE YOUR HILLTOPADS POPUNDER CODE HERE -->

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message','')
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":user_msg}
        ]
    )
    return jsonify({"reply": completion.choices[0].message.content})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
