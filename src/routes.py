from src import db, app
from src.models import usuario_models, post_models, comentario_models, curtida_models
from flask import render_template, redirect, request, url_for, jsonify
from src import login_manager
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy.orm import joinedload
from sqlalchemy import func




@app.route("/")
def index():
    posts = post_models.Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/teste")
def teste():
    return render_template("teste.html")


# função de carregar usuário
@login_manager.user_loader
def load_user(user_id):
    return usuario_models.Usuario.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"success": False, "mensagem": "Você precisa estar logado."}), 401


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario_db = usuario_models.Usuario.query.filter_by(email=email).first()

        if usuario_db and usuario_db.senha == senha:
            login_user(usuario_db)
            return redirect(url_for("index", msg="sucesso"))
        else:
            return redirect(url_for("index", msg="erro"))

    return redirect(url_for("index"))


@app.route("/logout")
@login_required  # garante que só usuários logados podem sair
def logout():
    logout_user()  # termina a sessão do usuário
    return redirect(url_for("index"))  # redireciona para a página inicial





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
    post = post_models.Post.query.get(post_id)
    if not post:
        return jsonify({"success": False, "mensagem": "Post não encontrado."}), 404

    curtida = curtida_models.Curtida.query.filter_by(
        usuario_id=current_user.id,
        post_id=post.id
    ).first()

    if curtida:
        # Ao invés de deletar, apenas inverte o boolean
        curtida.curtida = not curtida.curtida
        db.session.commit()
        if curtida.curtida:
            return jsonify({"success": True, "curtida": True, "mensagem": "Post curtido!"})
        else:
            return jsonify({"success": True, "curtida": False, "mensagem": "Curtida removida!"})
    else:
        nova_curtida = curtida_models.Curtida(
            usuario_id=current_user.id,
            post_id=post.id,
            curtida=True
        )
        db.session.add(nova_curtida)
        db.session.commit()
        return jsonify({"success": True, "curtida": True, "mensagem": "Post curtido!"})



        

        
@app.route("/curtidas_usuario", methods=["GET"])
@login_required
def listar_curtidas_usuario():
    # Busca todas as curtidas do usuário logado
    curtidas = (
        db.session.query(
            curtida_models.Curtida.post_id,
            curtida_models.Curtida.curtida
        )
        .filter_by(usuario_id=current_user.id)
        .all()
    )

    # Monta um dicionário no formato { post_id: True/False }
    resultado = {
        c.post_id: c.curtida for c in curtidas
    }

    return jsonify(resultado)






@app.route("/total_curtidas", methods=["GET"])
def total_curtidas():
    # Consulta o total de curtidas por post (curtida=True)
    resultados = (
        db.session.query(
            curtida_models.Curtida.post_id,
            func.count(curtida_models.Curtida.id).label("total")
        )
        .filter_by(curtida=True)  # apenas curtidas ativas
        .group_by(curtida_models.Curtida.post_id)
        .all()
    )

    # Converte em dicionário {post_id: total}
    total_por_post = {post_id: total for post_id, total in resultados}

    return jsonify(total_por_post)





@app.route("/comentarios", methods=["GET"])
def listar_comentarios():
    # Busca todos os comentários, já trazendo o usuário relacionado
    comentarios = (
        comentario_models.Comentario.query
        .options(joinedload(comentario_models.Comentario.usuario))
        .all()
    )

    resultado = []
    for c in comentarios:
        resultado.append({
            "id": c.id,
            "post_id": c.post_id,
            "usuario_id": c.usuario_id,
            "usuario_nome": getattr(c.usuario, "nome", "Usuário desconhecido"),
            "texto": c.texto,
            "eh_do_logado": (current_user.is_authenticated and c.usuario_id == current_user.id)
        })

    return jsonify(resultado)






        
    


