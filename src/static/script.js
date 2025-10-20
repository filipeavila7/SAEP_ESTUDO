
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

