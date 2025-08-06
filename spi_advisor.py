import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="SPI-Advisor",
    page_icon="🧭",
    layout="wide"
)

# --- Funções de Lógica e Conteúdo ---

def obter_justificativa(modelo):
    """Retorna o texto de justificativa para um modelo específico."""
    justificativas = {
        "CMMI": """
        **O CMMI se destacou principalmente por sua robustez e reconhecimento internacional.**
        - **Ideal para:** Grandes empresas e setores altamente regulados que buscam um alto nível de maturidade e padronização.
        - **Foco em:** Obter certificação internacional, garantir conformidade e alcançar uma melhoria de qualidade profunda.
        - **Trade-off principal:** Exige um **alto investimento** e pode enfrentar **forte resistência cultural** devido ao seu alto nível de formalismo.
        """,
        "ISO/IEC SPICE": """
        **O ISO/IEC SPICE se destacou por sua flexibilidade e foco em conformidade.**
        - **Ideal para:** Empresas que precisam se alinhar a normas setoriais específicas (ex: automotiva) ou que desejam uma avaliação de capacidade modular.
        - **Foco em:** Garantir conformidade para atuar em cadeias de suprimento e realizar diagnósticos de processo detalhados.
        - **Trade-off principal:** Embora flexível, o modelo pode ser **tecnicamente complexo** de interpretar e exige expertise. É um padrão mais estabelecido e difundido que seu sucessor.
        """,
        "ISO/IEC 330xx": """
        **O ISO/IEC 330xx se destacou por ser a evolução moderna do SPICE, focado em padronização.**
        - **Ideal para:** Organizações que já possuem maturidade e buscam atualizar suas práticas de avaliação com métricas modernas.
        - **Foco em:** Modernizar a avaliação de processos e facilitar o benchmarking global.
        - **Trade-off principal:** Como um padrão mais recente, possui **menos dados consolidados na literatura**, mas representa a direção futura das normas ISO de avaliação.
        """,
        "MPS.BR": """
        **O MPS.BR se destacou por sua acessibilidade e adequação ao contexto brasileiro.**
        - **Ideal para:** Pequenas e Médias Empresas (PMEs) que buscam uma primeira iniciativa de melhoria de processo com um caminho claro e viável.
        - **Foco em:** Implementar uma melhoria de **baixo custo e em menor tempo**, padronizando processos essenciais.
        - **Trade-off principal:** Possui **menor reconhecimento internacional** que o CMMI, o que pode ser uma limitação dependendo dos seus objetivos de mercado.
        """
    }
    return justificativas.get(modelo, "Nenhuma justificativa disponível.")

def obter_analise_desempate(modelos):
    """Gera o texto para a análise de desempate, com lógica aprimorada para múltiplos empates."""
    st.error(f"### Análise de Empate: {len(modelos)} Modelos Altamente Adequados")
    st.write(f"Com base em suas respostas, os modelos **{ ' e '.join(modelos) }** se mostraram igualmente alinhados ao seu contexto. A decisão final dependerá de qual trade-off sua organização está mais disposta a fazer.")

    for modelo in modelos:
        st.subheader(f"Opção: {modelo}")
        st.write(obter_justificativa(modelo))
    
    st.subheader("O Trade-off Final: Como Decidir?")
    
    modelos_set = set(modelos)
    
    # LÓGICA DE DESEMPATE
    if len(modelos_set) == 3 and modelos_set == {'ISO/IEC SPICE', 'ISO/IEC 330xx', 'MPS.BR'}:
        st.write("Para desempatar entre os três, você precisa definir qual destes perfis representa a **prioridade máxima** da sua empresa:")
        st.info("""
        - **Perfil A: O Pragmatismo Nacional.** Se a sua prioridade absoluta é o **melhor custo-benefício e a implementação mais rápida**, com foco total na realidade do mercado brasileiro, então sua escolha é **MPS.BR**.

        - **Perfil B: O Padrão Internacional Consolidado.** Se a sua prioridade é adotar um padrão flexível, com **amplo reconhecimento internacional e uma vasta base de conhecimento já estabelecida**, então sua escolha é **ISO/IEC SPICE**.
        
        - **Perfil C: A Inovação e o Futuro.** Se a sua prioridade é usar o padrão **mais moderno, com métricas preparadas para o futuro e benchmarking global**, mesmo que seja menos difundido hoje, então sua escolha é **ISO/IEC 330xx**.
        """)
    elif len(modelos_set) == 2:
        if modelos_set == {'CMMI', 'ISO/IEC SPICE'}:
            st.info("**Prioridade Máxima:** Reconhecimento de mercado e um selo de maturidade de alto nível **(escolha CMMI)** OU a flexibilidade para se adaptar a uma norma setorial específica **(escolha ISO/IEC SPICE)?**")
        elif modelos_set == {'ISO/IEC SPICE', 'MPS.BR'}:
            st.info("**Prioridade Máxima:** Ter um padrão internacional flexível **(escolha ISO/IEC SPICE)** OU o melhor custo-benefício para o mercado nacional **(escolha MPS.BR)?**")
        elif modelos_set == {'CMMI', 'MPS.BR'}:
            st.info("**Prioridade Máxima:** Reconhecimento global e profundidade máxima, mesmo com alto custo **(escolha CMMI)** OU uma implementação rápida e acessível com foco no Brasil **(escolha MPS.BR)?**")
        elif modelos_set == {'ISO/IEC SPICE', 'ISO/IEC 330xx'}:
            st.info("**Prioridade Máxima:** Um padrão mais **estabelecido e difundido (escolha ISO/IEC SPICE)** OU um padrão mais **moderno com métricas padronizadas para o futuro (escolha ISO/IEC 330xx)?**")
        else: # Fallback para outros empates duplos
            st.info("Analise as justificativas individuais de cada modelo acima e discuta com sua equipe qual dos 'trade-offs principais' é o mais crítico para o sucesso da sua iniciativa.")
    else: # Fallback para empates triplos não previstos ou quádruplos
        st.info("Dado o empate entre múltiplos modelos, a decisão final é mais complexa. Analise as justificativas individuais de cada um e discuta com sua equipe qual dos 'trade-offs principais' melhor representa a prioridade máxima da sua organização neste momento.")


def calcular_recomendacao(porte, setor, recursos, objetivo, cultura, formalismo):
    """Calcula a pontuação para cada modelo com a lógica definitiva."""
    scores = {'CMMI': 0, 'ISO/IEC SPICE': 0, 'ISO/IEC 330xx': 0, 'MPS.BR': 0}

    if porte == 'PME (até 100 funcionários)':
        scores['MPS.BR'] += 3; scores['ISO/IEC SPICE'] += 1; scores['ISO/IEC 330xx'] += 1; scores['CMMI'] -= 1
    elif porte == 'Grande Empresa (>100 funcionários)':
        scores['CMMI'] += 2; scores['ISO/IEC SPICE'] += 1

    if setor == 'Altamente Regulado (Saúde, Finanças, Automotivo, etc.)':
        scores['CMMI'] += 3; scores['ISO/IEC SPICE'] += 2; scores['ISO/IEC 330xx'] += 2
    else:
        scores['MPS.BR'] += 1

    if recursos == 'Baixo':
        scores['CMMI'] -= 3; scores['MPS.BR'] += 3; scores['ISO/IEC SPICE'] += 1
    elif recursos == 'Moderado':
        scores['ISO/IEC SPICE'] += 2; scores['ISO/IEC 330xx'] += 2; scores['MPS.BR'] += 1; scores['CMMI'] += 1
    elif recursos == 'Alto':
        scores['CMMI'] += 3

    if objetivo == 'Obter certificação INTERNACIONAL':
        scores['CMMI'] += 3; scores['ISO/IEC SPICE'] += 2; scores['ISO/IEC 330xx'] += 2
    elif objetivo == 'Melhorar a qualidade e eficiência INTERNA':
        scores['CMMI'] += 1; scores['ISO/IEC SPICE'] += 1; scores['ISO/IEC 330xx'] += 1; scores['MPS.BR'] += 2
    elif objetivo == 'Implementar uma melhoria de BAIXO CUSTO':
        scores['MPS.BR'] += 3; scores['CMMI'] -= 2

    if cultura == 'Flexível e aberta a métodos ágeis':
        scores['CMMI'] -= 1; scores['ISO/IEC SPICE'] += 1; scores['ISO/IEC 330xx'] += 1; scores['MPS.BR'] += 1
    elif cultura == 'Tradicional e orientada a processos formais':
        scores['CMMI'] += 2

    if formalismo == 'Rígido, prescritivo e com níveis definidos':
        scores['CMMI'] += 3; scores['MPS.BR'] += 1
    elif formalismo == 'Modular, flexível e focado em áreas específicas':
        scores['ISO/IEC SPICE'] += 3; scores['ISO/IEC 330xx'] += 3

    return scores


# --- Interface da Aplicação ---
st.title("🧭 SPI-Advisor: Guia Estratégico Interativo")
st.markdown("Esta ferramenta foi projetada para auxiliá-lo na escolha do modelo de melhoria de processo de software mais adequado para o seu contexto. Baseado na teoria de que **não existe um modelo \"melhor\", mas sim o mais adequado**, as perguntas a seguir o guiarão por uma análise de trade-offs estratégicos.")
st.markdown("---")

# --- Formulário Principal ---
st.header("1. Análise do seu Contexto")
st.markdown("Responda às perguntas abaixo para obter sua recomendação.")
col1, col2 = st.columns(2)
with col1:
    porte = st.selectbox("**Qual o porte da sua empresa?**", ("PME (até 100 funcionários)", "Grande Empresa (>100 funcionários)"))
    recursos = st.select_slider("**Orçamento e tempo disponíveis:**", options=["Baixo", "Moderado", "Alto"], value="Moderado")
    cultura = st.radio("**Cultura da sua organização:**", ("Flexível e aberta a métodos ágeis", "Tradicional e orientada a processos formais"))
with col2:
    setor = st.selectbox("**Seu setor de atuação é:**", ("TI Geral / Outros", "Altamente Regulado (Saúde, Finanças, Automotivo, etc.)"))
    objetivo = st.selectbox("**Qual é o principal objetivo estratégico da sua iniciativa?**", ("Melhorar a qualidade e eficiência INTERNA", "Obter certificação INTERNACIONAL", "Implementar uma melhoria de BAIXO CUSTO"))
    formalismo = st.radio("**Qual o nível de formalismo desejado para o modelo?**", ("Modular, flexível e focado em áreas específicas", "Rígido, prescritivo e com níveis definidos"))

st.markdown("<br>", unsafe_allow_html=True)
analisar = st.button("Analisar e Recomendar", type="primary", use_container_width=True)
st.markdown("---")

# --- Área de Resultados ---
if analisar:
    st.header("2. Análise e Recomendação Estratégica")
    scores = calcular_recomendacao(porte, setor, recursos, objetivo, cultura, formalismo)
    max_score = max(scores.values())
    modelos_empatados = [modelo for modelo, score in scores.items() if score == max_score]

    if len(modelos_empatados) == 1:
        modelo_recomendado = modelos_empatados[0]
        st.info(f"### **Modelo Recomendado: {modelo_recomendado}**")
        st.markdown(obter_justificativa(modelo_recomendado))
    else:
        obter_analise_desempate(modelos_empatados)

    st.subheader("Pontuação Comparativa")
    df_scores = pd.DataFrame(list(scores.items()), columns=['Modelo', 'Pontuação']).set_index('Modelo')
    st.bar_chart(df_scores)
    st.markdown("A pontuação reflete o nível de alinhamento de cada modelo com o perfil que você descreveu.")
    st.markdown("---")

    st.header("3. Matriz de Decisão Estratégica")
    st.markdown("Veja abaixo a matriz comparativa completa, que fundamenta a recomendação.")
    data = {
        'Dimensão Estratégica': ['**Contexto Ideal**', '**Recursos e Investimento**', '**Cultura e Fator Humano**', '**Estrutura e Flexibilidade**', '**Objetivo Principal**'],
        'CMMI': ['Grandes Empresas, Setores Regulados', 'Alto', 'Desafio: Alta Resistência Cultural', 'Rígida, Prescritiva, Níveis de Maturidade', 'Reconhecimento Internacional, Maturidade Máxima'],
        'ISO/IEC SPICE': ['Conformidade Setorial, Flexibilidade', 'Moderado', 'Desafio: Interpretação Técnica', 'Modular, Flexível, Foco em Capacidade', 'Conformidade com Normas, Diagnóstico'],
        'ISO/IEC 330xx*': ['Organizações Maduras, Modernização', 'Moderado*', 'Desafio: Adaptação Cultural*', 'Evolução do SPICE, Métricas Padronizadas*', 'Modernização da Avaliação, Benchmarking Global*'],
        'MPS.BR': ['PMEs no Brasil', 'Baixo', 'Desafio: Resistência e Rotatividade', 'Simplificada, Gradual, Foco Nacional', 'Acessibilidade e Melhoria Inicial']
    }
    df_matriz = pd.DataFrame(data).set_index('Dimensão Estratégica')
    st.table(df_matriz)
    st.caption("*Nota sobre o ISO/IEC 330xx: As informações para este modelo são baseadas em um número limitado de estudos em seu mapeamento. Ele deve ser visto como uma versão mais moderna do SPICE.")
    st.markdown("---")
    st.warning("**Aviso Importante:** Esta ferramenta é um guia de apoio à decisão. Ela não substitui a necessidade de uma análise interna aprofundada e, se necessário, a consulta com especialistas.")