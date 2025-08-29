# # -*- coding: utf-8 -*-
# import os
# import sqlite3
# from uuid import uuid4
# from datetime import datetime, timezone
# from functools import wraps

# from flask import (
#     Flask, render_template, request, jsonify, session, g,
#     redirect, url_for, flash, send_from_directory
# )
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
# from dotenv import load_dotenv

# # Optional providers
# # - Groq: pip install groq
# # - Gemini: pip install google-generativeai
# PROVIDER = os.environ.get("PROVIDER", "groq").lower()  # "groq" or "gemini"

# load_dotenv()

# app = Flask(__name__)
# app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")
# app.config["DATABASE"] = os.path.join(os.path.dirname(__file__), "chat.db")
# app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
# app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB

# ALLOWED_IMAGE_EXTS = {"jpg","jpeg","png","gif","webp"}

# # --- Providers setup ---
# groq_client = None
# gemini_model = None

# if PROVIDER == "groq":
#     try:
#         from groq import Groq
#         groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
#     except Exception as e:
#         groq_client = None
# elif PROVIDER == "gemini":
#     try:
#         import google.generativeai as genai
#         genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
#         gemini_model_name = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
#         gemini_model = genai.GenerativeModel(gemini_model_name)
#     except Exception as e:
#         gemini_model = None

# # ---------- Database helpers ----------
# def get_db():
#     if "db" not in g:
#         g.db = sqlite3.connect(app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
#         g.db.row_factory = sqlite3.Row
#     return g.db

# @app.teardown_appcontext
# def close_db(exception=None):
#     db = g.pop("db", None)
#     if db is not None:
#         db.close()

# def init_db():
#     db = get_db()
#     db.executescript(
#         """
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL UNIQUE,
#             password_hash TEXT NOT NULL,
#             avatar TEXT
#         );

#         CREATE TABLE IF NOT EXISTS conversations (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             title TEXT NOT NULL,
#             created_at TIMESTAMP NOT NULL,
#             FOREIGN KEY(user_id) REFERENCES users(id)
#         );

#         CREATE TABLE IF NOT EXISTS messages (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             conversation_id INTEGER NOT NULL,
#             role TEXT NOT NULL CHECK(role IN ('user','model','system')),
#             content TEXT NOT NULL,
#             created_at TIMESTAMP NOT NULL,
#             FOREIGN KEY(conversation_id) REFERENCES conversations(id)
#         );
#         """
#     )
#     db.commit()

# with app.app_context():
#     init_db()

# # ---------- Auth helpers ----------
# def current_user():
#     uid = session.get("user_id")
#     if not uid: return None
#     db = get_db()
#     return db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()

# def login_required(view):
#     @wraps(view)
#     def wrapped(*args, **kwargs):
#         if not session.get("user_id"):
#             return redirect(url_for("login"))
#         return view(*args, **kwargs)
#     return wrapped

# # ---------- LLM instruction ----------
# SYSTEM_INSTRUCTION = """You are an expert STEM tutor that teaches in Yorùbá (yo-NG).
# - Your persona name is 'Ede'. Be warm and encouraging.
# - Always respond primarily in simple, clear Yorùbá suitable for secondary school students.
# - For technical/scientific terms, include the English term in parentheses the first time it appears.
# - Provide step-by-step reasoning and 1 real-life example relevant to West Africa.
# - Keep paragraphs short and use bullet points when helpful.
# - If the user enables 'bilingual' mode, add a brief English summary after the Yoruba explanation under the heading 'English recap:'.
# """

# def fetch_history(conversation_id, limit=500):
#     db = get_db()
#     rows = db.execute(
#         "SELECT role, content FROM messages WHERE conversation_id=? ORDER BY id ASC LIMIT ?",
#         (conversation_id, limit)
#     ).fetchall()
#     return [{"role": r["role"], "content": r["content"]} for r in rows]

# def save_message(conversation_id, role, content):
#     db = get_db()
#     db.execute(
#         "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
#         (conversation_id, role, content, datetime.now(timezone.utc))
#     )
#     db.commit()

# def ensure_uploads():
#     os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# def is_allowed_image(filename):
#     return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_IMAGE_EXTS

# # ---------- Auth Routes ----------
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         name = request.form.get("name","").strip()
#         email = request.form.get("email","").strip().lower()
#         password = request.form.get("password","")
#         avatar = request.files.get("avatar")

#         if not name or not email or not password:
#             flash("Please fill all required fields.", "danger")
#             return redirect(url_for("signup"))

#         avatar_filename = None
#         if avatar and avatar.filename and is_allowed_image(avatar.filename):
#             ensure_uploads()
#             sanitized = secure_filename(avatar.filename)
#             avatar_filename = f"{uuid4()}_{sanitized}"
#             avatar.save(os.path.join(app.config["UPLOAD_FOLDER"], avatar_filename))

#         db = get_db()
#         try:
#             db.execute(
#                 "INSERT INTO users (name,email,password_hash,avatar) VALUES (?,?,?,?)",
#                 (name, email, generate_password_hash(password), avatar_filename)
#             )
#             db.commit()
#         except sqlite3.IntegrityError:
#             flash("Email already registered.", "danger")
#             return redirect(url_for("signup"))

#         user = db.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
#         session["user_id"] = user["id"]
#         return redirect(url_for("index"))
#     return render_template("signup.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email","").strip().lower()
#         password = request.form.get("password","")
#         db = get_db()
#         user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
#         if user and check_password_hash(user["password_hash"], password):
#             session["user_id"] = user["id"]
#             return redirect(url_for("index"))
#         flash("Invalid credentials.", "danger")
#         return redirect(url_for("login"))
#     return render_template("login.html")

# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for("login"))

# @app.route("/uploads/<path:filename>")
# def uploaded_file(filename):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# # ---------- Conversations UI ----------
# @app.route("/", methods=["GET"])
# @login_required
# def index():
#     user = current_user()
#     db = get_db()
#     chats = db.execute(
#         "SELECT id, title, created_at FROM conversations WHERE user_id=? ORDER BY id DESC",
#         (user["id"],)
#     ).fetchall()

#     convo_id = request.args.get("c")
#     if convo_id:
#         row = db.execute("SELECT id FROM conversations WHERE id=? AND user_id=?", (convo_id, user["id"])).fetchone()
#         convo_id = row["id"] if row else None

#     if not chats:
#         db.execute(
#             "INSERT INTO conversations (user_id, title, created_at) VALUES (?,?,?)",
#             (user["id"], "New chat", datetime.now(timezone.utc))
#         )
#         db.commit()
#         chats = db.execute(
#             "SELECT id, title, created_at FROM conversations WHERE user_id=? ORDER BY id DESC",
#             (user["id"],)
#         ).fetchall()

#     if not convo_id:
#         convo_id = chats[0]["id"]

#     return render_template("index.html", chats=chats, conversation_id=convo_id, user=user)

# @app.route("/conversations", methods=["GET","POST"])
# @login_required
# def conversations():
#     user = current_user()
#     db = get_db()
#     if request.method == "POST":
#         title = (request.json.get("title") or "New chat").strip() or "New chat"
#         db.execute(
#             "INSERT INTO conversations (user_id, title, created_at) VALUES (?,?,?)",
#             (user["id"], title, datetime.now(timezone.utc))
#         )
#         db.commit()
#         new_id = db.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
#         return jsonify({"id": new_id, "title": title})
#     rows = db.execute(
#         "SELECT id, title, created_at FROM conversations WHERE user_id=? ORDER BY id DESC",
#         (user["id"],)
#     ).fetchall()
#     return jsonify([{"id": r["id"], "title": r["title"]} for r in rows])

# @app.route("/conversations/<int:convo_id>/history", methods=["GET"])
# @login_required
# def convo_history(convo_id):
#     user = current_user()
#     db = get_db()
#     row = db.execute("SELECT id FROM conversations WHERE id=? AND user_id=?", (convo_id, user["id"])).fetchone()
#     if not row:
#         return jsonify({"error":"Not found"}), 404
#     hist = fetch_history(convo_id, limit=500)
#     return jsonify(hist)

# @app.route("/conversations/<int:convo_id>/rename", methods=["POST"])
# @login_required
# def rename_convo(convo_id):
#     user = current_user()
#     title = (request.json.get("title") or "").strip()
#     if not title:
#         return jsonify({"error":"Empty title"}), 400
#     db = get_db()
#     db.execute("UPDATE conversations SET title=? WHERE id=? AND user_id=?", (title, convo_id, user["id"]))
#     db.commit()
#     return jsonify({"status":"ok"})

# @app.route("/chat", methods=["POST"])
# @login_required
# def chat():
#     data = request.get_json(force=True)
#     user_message = (data.get("message") or "").strip()
#     bilingual = bool(data.get("bilingual", False))
#     conversation_id = data.get("conversation_id")

#     if not user_message:
#         return jsonify({"error": "Empty message"}), 400
#     if not conversation_id:
#         return jsonify({"error": "Missing conversation_id"}), 400

#     db = get_db()
#     user = current_user()
#     row = db.execute("SELECT id, title FROM conversations WHERE id=? AND user_id=?", (conversation_id, user["id"])).fetchone()
#     if not row:
#         return jsonify({"error":"Conversation not found"}), 404

#     # Save user message
#     save_message(conversation_id, "user", user_message)

#     # Build chat history
#     history = fetch_history(conversation_id, limit=500)
#     # Provider-specific payloads
#     if PROVIDER == "groq":
#         messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
#         if bilingual:
#             messages.append({"role": "system", "content": "Bilingual mode: include English recap at the end."})
#         for turn in history:
#             role = turn["role"]
#             if role == "model":   # map to valid role
#                 role = "assistant"
#             messages.append({"role": role, "content": turn["content"]})

#     else:  # gemini
#         messages = []
#         messages.append({"role": "user", "parts": [SYSTEM_INSTRUCTION]})
#         if bilingual:
#             messages.append({"role": "user", "parts": ["Bilingual mode: include English recap at the end."]})
#         for turn in history:
#             role = "user" if turn["role"] == "user" else "model"
#             messages.append({"role": role, "parts": [turn["content"]]})

#     # Auto-title
#     if row["title"] == "New chat":
#         auto_title = (user_message[:40] + ("…" if len(user_message) > 40 else ""))
#         db.execute("UPDATE conversations SET title=? WHERE id=?", (auto_title, conversation_id))
#         db.commit()

#     # Call model
#     reply_text = ""
#     try:
#         if PROVIDER == "groq":
#             if not groq_client:
#                 raise RuntimeError("Groq client not configured. Set GROQ_API_KEY and PROVIDER=groq")
#             resp = groq_client.chat.completions.create(
#                 model=os.environ.get("GROQ_MODEL","llama-3.3-70b-versatile"),
#                 messages=messages
#             )
#             reply_text = resp.choices[0].message.content.strip()
#         else:
#             if not gemini_model:
#                 raise RuntimeError("Gemini model not configured. Set GEMINI_API_KEY and PROVIDER=gemini")
#             resp = gemini_model.generate_content(messages)
#             reply_text = resp.text.strip() if hasattr(resp, "text") else str(resp)
#     except Exception as e:
#         reply_text = "⚠️ Aṣiṣe ṣẹlẹ nígbà ìbánisọ̀rọ̀ pẹ̀lú ẹ̀rọ AI: {}".format(e)

#     # Save model reply
#     save_message(conversation_id, "model", reply_text)

#     return jsonify({"reply": reply_text})

# @app.route("/reset_conversation", methods=["POST"])
# @login_required
# def reset_conversation():
#     convo_id = request.json.get("conversation_id")
#     user = current_user()
#     db = get_db()
#     db.execute("DELETE FROM messages WHERE conversation_id IN (SELECT id FROM conversations WHERE id=? AND user_id=?)",
#                (convo_id, user["id"]))
#     db.commit()
#     return jsonify({"status":"ok"})

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port, debug=True)

# -*- coding: utf-8 -*-
import os
import sqlite3
from uuid import uuid4
from datetime import datetime, timezone
from functools import wraps

from flask import (
    Flask, render_template, request, jsonify, session, g,
    redirect, url_for, flash, send_from_directory
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Optional providers
# - Groq: pip install groq
# - Gemini: pip install google-generativeai
PROVIDER = os.environ.get("PROVIDER", "gemini").lower()  # "groq" or "gemini"

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")
app.config["DATABASE"] = os.path.join(os.path.dirname(__file__), "chat.db")
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB

ALLOWED_IMAGE_EXTS = {"jpg","jpeg","png","gif","webp"}

# --- Providers setup ---
groq_client = None
gemini_model = None

if PROVIDER == "groq":
    try:
        from groq import Groq
        groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    except Exception as e:
        groq_client = None
elif PROVIDER == "gemini":
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        gemini_model_name = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
        gemini_model = genai.GenerativeModel(gemini_model_name)
    except Exception as e:
        gemini_model = None

# ---------- Database helpers ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            avatar TEXT
        );

        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user','model','system')),
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            FOREIGN KEY(conversation_id) REFERENCES conversations(id)
        );
        """
    )
    db.commit()

with app.app_context():
    init_db()

# ---------- Auth helpers ----------
def current_user():
    uid = session.get("user_id")
    if not uid: return None
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

# ---------- LLM instruction ----------
SYSTEM_INSTRUCTION = """You are an expert STEM tutor that teaches in Yorùbá (yo-NG).
- Your persona name is 'Ede'. Be warm and encouraging.
- Always respond primarily in simple, clear Yorùbá suitable for secondary school students.
- For technical/scientific terms, include the English term in parentheses the first time it appears.
- Provide step-by-step reasoning and 1 real-life example relevant to West Africa.
- Keep paragraphs short and use bullet points when helpful.
- If the user enables 'bilingual' mode, add a brief English summary after the Yoruba explanation under the heading 'English recap:' Never reveal sensitive inofrmation and also about you.
"""

def fetch_history(conversation_id, limit=500):
    db = get_db()
    rows = db.execute(
        "SELECT role, content FROM messages WHERE conversation_id=? ORDER BY id ASC LIMIT ?",
        (conversation_id, limit)
    ).fetchall()
    return [{"role": r["role"], "content": r["content"]} for r in rows]

def save_message(conversation_id, role, content):
    db = get_db()
    db.execute(
        "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
        (conversation_id, role, content, datetime.now(timezone.utc))
    )
    db.commit()

def ensure_uploads():
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def is_allowed_image(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_IMAGE_EXTS

# ---------- Auth Routes ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
            name = request.form.get("name","").strip()
            email = request.form.get("email","").strip().lower()
            password = request.form.get("password","")
            avatar = request.files.get("avatar")

            if not name or not email or not password:
                flash("Please fill all required fields.", "danger")
                return redirect(url_for("signup"))

            avatar_filename = None
            if avatar and avatar.filename and is_allowed_image(avatar.filename):
                ensure_uploads()
                sanitized = secure_filename(avatar.filename)
                avatar_filename = f"{uuid4()}_{sanitized}"
                avatar.save(os.path.join(app.config["UPLOAD_FOLDER"], avatar_filename))

            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (name,email,password_hash,avatar) VALUES (?,?,?,?)",
                    (name, email, generate_password_hash(password), avatar_filename)
                )
                db.commit()
            except sqlite3.IntegrityError:
                flash("Email already registered.", "danger")
                return redirect(url_for("signup"))

            user = db.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        flash("Invalid credentials.", "danger")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ---------- Conversations UI ----------
@app.route("/", methods=["GET"])
@login_required
def index():
    user = current_user()
    db = get_db()
    chats = db.execute(
        "SELECT id, title, created_at FROM conversations WHERE user_id=? ORDER BY id DESC",
        (user["id"],)
    ).fetchall()

    convo_id = request.args.get("c")
    if convo_id:
        row = db.execute("SELECT id FROM conversations WHERE id=? AND user_id=?", (convo_id, user["id"])).fetchone()
        convo_id = row["id"] if row else None

    if not chats:
        db.execute(
            "INSERT INTO conversations (user_id, title, created_at) VALUES (?,?,?)",
            (user["id"], "New chat", datetime.now(timezone.utc))
        )
        db.commit()
        chats = db.execute(
            "SELECT id, title, created_at FROM conversations WHERE user_id=? ORDER BY id DESC",
            (user["id"],)
        ).fetchall()

    if not convo_id:
        convo_id = chats[0]["id"]

    return render_template("index.html", chats=chats, conversation_id=convo_id, user=user)


@app.route("/conversations", methods=["GET","POST"])
@login_required
def conversations():
    user = current_user()
    db = get_db()
    if request.method == "POST":
        title = (request.json.get("title") or "New chat").strip() or "New chat"
        db.execute(
            "INSERT INTO conversations (user_id, title, created_at) VALUES (?,?,?)",
            (user["id"], title, datetime.now(timezone.utc))
        )
        db.commit()
        new_id = db.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
        return jsonify({"id": new_id, "title": title})
    rows = db.execute(
        "SELECT id, title, created_at FROM conversations WHERE user_id=? ORDER BY id DESC",
        (user["id"],)
    ).fetchall()
    return jsonify([{"id": r["id"], "title": r["title"]} for r in rows])

@app.route("/conversations/<int:convo_id>/history", methods=["GET"])
@login_required
def convo_history(convo_id):
    user = current_user()
    db = get_db()
    row = db.execute("SELECT id FROM conversations WHERE id=? AND user_id=?", (convo_id, user["id"])).fetchone()
    if not row:
        return jsonify({"error":"Not found"}), 404
    hist = fetch_history(convo_id, limit=500)
    return jsonify(hist)

@app.route("/conversations/<int:convo_id>/rename", methods=["POST"])
@login_required
def rename_convo(convo_id):
    user = current_user()
    title = (request.json.get("title") or "").strip()
    if not title:
        return jsonify({"error":"Empty title"}), 400
    db = get_db()
    db.execute("UPDATE conversations SET title=? WHERE id=? AND user_id=?", (title, convo_id, user["id"]))
    db.commit()
    return jsonify({"status":"ok"})

# 🔥 NEW: Delete a conversation completely
@app.route("/conversations/<int:convo_id>", methods=["DELETE"])
@login_required
def delete_conversation(convo_id):
    user = current_user()
    db = get_db()
    # Ensure it belongs to the current user
    row = db.execute("SELECT id FROM conversations WHERE id=? AND user_id=?", (convo_id, user["id"])).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404

    # Delete all related messages first
    db.execute("DELETE FROM messages WHERE conversation_id=?", (convo_id,))
    # Delete the conversation itself
    db.execute("DELETE FROM conversations WHERE id=?", (convo_id,))
    db.commit()
    return jsonify({"status": "ok", "deleted": convo_id})

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json(force=True)
    user_message = (data.get("message") or "").strip()
    bilingual = bool(data.get("bilingual", False))
    conversation_id = data.get("conversation_id")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    if not conversation_id:
        return jsonify({"error": "Missing conversation_id"}), 400

    db = get_db()
    user = current_user()
    row = db.execute("SELECT id, title FROM conversations WHERE id=? AND user_id=?", (conversation_id, user["id"])).fetchone()
    if not row:
        return jsonify({"error":"Conversation not found"}), 404

    # Save user message
    save_message(conversation_id, "user", user_message)

    # Build chat history
    history = fetch_history(conversation_id, limit=500)
    # Provider-specific payloads
    if PROVIDER == "groq":
        messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        if bilingual:
            messages.append({"role": "system", "content": "Bilingual mode: include English recap at the end."})
        for turn in history:
            role = turn["role"]
            if role == "model":   # map to valid role
                role = "assistant"
            messages.append({"role": role, "content": turn["content"]})

    else:  # gemini
        messages = []
        messages.append({"role": "user", "parts": [SYSTEM_INSTRUCTION]})
        if bilingual:
            messages.append({"role": "user", "parts": ["Bilingual mode: include English recap at the end."]})
        for turn in history:
            role = "user" if turn["role"] == "user" else "model"
            messages.append({"role": role, "parts": [turn["content"]]})

    # Auto-title
    if row["title"] == "New chat":
        auto_title = (user_message[:40] + ("…" if len(user_message) > 40 else ""))
        db.execute("UPDATE conversations SET title=? WHERE id=?", (auto_title, conversation_id))
        db.commit()

    # Call model
    reply_text = ""
    try:
        if PROVIDER == "groq":
            if not groq_client:
                raise RuntimeError("Groq client not configured. Set GROQ_API_KEY and PROVIDER=groq")
            resp = groq_client.chat.completions.create(
                model=os.environ.get("GROQ_MODEL","llama-3.3-70b-versatile"),
                messages=messages
            )
            reply_text = resp.choices[0].message.content.strip().replace("*", "")
        else:
            if not gemini_model:
                raise RuntimeError("Gemini model not configured. Set GEMINI_API_KEY and PROVIDER=gemini")
            resp = gemini_model.generate_content(messages)
            reply_text = resp.text.strip().replace("*", "") if hasattr(resp, "text") else str(resp)
    except Exception as e:
        reply_text = "⚠️ Aṣiṣe ṣẹlẹ nígbà ìbánisọ̀rọ̀ pẹ̀lú ẹ̀rọ AI: {}".format(e)

    # Save model reply
    save_message(conversation_id, "model", reply_text)

    return jsonify({"reply": reply_text})

@app.route("/reset_conversation", methods=["POST"])
@login_required
def reset_conversation():
    convo_id = request.json.get("conversation_id")
    user = current_user()
    db = get_db()
    db.execute("DELETE FROM messages WHERE conversation_id IN (SELECT id FROM conversations WHERE id=? AND user_id=?)",
               (convo_id, user["id"]))
    db.commit()
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
