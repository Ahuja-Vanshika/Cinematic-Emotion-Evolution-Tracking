import streamlit as st

st.set_page_config(
    page_title = "Movie Emotions Atlas",
    page_icon = "🎬",
    layout = "wide"
)

# HEADER
st.title("Movie Emotion Atlas")
st.subheader("How the world's feelings about classic films changed over time")

st.divider()

st.markdown("""
This project tracks how the public emotional perception of 7 classic film
has evolved from their release year to 2026 using social media data from **Reddit**
and **Letterboxd**.
            
Using zero-shot emotion classification powered by 'facebook/bart-large-mnli',
we analyze thousands of reviews and discussions to map the emotional journey of each
film across time.
""")

st.divider()

st.subheader("🎥Movies Covered")

movies = {
    "Titanic (1997)"              : "Love story evolution — from blockbuster romance to nostalgic classic",
    "The Shawshank Redemption (1994)" : "Flopped on release → became the greatest film ever made",
    "The Dark Knight (2008)"      : "Excitement → grief → cultural icon",
    "Parasite (2019)"             : "Fascination → shock → social commentary",
    "Interstellar (2014)"         : "Divisive on release → grew massively in appreciation",
    "La La Land (2016)"           : "Love → Oscars backlash → re-appreciated",
    "Schindler's List (1993)"     : "Grief → reverence → how does Holocaust remembrance evolve?",
}

for movie, description in movies.items():
    st.markdown(f"**{movie}** - {description}")

st.divider()

st.subheader("Navigate")

col1, col2 = st.columns(2)

with col1:
    st.info(""" 
    **Movie Explorer**
    
    Deep dive into one movie at a time
    See how emotions evolved year by year
""")
    
with col2:
    st.info("""
    **Cross Movie Comparison**
    Compare one emotion across all movies.
    See which film triggered the most nostalgia, criticism, or love.
""")
    
st.divider()