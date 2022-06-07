import streamlit as st

__all__ = ["apresentacao"]
def apresentacao():
    st.header('Bem vindo ao TFT Tracker')
    st.write('Na aba Tracker você poderá acompanhar a evolução diária de qualquer player de qualquer região incluindo você próprio. ')
    st.write('A ideia desta ferramenta é descobrir pessoas que estão jogando bem o patch e analisar suas estatisticas através de sites como o lolchess e idenficar como e porque eles estão sendo bem sucedidos.')
    st.write('Na aba Tracker, você podrá escolher uma região e atualizar em tempo real a evolução de pdls das pessoas junto a ladder atual.')
    st.write('Todos os dias por volta de meia noite o valor do pdl diário será reniciado e assim começando a contagem de um novo dia.')


if __name__ == "__main__":
    apresentacao()