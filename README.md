# Assistant RH 🔍 - Groupe 36

Ce projet est une interface interactive avec Streamlit permettant de poser des questions sur des documents PDF RH. Il utilise des modèles de type embeddings (SentenceTransformer) et génération de texte (GPT-2).

## ⚙️ Installation

Cloner le repo, puis installer les dépendances :

```bash
pip install -r requirements.txt
```

Placez vos fichiers PDF dans le dossier `docs/`.

## 🚀 Lancement de l'app

```bash
streamlit run app.py
```

## 📁 Arborescence

```
mon-projet/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── docs/
    ├── document1.pdf
    └── ...
```

## 🧠 Techno utilisées

- Streamlit
- Sentence-Transformers
- FAISS
- Transformers (GPT2)
- PyPDF2
