import os
import joblib
import pandas as pd
import streamlit as st
import hmac
##################### Gerar Senhas
# ============================================================
# CONFIGURAÇÃO ÚNICA DO STREAMLIT
# ============================================================
st.set_page_config(
    page_title="Classificação de Risco COVID",
    page_icon="🩺",
    layout="wide"
)
# ============================================================
# LOGIN
# ============================================================
def carregar_usuarios():

    try:
        return st.secrets["usuarios"]

    except Exception:
        return None
def autenticar(usuario, senha):

    usuarios = carregar_usuarios()

    if usuarios is None:
        return False, "Usuários ainda não configurados."

    if usuario not in usuarios:
        return False, "Usuário ou senha inválidos."

    senha_correta = str(
        usuarios[usuario]["senha"]
    )

    if hmac.compare_digest(
        str(senha),
        senha_correta
    ):

        nome = str(
            usuarios[usuario].get(
                "nome",
                usuario
            )
        )

        return True, nome

    return False, "Usuário ou senha inválidos."
# ============================================================
# CONTROLE DA SESSÃO
# ============================================================

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False


# ============================================================
# TELA DE LOGIN
# ============================================================

if not st.session_state.autenticado:

    st.title("🔐 Acesso ao sistema")

    st.write(
        "Digite seu usuário e sua senha para continuar."
    )

    usuario = st.text_input(
        "Usuário",
        placeholder="Digite seu usuário"
    )

    senha = st.text_input(
        "Senha",
        type="password",
        placeholder="Digite sua senha"
    )

    if st.button(
        "Entrar",
        use_container_width=True,
        type="primary"
    ):

        if not usuario or not senha:

            st.warning(
                "Informe o usuário e a senha."
            )

        else:

            sucesso, resultado = autenticar(
                usuario,
                senha
            )

            if sucesso:

                st.session_state.autenticado = True
                st.session_state.usuario = usuario
                st.session_state.nome_usuario = resultado

                st.rerun()

            else:

                st.error(resultado)

    # Impede que o restante do aplicativo apareça
    st.stop()


# ============================================================
# USUÁRIO LOGADO
# ============================================================

nome_usuario = st.session_state.get(
    "nome_usuario",
    st.session_state.get("usuario", "")
)


# ============================================================
# BOTÃO SAIR
# ============================================================

with st.sidebar:

    st.success(
        f"👤 Usuário: {nome_usuario}"
    )

    if st.button(
        "🚪 Sair",
        use_container_width=True
    ):

        st.session_state.autenticado = False

        st.session_state.pop(
            "usuario",
            None
        )

        st.session_state.pop(
            "nome_usuario",
            None
        )

        st.rerun()


# ============================================================
# A PARTIR DAQUI COMEÇA SEU CÓDIGO COVID
# ============================================================

ARQUIVO_MODELO = "modelo_covid.pkl"


@st.cache_resource
def carregar_modelo():

    return joblib.load(
        ARQUIVO_MODELO
    )


if not os.path.exists(
    ARQUIVO_MODELO
):

    st.error(
        "Modelo não encontrado. "
        "Execute treinar_modelo.py antes de abrir o aplicativo."
    )

    st.stop()


modelo = carregar_modelo()


st.title(
    "Modelo de Classificação Para Pacientes Suspeitos de COVID-19"
)

st.warning(
    """
    Aplicativo desenvolvido com base em modelos epidemiológicos.
    O modelo deve estar sempre em revisão com profissionais de saúde.
    """
)
####################Fim do Código Gerar Senha

# ============================================================
# CARREGAR MODELO
# ============================================================

ARQUIVO_MODELO = "modelo_covid.pkl"


@st.cache_resource
def carregar_modelo():

    return joblib.load(ARQUIVO_MODELO)


if not os.path.exists(ARQUIVO_MODELO):

    st.error(
        "Modelo não encontrado. "
        "Execute treinar_modelo.py antes de abrir o aplicativo."
    )

    st.stop()


modelo = carregar_modelo()


# ============================================================
# CABEÇALHO
# ============================================================

st.title("Modelo de Classificação Para Pacientes Suspeitos de COVID-19")

st.warning("""Aplicativo desenvolvido com base em modelos Epdemiológicos
    Claro que o modelo deve sempre esta em revisão com os profissionais de Saúde"""
    
)


# ============================================================
# ABAS
# ============================================================

aba1, aba2 = st.tabs([
    " Classificar paciente",
    " Avaliação do modelo"
])


# ============================================================
# ABA 1 — CLASSIFICAÇÃO
# ============================================================

with aba1:

    st.subheader("Dados do paciente")

    # --------------------------------------------------------
    # DEMOGRÁFICOS
    # --------------------------------------------------------

    st.markdown("### 1. Dados demográficos")

    col1, col2 = st.columns(2)

    with col1:

        idade = st.number_input(
            "Idade",
            min_value=18,
            max_value=100,
            value=45,
            step=1
        )

    with col2:

        sexo = st.selectbox(
            "Sexo",
            ["Masculino", "Feminino"]
        )


    # --------------------------------------------------------
    # SINAIS VITAIS
    # --------------------------------------------------------

    st.markdown("### 2. Sinais vitais")

    col1, col2, col3 = st.columns(3)

    with col1:

        temperatura = st.number_input(
            "Temperatura (°C)",
            min_value=34.0,
            max_value=43.0,
            value=37.5,
            step=0.1
        )

    with col2:

        saturacao_o2 = st.number_input(
            "Saturação de O₂ (%)",
            min_value=70.0,
            max_value=100.0,
            value=96.0,
            step=1.0
        )

    with col3:

        frequencia_cardiaca = st.number_input(
            "Frequência cardíaca (bpm)",
            min_value=30,
            max_value=200,
            value=85,
            step=1
        )


    col1, col2 = st.columns(2)

    with col1:

        frequencia_respiratoria = st.number_input(
            "Frequência respiratória",
            min_value=5,
            max_value=60,
            value=18,
            step=1
        )

    with col2:

        pressao_sistolica = st.number_input(
            "Pressão sistólica",
            min_value=50,
            max_value=250,
            value=120,
            step=1
        )


    # --------------------------------------------------------
    # COMORBIDADES
    # --------------------------------------------------------

    st.markdown("### 3. Comorbidades")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        diabetes = st.checkbox("Diabetes")

    with col2:
        hipertensao = st.checkbox("Hipertensão")

    with col3:
        obesidade = st.checkbox("Obesidade")

    with col4:
        doenca_cardiovascular = st.checkbox(
            "Doença cardiovascular"
        )


    # --------------------------------------------------------
    # SINTOMAS
    # --------------------------------------------------------

    st.markdown("### 4. Sintomas")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        falta_ar = st.checkbox("Falta de ar")

    with col2:
        tosse = st.checkbox("Tosse")

    with col3:
        febre = st.checkbox("Febre")

    with col4:
        dor_peito = st.checkbox("Dor no peito")


    st.divider()


    # --------------------------------------------------------
    # CLASSIFICAR
    # --------------------------------------------------------

    if st.button(
        "🔍 CLASSIFICAR PACIENTE",
        type="primary",
        use_container_width=True
    ):

        dados_paciente = pd.DataFrame({

            "idade": [idade],

            "sexo": [sexo],

            "temperatura": [temperatura],

            "saturacao_o2": [saturacao_o2],

            "frequencia_cardiaca": [
                frequencia_cardiaca
            ],

            "frequencia_respiratoria": [
                frequencia_respiratoria
            ],

            "pressao_sistolica": [
                pressao_sistolica
            ],

            "diabetes": [int(diabetes)],

            "hipertensao": [int(hipertensao)],

            "obesidade": [int(obesidade)],

            "doenca_cardiovascular": [
                int(doenca_cardiovascular)
            ],

            "falta_ar": [int(falta_ar)],

            "tosse": [int(tosse)],

            "febre": [int(febre)],

            "dor_peito": [int(dor_peito)]
        })


        # ----------------------------------------------------
        # PREDIÇÃO
        # ----------------------------------------------------

        resultado = modelo.predict(
            dados_paciente
        )[0]

        probabilidades = modelo.predict_proba(
            dados_paciente
        )[0]

        classes = modelo.classes_


        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        st.subheader("Resultado da classificação")

        if resultado == "Baixo":

            st.success("🟢 RISCO ESTIMADO: BAIXO")

        elif resultado == "Moderado":

            st.warning("🟠 RISCO ESTIMADO: MODERADO")

        else:

            st.error("🔴 RISCO ESTIMADO: ALTO")


        # ----------------------------------------------------
        # PROBABILIDADES
        # ----------------------------------------------------

        st.subheader("Probabilidades estimadas")

        probabilidades_df = pd.DataFrame({

            "Classificação": classes,

            "Probabilidade": probabilidades * 100

        })


        col1, col2, col3 = st.columns(3)

        for classe, probabilidade in zip(
            classes,
            probabilidades
        ):

            percentual = probabilidade * 100

            if classe == "Baixo":

                col1.metric(
                    "🟢 Baixo",
                    f"{percentual:.1f}%"
                )

            elif classe == "Moderado":

                col2.metric(
                    "🟠 Moderado",
                    f"{percentual:.1f}%"
                )

            elif classe == "Alto":

                col3.metric(
                    "🔴 Alto",
                    f"{percentual:.1f}%"
                )


        st.bar_chart(
            probabilidades_df.set_index(
                "Classificação"
            )
        )


        # ----------------------------------------------------
        # DADOS UTILIZADOS
        # ----------------------------------------------------

        with st.expander(
            "Ver dados utilizados na classificação"
        ):

            st.dataframe(
                dados_paciente,
                use_container_width=True
            )


# ============================================================
# ABA 2 — AVALIAÇÃO
# ============================================================

with aba2:

    st.subheader("Avaliação do modelo")

    st.write(
        "Resultados obtidos durante o treinamento "
        "com dados sintéticos."
    )


    # --------------------------------------------------------
    # MÉTRICAS
    # --------------------------------------------------------

    caminho_metricas = "resultados/metricas.txt"

    if os.path.exists(caminho_metricas):

        with open(
            caminho_metricas,
            "r",
            encoding="utf-8"
        ) as arquivo:

            metricas = arquivo.read()

        st.text(metricas)

    else:

        st.info(
            "Execute treinar_modelo.py para gerar "
            "as métricas."
        )


    # --------------------------------------------------------
    # MATRIZ DE CONFUSÃO
    # --------------------------------------------------------

    caminho_matriz = (
        "resultados/matriz_confusao.png"
    )

    if os.path.exists(caminho_matriz):

        st.subheader("Matriz de confusão")

        st.image(
            caminho_matriz,
            use_container_width=True
        )


    # --------------------------------------------------------
    # IMPORTÂNCIA DAS VARIÁVEIS
    # --------------------------------------------------------

    caminho_importancia = (
        "resultados/importancia_variaveis.png"
    )

    if os.path.exists(caminho_importancia):

        st.subheader("Importância das variáveis")

        st.image(
            caminho_importancia,
            use_container_width=True
        )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "Preencha os Parâmetros Para Receber Sua Classificação "
    )