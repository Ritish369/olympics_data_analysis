# Used to make directories and all on Heroku
# This is a configuration/barch file
mkdir -p ~/.streamlit/

echo"\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml