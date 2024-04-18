import pickle

# Dictionary to store translations
translations = {
    'fr': {
        'language': "Français",
        'title': "Assistant Intelligent du Pôle Digital",
        'about_us_title': "À propos de nous",
        'about_us_description': """
## À propos de nous
Cette application est votre passerelle vers l'assistant intelligent du pôle digital.\n \n Elle est construite en utilisant :
- [Streamlit](https://streamlit.io/)
- [Modèle LLM de OpenAI](https://platform.openai.com/docs/models)
- [Pôle Digital](https://www.poledigital.ma/)
""",
        'created_by': "Créé par l'équipe d'IA du Pôle Digital",
        'discover_financial_aid': "Découvrez les aides financières de l'état pour la promotion des investissements agricoles",
        'enter_your_question': "Entrez votre question ici",
        'loading_documents': "Chargement des documents, veuillez patienter un moment ! Cela peut prendre 1 à 2 minutes.",
        'thinking': "Réflexion...",
        'initial_message': "Découvrez les aides financières de l'état pour la promotion des investissements agricoles"
    },
    'ar': {
        'language': "العربية",
        'title': "المساعد الذكي للقطب الرقمي",
        'about_us_title': "معلومات عنا",
        'about_us_description': """
## معلومات عنا
هذا التطبيق هو تواصل مع المساعد الذكي للقطب الرقمي.\n \n  تم بناؤه باستخدام:
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://platform.openai.com/docs/models)
- [Pôle Digital](https://www.poledigital.ma/)
""",
        'created_by': "تم إنشاؤه من قبل فريق الذكاء الاصطناعي للقطب الرقمي",
        'discover_financial_aid': "إكتشف المساعدات المالية للدولة لتشجيع الاستثمارات في القطاع الفلاحي",
        'enter_your_question': "أدخل سؤالك هنا",
        'loading_documents': "جاري تحميل المستندات انتظر قليلاً! قد يستغرق هذا الأمر من 1 إلى 2 دقيقة.",
        'thinking': "جارٍ التفكير...",
        'initial_message': "تعرف على المساعدات المالية الحكومية لتشجيع الاستثمار الزراعي"
    }
}
# <!--  LLM Model-->
# Serializing the dictionary and writing it to a file
with open('translations.pkl', 'wb') as file:
    pickle.dump(translations, file)

print("Dictionary has been serialized and saved.")