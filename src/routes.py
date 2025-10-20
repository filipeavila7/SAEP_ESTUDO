from src import db, app
from src.models import usuario_models, post_models, comentario_models, curtida_models
from flask import render_template, redirect, request, url_for, jsonify
from src import login_manager
from flask_login import login_user, login_required, current_user




@app.route("/")
def index():
    return render_template("index.html")


# função de carregar usuário
@login_manager.user_loader
def load_user(user_id):
    return usuario_models.Usuario.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario_db = usuario_models.Usuario.query.filter_by(email=email).first()

        if usuario_db and usuario_db.senha == senha:
            login_user(usuario_db)
            print("login realizado com sucesso")
            return redirect(url_for("index"))
        
        else:
            print("usuario ou senha inválidos")




@app.route("/comentario/<int:post_id>", methods=["POST"])
@login_required
def add_comentario(post_id):
    # Pega o texto enviado pelo front
    texto = request.form.get("texto", "").strip()
    if not texto:
        return jsonify({"success": False, "mensagem": "O comentário não pode estar vazio."}), 400

    # Verifica se o post existe
    post = post_models.Post.query.get(post_id)
    if not post:
        return jsonify({"success": False, "mensagem": "Post não encontrado."}), 404

    # Cria o comentário
    comentario = comentario_models.Comentario(
        usuario_id=current_user.id,
        post_id=post.id,
        texto=texto
    )

    db.session.add(comentario)
    db.session.commit()

    return jsonify({
        "success": True,
        "mensagem": "Comentário adicionado com sucesso!",
        "comentario": {
            "id": comentario.id,
            "usuario_id": comentario.usuario_id,
            "post_id": comentario.post_id,
            "texto": comentario.texto
        }
    })



@app.route("/curtir/<int:post_id>", methods=["POST"])
@login_required
def curtir_post(post_id):
    # Verifica se o post existe
    post = post_models.Post.query.get(post_id)
    if not post:
        return jsonify({"success": False, "mensagem": "Post não encontrado."}), 404

    # Verifica se o usuário já curtiu o post
    curtida = curtida_models.Curtida.query.filter_by(
        usuario_id=current_user.id,
        post_id=post.id
    ).first()

    if curtida:
        # Usuário já curtiu → remove a curtida (descurtir)
        db.session.delete(curtida)
        db.session.commit()
        return jsonify({"success": True, "curtida": False, "mensagem": "Curtida removida!"})
    else:
        # Usuário não curtiu → cria a curtida
        nova_curtida = curtida_models.Curtida(
            usuario_id=current_user.id,
            post_id=post.id,
            curtida=True  # opcional, só para marcar que é curtido
        )
        db.session.add(nova_curtida)
        db.session.commit()
        return jsonify({"success": True, "curtida": True, "mensagem": "Post curtido!"})



        

        






        
    


