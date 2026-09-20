import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="SPI-Advisor",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 2rem;
        transition: all 0.3s ease;
    }
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
    }
    </style>
""", unsafe_allow_html=True)

if 'etapa' not in st.session_state:
    st.session_state.etapa = 'formulario'

def obter_justificativa(modelo):
    justificativas = {
        "CMMI": "**CMMI (Capability Maturity Model Integration)**\nDestaca-se pela robustez e reconhecimento internacional em níveis de maturidade. Ideal para grandes empresas, cadeias globais e setores altamente regulados. Exige investimento financeiro substancial e esforço contínuo da equipe de engenharia.",
        "ISO/IEC 15504": "**ISO/IEC 15504 (SPICE)**\nDestaca-se pela flexibilidade e avaliação baseada na capacidade de processos individuais. Muito requisitado para conformidade setorial (ex: Automotive SPICE). Exige avaliadores com alta expertise técnica.",
        "ISO/IEC 330xx": "**Série ISO/IEC 330xx**\nA evolução moderna da 15504. Fornece uma estrutura robusta e independente para avaliação, com foco na padronização e modernização das métricas, ideal para organizações maduras que buscam benchmarking contínuo.",
        "MPS.BR": "**MPS.BR (Melhoria de Processo do Software Brasileiro)**\nDestaca-se pela acessibilidade, baixo custo e adequação à realidade nacional. Composto por 7 níveis graduais, é a principal rampa de acesso à qualidade de software para PMEs brasileiras."
    }
    return justificativas.get(modelo, "")

def calcular_recomendacao(respostas):
    scores = {'CMMI': 0, 'ISO/IEC 15504': 0, 'ISO/IEC 330xx': 0, 'MPS.BR': 0}

    if respostas['porte'] == 'PME (até 100 colaboradores)':
        scores['MPS.BR'] += 3
        scores['ISO/IEC 15504'] += 1
        scores['ISO/IEC 330xx'] += 1
        scores['CMMI'] -= 2
    else:
        scores['CMMI'] += 3
        scores['ISO/IEC 15504'] += 2
        scores['ISO/IEC 330xx'] += 2

    if respostas['setor'] == 'Altamente Regulado (Saúde, Finanças, Automóvel)':
        scores['CMMI'] += 4
        scores['ISO/IEC 15504'] += 4
        scores['ISO/IEC 330xx'] += 3
    else:
        scores['MPS.BR'] += 3
        scores['CMMI'] += 1

    if respostas['mercado'] == 'Nacional (Brasil)':
        scores['MPS.BR'] += 4
        scores['CMMI'] -= 1
    else:
        scores['CMMI'] += 4
        scores['ISO/IEC 15504'] += 3
        scores['ISO/IEC 330xx'] += 3
        scores['MPS.BR'] -= 3

    if respostas['recursos'] == 'Baixo (Equipe enxuta, orçamento restrito)':
        scores['CMMI'] -= 10
        scores['MPS.BR'] += 5
        scores['ISO/IEC 15504'] += 1
    else:
        scores['CMMI'] += 5
        scores['ISO/IEC 15504'] += 2
        scores['ISO/IEC 330xx'] += 2

    if respostas['turnover'] == 'Alto (Forte necessidade de reter conhecimento)':
        scores['CMMI'] += 2
        scores['MPS.BR'] -= 1
    else:
        scores['ISO/IEC 15504'] += 2
        scores['ISO/IEC 330xx'] += 2

    if respostas['agile'] == 'Avançado (CI/CD, DevOps, Integração Contínua)':
        scores['CMMI'] -= 3
        scores['ISO/IEC 330xx'] += 3
        scores['ISO/IEC 15504'] += 2
        scores['MPS.BR'] += 1

    return scores

def gerar_grafico_radar(modelos_recomendados, respostas):
    categorias = ['Custo de Investimento', 'Rigidez Documental', 'Peso Internacional', 'Aderência Ágil', 'Foco no Mercado BR']
    
    perfis_modelos = {
        'CMMI': [5, 5, 5, 2, 1], 
        'ISO/IEC 15504': [3, 4, 4, 3, 2],
        'ISO/IEC 330xx': [3, 3, 4, 4, 2], 
        'MPS.BR': [2, 3, 1, 4, 5]
    }
    
    perfil_empresa = [
        5 if "Alto" in respostas['recursos'] else 1,
        5 if "Regulado" in respostas['setor'] else 2,
        5 if "Internacional" in respostas['mercado'] else 1,
        5 if "Avançado" in respostas['agile'] else 2,
        5 if "Nacional" in respostas['mercado'] else 1
    ]

    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=perfil_empresa, 
        theta=categorias, 
        fill='toself', 
        name='Perfil da sua Organização', 
        line_color='rgba(46, 134, 193, 0.8)', 
        fillcolor='rgba(46, 134, 193, 0.3)'
    ))
    
    cores = ['rgba(231, 76, 60, 0.9)', 'rgba(39, 174, 96, 0.9)', 'rgba(243, 156, 18, 0.9)']
    
    for i, modelo in enumerate(modelos_recomendados):
        fig.add_trace(go.Scatterpolar(
            r=perfis_modelos[modelo], 
            theta=categorias, 
            mode='lines', 
            name=f'Exigência: {modelo}', 
            line_color=cores[i % len(cores)], 
            line_width=3
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])), 
        showlegend=True, 
        margin=dict(l=40, r=40, t=40, b=40), 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        dragmode=False 
    )
    return fig

if st.session_state.etapa == 'formulario':
    
    st.title("SPI-Advisor")
    st.markdown("##### Motor de Decisão para Melhoria de Processos de Software")
    st.markdown("Analise os trade-offs do seu contexto organizacional preenchendo as dimensões abaixo.")
    st.markdown("---")
    
    with st.form("form_diagnostico"):
        st.markdown("### 1. Estrutura e Mercado")
        porte = st.selectbox("Dimensão da equipe de engenharia:", ["PME (até 100 colaboradores)", "Grande Empresa (> 100 colaboradores)"])
        setor = st.selectbox("Setor de atuação:", ["Tecnologia Geral ou Não Regulado", "Altamente Regulado (Saúde, Finanças, Automóvel)"])
        mercado = st.selectbox("Foco geográfico dos clientes:", ["Nacional (Brasil)", "Internacional (Exportação)"])
        
        st.markdown("### 2. Cultura Operacional")
        recursos = st.selectbox("Disponibilidade Financeira e Tempo:", ["Baixo (Equipe enxuta, orçamento restrito)", "Alto (Capacidade para auditorias externas)"])
        turnover = st.selectbox("Nível de rotatividade (turnover):", ["Baixo a Moderado (Equipe estável)", "Alto (Forte necessidade de reter conhecimento)"])
        agile = st.selectbox("Integração de práticas Ágeis:", ["Iniciante / Intermediário", "Avançado (CI/CD, DevOps, Integração Contínua)"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Analisar Contexto e Recomendar Modelo", type="primary", use_container_width=True)
        
        if submitted:
            st.session_state.respostas = {
                'porte': porte, 'setor': setor, 'mercado': mercado, 
                'recursos': recursos, 'turnover': turnover, 'agile': agile
            }
            st.session_state.etapa = 'resultado'
            st.rerun()

elif st.session_state.etapa == 'resultado':
    
    if st.button("← Ajustar Variáveis do Cenário", type="secondary"):
        st.session_state.etapa = 'formulario'
        st.rerun()
        
    respostas = st.session_state.respostas
    scores = calcular_recomendacao(respostas)
    
    ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    pontuacao_max = ranking[0][1]
    modelos_vencedores = [modelo for modelo, score in ranking if score == pontuacao_max]
    
    st.markdown("---")
    
    if len(modelos_vencedores) > 1:
        st.warning(f"Empate Estratégico: {' e '.join(modelos_vencedores)}")
        st.markdown("Seu cenário organizacional apresenta um equilíbrio entre as exigências e os benefícios destes modelos. A decisão final dependerá de prioridades de longo prazo da gestão.")
        for m in modelos_vencedores:
            st.markdown(obter_justificativa(m))
    else:
        modelo_recomendado = modelos_vencedores[0]
        st.success(f"Recomendação Primária: {modelo_recomendado}")
        st.markdown(obter_justificativa(modelo_recomendado))
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### Alinhamento de Trade-off (Análise Visual)")
    fig_radar = gerar_grafico_radar(modelos_vencedores, respostas)
    st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("### Tabela de Aderência")
    df_ranking = pd.DataFrame(ranking, columns=['Modelo SPI', 'Pontuação de Aderência']).set_index('Modelo SPI')
    st.table(df_ranking) 
    
    st.markdown("---")
    relatorio_texto = f"""=== PARECER TÉCNICO: SPI-ADVISOR ===
Data da Análise: {datetime.now().strftime("%d/%m/%Y %H:%M")}

[1. CONTEXTO AVALIADO]
- Dimensão da Equipe: {respostas['porte']}
- Setor: {respostas['setor']}
- Mercado: {respostas['mercado']}
- Disponibilidade de Recursos: {respostas['recursos']}
- Nível de Turnover: {respostas['turnover']}
- Maturidade Ágil: {respostas['agile']}

[2. RESULTADO DA INFERÊNCIA]
Modelos Mais Adequados: {', '.join(modelos_vencedores)}
Pontuação Máxima Atingida: {pontuacao_max}

Ranking Completo:
"""
    for m, s in ranking:
        relatorio_texto += f"- {m}: {s} pontos\n"
        
    relatorio_texto += "\nNota: Pontuações negativas indicam restrições severas entre o contexto da empresa e as exigências do modelo."

    st.download_button(
        label="Fazer Download do Parecer (.txt)",
        data=relatorio_texto,
        file_name="parecer_spi_advisor.txt",
        mime="text/plain",
        type="primary"
    )
