import streamlit as st
import re
import random
import time
from langdetect import detect


SUPPORTED_LANGUAGES = {
    'en': 'English',
    'ar': 'Arabic',
    'zh': 'Chinese',
    'ur': 'Urdu',
    'hi': 'Hindi',
    'de': 'German'
}


RULES = {
    "greeting": {
        "patterns": {
            'en': ["hi", "hello", "hey", "good morning", "greetings", "good afternoon", "good evening", "hi there", "hey there"],
            'ar': ["مرحبا", "السلام عليكم", "اهلا", "صباح الخير", "مساء الخير"],
            'zh': ["你好", "您好", "早上好", "下午好", "晚上好"],
            'ur': ["سلام", "ہیلو", "آداب", "صبح بخیر", "شام بخیر"],
            'hi': ["नमस्ते", "हैलो", "स्वागत", "शुभ प्रभात", "शुभ संध्या"],
            'de': ["hallo", "guten tag", "guten morgen", "guten abend", "hi", "hey"]
        },
        "responses": {
            'en': [
                "Hello! Welcome to ** Shoaib Vista Solutions**. How can I assist you today?",
                "Hi there! I'm your AI Vista assistant. What can I do for you?",
                "Greetings! I'm Shoaib from AI Vista Solutions. How may I help you?"
            ],
            'ar': [
                "مرحبا! أهلا بكم في **AI Vista Solutions**. كيف يمكنني مساعدتك اليوم؟",
                "أهلاً! أنا مساعدك في AI Vista. كيف يمكنني مساعدتك؟",
                "تحياتي! أنا Shoaib من AI Vista Solutions. كيف يمكنني مساعدتك؟"
            ],
            'zh': [
                "您好！欢迎来到**AI Vista Solutions**。我今天能为您提供什么帮助？",
                "你好！我是AI Vista的助手。我能为您做什么？",
                "问候！我是AI Vista Solutions的Shoaib。我如何帮助您？"
            ],
            'ur': [
                "ہیلو! **AI Vista Solutions** میں خوش آمدید۔ میں آپ کی کس طرح مدد کر سکتا ہوں؟",
                "ہیلو! میں AI Vista کا اسسٹنٹ ہوں۔ میں آپ کی کیا خدمت کر سکتا ہوں؟",
                "سلام! میں AI Vista Solutions سے Shoaib ہوں۔ میں آپ کی کس طرح مدد کر سکتا ہوں؟"
            ],
            'hi': [
                "नमस्ते! **AI Vista Solutions** में आपका स्वागत है। मैं आपकी कैसे सहायता कर सकता हूँ?",
                "हैलो! मैं AI Vista का सहायक हूँ। मैं आपकी क्या मदद कर सकता हूँ?",
                "अभिवादन! मैं AI Vista Solutions से Shoaib हूँ। मैं आपकी कैसे मदद कर सकता हूँ?"
            ],
            'de': [
                "Hallo! Willkommen bei **AI Vista Solutions**. Wie kann ich Ihnen helfen?",
                "Guten Tag! Ich bin Ihr AI Vista-Assistent. Womit kann ich Ihnen helfen?",
                "Grüße! Ich bin Shoaib von AI Vista Solutions. Wie kann ich Ihnen helfen?"
            ]
        }
    },
  
    "bot_name": {
        "patterns": {
            'en': ["what is your name", "who are you", "your name", "what should I call you"],
            'ar': ["ما اسمك", "من أنت", "اسمك", "ماذا يجب أن أسميك"],
            'zh': ["你叫什么名字", "你是谁", "你的名字", "我应该怎么称呼你"],
            'ur': ["آپ کا نام کیا ہے", "آپ کون ہیں", "آپ کا نام", "میں آپ کو کیا کہوں"],
            'hi': ["तुम्हारा नाम क्या है", "तुम कौन हो", "तुम्हारा नाम", "मुझे तुम्हें क्या कहना चाहिए"],
            'de': ["wie heißt du", "wer bist du", "dein name", "wie soll ich dich nennen"]
        },
        "responses": {
            'en': [
                "I'm **Shoaib**, your virtual assistant from AI Vista Solutions!",
                "You can call me **Shoaib** - your friendly AI helper from AI Vista Solutions!",
                "I'm **Shoaib**, here to assist with all your tech queries."
            ],
            'ar': [
                "أنا **Shoaib**، مساعدك الافتراضي من AI Vista Solutions!",
                "يمكنك مناداتي **Shoaib** - مساعدك الودود من AI Vista Solutions!",
                "أنا **Shoaib**، هنا لمساعدتك في جميع استفساراتك التقنية."
            ],
            'zh': [
                "我是**Shoaib**，您的AI Vista Solutions虚拟助手！",
                "您可以叫我**Shoaib**——您来自AI Vista Solutions的友好AI助手！",
                "我是**Shoaib**，在这里帮助您解决所有技术问题。"
            ],
            'ur': [
                "میں **Shoaib** ہوں، AI Vista Solutions کا آپ کا ورچوئل اسسٹنٹ!",
                "آپ مجھے **Shoaib** کہہ سکتے ہیں - AI Vista Solutions کا آپ کا دوستانہ AI مددگار!",
                "میں **Shoaib** ہوں، آپ کے تمام ٹیکنالوجی کے سوالات میں مدد کے لیے حاضر ہوں۔"
            ],
            'hi': [
                "मैं **Shoaib** हूँ, AI Vista Solutions से आपका वर्चुअल सहायक!",
                "आप मुझे **Shoaib** कह सकते हैं - AI Vista Solutions से आपका मित्रवत AI सहायक!",
                "मैं **Shoaib** हूँ, आपके सभी तकनीकी प्रश्नों में सहायता के लिए यहां हूँ।"
            ],
            'de': [
                "Ich bin **Shoaib**, Ihr virtueller Assistent von AI Vista Solutions!",
                "Sie können mich **Shoaib** nennen - Ihr freundlicher KI-Helfer von AI Vista Solutions!",
                "Ich bin **Shoaib**, hier um Ihnen bei allen technischen Fragen zu helfen."
            ]
        }
    },
    "gratitude": {
        "patterns": {
            'en': ["thanks", "thank you", "appreciate it", "thanks a lot", "thank you very much", "thx"],
            'ar': ["شكرا", "شكرا لك", "أقدر ذلك", "شكرا جزيلا", "أشكرك كثيرا"],
            'zh': ["谢谢", "谢谢你", "感谢", "非常感谢", "太感谢了"],
            'ur': ["شکریہ", "آپ کا شکریہ", "تعریف", "بہت شکریہ", "آپ کا بہت شکریہ"],
            'hi': ["धन्यवाद", "शुक्रिया", "सराहना", "बहुत धन्यवाद", "आपका बहुत धन्यवाद"],
            'de': ["danke", "danke schön", "danke dir", "vielen dank", "herzlichen dank"]
        },
        "responses": {
            'en': [
                "You're welcome! Is there anything else I can help with?",
                "Happy to help! Let me know if you need anything else.",
                "No problem at all! Feel free to ask more questions.",
                "Glad I could assist! Don't hesitate to reach out if you have more questions."
            ],
            'ar': [
                "على الرحب والسعة! هل هناك أي شيء آخر يمكنني المساعدة به؟",
                "سعيد بمساعدتك! لا تتردد في إخباري إذا كنت بحاجة إلى أي شيء آخر.",
                "لا مشكلة على الإطلاق! لا تتردد في طرح المزيد من الأسئلة.",
                "سعيد لأنني استطعت المساعدة! لا تتردد في التواصل إذا كان لديك المزيد من الأسئلة."
            ],
            'zh': [
                "不客气！还有什么我可以帮忙的吗？",
                "很高兴能帮忙！如果您还有其他需要请告诉我。",
                "完全没问题！随时可以问更多问题。",
                "很高兴能帮助您！如果有更多问题请随时联系。"
            ],
            'ur': [
                "آپ کا استقبال ہے! کیا میں آپ کی کسی اور چیز میں مدد کر سکتا ہوں؟",
                "مدد کر کے خوشی ہوئی! اگر آپ کو کچھ اور چاہیے تو مجھے بتائیں۔",
                "کوئی مسئلہ نہیں! مزید سوالات پوچھنے میں آزاد محسوس کریں۔",
                "خوشی ہوئی کہ میں مدد کر سکا! اگر آپ کے مزید سوالات ہیں تو رابطہ کرنے میں ہچکچائیں نہیں۔"
            ],
            'hi': [
                "आपका स्वागत है! क्या मैं आपकी किसी और चीज़ में मदद कर सकता हूँ?",
                "मदद करके खुशी हुई! अगर आपको कुछ और चाहिए तो मुझे बताएं।",
                "कोई समस्या नहीं! और प्रश्न पूछने के लिए स्वतंत्र महसूस करें।",
                "खुशी हुई कि मैं सहायता कर सका! यदि आपके और प्रश्न हैं तो संपर्क करने में संकोच न करें।"
            ],
            'de': [
                "Gern geschehen! Kann ich Ihnen noch weiterhelfen?",
                "Freut mich zu helfen! Lassen Sie mich wissen, wenn Sie noch etwas brauchen.",
                "Kein Problem! Fühlen Sie sich frei, weitere Fragen zu stellen.",
                "Freut mich, dass ich helfen konnte! Zögern Sie nicht, sich bei weiteren Fragen zu melden."
            ]
        }
    },
    "services": {
        "patterns": {
            'en': ["what services do you offer", "what do you develop", "can you build a website", "what can you create", "tell me about your services", "services", "your services", "capabilities", "what do you do"],
            'ar': ["ما هي الخدمات التي تقدمها", "ماذا تطور", "هل يمكنك بناء موقع ويب", "ماذا يمكنك إنشاء", "أخبرني عن خدماتك", "خدمات", "خدماتك", "إمكانيات", "ماذا تفعل"],
            'zh': ["你们提供什么服务", "你们开发什么", "你能建网站吗", "你能创建什么", "告诉我你们的服务", "服务", "你们的服务", "能力", "你们做什么"],
            'ur': ["آپ کیا خدمات پیش کرتے ہیں", "آپ کیا تیار کرتے ہیں", "کیا آپ ایک ویب سائٹ بنا سکتے ہیں", "آپ کیا بنا سکتے ہیں", "مجھے اپنی خدمات کے بارے میں بتائیں", "خدمات", "آپ کی خدمات", "صلاحیتیں", "آپ کیا کرتے ہیں"],
            'hi': ["आप क्या सेवाएँ प्रदान करते हैं", "आप क्या विकसित करते हैं", "क्या आप एक वेबसाइट बना सकते हैं", "आप क्या बना सकते हैं", "मुझे अपनी सेवाओं के बारे में बताएं", "सेवाएँ", "आपकी सेवाएँ", "क्षमताएँ", "आप क्या करते हैं"],
            'de': ["welche dienstleistungen bieten sie an", "was entwickeln sie", "können sie eine website erstellen", "was können sie erstellen", "erzählen sie mir von ihren dienstleistungen", "dienstleistungen", "ihre dienstleistungen", "fähigkeiten", "was machen sie"]
        },
        "responses": {
            'en': """**Our Services**:
- **Web Development**: React, Angular, Django, Flask
- **Mobile Apps**: Flutter, React Native, Swift
- **AI/ML Solutions**: Custom models, Computer Vision, NLP
- **Cloud Services**: AWS, Azure, GCP deployment
- **DevOps & CI/CD**: Docker, Kubernetes, Terraform

*Let me know if you'd like details about any specific service!*""",
            'ar': """**خدماتنا**:
- **تطوير الويب**: React, Angular, Django, Flask
- **تطبيقات الجوال**: Flutter, React Native, Swift
- **حلول الذكاء الاصطناعي**: نماذج مخصصة، رؤية حاسوبية، معالجة اللغة الطبيعية
- **خدمات السحابة**: نشر على AWS، Azure، GCP
- **DevOps & CI/CD**: Docker، Kubernetes، Terraform

*أخبرني إذا كنت تريد تفاصيل عن أي خدمة محددة!*""",
            'zh': """**我们的服务**:
- **网页开发**: React, Angular, Django, Flask
- **移动应用**: Flutter, React Native, Swift
- **AI/ML解决方案**: 定制模型，计算机视觉，自然语言处理
- **云服务**: AWS, Azure, GCP部署
- **DevOps & CI/CD**: Docker, Kubernetes, Terraform

*如果您想了解任何特定服务的详细信息，请告诉我！*""",
            'ur': """**ہماری خدمات**:
- **ویب ڈویلپمنٹ**: React, Angular, Django, Flask
- **موبائل ایپس**: Flutter, React Native, Swift
- **AI/ML حل**: حسب ضرورت ماڈلز، کمپیوٹر ویژن، نیچرل لینگویج پروسیسنگ
- **کلاؤڈ خدمات**: AWS، Azure، GCP پر تعیناتی
- **DevOps & CI/CD**: Docker، Kubernetes، Terraform

*اگر آپ کسی مخصوص خدمت کے بارے میں تفصیلات چاہتے ہیں تو مجھے بتائیں!*""",
            'hi': """**हमारी सेवाएँ**:
- **वेब विकास**: React, Angular, Django, Flask
- **मोबाइल ऐप्स**: Flutter, React Native, Swift
- **AI/ML समाधान**: कस्टम मॉडल, कंप्यूटर विज़न, प्राकृतिक भाषा प्रसंस्करण
- **क्लाउड सेवाएँ**: AWS, Azure, GCP पर तैनाती
- **DevOps & CI/CD**: Docker, Kubernetes, Terraform

*यदि आप किसी विशिष्ट सेवा के बारे में विवरण चाहते हैं तो मुझे बताएं!*""",
            'de': """**Unsere Dienstleistungen**:
- **Webentwicklung**: React, Angular, Django, Flask
- **Mobile Apps**: Flutter, React Native, Swift
- **KI/ML-Lösungen**: Benutzerdefinierte Modelle, Computer Vision, NLP
- **Cloud-Services**: Bereitstellung auf AWS, Azure, GCP
- **DevOps & CI/CD**: Docker, Kubernetes, Terraform

*Lassen Sie mich wissen, wenn Sie Details zu einem bestimmten Service wünschen!*"""
        }
    },
    "pricing": {
        "patterns": {
            'en': ["how much does a website cost", "what are your rates", "pricing", "how much do you charge", "cost", "budget", "price"],
            'ar': ["كم يكلف موقع الويب", "ما هي أسعارك", "التسعير", "كم تطلب", "التكلفة", "الميزانية", "السعر"],
            'zh': ["建一个网站要多少钱", "你们的费率是多少", "定价", "你们收费多少", "成本", "预算", "价格"],
            'ur': ["ایک ویب سائٹ کی قیمت کتنی ہے", "آپ کی قیمتیں کیا ہیں", "قیمتوں کا تعین", "آپ کتنا چارج کرتے ہیں", "لاگت", "بجٹ", "قیمت"],
            'hi': ["एक वेबसाइट की लागत कितनी है", "आपकी दरें क्या हैं", "मूल्य निर्धारण", "आप कितना शुल्क लेते हैं", "लागत", "बजट", "मूल्य"],
            'de': ["wie viel kostet eine website", "was sind ihre preise", "preisgestaltung", "wie viel berechnen sie", "kosten", "budget", "preis"]
        },
        "responses": {
            'en': """**Pricing Structure**:
- Basic Website: $1,000 - $5,000
- Custom Web App: $5,000 - $50,000+
- Mobile App: $10,000 - $100,000
- Enterprise Solutions: Custom pricing
- *All projects include free initial consultation*""",
            'ar': """**هيكل التسعير**:
- موقع ويب أساسي: 1,000 - 5,000 دولار
- تطبيق ويب مخصص: 5,000 - 50,000+ دولار
- تطبيق جوال: 10,000 - 100,000 دولار
- حلول المؤسسات: تسعير مخصص
- *جميع المشاريع تشمل استشارة أولية مجانية*""",
            'zh': """**定价结构**:
- 基础网站: 1,000 - 5,000美元
- 定制Web应用: 5,000 - 50,000+美元
- 移动应用: 10,000 - 100,000美元
- 企业解决方案: 定制定价
- *所有项目包括免费初步咨询*""",
            'ur': """**قیمتوں کا ڈھانچہ**:
- بنیادی ویب سائٹ: $1,000 - $5,000
- حسب ضرورت ویب ایپ: $5,000 - $50,000+
- موبائل ایپ: $10,000 - $100,000
- انٹرپرائز حل: حسب ضرورت قیمت
- *تمام منصوبوں میں مفت ابتدائی مشاورت شامل ہے*""",
            'hi': """**मूल्य निर्धारण संरचना**:
- बेसिक वेबसाइट: $1,000 - $5,000
- कस्टम वेब ऐप: $5,000 - $50,000+
- मोबाइल ऐप: $10,000 - $100,000
- एंटरप्राइज़ समाधान: कस्टम मूल्य निर्धारण
- *सभी परियोजनाओं में मुफ्त प्रारंभिक परामर्श शामिल है*""",
            'de': """**Preisstruktur**:
- Einfache Website: $1.000 - $5.000
- Individuelle Webanwendung: $5.000 - $50.000+
- Mobile App: $10.000 - $100.000
- Enterprise-Lösungen: Individuelle Preisgestaltung
- *Alle Projekte beinhalten eine kostenlose Erstberatung*"""
        }
    },
    "portfolio": {
        "patterns": {
            'en': ["show me your projects", "portfolio", "past work", "examples", "case studies"],
            'ar': ["أرني مشاريعك", "محفظة الأعمال", "أعمال سابقة", "أمثلة", "دراسات حالة"],
            'zh': ["给我看看你们的项目", "作品集", "过去的工作", "例子", "案例研究"],
            'ur': ["مجھے اپنے منصوبے دکھائیں", "پورٹ فولیو", "پچھلے کام", "مثالیں", "کیس اسٹڈیز"],
            'hi': ["मुझे अपने प्रोजेक्ट दिखाओ", "पोर्टफोलियो", "पिछला काम", "उदाहरण", "केस स्टडी"],
            'de': ["zeigen sie mir ihre projekte", "portfolio", "bisherige arbeiten", "beispiele", "fallstudien"]
        },
        "responses": {
            'en': [
                "You can explore our portfolio here: [AI Vista Solutions Projects](https://aivistasolutions.com/projects)",
                "Check out our recent work: [Our Portfolio](https://aivistasolutions.com/portfolio)"
            ],
            'ar': [
                "يمكنك استكشاف أعمالنا هنا: [مشاريع AI Vista Solutions](https://aivistasolutions.com/projects)",
                "اطلع على أعمالنا الحديثة: [محفظة أعمالنا](https://aivistasolutions.com/portfolio)"
            ],
            'zh': [
                "您可以在这里查看我们的作品集: [AI Vista Solutions项目](https://aivistasolutions.com/projects)",
                "查看我们最近的工作: [我们的作品集](https://aivistasolutions.com/portfolio)"
            ],
            'ur': [
                "آپ ہمارا پورٹ فولیو یہاں دیکھ سکتے ہیں: [AI Vista Solutions کے منصوبے](https://aivistasolutions.com/projects)",
                "ہمارے حالیہ کام دیکھیں: [ہمارا پورٹ فولیو](https://aivistasolutions.com/portfolio)"
            ],
            'hi': [
                "आप हमारा पोर्टफोलियो यहां देख सकते हैं: [AI Vista Solutions परियोजनाएँ](https://aivistasolutions.com/projects)",
                "हमारा हालिया काम देखें: [हमारा पोर्टफोलियो](https://aivistasolutions.com/portfolio)"
            ],
            'de': [
                "Sie können unser Portfolio hier einsehen: [AI Vista Solutions Projekte](https://aivistasolutions.com/projects)",
                "Sehen Sie sich unsere aktuellen Arbeiten an: [Unser Portfolio](https://aivistasolutions.com/portfolio)"
            ]
        }
    },
    "contact": {
        "patterns": {
            'en': ["how to contact you", "email", "phone number", "get in touch", "contact no", "reach you", "contact details"],
            'ar': ["كيفية الاتصال بك", "البريد الإلكتروني", "رقم الهاتف", "تواصل معنا", "رقم الاتصال", "الوصول إليك", "تفاصيل الاتصال"],
            'zh': ["如何联系你们", "电子邮件", "电话号码", "取得联系", "联系电话", "联系你们", "联系方式"],
            'ur': ["آپ سے کیسے رابطہ کریں", "ای میل", "فون نمبر", "رابطہ کریں", "رابطہ نمبر", "آپ تک پہنچیں", "رابطہ کی تفصیلات"],
            'hi': ["आपसे कैसे संपर्क करें", "ईमेल", "फोन नंबर", "संपर्क करें", "संपर्क नंबर", "आप तक पहुंचें", "संपर्क विवरण"],
            'de': ["wie kann ich sie kontaktieren", "e-mail", "telefonnummer", "kontakt aufnehmen", "kontaktnummer", "sie erreichen", "kontaktdaten"]
        },
        "responses": {
            'en': """**Contact Us**:
 Email: contact@aivistasolutions.com  
 Phone: +92 345 1678312  
 Address: DHA Phase 9, Lahore, Pakistan  
 Website: [aivistasolutions.com](https://aivistasolutions.com)""",
            'ar': """**اتصل بنا**:
 البريد الإلكتروني: contact@aivistasolutions.com  
 الهاتف: +92 345 1678312  
 العنوان: DHA المرحلة 9، لاهور، باكستان  
 الموقع: [aivistasolutions.com](https://aivistasolutions.com)""",
            'zh': """**联系我们**:
 电子邮件: contact@aivistasolutions.com  
 电话: +92 345 1678312  
 地址: 巴基斯坦拉合尔DHA第9阶段  
 网站: [aivistasolutions.com](https://aivistasolutions.com)""",
            'ur': """**ہم سے رابطہ کریں**:
 ای میل: contact@aivistasolutions.com  
 فون: +92 345 1678312  
 پتہ: DHA فیز 9، لاہور، پاکستان  
 ویب سائٹ: [aivistasolutions.com](https://aivistasolutions.com)""",
            'hi': """**हमसे संपर्क करें**:
 ईमेल: contact@aivistasolutions.com  
 फोन: +92 345 1678312  
 पता: DHA चरण 9, लाहौर, पाकिस्तान  
 वेबसाइट: [aivistasolutions.com](https://aivistasolutions.com)""",
            'de': """**Kontaktieren Sie uns**:
 E-Mail: contact@aivistasolutions.com  
 Telefon: +92 345 1678312  
 Adresse: DHA Phase 9, Lahore, Pakistan  
 Website: [aivistasolutions.com](https://aivistasolutions.com)"""
        }
    },
    "hiring": {
        "patterns": {
            'en': ["are you hiring", "job openings", "how to apply", "careers", "we need developers", "hiring", "jobs", "vacancies"],
            'ar': ["هل توظفون", "وظائف شاغرة", "كيفية التقديم", "وظائف", "نحتاج مطورين", "توظيف", "وظائف", "شواغر"],
            'zh': ["你们在招聘吗", "职位空缺", "如何申请", "职业", "我们需要开发人员", "招聘", "工作", "空缺"],
            'ur': ["کیا آپ نوکریاں دے رہے ہیں", "ملازمت کے مواقع", "کیسے درخواست دیں", "کیریئرز", "ہمیں ڈویلپرز کی ضرورت ہے", "نوکریاں", "ملازمتیں", "خالی جگہیں"],
            'hi': ["क्या आप भर्ती कर रहे हैं", "नौकरी के अवसर", "आवेदन कैसे करें", "करियर", "हमें डेवलपर्स की आवश्यकता है", "भर्ती", "नौकरियां", "रिक्तियां"],
            'de': ["stellen sie ein", "offene stellen", "wie bewerbe ich mich", "karriere", "wir brauchen entwickler", "einstellung", "jobs", "stellenangebote"]
        },
        "responses": {
            'en': """**Current Openings**:
1. Senior Python Developer (Remote)
2. Frontend Engineer (React)
3. DevOps Specialist
4. AI/ML Engineer

 Apply at: [AI Vista Solutions Careers](https://aivistasolutions.com/careers)  
*We offer competitive salaries and flexible work arrangements!*""",
            'ar': """**الوظائف الشاغرة الحالية**:
1. مطور بايثون كبير (عن بعد)
2. مهندس واجهة أمامية (React)
3. أخصائي DevOps
4. مهندس ذكاء اصطناعي/تعلم آلي

 تقدم هنا: [وظائف AI Vista Solutions](https://aivistasolutions.com/careers)  
*نقدم رواتب تنافسية وترتيبات عمل مرنة!*""",
            'zh': """**当前职位空缺**:
1. 高级Python开发人员(远程)
2. 前端工程师(React)
3. DevOps专家
4. AI/ML工程师

 申请地址: [AI Vista Solutions职业](https://aivistasolutions.com/careers)  
*我们提供有竞争力的薪资和灵活的工作安排!*""",
            'ur': """**موجودہ خالی ملازمت**:
1. سینئر پائتھن ڈویلپر (ریموٹ)
2. فرنٹ اینڈ انجینئر (React)
3. DevOps سپیشلسٹ
4. AI/ML انجینئر

 درخواست دیں: [AI Vista Solutions کیریئرز](https://aivistasolutions.com/careers)  
*ہم مسابقتی تنخواہیں اور لچکدار کام کے انتظامات پیش کرتے ہیں!*""",
            'hi': """**वर्तमान रिक्तियां**:
1. वरिष्ठ पायथन डेवलपर (रिमोट)
2. फ्रंटएंड इंजीनियर (React)
3. DevOps विशेषज्ञ
4. AI/ML इंजीनियर

 आवेदन करें: [AI Vista Solutions करियर](https://aivistasolutions.com/careers)  
*हम प्रतिस्पर्धी वेतन और लचीले कार्य व्यवस्था प्रदान करते हैं!*""",
            'de': """**Aktuelle Stellenangebote**:
1. Senior Python Entwickler (Remote)
2. Frontend Ingenieur (React)
3. DevOps Spezialist
4. KI/ML Ingenieur

 Bewerben Sie sich unter: [AI Vista Solutions Karriere](https://aivistasolutions.com/careers)  
*Wir bieten wettbewerbsfähige Gehälter und flexible Arbeitsregelungen!*"""
        }
    },
    "timeline": {
        "patterns": {
            'en': ["how long does a project take", "project duration", "delivery time", "when will it be ready", "timeline", "deadline"],
            'ar': ["كم من الوقت يستغرق المشروع", "مدة المشروع", "وقت التسليم", "متى سيكون جاهزًا", "الجدول الزمني", "الموعد النهائي"],
            'zh': ["项目需要多长时间", "项目持续时间", "交付时间", "什么时候能完成", "时间表", "截止日期"],
            'ur': ["منصوبے میں کتنا وقت لگتا ہے", "منصوبے کی مدت", "ترسیل کا وقت", "یہ کب تیار ہوگا", "ٹائم لائن", "آخری تاریخ"],
            'hi': ["एक परियोजना में कितना समय लगता है", "परियोजना अवधि", "वितरण समय", "यह कब तैयार होगा", "समयरेखा", "अंतिम तिथि"],
            'de': ["wie lange dauert ein projekt", "projektdauer", "lieferzeit", "wann wird es fertig sein", "zeitplan", "frist"]
        },
        "responses": {
            'en': """**Typical Timelines**:
- MVP Development: 2-3 months
- Enterprise Solution: 6-12 months
- Website: 4-8 weeks
- Mobile App: 3-6 months

*Exact timeline depends on project complexity*""",
            'ar': """**المواعيد النموذجية**:
- تطوير MVP: 2-3 أشهر
- حل المؤسسات: 6-12 شهرًا
- موقع الويب: 4-8 أسابيع
- تطبيق الجوال: 3-6 أشهر

*الجدول الزمني الدقيق يعتمد على تعقيد المشروع*""",
            'zh': """**典型时间表**:
- MVP开发: 2-3个月
- 企业解决方案: 6-12个月
- 网站: 4-8周
- 移动应用: 3-6个月

*确切时间表取决于项目复杂性*""",
            'ur': """**عام ٹائم لائنز**:
- MVP ڈویلپمنٹ: 2-3 ماہ
- انٹرپرائز حل: 6-12 ماہ
- ویب سائٹ: 4-8 ہفتے
- موبائل ایپ: 3-6 ماہ

*عین ٹائم لائن منصوبے کی پیچیدگی پر منحصر ہے*""",
            'hi': """**विशिष्ट समयरेखा**:
- MVP विकास: 2-3 महीने
- एंटरप्राइज़ समाधान: 6-12 महीने
- वेबसाइट: 4-8 सप्ताह
- मोबाइल ऐप: 3-6 महीने

*सटीक समयरेखा परियोजना की जटिलता पर निर्भर करती है*""",
            'de': """**Typische Zeitpläne**:
- MVP-Entwicklung: 2-3 Monate
- Enterprise-Lösung: 6-12 Monate
- Website: 4-8 Wochen
- Mobile App: 3-6 Monate

*Genauer Zeitplan hängt von der Projektkomplexität ab*"""
        }
    },
"location": {
    "patterns": {
        'en': ["where are you located", "address", "location", "your office", "Software location", "based in", "headquarters"],
        'ar': ["أين تقعون", "ما هو عنوانكم", "موقعكم", "مكتبكم", "موقع البرنامج", "مقر الشركة"],
        'zh': ["你们在哪里", "地址", "位置", "你们的办公室", "软件位置", "总部"],
        'ur': ["آپ کہاں واقع ہیں", "پتہ", "مقام", "آپ کا دفتر", "سافٹ ویئر کا مقام", "ہیڈکوارٹر"],
        'hi': ["आप कहाँ स्थित हैं", "पता", "स्थान", "आपका कार्यालय", "सॉफ़्टवेयर स्थान", "मुख्यालय"],
        'de': ["wo befinden sie sich", "adresse", "standort", "ihr büro", "softwarestandort", "hauptsitz"]
    },
    "responses": {
        'en': """**Our Locations**:
- **HQ**: Lahore, Pakistan  
- **Development Center**: DHA Phase 9, Lahore  
- **Global Presence**: USA, Germany, UAE""",
        'ar': """**موقعنا**:
- **المقر الرئيسي**: لاهور، باكستان  
- **مركز التطوير**: DHA المرحلة 9، لاهور  
- **وجود عالمي**: الولايات المتحدة الأمريكية، ألمانيا، الإمارات العربية المتحدة""",
        'zh': """**我们的地址**:
- **总部**: 巴基斯坦拉合尔  
- **开发中心**: 拉合尔DHA第9阶段  
- **全球业务**: 美国，德国，阿联酋""",
        'ur': """**ہمارا مقام**:
- **ہیڈکوارٹر**: لاہور، پاکستان  
- **ڈویلپمنٹ سینٹر**: DHA فیز 9، لاہور  
- **عالمی موجودگی**: امریکہ، جرمنی، متحدہ عرب امارات""",
        'hi': """**हमारा स्थान**:
- **मुख्यालय**: लाहौर, पाकिस्तान  
- **विकास केंद्र**: DHA फेज़ 9, लाहौर  
- **वैश्विक उपस्थिति**: यूएसए, जर्मनी, UAE""",
        'de': """**Unser Standort**:
- **Hauptsitz**: Lahore, Pakistan  
- **Entwicklungszentrum**: DHA Phase 9, Lahore  
- **Globale Präsenz**: USA, Deutschland, VAE"""
    }
},
"technology": {
    "patterns": {
        'en': ["what tech do you use", "technology stack", "programming languages", "frameworks", "tech stack", "tools"],
        'ar': ["ما هي التقنيات التي تستخدمها", "مجموعة التكنولوجيا", "لغات البرمجة", "الأطر", "مجموعة الأدوات"],
        'zh': ["你们使用什么技术", "技术栈", "编程语言", "框架", "技术工具"],
        'ur': ["آپ کون سی ٹیکنالوجیز استعمال کرتے ہیں", "ٹیکنالوجی اسٹیک", "پروگرامنگ زبانیں", "فریم ورک", "ٹولز"],
        'hi': ["आप कौन सी तकनीक का उपयोग करते हैं", "प्रौद्योगिकी स्टैक", "प्रोग्रामिंग भाषाएँ", "फ्रेमवर्क", "उपकरण"],
        'de': ["welche technologie verwenden sie", "technologie-stack", "programmiersprachen", "frameworks", "tools"]
    },
    "responses": {
        'en': """**Our Tech Stack**:
        Frontend-->React
        Frontend-->Angular
        Backend-->Python
        Backend-->Node.js
        Database-->PostgreSQL
        Database-->MongoDB
        DevOps-->AWS
        DevOps-->Docker""",
        'ar': """**مجموعة تقنياتنا**:
        الواجهة الأمامية-->React
        الواجهة الأمامية-->Angular
        الخلفية-->Python
        الخلفية-->Node.js
        قاعدة البيانات-->PostgreSQL
        قاعدة البيانات-->MongoDB
        DevOps-->AWS
        DevOps-->Docker""",
        'zh': """**我们的技术栈**:
        前端-->React
        前端-->Angular
        后端-->Python
        后端-->Node.js
        数据库-->PostgreSQL
        数据库-->MongoDB
        DevOps-->AWS
        DevOps-->Docker""",
        'ur': """**ہماری ٹیکنالوجی اسٹیک**:
        فرنٹ اینڈ-->React
        فرنٹ اینڈ-->Angular
        بیک اینڈ-->Python
        بیک اینڈ-->Node.js
        ڈیٹا بیس-->PostgreSQL
        ڈیٹا بیس-->MongoDB
        DevOps-->AWS
        DevOps-->Docker""",
        'hi': """**हमारा तकनीकी स्टैक**:
        फ्रंटेंड-->React
        फ्रंटेंड-->Angular
        बैकेंड-->Python
        बैकेंड-->Node.js
        डाटाबेस-->PostgreSQL
        डाटाबेस-->MongoDB
        DevOps-->AWS
        DevOps-->Docker""",
        'de': """**Unser Tech-Stack**:
        Frontend-->React
        Frontend-->Angular
        Backend-->Python
        Backend-->Node.js
        Datenbank-->PostgreSQL
        Datenbank-->MongoDB
        DevOps-->AWS
        DevOps-->Docker"""
    }
},

"about": {
    "patterns": {
        'en': ["about", "company", "history", "who are you", "background"],
        'ar': ["عن", "شركة", "تاريخ", "من أنتم", "خلفية"],
        'zh': ["关于", "公司", "历史", "你们是谁", "背景"],
        'ur': ["کے بارے میں", "کمپنی", "تاریخ", "آپ کون ہیں", "پس منظر"],
        'hi': ["के बारे में", "कंपनी", "इतिहास", "आप कौन हैं", "पृष्ठभूमि"],
        'de': ["über", "unternehmen", "geschichte", "wer sind sie", "hintergrund"]
    },
    "responses": {
        'en': """**About AI Vista Solutions**:
- Founded in 2015  
- 50+ technology experts  
- 200+ successful projects delivered  
- Serving clients in 15+ countries

**Why Choose Us?**:
- 95% client retention rate  
- Agile development approach  
- Dedicated project managers""",
        'ar': """**عن AI Vista Solutions**:
- تأسست في 2015  
- أكثر من 50 خبيرًا في التكنولوجيا  
- تم تسليم أكثر من 200 مشروع بنجاح  
- نقدم خدماتنا للعملاء في أكثر من 15 دولة

**لماذا تختارنا؟**:
- معدل الاحتفاظ بالعملاء 95%  
- نهج تطوير مرن  
- مدراء مشاريع مخصصون""",
        'zh': """**关于 AI Vista Solutions**:
- 成立于2015年  
- 拥有50+技术专家  
- 交付了200+成功项目  
- 为15+个国家的客户提供服务

**为什么选择我们？**:
- 95%的客户保持率  
- 敏捷开发方法  
- 专门的项目经理""",
        'ur': """**AI Vista Solutions کے بارے میں**:
- 2015 میں قائم ہوا  
- 50+ ٹیکنالوجی ماہرین  
- 200+ کامیاب پروجیکٹس مکمل کیے  
- 15+ ممالک میں کلائنٹس کی خدمت

**کیوں ہمیں منتخب کریں؟**:
- 95% کلائنٹ برقرار رکھنے کی شرح  
- ایجائل ڈویلپمنٹ طریقہ کار  
- مخصوص پروجیکٹ مینیجرز""",
        'hi': """**AI Vista Solutions के बारे में**:
- 2015 में स्थापित  
- 50+ तकनीकी विशेषज्ञ  
- 200+ सफल परियोजनाएँ डिलीवर कीं  
- 15+ देशों में ग्राहकों को सेवा दे रहे हैं

**हमें क्यों चुनें?**:
- 95% ग्राहक बनाए रखने की दर  
- एजाइल विकास दृष्टिकोण  
- समर्पित परियोजना प्रबंधक""",
        'de': """**Über AI Vista Solutions**:
- Gegründet 2015  
- 50+ Technologieexperten  
- 200+ erfolgreiche Projekte geliefert  
- Serviert Kunden in über 15 Ländern

**Warum uns wählen?**:
- 95% Kundenbindungsrate  
- Agiler Entwicklungsansatz  
- Dedizierte Projektmanager"""
    }
},
  
    "default": {
        "responses": {
            'en': ["I'm not sure I understand. Could you rephrase that?"],
            'ar': ["أنا لست متأكدًا من فهمي. هل يمكنك إعادة صياغة ذلك؟"],
            'zh': ["我不太明白。您能换种说法吗？"],
            'ur': ["مجھے سمجھ نہیں آیا۔ کیا آپ اسے دوبارہ کہہ سکتے ہیں؟"],
            'hi': ["मुझे समझ नहीं आया। क्या आप इसे दोबारा कह सकते हैं?"],
            'de': ["Ich bin mir nicht sicher, ob ich das verstehe. Könnten Sie das anders formulieren?"]
        }
    }
}

def detect_language(text):
    try:
        
        if any('\u0900' <= char <= '\u097F' for char in text):  
            return 'hi'
        if any('\u0600' <= char <= '\u06FF' for char in text):  
            
            urdu_keywords = ["ہے", "کی", "کے", "ہیں", "میں", "سلام", "ہیلو", "آداب", "ترسیل کا وقت", 
                             "یہ کب تیار ہوگا", "ٹائم لائن", "آخری تاریخ", "فون", "ای میل", 
                             "رابطہ", "صبح بخیر", "ہمیں", "ہماری", "ہمارے", "کام", "پروڈکٹ", 
                             "سروسز", "پیشکشیں", "ملازمتیں", "نوکریاں", "خالی جگہیں", "پس منظر", "کمپنی",
                             "پروگرامنگ زبانیں", "فریم ورک", "ٹولز", "پتہ", "مقام", "آپ کا دفتر", "سافٹ ویئر کا مقام",
                             "ہیڈکوارٹر", "آخری تاریخ", "صلاحیتیں", "لاگت", "بجٹ", "قیمت", "آپ کا نام", "شکریہ", "آپ کا شکریہ", 
                             "تعریف", "بہت شکریہ", "آپ کا بہت شکریہ"]
            if any(keyword in text for keyword in urdu_keywords):
                return 'ur'
            return 'ar'
        if any('\u4e00' <= char <= '\u9fff' for char in text):  
            return 'zh'
            
        
        german_keywords = ["hallo", "guten", "tag", "morgen", "abend", "danke", "bitte", 
                          "kontakt", "telefonnummer", "e-mail", "wie", "kann", "ich", "sie", 
                          "helfen", "frage", "problem", "adresse", "website", "unternehmen",
                          "fallstudien","über","hintergrund","technologie-stack", "programmiersprachen",
                          "standort", "ihr büro", "softwarestandort", "hauptsitz",
                          "stellen sie ein", "offene stellen", "wie bewerbe ich mich", "karriere", "wir brauchen entwickler", "einstellung",
                          "zeigen sie mir ihre projekte", "portfolio", "bisherige arbeiten", "beispiele", "fallstudien",
                          "danke", "danke schön", "danke dir", "vielen dank", "herzlichen dank",
                          "projektdauer", "lieferzeit", "wann wird es fertig sein", "zeitplan", "frist","stellenangebote",
                           "preisgestaltung", "kosten", "preis","dienstleistungen", "ihre dienstleistungen", "fähigkeiten", 
                           "was machen sie","wer bist du", "dein name",]
        if any(keyword in text.lower() for keyword in german_keywords):
            return 'de'
        return 'en'
            
       
        lang = detect(text)
        if lang in SUPPORTED_LANGUAGES:
            return lang
            
    except:
        pass
    return 'en'  

def preprocess_text(text, lang='en'):
    text = text.lower().strip()
    
    if lang == 'zh':
        return re.sub(r'[^\w\u4e00-\u9fff]', '', text)
    elif lang in ['ar', 'ur']:  # Handle both Arabic and Urdu
        return re.sub(r'[^\w\s\u0600-\u06FF]', '', text)
    elif lang == 'hi':
        return re.sub(r'[^\w\s\u0900-\u097F]', '', text)
    elif lang == 'de':
      
        return re.sub(r'[^\w\säöüß]', '', text)
    else:
        return re.sub(r'[^\w\s]', '', text)

def detect_intent(user_input, lang='en'):
    processed_input = preprocess_text(user_input, lang)
    
   
    for intent, data in RULES.items():
        if intent == "default":
            continue
            
        patterns = data.get("patterns", {}).get(lang, [])
        if isinstance(patterns, str):
            patterns = [patterns]
            
        for pattern in patterns:
            if pattern.lower() == processed_input:
                return intent
    
  
    for intent, data in RULES.items():
        if intent == "default":
            continue
            
        patterns = data.get("patterns", {}).get(lang, [])
        if isinstance(patterns, str):
            patterns = [patterns]
            
        for pattern in patterns:
            if pattern.lower() in processed_input:
                return intent
                
    return "default"

def get_response(intent, lang='en'):
    try:
        responses = RULES.get(intent, {}).get("responses", {}).get(lang, [])
        
        if not responses and lang != 'en':
            responses = RULES.get(intent, {}).get("responses", {}).get('en', [])
        
        if isinstance(responses, list):
            return random.choice(responses) if responses else RULES["default"]["responses"][lang][0]
        return responses if responses else RULES["default"]["responses"][lang][0]
    except:
        return RULES["default"]["responses"].get(lang, ["I'm not sure I understand. Could you rephrase that?"])[0]

def main():
    st.set_page_config(
        page_title="AI Vista Solutions Assistant",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    st.markdown(
    """
    <h2 style='text-align: center; color: #4B8BBE; font-family: "Georgia", serif;'>
         Created by <strong>Muhammad Shoaib Sattar</strong>
    </h2>
    """,
    unsafe_allow_html=True
        )

    

    st.title("AI Vista Solutions Assistant")
    st.markdown("Ask about our services of Software Company in English, Arabic, Chinese, Urdu, Hindi, or German")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm Your AI Vista Solutions Assistant. How can I help you today?", "lang": "en"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else None):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your question here...")
    if user_input:
        detected_lang = detect_language(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input, "lang": detected_lang})
        
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Thinking..."):
            time.sleep(0.3)
            try:
                intent = detect_intent(user_input, detected_lang)
                response = get_response(intent, detected_lang)
            except Exception as e:
                st.error(f"System error: {str(e)}")
                response = get_response("default", detected_lang)

        st.session_state.messages.append({"role": "assistant", "content": response, "lang": detected_lang})
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(response)

if __name__ == "__main__":
    main()
