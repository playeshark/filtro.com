from flask import Flask, render_template, request # type: ignore
from googleapiclient.discovery import build # type: ignore

app = Flask(__name__)

# Configure sua chave de API e ID do mecanismo de busca
API_KEY = 'AIzaSyDiqaC1Q0ab1vg2d97_8ywGf0kap5TIQ6g'
CSE_ID = 'f5d24e147bf8241c3'  # Apenas o ID, sem <script>

# Função para buscar no Google
def search_google(query):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=query, cx=CSE_ID).execute()
    results = []
    for item in res.get("items", []):
        results.append({'url': item['link'], 'title': item['title'], 'snippet': item.get('snippet', '')})
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            results = search_google(query)
    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)
