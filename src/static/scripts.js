
//abrir modal de login
const modal = document.getElementById("modalLogin");
const btn = document.getElementById("abrirModal");
const fechar = document.querySelector(".fechar");

btn.onclick = () => {
  modal.style.display = "block";
}

fechar.onclick = () => {
  modal.style.display = "none";
}

window.onclick = (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
}

//exibir msg de login


// Pega a query string (?msg=sucesso ou ?msg=erro)
const params = new URLSearchParams(window.location.search);
const msg = params.get("msg");

if (msg) {
  const div = document.createElement("div");
  div.className = "alerta";

  if (msg === "sucesso") {
    div.textContent = "✅ Login realizado com sucesso!";
    div.style.backgroundColor = "#4CAF50";
  } else if (msg === "erro") {
    div.textContent = "❌ Usuário ou senha inválidos!";
    div.style.backgroundColor = "#e74c3c";
    // opcional: reabrir o modal automaticamente
    document.getElementById("modalLogin").style.display = "block";
  }

  div.style.position = "fixed";
  div.style.top = "80px";
  div.style.right = "20px";
  div.style.padding = "12px 18px";
  div.style.borderRadius = "8px";
  div.style.color = "#fff";
  div.style.fontWeight = "bold";
  div.style.boxShadow = "0 2px 6px rgba(0,0,0,0.3)";
  div.style.zIndex = "999";

  document.body.appendChild(div);

  // Esconde depois de 3 segundos
  setTimeout(() => div.remove(), 3000);
}



// Função para curtir/descurtir
async function curtirPost(postId, btn) {
  try {
    const response = await fetch(`/curtir/${postId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });

    const data = await response.json();

    if (data.success) {
      if (data.curtida) {
        btn.src = "static/img/curtido.png";
        btn.classList.add('curtido');
        // 🔄 Atualiza o contador de curtidas em tempo real
        atualizarTotais();
      } else {
        btn.src = "static/img/heart.png";
        btn.classList.remove('curtido');
        // 🔄 Atualiza o contador de curtidas em tempo real
        atualizarTotais();
      }
    } else {
      console.error(data.mensagem);
    }
  } catch (error) {
    console.error('Erro ao curtir post:', error);
  }
}




//  Carregar curtidas ao abrir a página
(async function carregarCurtidas() {
  console.log("🔄 Iniciando fetch de curtidas...");

  try {
    const response = await fetch("/curtidas_usuario");
    if (!response.ok) throw new Error("Erro na requisição");

    const curtidas = await response.json();
    console.log("Dados recebidos:", curtidas);

    // Atualiza os corações dos cards
    document.querySelectorAll(".card-pet").forEach(card => {
      const postId = card.dataset.postId;
      const btn = card.querySelector(".curtir-btn");

      if (!btn) return;

      if (curtidas[postId]) {
        btn.src = "static/img/curtido.png";
        btn.classList.add("curtido");
        console.log(`❤️ Post ${postId} está curtido`);
      } else {
        btn.src = "static/img/heart.png";
        btn.classList.remove("curtido");
        console.log(`🤍 Post ${postId} não está curtido`);
      }
    });

  } catch (error) {
    console.error("💥 Erro ao carregar curtidas:", error);
  }

})();


async function atualizarTotais() {
  try {
    const response = await fetch("/total_curtidas");
    const totais = await response.json();
    console.log("📊 Totais recebidos:", totais);

    document.querySelectorAll(".card-pet").forEach(card => {
      const postId = card.dataset.postId; // string
      const span = card.querySelector(".total-curtidas");
      if (span) {
        span.textContent = totais[postId] || 0;
      }
    });
  } catch (err) {
    console.error("💥 Erro ao atualizar totais:", err);
  }
}

// chama a função para atualizar quando a página carrega
atualizarTotais();



// função para abrir e listar os comentarios
function abrirComentarios(postId) {
  const modal = document.getElementById('modalComentarios');
  const lista = document.getElementById('comentarios-lista');

  // Mostra mensagem de carregamento
  lista.innerHTML = "<p>Carregando...</p>";

  // Abre o modal
  modal.style.display = "flex";

  // Atualiza o postId no modal
  modal.dataset.postId = postId;

  // Busca os comentários via fetch
  fetch(`/comentarios/${postId}`)
    .then(res => res.json())
    .then(comentarios => {
      if (comentarios.length) {
        // Lista os comentários
        lista.innerHTML = comentarios
          .map(c => `<p><strong>${c.usuario_nome}:</strong> ${c.texto}</p>`)
          .join('');
      } else {
        lista.innerHTML = "<p>Seja o primeiro a comentar!</p>";
      }
      console.log("📄 Comentários carregados:", comentarios);
    })
    .catch(err => {
      console.error("💥 Erro ao carregar comentários:", err);
      lista.innerHTML = "<p>Erro ao carregar comentários.</p>";
    });

  // Seleciona o modal e o botão de fechar

  const fecharBtn = document.querySelector('.fechar-comentario');

  if (fecharBtn && modal) {
    fecharBtn.onclick = () => {
      modal.style.display = 'none';
    };
  }

  // Fecha ao clicar fora do modal
  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });


}


// 📩 Enviar comentário
document.getElementById('form-comentario').addEventListener('submit', async (e) => {
  e.preventDefault();

  console.log("🚀 Evento de envio de comentário acionado!");

  const modal = document.getElementById('modalComentarios'); // ✅ usar o mesmo ID que abrirComentarios
  if (!modal) {
    console.error("❌ Modal de comentários não encontrado!");
    return;
  }

  const postId = modal.dataset.postId;
  if (!postId) {
    console.error("❌ Post ID não definido no modal!");
    return;
  }

  const textoInput = document.getElementById('comentario-texto');
  const texto = textoInput.value.trim();

  console.log("🆔 Post ID:", postId);
  console.log("📝 Texto digitado:", texto);

  if (!texto) {
    console.warn("⚠️ Nenhum texto foi digitado!");
    alert("Escreva algo antes de enviar!");
    return;
  }

  const formData = new FormData();
  formData.append("texto", texto);

  console.log("📦 Dados preparados para envio:", [...formData.entries()]);

  try {
    console.log(`📡 Enviando requisição para /comentario/${postId}...`);

    const response = await fetch(`/comentario/${postId}`, {
      method: "POST",
      body: formData
    });

    console.log("📬 Resposta recebida:", response);

    if (!response.ok) {
      console.error("❌ Erro HTTP:", response.status, response.statusText);
      alert("Erro na comunicação com o servidor.");
      return;
    }

    const data = await response.json();
    console.log("📨 Dados retornados do backend:", data);

    if (data.success) {
      console.log("✅ Comentário adicionado com sucesso!");
      textoInput.value = ""; // limpa o campo
      abrirComentarios(postId); // 🔄 atualiza lista
    } else {
      console.warn("⚠️ Erro ao adicionar comentário:", data.mensagem);
      alert(data.mensagem || "Erro ao enviar comentário.");
    }

  } catch (error) {
    console.error("💥 Erro inesperado ao enviar comentário:", error);
    alert("Erro inesperado. Veja o console para mais detalhes.");
  }
});