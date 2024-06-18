Professor, meu maior problema está sendo referenciar as imagens em principal.html. Você pode ver por este campo: <section aria-label="Programação">
                <h1>Livros de Programação:</h1>
                <div class="carrossel">
                    <button id="anterior" class="carrossel-botao">↞</button>
                    
                    <!-- Início do Formulário -->
                    <form action="{{ url_for('confirmar') }}" method="POST" enctype="multipart/form-data">
                        {{ form.csrf_token }}
                        {% for livro in livros %}
                            <input type="hidden" name="livro_id" value="{{ livro.id }}">
                            {% if livro.imagem %}
                                <img src="{{ url_for('static', filename='fotografias/' ~ livro.imagem) }}" alt="{{ livro.titulo }}">
                            {% else %}
                                <img src="{{ url_for('static', filename='livro.png') }}" alt="Sem imagem">
                            {% endif %}
                            <p>{{ livro.titulo }}</p>
                        {% endfor %}
                        <input type="submit" value="Confirmar">
                    </form>
                    <!-- Fim do Formulário -->
                    
                    <button id="proximo" class="carrossel-botao">↠</button>
                </div>
            </section>

            Nesta seção está como um redirecionamento para o template lista_livros.html. Não é o que eu quero, o que estou me 
            batendo é que não consigo colocar as fotos nessa seção Programação, mesmo estando tudo certo no BD. Vou deixar uma 
            cópia do BD/tabelas pro senhor dar uma olhada também, por gentileza.
