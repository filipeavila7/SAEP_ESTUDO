
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
      } else {
        btn.src = "static/img/heart.png";
        btn.classList.remove('curtido');
      }
    } else {
      console.error(data.mensagem);
    }
  } catch (error) {
    console.error('Erro ao curtir post:', error);
  }
}

// Quando a página carregar
window.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("/curtidas_usuario");
    const curtidas = await res.json(); // { post_id: true/false }

    document.querySelectorAll(".curtir-btn").forEach(btn => {
      const postId = parseInt(btn.dataset.postId);

      // Atualiza o coração conforme o banco
      if (curtidas[postId]) {
        btn.src = "static/img/curtido.png";
        btn.classList.add("curtido");
      } else {
        btn.src = "static/img/heart.png";
        btn.classList.remove("curtido");
      }

      // Adiciona clique
      btn.addEventListener("click", () => curtirPost(postId, btn));
    });

  } catch (error) {
    console.error("Erro ao carregar curtidas:", error);
  }
});
