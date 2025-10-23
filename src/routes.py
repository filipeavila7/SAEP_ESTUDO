from src import db, app
from src.models import usuario_models, post_models, comentario_models, curtida_models
from flask import render_template, redirect, request, url_for, jsonify
from src import login_manager
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy.orm import joinedload
from sqlalchemy import func



# rota index, é a rota principal
@app.route("/")
def index():
    return render_template("index.html")


# função de carregar os usuários logados
@login_manager.user_loader
def load_user(user_id):
    return usuario_models.Usuario.query.get(int(user_id))


#função para caso o usuario tentar realizar uma ação sem que esteja logado 
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"success": False, "mensagem": "Você precisa estar logado."}), 401



# rota e função de login
@app.route("/login", methods=["GET", "POST"]) # metodo post para pegar os dados enviados pelo formulario
def login():
    # caso o método seja post
    if request.method == "POST":
        # pega os dados do campo do formulario, no caso email e senha
        email = request.form["email"]
        senha = request.form["senha"]

        # cria a variavel usuario_db que é filtrado pelo email no banco
        usuario_db = usuario_models.Usuario.query.filter_by(email=email).first()

        # caso o email e a senha do banco bata com a senha do front
        if usuario_db and usuario_db.senha == senha:
            #usuario é logado e mandado para a index
            login_user(usuario_db)
            return redirect(url_for("index", msg="sucesso"))
        else:
            # caso esteja incorreto, ele tambem é mandado para a index
            return redirect(url_for("index", msg="erro"))

    return redirect(url_for("index"))



#função de logout
@app.route("/logout")
@login_required  # garante que só usuários logados podem sair
def logout():
    logout_user()  # termina a sessão do usuário
    return redirect(url_for("index"))  # redireciona para a página inicial



# rota e função para comentar em um post, para comentar, tera que passar o id de um post especifico, e metodo post para o formulario
@app.route("/comentario/<int:post_id>", methods=["POST"])
@login_required # o usuario precisa estar logado
# precisa de um id de post como parametro
def add_comentario(post_id):

    # Pega o texto enviado pelo front
    texto = request.form.get("texto", "").strip()

    # caso o texto esteja vazio
    if not texto:
        return jsonify({"success": False, "mensagem": "O comentário não pode estar vazio."}), 400

    # Verifica se o post existe
    post = post_models.Post.query.get(post_id)
    if not post:
        return jsonify({"success": False, "mensagem": "Post não encontrado."}), 404

    # Cria o comentário
    comentario = comentario_models.Comentario(
        usuario_id=current_user.id, #usuario logado
        post_id=post.id, #id do post que esta sendo comentado
        texto=texto # texto do comentario
    )


    # salva no banco
    db.session.add(comentario)

    # capturas de erros
    try:
        db.session.commit()
        print("✅ Comentário salvo com sucesso!")
    except Exception as e:
        db.session.rollback()
        print("💥 ERRO ao salvar no banco:", e)
        return jsonify({"success": False, "mensagem": "Erro ao salvar comentário."}), 500

    # retorna um objeto json que o java script vai capturar
    return jsonify({
        "success": True, # sucesso
        "mensagem": "Comentário adicionado com sucesso!", # mensagem de sucesso
        "comentario": { # cria o objeto de comentario
            "id": comentario.id, #id do comentario
            "usuario_id": comentario.usuario_id, # id do usuario
            "post_id": comentario.post_id, # id do post
            "texto": comentario.texto # texto do comentario
        }
    })




# rota para curtir um post, tambem é necessário o id do post e sera usado como parametro na função
@app.route("/curtir/<int:post_id>", methods=["POST"])
@login_required  # o usuario precisa estar logado
def curtir_post(post_id):
    # faz uma busca do post pelo id dele recebido como parametro, ou seja o id do post do front
    post = post_models.Post.query.get(post_id)
    # caso não encontre no banco, informa um erro
    if not post:
        return jsonify({"success": False, "mensagem": "Post não encontrado."}), 404
    
    # verifica se o usuário atual já curtiu esse post antes:
    curtida = curtida_models.Curtida.query.filter_by(
        usuario_id=current_user.id, # busca pelo id do usuario que esta logado
        post_id=post.id # e o id do post
    ).first() # retorna o primeiro resultado encontrado, ou None se não existir.


    # caso ja esteja curtido
    if curtida:

        # inverte o valor boleano da curtida
        if curtida.curtida == True:
            curtida.curtida = False
        else:
          curtida.curtida = True
        
        db.session.commit() # salva no banco

        # retorna um json para cada situação da curtida
        if curtida.curtida:
            return jsonify({"success": True, "curtida": True, "mensagem": "Post curtido!"})
        else:
            return jsonify({"success": True, "curtida": False, "mensagem": "Curtida removida!"})
    

    # caso o usuario ainda não tenha curtido
    else:
        # cria a variavel nova curtida
        nova_curtida = curtida_models.Curtida(
            usuario_id=current_user.id, # o usuario é igual ao usuario logado
            post_id=post.id, # o id do post que ele curtiu
            curtida=True # deixa o valor da curtida 1 no banco
        )

        # adciona e salva no banco 
        db.session.add(nova_curtida)
        db.session.commit()
        return jsonify({"success": True, "curtida": True, "mensagem": "Post curtido!"})



        

# função para listar as curtidas feitas pelos usuários      
@app.route("/curtidas_usuario", methods=["GET"]) # método get pois se trata de uma listagem, e não esta enviando dados
@login_required # apenas os usuarios logados podem ver as suas curtidas
def listar_curtidas_usuario():



    # Busca todas as curtidas do usuário logado
    curtidas = (
        # faz uma pesquisa de 2 campos
        db.session.query(
            curtida_models.Curtida.post_id, # o id do post curtido
            curtida_models.Curtida.curtida # a curtida, True ou False
        )
        # filtra apenas as curtidas do usuario logado
        .filter_by(usuario_id=current_user.id)
        .all() # executa a consulta e retorna uma lista de resultados.
    )

    # Monta um dicionário no formato { post_id: True/False }
    resultado = {
        c.post_id: c.curtida for c in curtidas
    }
 
    # retorna o json  { post_id: True/False }
    return jsonify(resultado)




# função que faz o total de curtidas
@app.route("/total_curtidas", methods=["GET"]) # get para consulta
def total_curtidas():
    # Consulta o total de curtidas por post (curtida=True)
    resultados = (
        db.session.query(
            curtida_models.Curtida.post_id, #id do post
            func.count(curtida_models.Curtida.id).label("total") # função para contar as curtidas, cria um as chamado totat 
        )
        .filter_by(curtida=True)  # filtra apenas curtidas ativas
        .group_by(curtida_models.Curtida.post_id) # GROUP BY agrupa todas as linhas por post_id. 
        # ou seja, a contagem (COUNT) vai ser separada para cada post, e não para todos os posts juntos.
        .all() # Executa a query e retorna uma lista de tuplas com (post_id, total) para cada grupo.
    )

    '''
    SELECT post_id, COUNT(id) AS total
    FROM curtida
    WHERE curtida = True
    GROUP BY post_id;
    '''

    # Converte em dicionário {post_id: total}
    # post_id : total -> sendo a chave e o valor
    #for post_id e total, são percorridos na tupla resultados que o all() fez
    total_por_post = {post_id: total for post_id, total in resultados}


    # retorna em objeto json
    return jsonify(total_por_post)






# rota para listar os comentarios de um post especifico, usando o post_id 
@app.route("/comentarios/<int:post_id>", methods=["GET"])
def listar_comentarios(post_id):
    # Busca apenas os comentários do post específico
    comentarios = (
        comentario_models.Comentario.query #faz uma busca na tabela de comentario
        .options(joinedload(comentario_models.Comentario.usuario)) #carrega junto o usuário relacionado para não precisar de outra query depois
        .filter_by(post_id=post_id) # filtra pelo o id do post relacionado
        .all() # executa a query e retorna uma lista de objetos Comentario.
    )

    resultado = [] # cria uma lista de resultados
    # usa o c para percorrer os comentarios e jogar na lisra
    for c in comentarios:
        # adciona na lista de comentarios o dicionario:
        resultado.append({
            "id": c.id, #id do comentario
            "post_id": c.post_id, # id do post
            "usuario_id": c.usuario_id, # id do usuario
            "usuario_nome": getattr(c.usuario, "nome", "Usuário desconhecido"), # o nome do usuario, do campo nome, usa o getattr, para caso não tenha nome, ele fique como usuario desconhecido
            "texto": c.texto, # texto do comentario
            "eh_do_logado": ( # booleano que indica se o comentário pertence ao usuário logado (True se for dele, False caso contrário)
                current_user.is_authenticated and c.usuario_id == current_user.id
            )
        })

    # retorna tudo em objeto json para o front consumir
    return jsonify(resultado)