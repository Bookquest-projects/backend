from flask import Flask
from flask_cors import CORS

from books import books_bp
from KeywordGenerator import KeywordGenerator

app = Flask(__name__)
CORS(app)
app.register_blueprint(books_bp)

if __name__ == "__main__":
    summary = ("Dans l'Angleterre du XIIe siècle ravagée par la guerre et"
               " la famine, des êtres luttent pour s'assurer le pouvoir,"
               " la gloire, la sainteté, l'amour, ou simplement de quoi "
               "survivre. Les batailles sont féroces, les hasards "
               "prodigieux, la nature cruelle. La haine règne, mais "
               "l'amour aussi, malmené constamment, blessé parfois, "
               "mais vainqueur enfin quand un Dieu, à la vérité souvent"
               " trop distrait, consent à se laisser toucher par la foi"
               " des hommes. Abandonnant le monde de l'espionnage, Ken"
               " Follett, le maître du suspense, nous livre avec Les"
               " Piliers de la Terre une œuvre monumentale dont "
               "l'intrigue, aux rebonds incessants, s'appuie sur un"
               " extraordinaire travail d'historien. Promené de"
               " pendaisons en meurtres, des forêts anglaises au cœur de"
               " l'Andalousie, de Tours à Saint-Denis, le lecteur se"
               " trouve irrésistiblement happé dans le tourbillon d'une"
               " superbe épopée romanesque.")

    stop_words_french = [
        "à", "alors", "au", "aucun", "aussi", "autre", "avant",
        "avec", "avoir", "bon", "car", "ce", "cela", "ces", "ceux",
        "chaque", "ci", "comme", "comment", "dans", "des", "du",
        "dedans", "dehors", "depuis", "devrait", "doit", "donc",
        "dos", "début", "elle", "elles", "en", "encore", "essai",
        "est", "et", "eu", "fait", "faites", "fois", "font",
        "hors", "ici", "il", "ils", "je", "juste", "la", "le",
        "les", "leur", "là", "ma", "maintenant", "mais", "mes",
        "mien", "moins", "mon", "mot", "même", "ni", "nommés",
        "notre", "nous", "ou", "où", "par", "parce", "pas", "peut",
        "peu", "plupart", "pour", "pourquoi", "quand", "que",
        "quel", "quelle", "quelles", "quels", "qui", "sa",
        "sans", "ses", "seulement", "si", "sien", "son", "sont",
        "sous", "soyez", "sujet", "sur", "ta", "tandis",
        "tellement", "tels", "tes", "ton", "tous", "tout",
        "trop", "très", "tu", "voient", "vont", "votre", "vous",
        "vu", "ça", "étaient", "état", "étions", "été", "être",
        "une", "un", "des", "de", "le", "la", "les", "leur",
        "leurs", "entre", "cette", "cet", "ce", "ces", "se", "ses"
    ]

    generator = KeywordGenerator()
    keywords = generator.get_keyword(summary,
                                     top_n=10,
                                     stop_words=stop_words_french,
                                     use_mmr=True,
                                     diversity=0.3,
                                     use_maxsum=True)
    print("Keywords:", keywords)
