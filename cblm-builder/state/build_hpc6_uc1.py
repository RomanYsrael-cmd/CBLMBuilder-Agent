import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "state" / "payloads" / "HPC6_uc1_payload.json"


def wc(text: str) -> int:
    return len(text.split())


def key_facts(entry: dict) -> str:
    variant = entry["variant"]
    title = entry["title"]
    subtopics = ", ".join(entry["subtopics"])
    context = entry["context"]
    example = entry["example"]
    workplace = entry["workplace"]
    caution = entry["caution"]
    reinforcement = entry["reinforcement"]

    p1a = (
        f"{title} is a foundational content area for learners who need to use French with confidence in daily life and in simple workplace interactions. "
        f"In this lesson, the trainee studies {subtopics}, which together form the first layer of practical language use. "
        f"The aim is not only to memorize isolated expressions, but to understand when a phrase is appropriate, how tone changes meaning, and how pronunciation supports clarity. "
        f"When a learner can select the correct expression at the correct moment, communication becomes smoother and more respectful. "
        f"This matters in a competency-based module because greetings, polite exchanges, and short responses are often the first evidence that a learner can function in a real social or work setting. "
        f"A strong start in {title.lower()} also helps the trainee become less hesitant when speaking, because routine expressions reduce anxiety and create a predictable communication pattern."
    )
    p1b = (
        f"In the context of {title.lower()}, the learner develops control over {subtopics}. "
        f"These are not random vocabulary items. They are high-frequency expressions used when opening a conversation, responding politely, and keeping communication clear in ordinary situations. "
        f"A TESDA-style learner should recognize that language competence begins with repeated functional use. "
        f"When the trainee practices these forms aloud, notices pronunciation, and observes the social purpose of each expression, French becomes a usable tool rather than a purely academic subject. "
        f"This content therefore supports confidence, courtesy, and readiness for routine interactions in school, training, customer-facing tasks, and introductory workplace communication."
    )
    p1c = (
        f"Learners encounter {title.lower()} very early because it gives structure to real conversation. "
        f"The subtopics {subtopics} help the trainee move from silence to participation by offering ready language for starting, sustaining, and closing simple exchanges. "
        f"In competency-based learning, this content is valuable because it produces observable behavior: the learner can greet, introduce, ask, respond, and acknowledge another person in French. "
        f"Instead of treating phrases as disconnected samples, the trainee studies purpose, register, and pronunciation so that each expression matches the situation. "
        f"This makes early French communication practical, respectful, and easier to transfer into authentic daily and workplace settings."
    )

    p2a = (
        f"A detailed understanding of this content requires attention to meaning, structure, and use. {context} "
        f"The learner should notice how French expressions may change according to singular or plural form, level of familiarity, gender agreement, or the setting where the expression is spoken. "
        f"For example, a phrase used with a friend may not be the best choice when addressing a supervisor, guest, or unfamiliar coworker. "
        f"Accurate pronunciation also matters because even a familiar expression can sound unclear if stress, liaison, or vowel quality is ignored. "
        f"Practice should therefore include listening, repetition, guided role play, and short oral drills. "
        f"The trainee must connect language choice to purpose: greeting, requesting, apologizing, introducing, clarifying, or responding. "
        f"Once these functions are understood, the learner can use short French exchanges more naturally and with fewer pauses."
    )
    p2b = (
        f"Mastery grows when the trainee looks beyond translation and studies how the expressions operate in context. {context} "
        f"French communication depends on choosing expressions that fit the relationship between speakers and the purpose of the exchange. "
        f"A learner should observe whether the phrase signals courtesy, friendliness, formality, or a need for clarification. "
        f"Pronunciation drills, substitution exercises, and paired speaking tasks help transform vocabulary into active skill. "
        f"The learner also benefits from noticing patterns such as agreement, article use, and standard formulae that appear repeatedly in beginner conversation. "
        f"When these patterns are recognized, the trainee gains greater speed and accuracy, which is essential in face-to-face situations where there is little time to plan every sentence."
    )
    p2c = (
        f"To understand the lesson deeply, the learner must examine both the language forms and the communication purpose behind them. {context} "
        f"In French, even short expressions carry signals about politeness, social distance, and confidence. "
        f"A trainee should practice the expressions in complete mini-dialogues rather than as isolated lines, because real communication involves turn-taking and response. "
        f"Attention should also be given to pronunciation, especially sounds that distinguish one expression from another and help the listener interpret the message correctly. "
        f"Through repeated speaking activities, the learner begins to select phrases more automatically, which is important for routine work interactions, public contact, and daily conversation."
    )

    p3 = (
        f"A realistic example helps make the content concrete. {example} "
        f"This example shows that language learning is not limited to reciting words from memory. "
        f"The speaker must choose expressions that match the time of day, the relationship between people, and the intention of the conversation. "
        f"If the trainee changes one expression, the whole tone of the interaction may shift from warm to abrupt or from respectful to too casual. "
        f"That is why practice activities should include short situational dialogues, peer feedback, and correction of pronunciation and word choice. "
        f"When the learner repeats similar situations with small variations, the expressions become easier to retrieve in real communication."
    )

    p4 = (
        f"In workplace application, {workplace} "
        f"Employees who handle front-desk tasks, coordination work, visitor assistance, or simple customer support often need dependable expressions more than long speeches. "
        f"A worker who can open a conversation politely, identify people and roles, respond courteously, and describe basic information creates a more professional impression. "
        f"This is especially important in multilingual environments where short, accurate French exchanges may support service quality and teamwork. "
        f"The trainee should therefore practice the content with role plays that simulate office encounters, reception interactions, colleague introductions, and routine requests. "
        f"Common errors must also be monitored. {caution} "
        f"Correcting these issues early helps the learner avoid habits that weaken communication."
    )

    p5 = (
        f"In summary, {reinforcement} "
        f"The trainee should leave this lesson able to recognize the purpose of the target expressions, pronounce them with reasonable clarity, and use them in context-appropriate ways. "
        f"Competence is shown when the learner can transfer the language from classroom drills to short authentic interactions without depending fully on a script. "
        f"Regular practice, listening exposure, and guided speaking tasks will strengthen retention. "
        f"As the learner progresses to more complex French tasks, this content remains important because it provides the practical building blocks for workplace readiness, cultural courtesy, and confident beginner communication."
    )

    paragraphs = {
        "A": [p1a, p2a, p3, p4, p5],
        "B": [p1b, p2b, p3, p4, p5],
        "C": [p1c, p2c, p3, p4, p5],
    }[variant]
    text = "\n\n".join(paragraphs)
    assert wc(text) >= 600, f"{title} Key Facts too short: {wc(text)} words"
    return text


def mcq_block(items: list[dict]) -> tuple[str, str]:
    questions = []
    answers = []
    for idx, item in enumerate(items, start=1):
        opts = item["options"]
        questions.append(
            f"{idx}. {item['q']}\n"
            f"A. {opts[0]}\n"
            f"B. {opts[1]}\n"
            f"C. {opts[2]}\n"
            f"D. {opts[3]}"
        )
        answers.append(f"{idx}. {item['answer']}")
    return "\n\n".join(questions), "\n".join(answers)


content_entries = [
    {
        "field": "1_1",
        "title": "Greetings and Introductions",
        "subtopics": ["greetings", "introductions", "opening exchanges"],
        "variant": "A",
        "context": "The learner studies common greetings such as Bonjour, Bonsoir, and Salut, and combines them with introductory forms like Je m'appelle..., Voici..., and Enchante.",
        "example": "A trainee meets a visiting French-speaking client at reception, says Bonjour, introduces himself, confirms the visitor's name, and then introduces the visitor to the supervisor using a short but polite exchange.",
        "workplace": "the ability to greet and introduce people properly supports reception work, office coordination, hotel assistance, tour guidance, and any role where first contact shapes the impression of service.",
        "caution": "Typical mistakes include using overly casual forms in formal settings, forgetting titles such as Monsieur or Madame, or mispronouncing names and key greeting phrases.",
        "reinforcement": "greetings and introductions are the entry point to all later oral communication because they establish rapport, respect, and readiness to continue a conversation",
        "apply": {
            "title": "Conduct a Basic French Introduction",
            "objective": "Introduce yourself and another person in French using correct greetings, names, and courtesy expressions.",
            "sup_mat": "Dialogue cue cards\nName tags\nPronunciation guide",
            "equipment": "Table and chairs\nPrinted activity sheet\nPen",
            "steps": "1. Review greeting and introduction expressions.\n2. Pair with a classmate and assign roles.\n3. Perform a self-introduction.\n4. Introduce your partner to a third person.\n5. Repeat using a formal workplace scenario.\n6. Receive feedback on pronunciation and courtesy.",
            "assessment": "Demonstration with oral questioning and performance checklist.",
            "pcs": [
                "Used an appropriate French greeting for the scenario.",
                "Stated names and introductions clearly.",
                "Observed polite and respectful expressions.",
                "Pronounced key phrases with understandable accuracy.",
                "Completed the exchange confidently and logically.",
            ],
        },
        "mcqs": [
            {"q": "Which greeting is most appropriate in a formal daytime workplace setting?", "options": ["Bonjour", "Salut", "A bientot", "Merci"], "answer": "A"},
            {"q": "What does 'Je m'appelle' mean?", "options": ["I am leaving", "My name is", "How are you", "Please sit down"], "answer": "B"},
            {"q": "Which expression is commonly used when introducing another person?", "options": ["Voici", "Pardon", "Oui", "Peut-etre"], "answer": "A"},
            {"q": "Which title is appropriate for an adult man in French?", "options": ["Madame", "Mademoiselle", "Monsieur", "Merci"], "answer": "C"},
            {"q": "Why is pronunciation important during introductions?", "options": ["It replaces grammar", "It helps the listener understand correctly", "It removes the need for courtesy", "It shortens the conversation"], "answer": "B"},
            {"q": "Which expression is more casual than 'Bonjour'?", "options": ["Salut", "Bonsoir", "Au revoir", "Excusez-moi"], "answer": "A"},
            {"q": "What is the purpose of an introduction in the workplace?", "options": ["To avoid communication", "To create a respectful first interaction", "To end a meeting quickly", "To replace identification"], "answer": "B"},
            {"q": "Which expression best follows 'Bonjour, Monsieur' in a self-introduction?", "options": ["Je m'appelle Anna.", "A demain.", "Bonne nuit.", "De rien."], "answer": "A"},
            {"q": "When should a learner avoid using 'Salut'?", "options": ["When speaking with close friends", "When writing notes to family", "When addressing a supervisor formally", "When practicing alone"], "answer": "C"},
            {"q": "Which behavior supports a good introduction?", "options": ["Speaking too softly", "Ignoring the listener", "Using a polite opening and clear name statement", "Switching languages randomly"], "answer": "C"},
        ],
    },
    {
        "field": "1_2",
        "title": "Common Courtesy Expressions",
        "subtopics": ["polite expressions", "requests", "apologies and thanks"],
        "variant": "B",
        "context": "This includes forms such as S'il vous plait, Merci, Je vous en prie, Excusez-moi, and Pardon, together with the situations where each is most suitable.",
        "example": "A learner asks for assistance locating a document, says S'il vous plait when making the request, responds with Merci after receiving help, and uses Excusez-moi to apologize for interrupting another employee.",
        "workplace": "courtesy expressions help maintain professionalism in reception areas, offices, shops, and training environments because they reduce friction and show respect even in brief interactions.",
        "caution": "Frequent errors include overusing one expression for all situations, omitting polite markers when making requests, or confusing apology expressions with simple attention-getting phrases.",
        "reinforcement": "common courtesy expressions make communication sound respectful and service-oriented, which is essential when speaking with clients, supervisors, coworkers, and visitors",
        "apply": {
            "title": "Use Courtesy Expressions in Workplace Exchanges",
            "objective": "Respond to common workplace situations using correct French expressions for request, thanks, apology, and polite acknowledgement.",
            "sup_mat": "Situation cards\nExpression reference sheet\nObservation checklist",
            "equipment": "Desk setup\nPrinted forms\nPen",
            "steps": "1. Read the assigned workplace situations.\n2. Identify the needed courtesy function.\n3. State the correct French expression.\n4. Perform the short exchange with a partner.\n5. Rotate roles and repeat with new situations.\n6. Review corrections from the trainer.",
            "assessment": "Role-play performance supported by oral feedback and checklist rating.",
            "pcs": [
                "Selected a courtesy expression appropriate to the situation.",
                "Used polite request or response forms correctly.",
                "Showed respectful tone during the exchange.",
                "Responded accurately to the partner's line.",
                "Completed the task with minimal prompting.",
            ],
        },
        "mcqs": [
            {"q": "Which expression means 'please' in French?", "options": ["Merci", "S'il vous plait", "Pardon", "Bonjour"], "answer": "B"},
            {"q": "Which expression is used to say 'thank you'?", "options": ["Merci", "Bonsoir", "Voila", "Salut"], "answer": "A"},
            {"q": "Which expression can be used to apologize or get attention politely?", "options": ["Excusez-moi", "Voici", "Enchante", "Bonne nuit"], "answer": "A"},
            {"q": "Why are courtesy expressions important in the workplace?", "options": ["They make communication respectful", "They remove the need for grammar", "They replace instructions", "They are used only in writing"], "answer": "A"},
            {"q": "Which expression is an appropriate response to thanks?", "options": ["Je vous en prie", "Je m'appelle", "A demain", "Peu importe"], "answer": "A"},
            {"q": "When making a polite request, which expression should be added?", "options": ["Bonsoir", "S'il vous plait", "Au revoir", "Salut"], "answer": "B"},
            {"q": "Which is the best expression after interrupting someone?", "options": ["Merci", "Excusez-moi", "Bonjour", "Enchanté"], "answer": "B"},
            {"q": "What can happen if courtesy expressions are omitted?", "options": ["The message may sound rude", "The sentence becomes longer", "The listener forgets French", "The task becomes automatic"], "answer": "A"},
            {"q": "Which expression best fits receiving help from a colleague?", "options": ["Merci", "Pardon", "Bonsoir", "Salut"], "answer": "A"},
            {"q": "Which choice shows a polite request?", "options": ["Donnez-moi le dossier.", "Le dossier, maintenant.", "Le dossier, s'il vous plait.", "Je pars."], "answer": "C"},
        ],
    },
    {
        "field": "1_3",
        "title": "Basic Conversational Phrases",
        "subtopics": ["simple questions", "short responses", "conversation maintenance"],
        "variant": "C",
        "context": "The trainee practices phrases used to ask and answer simple questions, express understanding, request repetition, and keep a short conversation moving.",
        "example": "During a break, a learner asks a coworker Comment ca va, responds appropriately to the answer, asks for clarification with Repetez, s'il vous plait, and closes the exchange naturally.",
        "workplace": "basic conversational phrases are useful in orientation sessions, teamwork, visitor assistance, and routine interactions where a worker needs to exchange simple information without switching immediately to another language.",
        "caution": "Learners often rely on one memorized question only, forget to listen to the reply, or fail to use repair expressions when they do not understand.",
        "reinforcement": "basic conversational phrases help the learner sustain interaction, not just begin it, and this creates smoother communication in both social and work contexts",
        "apply": {
            "title": "Maintain a Short French Conversation",
            "objective": "Ask, answer, and sustain a brief French conversation using simple questions, responses, and clarification phrases.",
            "sup_mat": "Prompt cards\nConversation map\nTrainer observation sheet",
            "equipment": "Timer\nPrinted dialogue guide\nPen",
            "steps": "1. Review target conversational phrases.\n2. Select a partner and receive a scenario.\n3. Begin the conversation with an opening question.\n4. Use at least three follow-up or response phrases.\n5. Include one clarification expression.\n6. Close the conversation appropriately.",
            "assessment": "Guided role play with checklist-based performance assessment.",
            "pcs": [
                "Used correct opening and follow-up phrases.",
                "Answered simple questions appropriately.",
                "Applied a clarification phrase when needed.",
                "Maintained the exchange in logical sequence.",
                "Spoke with understandable pronunciation and confidence.",
            ],
        },
        "mcqs": [
            {"q": "Which phrase asks 'How are you?'", "options": ["Comment ca va ?", "Ou travaillez-vous ?", "Qui est-ce ?", "Combien ?"], "answer": "A"},
            {"q": "Which response means 'I am fine'?", "options": ["Ca va bien.", "Je m'appelle Marc.", "Au revoir.", "S'il vous plait."], "answer": "A"},
            {"q": "Which phrase politely asks someone to repeat?", "options": ["Répétez, s'il vous plait.", "Merci beaucoup.", "A plus tard.", "Bienvenue."], "answer": "A"},
            {"q": "What is the purpose of basic conversational phrases?", "options": ["To maintain a short exchange", "To write formal reports", "To replace all grammar lessons", "To avoid asking questions"], "answer": "A"},
            {"q": "Which phrase can show understanding?", "options": ["Je comprends.", "Je dors.", "Je pars.", "Je ferme."], "answer": "A"},
            {"q": "Why is listening important in conversation?", "options": ["It helps the speaker respond correctly", "It eliminates pronunciation practice", "It replaces vocabulary study", "It ends the conversation"], "answer": "A"},
            {"q": "Which is an example of a follow-up question?", "options": ["Et vous ?", "Bonsoir.", "Merci.", "Pardon."], "answer": "A"},
            {"q": "If the learner does not understand, what should be done?", "options": ["Stay silent only", "Use a clarification phrase", "Leave the conversation immediately", "Change the topic without warning"], "answer": "B"},
            {"q": "Which phrase can help close a simple conversation?", "options": ["A bientot.", "Comment vous appelez-vous ?", "Qui est-ce ?", "Ou est le bureau ?"], "answer": "A"},
            {"q": "A good conversational exchange requires the learner to", "options": ["memorize one line only", "ignore the reply", "use questions and responses in sequence", "avoid asking for clarification"], "answer": "C"},
        ],
    },
    {
        "field": "2_1",
        "title": "Jobs and Professions",
        "subtopics": ["occupation names", "self-identification", "role recognition"],
        "variant": "A",
        "context": "The trainee learns how to name common occupations in French, identify what a person does, and answer simple questions about work roles.",
        "example": "A learner says Je suis receptionniste, asks if a visitor is a manager or technician, and confirms the profession of a coworker during a simple office introduction.",
        "workplace": "knowledge of jobs and professions supports staff introductions, visitor handling, orientation, and clear identification of who is responsible for a task.",
        "caution": "Problems often occur when learners confuse masculine and feminine job titles, misapply articles, or fail to connect the occupation term to the person's actual function.",
        "reinforcement": "understanding jobs and professions allows the learner to identify people accurately and participate in practical workplace conversations",
        "apply": {
            "title": "Identify Jobs and Professions in French",
            "objective": "State and identify common professions in French using correct role names and simple descriptive sentences.",
            "sup_mat": "Occupation flashcards\nRole chart\nPractice worksheet",
            "equipment": "Whiteboard\nPrinted name cards\nPen",
            "steps": "1. Review target occupation vocabulary.\n2. Match French job titles with pictures or roles.\n3. Introduce yourself using a profession.\n4. Ask and answer questions about another person's job.\n5. Correct gender or article errors.\n6. Summarize three roles used in the scenario.",
            "assessment": "Oral recitation and role-play assessed through a checklist.",
            "pcs": [
                "Named occupations accurately in French.",
                "Used simple sentences to describe a profession.",
                "Matched the profession to the correct person or role.",
                "Observed correct language form during identification.",
                "Completed the activity with clear speech.",
            ],
        },
        "mcqs": [
            {"q": "What is the main purpose of learning job titles in French?", "options": ["To identify professions in conversation", "To replace office rules", "To avoid speaking", "To memorize numbers"], "answer": "A"},
            {"q": "Which sentence can be used to identify your profession?", "options": ["Je suis receptionniste.", "Je m'appelle bureau.", "Merci profession.", "Bonsoir travail."], "answer": "A"},
            {"q": "Why should learners study masculine and feminine job forms?", "options": ["To use titles accurately", "To shorten all sentences", "To avoid introductions", "To replace pronunciation"], "answer": "A"},
            {"q": "In a workplace conversation, profession vocabulary helps to", "options": ["identify responsibility", "erase schedules", "remove courtesy", "ignore roles"], "answer": "A"},
            {"q": "Which role is most likely part of job vocabulary?", "options": ["Technicien", "Bonjour", "Merci", "Hier"], "answer": "A"},
            {"q": "What error is common when learning professions?", "options": ["Confusing job titles with greetings", "Using only numbers", "Ignoring all nouns", "Writing in another language only"], "answer": "A"},
            {"q": "Which question best asks about a person's role?", "options": ["Quelle est votre profession ?", "Quelle heure est-il ?", "Ou habitez-vous ?", "Comment ca va ?"], "answer": "A"},
            {"q": "Why is role recognition important at work?", "options": ["It helps identify who handles a task", "It avoids all meetings", "It replaces equipment", "It makes all staff equal in duty"], "answer": "A"},
            {"q": "Which statement is related to occupation identification?", "options": ["Il est superviseur.", "Il est bonsoir.", "Il est merci.", "Il est calendrier."], "answer": "A"},
            {"q": "A learner shows competency when he or she can", "options": ["name and describe common work roles", "avoid all profession words", "memorize one greeting only", "speak without listening"], "answer": "A"},
        ],
    },
    {
        "field": "2_2",
        "title": "Office Vocabulary",
        "subtopics": ["common office items", "locations", "routine communication"],
        "variant": "B",
        "context": "This content focuses on words for office materials, equipment, and spaces such as le bureau, l'ordinateur, le dossier, l'imprimante, and la salle de reunion, together with simple phrases that use them.",
        "example": "A trainee identifies an ordinateur, asks for a dossier, points a visitor toward la salle de reunion, and reports that an imprimante is not working.",
        "workplace": "office vocabulary is essential in clerical tasks, reception support, scheduling, document handling, and basic coordination because many instructions depend on objects and locations.",
        "caution": "Learners may memorize item names without knowing how to use them in simple requests or directions, which limits practical communication.",
        "reinforcement": "office vocabulary turns French from a classroom subject into a usable workplace tool because it connects words directly to tasks, equipment, and locations",
        "apply": {
            "title": "Use Basic Office Vocabulary in Context",
            "objective": "Identify office items and locations in French and use them in simple workplace sentences and requests.",
            "sup_mat": "Label cards\nPicture prompts\nOffice map",
            "equipment": "Actual or simulated office materials\nPrinter or computer\nPen",
            "steps": "1. Identify labeled office items.\n2. Match French terms with equipment and places.\n3. Use each term in a simple sentence.\n4. Ask for or locate an item in French.\n5. Perform a short office interaction.\n6. Review corrections with the trainer.",
            "assessment": "Practical identification and guided speaking activity with checklist.",
            "pcs": [
                "Identified office vocabulary accurately.",
                "Used item names in correct simple sentences.",
                "Asked for or located an item clearly.",
                "Related vocabulary to the workplace scenario.",
                "Completed the task with acceptable pronunciation.",
            ],
        },
        "mcqs": [
            {"q": "Which term is most likely part of office vocabulary?", "options": ["L'imprimante", "Le weekend", "La plage", "Le sport"], "answer": "A"},
            {"q": "Why is office vocabulary important?", "options": ["It supports workplace communication", "It replaces greetings", "It removes the need for objects", "It is used only in literature"], "answer": "A"},
            {"q": "Which place name may appear in office vocabulary?", "options": ["La salle de reunion", "Le cinema", "Le stade", "La montagne"], "answer": "A"},
            {"q": "A learner asking for a document needs vocabulary for", "options": ["objects and requests", "weather only", "music only", "sports only"], "answer": "A"},
            {"q": "What does practical use of office vocabulary require?", "options": ["Using the word in context", "Memorizing silently only", "Avoiding sentence practice", "Skipping workplace examples"], "answer": "A"},
            {"q": "Which item would be found in an office?", "options": ["Le dossier", "Le poisson", "La bicyclette", "La guitare"], "answer": "A"},
            {"q": "Which statement best shows office vocabulary use?", "options": ["L'imprimante est ici.", "Le week-end est ici.", "Bonjour imprimante merci.", "Je suis calendrier."], "answer": "A"},
            {"q": "Why should learners connect vocabulary with locations?", "options": ["Because workplace directions often include places", "Because locations replace all grammar", "Because objects are unimportant", "Because speaking is unnecessary"], "answer": "A"},
            {"q": "Which error reduces communication quality?", "options": ["Knowing the item name but not using it in a sentence", "Repeating practice tasks", "Listening to pronunciation", "Matching labels with objects"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["identify and use office terms in routine interaction", "name sports in French only", "avoid requests", "ignore equipment"], "answer": "A"},
        ],
    },
    {
        "field": "2_3",
        "title": "Workplace Roles",
        "subtopics": ["responsibilities", "hierarchy", "interaction with staff"],
        "variant": "C",
        "context": "The learner studies how to refer to supervisors, assistants, reception staff, clients, and team members, and how to connect these roles with simple duties and relationships.",
        "example": "In a short scenario, the trainee identifies who supervises the shift, who receives visitors, who prepares documents, and who assists customers, all using simple French role language.",
        "workplace": "clear understanding of workplace roles improves coordination because employees can refer requests to the right person and describe responsibilities more accurately.",
        "caution": "A common problem is naming a role correctly but misunderstanding the responsibility attached to that role, which can cause confusion during instructions or referrals.",
        "reinforcement": "workplace roles vocabulary helps the learner understand organizational structure and communicate more appropriately within a team setting",
        "apply": {
            "title": "Describe Simple Workplace Roles",
            "objective": "Identify common workplace roles and explain basic responsibilities in French during a simulated team interaction.",
            "sup_mat": "Role cards\nOrganization chart\nTask list",
            "equipment": "Printed scenario sheets\nWhiteboard\nPen",
            "steps": "1. Review the organization chart.\n2. Match French role names with responsibilities.\n3. Introduce each person's role in a short sentence.\n4. Route simple requests to the correct role.\n5. Perform the team interaction scenario.\n6. Reflect on language accuracy and role clarity.",
            "assessment": "Scenario-based oral performance using a checklist.",
            "pcs": [
                "Identified workplace roles accurately.",
                "Linked each role with an appropriate responsibility.",
                "Used French role language clearly in the scenario.",
                "Directed requests to the correct person or office.",
                "Completed the interaction with logical sequencing.",
            ],
        },
        "mcqs": [
            {"q": "Why is it important to know workplace roles in French?", "options": ["To identify responsibilities clearly", "To avoid all tasks", "To replace schedules", "To eliminate teamwork"], "answer": "A"},
            {"q": "Which role is commonly linked with receiving visitors?", "options": ["Reception staff", "Athlete", "Musician", "Farmer"], "answer": "A"},
            {"q": "What should a learner understand besides the role name?", "options": ["The responsibility connected to it", "The weather outside", "Only the alphabet", "A random greeting"], "answer": "A"},
            {"q": "How does role vocabulary support coordination?", "options": ["It helps route requests correctly", "It replaces all documents", "It avoids all meetings", "It stops communication"], "answer": "A"},
            {"q": "Which phrase best relates to workplace roles?", "options": ["Il est superviseur.", "Il est imprimante.", "Il est merci.", "Il est bonsoir."], "answer": "A"},
            {"q": "A common error is", "options": ["knowing the title but not the duty", "practicing too often", "using labels", "reading examples"], "answer": "A"},
            {"q": "Which activity best develops this content?", "options": ["Matching staff roles with tasks", "Naming fruits only", "Reading sports scores", "Drawing maps only"], "answer": "A"},
            {"q": "What can happen if workplace roles are misunderstood?", "options": ["Instructions may be misdirected", "French becomes impossible", "All offices close", "The learner forgets greetings"], "answer": "A"},
            {"q": "Which setting most needs role identification?", "options": ["A team-based workplace", "A silent room only", "A beach trip", "A music class only"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["name roles and connect them to duties", "avoid describing responsibilities", "ignore organization charts", "memorize greetings only"], "answer": "A"},
        ],
    },
    {
        "field": "3_1",
        "title": "Adjectives Usage",
        "subtopics": ["descriptive words", "position of adjectives", "agreement in description"],
        "variant": "A",
        "context": "The trainee studies how adjectives describe people and objects, how some adjectives change position in relation to the noun, and how meaning can depend on correct agreement.",
        "example": "A learner describes a colleague as sympathique et organise, identifies a document as important, and compares how adjective placement changes the feel of a simple phrase.",
        "workplace": "adjective use helps staff describe people, materials, products, documents, and conditions clearly during everyday communication.",
        "caution": "Learners often choose the right adjective but forget to adapt it to the noun or place it correctly in the sentence.",
        "reinforcement": "adjectives make communication more precise because they add identifying details that listeners need in practical situations",
        "apply": {
            "title": "Describe People and Objects with Adjectives",
            "objective": "Use common French adjectives to describe people and objects in simple, accurate workplace-related sentences.",
            "sup_mat": "Adjective list\nPicture prompts\nSentence strips",
            "equipment": "Printed worksheet\nWhiteboard\nPen",
            "steps": "1. Review common descriptive adjectives.\n2. Match adjectives to people or objects.\n3. Form simple descriptive sentences.\n4. Check adjective placement and agreement.\n5. Read the sentences aloud.\n6. Revise errors based on trainer feedback.",
            "assessment": "Sentence production and oral reading assessed through a checklist.",
            "pcs": [
                "Selected adjectives appropriate to the noun.",
                "Used adjectives in understandable sentences.",
                "Observed correct adjective placement where required.",
                "Applied agreement accurately in most cases.",
                "Read or stated descriptions clearly.",
            ],
        },
        "mcqs": [
            {"q": "What is the main function of an adjective?", "options": ["To describe a noun", "To count objects", "To replace greetings", "To indicate time only"], "answer": "A"},
            {"q": "Why is adjective use important?", "options": ["It adds precise detail", "It removes all verbs", "It replaces workplace roles", "It shortens every sentence"], "answer": "A"},
            {"q": "Which item can be described by an adjective?", "options": ["A document", "A pronunciation mark only", "A number only", "A greeting only"], "answer": "A"},
            {"q": "A common error in adjective use is", "options": ["forgetting agreement", "using paper", "reviewing examples", "reading aloud"], "answer": "A"},
            {"q": "Which statement includes an adjective?", "options": ["Le dossier est important.", "Bonjour, merci.", "Je m'appelle Claire.", "A demain."], "answer": "A"},
            {"q": "Why should learners study adjective placement?", "options": ["Because some adjectives change position", "Because adjectives are never used", "Because placement does not matter", "Because nouns are unnecessary"], "answer": "A"},
            {"q": "In the workplace, adjectives help describe", "options": ["people and materials", "only weekends", "only sports", "only music"], "answer": "A"},
            {"q": "Which activity supports adjective learning?", "options": ["Describing pictures and objects", "Ignoring nouns", "Memorizing one greeting", "Avoiding sentence practice"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["describe a noun accurately", "avoid all description", "use numbers only", "translate nothing"], "answer": "A"},
            {"q": "Why must adjective meaning be clear?", "options": ["It helps the listener identify the noun correctly", "It replaces listening", "It ends the conversation", "It removes all grammar"], "answer": "A"},
        ],
    },
    {
        "field": "3_2",
        "title": "Gender and Agreement",
        "subtopics": ["masculine and feminine forms", "singular and plural agreement", "grammatical accuracy"],
        "variant": "B",
        "context": "This lesson explains how nouns in French have gender and how articles, adjectives, and some role labels must agree with the noun in gender and number.",
        "example": "A trainee compares un employe and une employee, then adjusts accompanying adjectives so that the sentence remains grammatically accurate when talking about one person or several people.",
        "workplace": "gender and agreement matter in workplace communication because inaccurate forms can create confusion, reduce professionalism, and weaken confidence in speaking and writing.",
        "caution": "Many learners know the vocabulary item but fail to adjust the article or adjective when the noun changes from masculine to feminine or from singular to plural.",
        "reinforcement": "gender and agreement are core accuracy features of French and they support clear, respectful, and grammatically sound communication",
        "apply": {
            "title": "Apply Gender and Agreement Correctly",
            "objective": "Use correct gender and number agreement in French when describing people, roles, and objects in simple sentences.",
            "sup_mat": "Agreement chart\nSentence correction sheet\nRole vocabulary list",
            "equipment": "Printed exercises\nWhiteboard\nPen",
            "steps": "1. Review masculine and feminine markers.\n2. Identify singular and plural noun forms.\n3. Adjust articles and adjectives to match the noun.\n4. Correct sample sentences with agreement errors.\n5. Create three original sentences.\n6. Present answers for feedback.",
            "assessment": "Written and oral correction task checked through a performance checklist.",
            "pcs": [
                "Identified the gender of target nouns correctly.",
                "Matched articles and adjectives with the noun form.",
                "Applied singular or plural agreement accurately.",
                "Corrected common agreement errors effectively.",
                "Produced understandable sentences using correct forms.",
            ],
        },
        "mcqs": [
            {"q": "What does agreement mean in French grammar?", "options": ["Words match the noun in gender and number", "All words stay unchanged", "Only verbs matter", "Only pronunciation matters"], "answer": "A"},
            {"q": "Why is gender important in French?", "options": ["Because nouns require matching forms", "Because greetings depend on weather", "Because all nouns are neutral", "Because it replaces vocabulary"], "answer": "A"},
            {"q": "Which part of a sentence may change because of agreement?", "options": ["Articles and adjectives", "Only punctuation", "Only page number", "Only handwriting"], "answer": "A"},
            {"q": "A common learner error is", "options": ["keeping the same adjective for all noun forms", "listening to examples", "reviewing charts", "asking questions"], "answer": "A"},
            {"q": "Why does agreement matter in the workplace?", "options": ["It supports accurate and professional communication", "It removes all speaking tasks", "It replaces courtesy", "It matters only in literature"], "answer": "A"},
            {"q": "Which activity best develops agreement skill?", "options": ["Correcting sentences", "Avoiding grammar practice", "Memorizing one noun only", "Ignoring articles"], "answer": "A"},
            {"q": "If a noun becomes plural, what may need to change?", "options": ["The article and adjective", "The calendar month", "The greeting only", "The speaker's name"], "answer": "A"},
            {"q": "What should learners do when a noun changes from masculine to feminine?", "options": ["Adjust related words to match", "Leave every word unchanged", "Delete the adjective", "Avoid the sentence"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["form sentences with correct agreement", "ignore noun forms", "avoid adjectives", "use greetings only"], "answer": "A"},
            {"q": "Which statement best describes agreement?", "options": ["It is a grammatical matching rule", "It is a greeting formula", "It is an office item", "It is a day of the week"], "answer": "A"},
        ],
    },
    {
        "field": "3_3",
        "title": "Physical Descriptions",
        "subtopics": ["appearance vocabulary", "identifying traits", "clear description in context"],
        "variant": "C",
        "context": "The trainee learns vocabulary for describing height, build, hair, visible features, and general appearance in a respectful and useful way.",
        "example": "A learner helps identify a visitor by describing basic physical traits politely, such as height, hair color, and clothing, while avoiding offensive or unnecessary comments.",
        "workplace": "physical descriptions are practical when identifying visitors, confirming the person to meet, assisting in reception areas, or clarifying who is being referred to in a safe and respectful manner.",
        "caution": "The learner must avoid insensitive descriptions, overstatement, and inaccurate adjective agreement when talking about appearance.",
        "reinforcement": "physical descriptions become useful when they are clear, respectful, and limited to details that help identify a person or object appropriately",
        "apply": {
            "title": "Give Respectful Physical Descriptions",
            "objective": "Describe a person or object in French using clear, respectful, and accurate physical description vocabulary.",
            "sup_mat": "Photo cards\nDescription guide\nObservation checklist",
            "equipment": "Printed images\nWhiteboard\nPen",
            "steps": "1. Review target vocabulary for appearance.\n2. Observe the assigned image or person description.\n3. Note useful identifying traits.\n4. Form respectful descriptive sentences in French.\n5. Deliver the description orally.\n6. Revise wording based on feedback.",
            "assessment": "Observed oral description with checklist-based scoring.",
            "pcs": [
                "Selected relevant and respectful descriptive details.",
                "Used correct vocabulary for visible traits.",
                "Applied accurate descriptive language in context.",
                "Avoided insensitive or unnecessary comments.",
                "Presented the description clearly and logically.",
            ],
        },
        "mcqs": [
            {"q": "What is the purpose of physical descriptions in this lesson?", "options": ["To identify people or objects clearly and respectfully", "To replace all introductions", "To criticize appearance", "To avoid speaking"], "answer": "A"},
            {"q": "Which detail may be part of a physical description?", "options": ["Hair color", "Salary only", "Meeting agenda only", "Printer model only"], "answer": "A"},
            {"q": "Why must physical descriptions be respectful?", "options": ["Because language should remain professional and appropriate", "Because grammar becomes optional", "Because details are never useful", "Because speaking is not allowed"], "answer": "A"},
            {"q": "Where can physical descriptions be useful at work?", "options": ["At reception or visitor identification", "Only in sports matches", "Only in weather reports", "Only in music lessons"], "answer": "A"},
            {"q": "Which is a common problem in this content?", "options": ["Using insensitive or inaccurate descriptions", "Reviewing vocabulary", "Practicing pronunciation", "Observing pictures"], "answer": "A"},
            {"q": "A good physical description should be", "options": ["clear and relevant", "offensive and exaggerated", "long and unrelated", "random and incomplete"], "answer": "A"},
            {"q": "Which activity best develops this skill?", "options": ["Describing a person's visible traits politely", "Ignoring all details", "Naming office machines only", "Avoiding adjectives"], "answer": "A"},
            {"q": "Why should the learner avoid unnecessary comments?", "options": ["To maintain appropriateness and professionalism", "To make the description confusing", "To replace grammar study", "To shorten all tasks"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["describe someone accurately and respectfully", "criticize appearance freely", "avoid all identifying detail", "memorize one greeting only"], "answer": "A"},
            {"q": "Which setting may require this skill?", "options": ["Helping identify a visitor", "Playing sports", "Ordering dinner only", "Studying months only"], "answer": "A"},
        ],
    },
]

rewritten_key_facts = {
    "1_1": """Greetings and Introductions are the first practical skills a beginner needs when using French in real interaction. This content teaches the learner how to open a conversation, identify oneself, identify another person, and establish a respectful tone from the first line spoken. In training situations, students often think a greeting is only a memorized word such as Bonjour. In reality, a greeting is a communication choice that reflects time of day, degree of formality, and relationship between speakers. Introductions work the same way. A trainee must know how to say a name, ask for another person's name, and introduce a third person in a way that sounds orderly and polite. These are small language actions, but they strongly affect confidence. When the learner can open a French interaction successfully, the next exchange becomes easier because the speaker already has control of the social beginning of the conversation.

The lesson begins with the major functions of greeting language. Bonjour is generally used in daytime formal or neutral situations, Bonsoir is more suitable in the evening, and Salut is common in casual settings with friends or familiar peers. The learner should not use these forms at random. Correct use depends on context. A workplace reception desk, office entrance, classroom observation, or client visit usually requires more formal language. The trainee also studies introductory expressions such as Je m'appelle, Comment vous appelez-vous, Voici, and Il s'agit de. These expressions help organize the exchange logically. Instead of saying isolated nouns, the learner presents identity in a complete communication sequence: greeting, name statement, role or purpose, and acknowledgement. Practicing this order is important because workplace interactions are often brief and need immediate clarity.

A useful classroom example is a reception scenario. A trainee assigned to front-desk duty sees a visitor arrive for an appointment. The trainee says Bonjour, Madame, then asks for the visitor's name in French. After confirming the name, the trainee uses Voici or Je vous presente to introduce the visitor to the supervisor. In this short event, several skills are combined: accurate greeting, respectful title, clear pronunciation, introduction of self or others, and controlled tone. The learner should notice that success depends not only on vocabulary but also on sequence. If the greeting is skipped, the exchange may sound abrupt. If the title is omitted in a formal setting, the speaker may sound overly casual. If the name is unclear, the interaction becomes inefficient. This is why repeated role-play is necessary in competency-based training.

Pronunciation deserves focused attention in this content area. French greetings and names can be misheard if the learner speaks too quickly or ignores sound differences. The trainer should encourage controlled pace, repeated listening, and model imitation. Learners must also practice eye contact, courteous body language, and appropriate volume because spoken language in the workplace is not only about grammar. It is about making the listener comfortable and understood. When students introduce themselves, they should also be able to add a short supporting detail, such as a role, department, or reason for meeting, because that reflects real-life use. For example, saying Je m'appelle Ana. Je suis stagiaire au bureau is more useful than simply stating a name. This turns a basic introduction into a functional workplace utterance.

In actual employment settings, greetings and introductions appear in many routine tasks. A hospitality worker welcomes guests. An office assistant receives suppliers. A trainee meets a French-speaking visitor during orientation. A customer service representative introduces a caller to the correct staff member. In each case, the speaker must show professionalism immediately. This means selecting the proper greeting, identifying the people involved, and avoiding overly casual language. Common mistakes include using Salut with a manager, forgetting Monsieur or Madame, mumbling the name, or switching to another language before attempting the basic French exchange. These errors weaken the impression of readiness. The learner should instead aim for simple, accurate, and courteous speech that shows control over the initial stage of communication.

By the end of this content, the trainee should be able to greet different people appropriately, state and ask for names, introduce another person, and maintain a respectful opening exchange in French. The main idea is that a greeting is not decorative language; it is a functional tool for establishing contact. Introductions are not extra details; they allow people to understand who is speaking and why the interaction is happening. With guided repetition, situational drills, and correction of tone and pronunciation, the learner gains a reliable communication routine. That routine becomes the foundation for later conversation, workplace courtesy, and broader oral competence in French.""",
    "1_2": """Common Courtesy Expressions teach the learner how to make French communication sound respectful, cooperative, and socially appropriate. In beginner language study, students often focus on naming objects or answering direct questions, but real communication also depends on manners. Words such as S'il vous plait, Merci, Je vous en prie, Excusez-moi, and Pardon are essential because they soften requests, acknowledge help, and repair moments of interruption or inconvenience. In TESDA-style instruction, this matters because courtesy is part of employability. A worker who knows the correct terms but speaks without politeness markers may still sound unprepared for service-oriented communication. This content therefore develops not only vocabulary, but professional behavior expressed through language.

Each courtesy expression has a practical function. S'il vous plait is used when requesting something politely. Merci expresses appreciation after receiving assistance, information, or service. Je vous en prie can respond to thanks in a formal and respectful way. Excusez-moi is useful when interrupting, getting attention, or apologizing for a minor inconvenience. Pardon may also be used to signal apology or ask for repetition in some situations. The learner should understand that these expressions are not interchangeable in every setting. Saying thank you when an apology is needed will not solve the communication problem. Likewise, making a request without a polite marker may sound demanding even if the grammar is correct. The lesson therefore links each expression to a communicative purpose and to the tone expected in the situation.

Consider a simple office example. A trainee needs a printed copy of a schedule from a coworker. The learner approaches and says Excusez-moi to get attention, then asks for the document with S'il vous plait, receives the document, and responds with Merci. If the coworker says Je vous en prie, the exchange ends on a cooperative note. This short sequence may look easy, but it shows a complete cycle of respectful interaction: approach, request, response, and acknowledgement. If any courtesy part is missing, the exchange sounds less professional. The same principle applies at a reception desk, in a classroom, in a hotel, or during customer handling. Courtesy language helps the speaker manage social contact while still completing the task efficiently.

This content also helps learners understand register. In many workplaces, polite language is expected when speaking to supervisors, guests, unfamiliar clients, or older adults. Even among coworkers, polite markers reduce tension and support teamwork. The trainer should therefore present courtesy expressions in realistic dialogue, not as isolated word lists only. Practice can include requesting help, apologizing for delays, asking someone to repeat, offering thanks for assistance, and responding appropriately. Pronunciation practice is also important. If the learner says an expression too softly, too quickly, or with unclear sounds, the politeness effect may be weakened because the listener may not recognize the expression immediately.

Workplace application is very strong in this lesson. Courtesy expressions are needed when giving or receiving documents, asking permission, answering customer questions, clarifying instructions, and responding to small mistakes. An employee who can say please, thank you, excuse me, and you are welcome in French supports a more positive service culture. This is particularly important in multilingual environments where even short respectful phrases create goodwill. Typical learner errors include overusing Merci for every function, forgetting polite markers when making requests, or failing to apologize after interrupting someone. Another error is translating directly from the home language without considering the most natural French expression for the situation.

The learner should leave this content able to choose the correct courtesy expression according to function, tone, and setting. Courtesy language does more than decorate speech. It protects relationships, reduces misunderstanding, and helps communication remain professional. When the trainee practices these expressions through short scenarios and receives correction on usage and tone, the phrases become easier to apply in authentic interaction. In summary, common courtesy expressions are core tools for respectful French communication in both daily life and workplace settings, and they should be used consistently whenever the learner requests, apologizes, thanks, or responds to another person.""",
    "1_3": """Basic Conversational Phrases help the learner move beyond single-word responses and participate in short but meaningful French exchanges. After mastering greetings and courtesy expressions, the next challenge is maintaining the conversation for several turns. This means asking simple questions, responding to common questions, showing understanding, requesting repetition, and closing the interaction naturally. The content is important because many real encounters do not stop after Bonjour. In a workplace or daily-life setting, the learner may need to ask how someone is, confirm a detail, answer a simple question, and continue the interaction without long hesitation. This lesson gives the trainee the language tools to keep communication active.

The learner studies phrases such as Comment ca va, Ca va bien, Et vous, Je comprends, Je ne comprends pas, Repetez, s'il vous plait, and A bientot. These expressions create a conversational framework. Some phrases open a topic, some keep the exchange moving, and some repair communication when the listener misses information. That repair function is especially valuable. Beginner speakers often remain silent when they do not understand, but real communication improves when the learner knows how to ask for clarification. Saying Repetez, s'il vous plait or Parlez plus lentement is more effective than pretending to understand. In competency-based training, this shows practical communication management rather than passive memorization.

An effective training example is a break-time conversation between two coworkers. One worker asks Comment ca va, the other responds Ca va bien, merci. Et vous, and the exchange continues with a simple question about the workday or schedule. During the conversation, one speaker misses a word and says Repetez, s'il vous plait. The conversation then continues instead of stopping. This example teaches several important points. First, a good conversation includes listening as well as speaking. Second, short follow-up phrases such as Et vous are important because they invite a reply and keep the interaction balanced. Third, clarification phrases are not signs of failure. They are professional tools that allow communication to continue accurately.

The trainer should guide learners to practice turn-taking. Many beginners memorize one question but do not know what to do after the other person answers. This is why conversational phrases should be drilled in connected sequences rather than alone. Learners need experience with openings, responses, follow-up questions, acknowledgement, clarification, and closing expressions. Pronunciation and pacing are still important, but listening skill is equally important here. The trainee must learn to catch familiar phrases, identify the main meaning, and respond in a relevant way. If the learner gives an unrelated answer, the conversation sounds mechanical and the real purpose of communication is lost.

In workplace situations, these phrases are helpful during orientation, visitor assistance, casual office interaction, simple customer contact, and teamwork. An employee may need to ask a short question, confirm understanding, request repetition, or close a brief discussion politely. These are not advanced grammar tasks, yet they strongly affect how smooth a conversation feels. Common problems include repeating the same phrase in every situation, ignoring the other speaker's reply, failing to ask for clarification, or stopping after one exchange. The trainer should therefore build activities that require the learner to adapt, listen, and respond logically.

By the end of this lesson, the trainee should be able to start a short French conversation, answer predictable questions, use follow-up language, ask for clarification when needed, and close the exchange appropriately. The key principle is that conversation is a sequence, not a single sentence. Basic conversational phrases give structure to that sequence and help the learner remain engaged. When practiced in realistic scenarios, they build confidence, responsiveness, and beginner-level communicative independence in French.""",
    "2_1": """Jobs and Professions provide the learner with practical vocabulary for identifying what people do in a workplace and how they are introduced in conversation. This content is more than memorizing occupation names. It trains the learner to connect a French profession term with a real role, person, and responsibility. In daily and workplace interaction, a speaker may need to say what job he or she has, ask about another person's profession, or identify who should handle a concern. For that reason, profession vocabulary supports both self-introduction and operational clarity. When learners know how to name jobs accurately, they communicate more efficiently in structured settings.

The lesson covers common occupation words and simple patterns such as Je suis..., Il est..., Elle est..., and Quelle est votre profession. These forms allow the learner to identify professions in sentences, not just in lists. It is also important to note that many profession terms reflect gender in French, so the learner must recognize whether the job title refers to a man or a woman and adjust language accordingly. This is not merely a grammar issue. It is part of accurate and respectful identification. The learner should also understand that some job titles are closely linked with specific actions, such as receiving visitors, supervising staff, filing documents, assisting clients, or handling equipment.

A useful real-world example is a workplace orientation activity. A trainee introduces herself as a stagiaire, identifies one coworker as a receptionniste, another as a superviseur, and another as a technicien. The trainee then answers simple questions about who handles front-desk work and who assists with technical concerns. This task combines vocabulary, listening, and role awareness. If the learner confuses the job title, the listener may misunderstand who should perform a certain duty. If the learner knows only the English term and cannot connect it to the French equivalent, communication becomes interrupted. Role-play helps solve this by linking occupation vocabulary directly to practical situations.

The teaching approach should emphasize recognition and use. Flashcards, picture matching, staff charts, and spoken drills can help learners connect job titles to faces and tasks. The trainer should not stop at translation. The learner should say complete lines such as Il est manager du bureau or Elle est receptionniste a l'hotel. These short descriptive patterns are useful because they mirror the kind of information shared in introductions and workplace conversations. It is also helpful to compare related roles so the learner sees distinctions, for example between an assistant and a supervisor, or between office staff and service personnel.

In workplace application, jobs and professions are essential when welcoming visitors, referring inquiries, describing one's own position, or identifying who can solve a problem. A receptionist may need to say that the manager is in a meeting. A trainee may need to explain that a technician will check the equipment. A staff member may identify a visitor's contact person. In all these situations, profession vocabulary creates order. Common learner errors include confusing titles with workplace locations, forgetting feminine or masculine forms, or using a profession word without understanding the duty attached to it. These errors can be corrected through scenario-based practice that requires both naming and functional understanding.

In summary, this content equips the learner to recognize occupations, state simple work identities, and connect profession vocabulary with real workplace tasks. The learner should be able to answer who a person is in the organization and what kind of role that person performs. That ability is useful in introductions, referrals, and routine office communication. With repetition, correction, and contextual practice, profession terms become active language tools rather than isolated memorized labels.""",
    "2_2": """Office Vocabulary focuses on the words learners need in order to function in a simple French-speaking office environment. Instead of speaking only about people, the learner must also refer to objects, equipment, places, and routine materials connected with everyday work. This includes items such as le dossier, l'ordinateur, l'imprimante, la table, and locations such as le bureau or la salle de reunion. These words become highly useful when the trainee asks for a document, explains where a meeting will happen, identifies equipment, or follows a simple instruction. The value of this lesson lies in immediate practical use. Many workplace tasks depend on naming the correct item clearly and quickly.

The learner should not study office vocabulary as a plain inventory list. Each word should be linked with a function. A dossier is not just a noun to memorize; it is a file that may be requested, submitted, reviewed, or stored. An ordinateur may be used to prepare information, enter records, or support communication. An imprimante may be available, unavailable, or in need of checking. A meeting room may be occupied, prepared, or pointed out to a visitor. The trainee benefits when each term is placed inside a realistic sentence and situation. In this way, vocabulary becomes easier to retain because it is connected to action and purpose rather than to abstract memorization.

Consider a practical office scene. A visitor arrives and asks where a meeting will take place. The trainee responds by identifying la salle de reunion and gives a simple direction. Later, the trainee asks a coworker for a dossier, reports that the imprimante is not working, and uses the word ordinateur while explaining where a record was prepared. This type of practice shows why object and location vocabulary matter. Communication in an office often depends on nouns more than on long explanations. If the learner cannot identify the document, room, or machine involved, even a polite speaker may fail to complete the task effectively.

Training activities should therefore include labeling, picture association, item identification, and simple oral production. Learners can match French terms to actual objects, create one-sentence descriptions, and perform short role plays involving requests and directions. It is also useful to teach vocabulary in clusters, such as furniture, documents, electronic equipment, and office spaces. This helps the learner recognize relationships between words. Pronunciation remains important because many office terms may sound unfamiliar to beginners. Correct repetition and visual support can improve retention and accuracy.

Office vocabulary has direct workplace value. Clerical support, front-desk assistance, scheduling, filing, and basic customer coordination all require language for materials and locations. When an employee can say where a document is, what equipment is needed, or which room should be used, the flow of work improves. Common learner mistakes include memorizing the noun without being able to use it in a request, confusing office objects with professions, or failing to connect location names with directional language. These issues should be corrected through repeated contextual use rather than through vocabulary lists alone.

By the end of this content, the learner should be able to identify common office items and places in French, use them in short practical sentences, and respond to simple workplace situations that involve documents, equipment, or rooms. The core lesson is that office vocabulary supports action. It helps the learner request, locate, report, and explain. Through guided practice, the trainee turns static words into functional workplace communication.

The learner should also understand that office vocabulary becomes stronger when paired with movement and task simulation. Pointing to the object, handling the material, and using the term inside a request or report increase retention. A trainee who says the French word while filing a folder, identifying a printer, or guiding someone to a meeting room is more likely to remember the vocabulary accurately. This direct connection between word and task is what makes the lesson useful in real work preparation.""",
    "2_3": """Workplace Roles help the learner understand how people are positioned within a work setting and how those positions affect communication. While jobs and professions name what someone is, workplace roles emphasize what someone is responsible for and how others relate to that person in daily operations. This distinction is important because communication in an organization often depends on knowing who receives visitors, who approves requests, who prepares documents, and who responds to client concerns. A beginner French learner benefits from role vocabulary because it supports referrals, instructions, and team coordination in simple language.

The learner studies role labels such as superviseur, assistant, receptionniste, client, employe, and other staff references that appear in ordinary workplace talk. The key task is to attach each label to a recognizable function. A supervisor may monitor work and approve tasks. A receptionist may receive visitors and route inquiries. An assistant may support documentation or scheduling. A client may request service or information. When the learner understands these links, communication becomes more purposeful. The language is no longer just descriptive; it becomes organizational. This is especially useful in beginner-level workplace French, where short sentences often carry important practical meaning.

One strong classroom example is a team coordination exercise. The trainer presents a simple office problem, such as a visitor arriving early, a document needing approval, or a customer asking for help. The learner identifies which workplace role should respond first and explains that choice in French. For example, the trainee may state that the receptionniste receives the visitor, the superviseur approves the document, or the assistant prepares the needed form. This activity teaches more than vocabulary. It builds awareness of responsibility, sequence, and appropriate referral. If the learner identifies the wrong role, the message may still be grammatical but the task logic will fail.

Instruction in this area should make use of organization charts, staff lists, role cards, and short scenarios. The learner should practice naming a role, describing a duty, and directing a request toward the correct person. This can be done through matching tasks, spoken explanations, and role-play. It is helpful to compare similar roles so the learner notices differences in authority and function. The training should also show how role language interacts with politeness. A learner may speak differently to a supervisor than to a peer, and that awareness improves the realism of communication practice.

In workplace application, role language is useful when routing messages, introducing staff, assigning simple concerns, and helping visitors understand who they need to meet. An employee may say that the assistant will prepare the file, that the manager is not yet available, or that the receptionist can help with the schedule. Clear role identification saves time and prevents confusion. Common learner problems include knowing the title but not the duty, mixing up role names and profession words, or referring every request to the wrong person. Scenario-based activities correct these habits because they require the learner to link language with actual workflow.

The learner should complete this content with the ability to identify common workplace roles, state basic responsibilities, and use that information in short French interactions. The deeper objective is organizational awareness expressed through language. When the trainee can connect people, duties, and communication needs, French becomes a functional workplace tool. This makes the learner better prepared for office-based interaction, visitor support, and beginner team communication.

Another important outcome is confidence in referral language. In real work settings, beginners often know that a request should be sent elsewhere but do not know how to explain that clearly. Role vocabulary helps the learner say who should receive the concern and why. That added precision supports teamwork, avoids delay, and shows practical readiness for structured communication.""",
    "3_1": """Adjectives Usage teaches the learner how to add meaningful detail when describing people and objects in French. Without adjectives, communication remains limited to naming only the person or thing. With adjectives, the learner can explain whether a document is important, whether a coworker is organized, whether an item is large or small, or whether a room is quiet or busy. This skill matters in daily and workplace settings because listeners often need more than identification. They need distinguishing information. A simple noun tells what something is, but an adjective helps clarify which one, what condition it has, or what quality is being emphasized.

In French, adjective use involves more than inserting a descriptive word into a sentence. The learner must know which adjectives are suitable for people, which are useful for objects, and how some adjectives are positioned before or after the noun. This creates an important instructional point. Learners should not assume that French description works exactly like English description. Some common adjectives follow established patterns, and meaning can sound unnatural if the word is placed incorrectly. The trainee should therefore learn adjectives together with sample phrases and complete sentences, not as isolated translations. This helps connect vocabulary, structure, and communicative purpose.

A practical example can come from a document-handling scenario. A trainee may need to describe one file as important, another as urgent, and a third as incomplete. In a different task, the trainee may describe a colleague as patient, organized, or friendly. These descriptions guide action. If a document is urgent, it should be handled first. If a visitor is elderly or if a guest appears confused, the response may need to be adjusted sensitively and respectfully. The example shows that adjectives are not only decorative. They influence how people understand priority, condition, and identity in real situations.

Teaching should focus on both recognition and production. Learners can examine pictures, office objects, or role cards and assign accurate adjectives to each. The trainer may ask why a certain adjective fits and whether it should appear before or after the noun in the target phrase. Short sentence building is helpful because it trains the learner to combine adjective choice with articles, nouns, and pronunciation. It is also important to vary the descriptive domain. Some adjectives refer to appearance, some to personality, some to size, and some to quality or condition. A broad range makes the learner more flexible when speaking.

In workplace communication, adjective use is practical in describing materials, people, spaces, and conditions. A staff member may refer to an important message, a small office, a polite customer, or a delayed delivery. These short descriptions allow the listener to understand the context quickly. Common learner errors include choosing an adjective that does not fit the noun, placing the adjective awkwardly, or forgetting that description should stay relevant and respectful. A trainee should not overload a sentence with unnecessary adjectives. The best descriptions are clear, accurate, and useful to the listener.

By the end of this content, the learner should be able to choose suitable adjectives, use them in simple French sentences, and apply descriptive language to practical situations involving people and objects. The central lesson is that adjectives increase precision. They help communication move from naming to explaining. With repeated use in spoken and written drills, the trainee gains better control of description and becomes more capable of giving useful information in beginner-level French interactions.

The learner should also see that adjective choice can influence tone. Calling a task urgent, a guest patient, or a message important changes how the listener responds. Because of that, adjective use supports both description and decision-making. Well-chosen descriptive words help people prioritize action, understand context, and respond more appropriately in workplace communication.""",
    "3_2": """Gender and Agreement are core features of French grammar and are essential for producing language that sounds accurate and organized. In this content, the learner studies how nouns are classified as masculine or feminine and how related words, especially articles and adjectives, often change to match them. The learner also studies how singular and plural forms affect these same relationships. This lesson is important because agreement errors appear quickly in beginner French. A speaker may know the right vocabulary word, yet the sentence still sounds incorrect if supporting words do not match the noun. Competence therefore requires not only vocabulary knowledge, but grammatical control.

The first step is recognizing that agreement is a matching system. If the noun changes, related words may also need to change. A masculine singular noun may take one article form, while a feminine noun takes another. When the noun becomes plural, both article and adjective may require adjustment. The trainee should see agreement as a pattern rather than as a set of random exceptions. Charts and examples are useful because they help the learner compare forms side by side. However, the learner must also apply the pattern in real sentences. Agreement becomes meaningful only when it is used in communication, such as describing a person, identifying a role, or referring to workplace materials.

A practical example is the description of employees in an office. The learner may compare one male employee and one female employee, then modify the article and adjective so that each sentence remains correct. The learner may also describe several documents and adjust the adjective to reflect plurality. This exercise teaches attention to detail. If the article does not match the noun, or if the adjective remains unchanged when the noun becomes plural, the listener may still understand part of the message, but the speaker's accuracy is reduced. In workplace training, this matters because correct grammar supports professional impression and confidence.

Instruction in this lesson should move from recognition to correction and then to production. Learners can first identify gender and number in model phrases. Next, they can correct sentences with deliberate agreement errors. Finally, they can produce original sentences about staff, objects, and simple descriptions. This progression is effective because it trains observation before expectation of independent performance. The trainer should also highlight common agreement problems that occur with profession words, descriptive adjectives, and noun groups used frequently in beginner conversation. When learners repeatedly notice these patterns, they begin to self-correct more efficiently.

Workplace application appears whenever a speaker needs to describe people, roles, items, or conditions with grammatical accuracy. A staff member may refer to a female supervisor, several visitors, or multiple documents requiring action. In each case, agreement supports clarity and demonstrates care in language use. Common learner problems include keeping the same adjective form for every noun, forgetting plural markers, or choosing the correct noun but the wrong article. These habits can be reduced through structured drills, short office-related sentences, and oral correction during role-play.

In summary, gender and agreement are not minor grammar details. They organize the sentence and allow French description to function correctly. The learner should finish this content able to identify gender and number, match related words accurately, and produce short sentences with improved grammatical control. This skill strengthens every later topic because articles, adjectives, and descriptive phrases appear throughout French communication.

The trainee should remember that agreement supports credibility. Even when the message is simple, accurate matching shows careful language use. As learners improve, this skill reduces hesitation because they begin to predict the forms that belong together. That growing control makes future speaking and writing tasks more efficient and more professional.""",
    "3_3": """Physical Descriptions develop the learner's ability to identify people and objects through visible traits while remaining respectful, accurate, and relevant. In daily conversation and workplace situations, there are times when a person must be recognized by appearance. This may happen at a reception area, during visitor assistance, or while clarifying who is expected in a meeting. The skill is useful only when it is handled carefully. A good physical description gives enough detail to identify someone, but it avoids insulting, excessive, or unnecessary comments. For that reason, this content combines vocabulary development with judgment and professionalism.

The learner studies words related to height, build, hair, visible features, and general appearance, together with the sentence patterns needed to present those traits clearly. The training should emphasize that description must stay purposeful. It is not appropriate to comment on every visible detail. The learner should select traits that help recognition, such as tall or short, hair color, clothing, or another neutral visible feature. This makes the description functional. The trainee must also remember that French descriptions often require adjective agreement and clear noun-adjective combinations, so the content links naturally with earlier grammar work.

A realistic example is a front-desk situation in which a learner expects a visitor but needs to confirm identity before directing the person to the correct office. The learner may say that the visitor is tall, has dark hair, and is wearing a blue jacket. These details are enough to support identification without sounding offensive. Another example involves describing a lost item or a document folder by color and size. In both cases, the description serves a practical purpose. The listener needs relevant identifying information, not unnecessary personal judgment. This is an important habit for workplace communication and customer service.

Teaching strategies should include picture prompts, observation tasks, and guided sentence building. Learners can observe a photo and choose which visible traits are suitable to mention. They can then compare answers and discuss why some details are useful while others should be omitted. Oral presentation is valuable because it allows the trainer to correct vocabulary, pronunciation, and tone. The trainer should remind learners that respect is part of competence. Even if the grammar is correct, an insensitive description is not acceptable in a professional environment. The learner must therefore practice neutral, fact-based language.

Workplace application is strongest in visitor identification, service coordination, and basic security-related clarification. An employee may need to tell a coworker which guest has arrived, describe the person waiting for an appointment, or identify an object by visible characteristics. Common learner errors include exaggerating appearance, choosing inappropriate descriptive terms, or giving too many details without organization. Another frequent problem is forgetting agreement when describing a person or object. These issues should be corrected through carefully designed scenarios that reward clarity, relevance, and respect.

By the end of this content, the learner should be able to describe a person or object in French using relevant physical traits, appropriate vocabulary, and professional judgment. The major lesson is that physical description is a practical identification tool, not a space for careless opinion. When used correctly, it improves communication, supports workplace efficiency, and helps the learner participate in French interactions with greater confidence and sensitivity.

The learner should practice organizing a description from most useful detail to least useful detail. For example, height, hair, clothing, and one other visible feature may be enough for identification. This orderly approach helps the listener process the information quickly. It also prevents the speaker from wandering into unnecessary comments that do not help the task. Repetition with photos, simulated visitors, and object descriptions will help the trainee develop consistency, accuracy, and restraint in this kind of communication.""",
}


qualification_title = "Foreign Language 2"
all_units = [
    "Use appropriate expressions in French in daily conversations and workplace settings.",
    "Read and understand simple texts and dialogues in French.",
    "Write short messages, emails, or notes using correct French grammar.",
    "Demonstrate cultural awareness and sensitivity in using the French language.",
]
all_modules = [
    "Using French Expressions in Daily and Workplace Conversations",
    "Reading Simple French Texts and Dialogues",
    "Writing Short French Messages, Emails, and Notes",
    "Practicing Cultural Awareness and Sensitivity in French Communication",
]

payload = {
    "sector": "EDU",
    "qualification_title": qualification_title,
    "unit_of_competency": all_units[0],
    "module_title": all_modules[0],
    "next_unit_of_competency": all_units[1],
    "Module_Descriptor": (
        "This module develops the learner's ability to use basic French expressions in daily conversations and simple workplace situations. "
        "It covers practical communication for greetings, introductions, courtesy expressions, short conversational exchanges, workplace vocabulary, role identification, and descriptive language for people and objects. "
        "The trainee applies these forms in guided oral tasks, role plays, and workplace-based scenarios that build confidence, politeness, and accuracy. "
        "By the end of the module, the learner is expected to communicate simple information in French with clear purpose, appropriate tone, and beginner-level workplace readiness."
    ),
    "Laboratory": "Language and Computer Laboratory",
    "training_materials": "\n".join(
        [
            "French expression handouts",
            "Pronunciation guide sheets",
            "Dialogue and role-play cards",
            "Occupation and office vocabulary flashcards",
            "Pictures for descriptive speaking activities",
            "Whiteboard and markers",
            "Laptop or desktop computer",
            "Audio speaker or headset",
            "Printed worksheets and assessment checklists",
        ]
    ),
    "uc_no": 1,
    "unit_of_competency_1": all_units[0],
    "unit_of_competency_2": all_units[1],
    "unit_of_competency_3": all_units[2],
    "unit_of_competency_4": all_units[3],
    "module_title_1": all_modules[0],
    "module_title_2": all_modules[1],
    "module_title_3": all_modules[2],
    "module_title_4": all_modules[3],
    "unit_of_competency_code_1": "EDU-FLG-001",
    "unit_of_competency_code_2": "EDU-FLG-002",
    "unit_of_competency_code_3": "EDU-FLG-003",
    "unit_of_competency_code_4": "EDU-FLG-004",
    "LO_1": "Basic Communication",
    "LO_2": "Workplace Vocabulary",
    "LO_3": "Describing People and Objects",
    "Contents_1_1": "Greetings and Introductions",
    "Contents_1_2": "Common Courtesy Expressions",
    "Contents_1_3": "Basic Conversational Phrases",
    "Contents_2_1": "Jobs and Professions",
    "Contents_2_2": "Office Vocabulary",
    "Contents_2_3": "Workplace Roles",
    "Contents_3_1": "Adjectives Usage",
    "Contents_3_2": "Gender and Agreement",
    "Contents_3_3": "Physical Descriptions",
}

for entry in content_entries:
    slot = entry["field"]
    mcq_text, answer_text = mcq_block(entry["mcqs"])
    payload[f"Contents_{slot}_Key_Facts"] = rewritten_key_facts[slot] if slot in rewritten_key_facts else key_facts(entry)
    payload[f"Contents_{slot}_LE_MC"] = mcq_text
    payload[f"Contents_{slot}_LE_MC_Answer"] = answer_text
    payload[f"la_{slot}_title"] = entry["apply"]["title"]
    payload[f"la_{slot}_objective"] = entry["apply"]["objective"]
    payload[f"la_{slot}_sup_mat"] = entry["apply"]["sup_mat"]
    payload[f"la_{slot}_equipment_list"] = entry["apply"]["equipment"]
    payload[f"la_{slot}_steps_list"] = entry["apply"]["steps"]
    payload[f"la_{slot}_assessmentmethod"] = entry["apply"]["assessment"]
    for idx, criterion in enumerate(entry["apply"]["pcs"], start=1):
        payload[f"la_{slot}_pc{idx}"] = criterion


def validate(payload: dict) -> None:
    required = [
        "sector",
        "qualification_title",
        "unit_of_competency",
        "module_title",
        "next_unit_of_competency",
        "Module_Descriptor",
        "Laboratory",
        "training_materials",
        "uc_no",
    ]
    for key in required:
        assert str(payload.get(key, "")).strip(), f"Missing {key}"

    descriptor_wc = wc(payload["Module_Descriptor"])
    assert 80 <= descriptor_wc <= 120, f"Module_Descriptor must be 80-120 words, got {descriptor_wc}"
    assert payload["uc_no"] == 1

    for entry in content_entries:
        slot = entry["field"]
        facts = payload[f"Contents_{slot}_Key_Facts"]
        assert wc(facts) >= 600, f"Short key facts for {slot}"
        questions = [part for part in payload[f"Contents_{slot}_LE_MC"].split("\n\n") if part.strip()]
        answers = [line for line in payload[f"Contents_{slot}_LE_MC_Answer"].splitlines() if line.strip()]
        assert len(questions) == 10, f"Need 10 MCQs for {slot}"
        assert len(answers) == 10, f"Need 10 answers for {slot}"
        for i in range(1, 6):
            assert payload[f"la_{slot}_pc{i}"].strip(), f"Missing PC {slot}-{i}"


validate(payload)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
print(str(OUT))
