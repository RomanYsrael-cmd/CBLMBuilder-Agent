import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "state" / "payloads" / "HPC6_uc2_payload.json"


def wc(text: str) -> int:
    return len(text.split())


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


rewritten_key_facts = {
    "1_1": """Reflexive Verbs are essential for understanding simple French texts that describe daily routine because they show actions a person does to or for himself or herself. In beginner reading materials, these verbs appear frequently in short paragraphs about waking up, getting ready for work, preparing for class, and ending the day. The learner therefore needs to recognize not only the main verb, but also the reflexive marker that signals how the action is being performed. When a trainee reads a sentence such as Je me leve or Elle se prepare, the reflexive form provides structure that helps the reader understand the routine being described. This content is important because many texts about personal schedule and daily habits depend on these patterns. Without understanding reflexive verbs, the learner may identify some vocabulary words but still miss the meaning of the sentence as a whole.

The lesson begins by showing how common reflexive verbs operate in context. Examples include se lever, se laver, s'habiller, se reposer, and se coucher. The learner should observe how the verb changes with the subject and how the reflexive pronoun also changes accordingly. This is especially useful in reading because the pattern often reveals who is doing the action and what stage of the routine is being discussed. Beginner readers do not need to analyze every rule in abstract form before reading. However, they do need to spot the recurring structure quickly so that a short text about routine becomes easier to decode. In competency-based instruction, recognition is a practical skill. The learner should be able to see a reflexive form inside a sentence and connect it immediately with a familiar action in daily life.

A helpful reading example is a short paragraph about an employee's morning routine. The text may explain that the employee wakes up early, gets dressed, prepares for work, and rests after arriving home. If the learner recognizes the reflexive verbs in sequence, the paragraph becomes logically organized. The reader can tell which events happen first and which happen later. This kind of text is common in beginner French because it introduces vocabulary, time expressions, and sentence order in a manageable way. It also helps the learner predict meaning from context. Once one or two reflexive verbs are recognized, the rest of the routine often becomes easier to follow.

Teaching should combine form recognition with reading practice. Learners may highlight reflexive verbs in a short passage, match them with pictures of routine actions, and then answer simple comprehension questions. This approach is effective because it turns grammar into a reading aid rather than a separate memorization task only. The trainer should also point out that reflexive verbs may appear in workplace-related daily routines, such as preparing for duty, washing up before a task, or getting ready for a meeting. The content therefore supports both personal and work-oriented texts.

In workplace application, reflexive verbs help the learner understand staff routines, schedules, and simple written descriptions of preparation steps. A trainee may read a short dialogue about how a worker prepares for a shift or a simple note about daily habits during training. Common learner problems include noticing the main verb but ignoring the reflexive marker, confusing reflexive verbs with non-reflexive forms, or translating word by word without following the routine sequence. These errors can be reduced by repeated reading of short passages that use familiar actions in clear order.

By the end of this content, the learner should be able to recognize common reflexive verbs in French texts, connect them to daily routine meaning, and use them as clues for reading comprehension. The larger lesson is that sentence structure supports understanding. When the learner sees how reflexive verbs function in real reading passages, French texts about daily life become less intimidating and more predictable. That increased recognition helps build confidence in reading simple routine-based material.

The learner should also practice comparing two routine passages so that recurring reflexive patterns become easier to spot across different subjects and settings. When the same structure appears in a home routine, a class preparation routine, or a simple workday text, the learner begins to read with stronger anticipation. That anticipation is useful because it reduces hesitation and supports faster comprehension of beginner French passages.""",
    "1_2": """Telling Time is a practical reading skill because many simple French texts and dialogues include hours, schedules, and references to when an activity happens. The learner needs to understand not only number words, but also the patterns used when time is expressed in French. In texts about daily routine, workplace duty, study schedules, and appointments, time markers organize the sequence of events. If the learner cannot interpret time accurately, comprehension becomes incomplete even when other vocabulary is familiar. This content therefore trains the learner to read time expressions as functional details that explain when actions begin, continue, or end.

The lesson covers common forms such as Il est huit heures, a sept heures, midi, minuit, et quart, et demie, and moins le quart. The learner should also understand the difference between a direct statement of the current time and a phrase that indicates when something takes place. These patterns appear repeatedly in short passages and dialogues. A beginner text may describe a worker who starts at eight o'clock, takes lunch at noon, and ends duty in the late afternoon. A dialogue may involve asking what time a meeting begins or when someone returns. The learner should practice identifying these expressions quickly because time often controls the meaning of the entire passage.

A useful reading example is a short office schedule written in simple French. The schedule may indicate arrival time, break time, a meeting hour, and dismissal time. When the learner reads the text carefully, each time phrase provides a reference point for comprehension. The reader can determine which action comes first, whether a person is early or late, and how long the activity may last. This makes time vocabulary highly practical. Even if the passage uses simple grammar, the meaning can still be missed if the time references are not understood correctly.

Instruction in this content should combine visual clocks, printed schedules, and brief reading passages. Learners can match written time expressions with clock faces, underline time markers in a paragraph, and answer questions about sequence. This helps them move from isolated number recognition to full reading comprehension. The trainer should also include texts connected with work and study settings, because those environments frequently use explicit schedules. A passage about arrival time, break time, or meeting time mirrors the type of information learners may encounter in real life.

Workplace application is direct. Staff schedules, appointment slips, break notices, orientation plans, and timetable boards all rely on accurate reading of time expressions. A learner who understands these expressions in French can follow routine information more effectively. Common problems include confusing one time form with another, reading the numbers correctly but missing the sentence meaning, or ignoring smaller details such as quarter past and half past. Repetition through short texts and practical questions helps correct these errors.

By the end of this lesson, the trainee should be able to interpret common French time expressions in simple texts and dialogues and use them to understand sequence and schedule. The key idea is that time tells the reader how events are arranged. When learners read time accurately, they gain stronger control over routine passages, workplace information, and basic daily communication texts in French.

Another useful practice is comparing two schedules and explaining how the time references change the order of activities. This helps learners see that a small difference in hour or phrasing can alter the full meaning of a timetable or notice. Repeated reading of simple schedules strengthens both vocabulary retention and practical comprehension in work-related settings.

When learners answer questions such as what happens first, what happens next, and when a task ends, they begin using time expressions as reading tools rather than isolated vocabulary. This habit is especially valuable in workplace documents where a missed hour can cause misunderstanding, lateness, or incorrect sequencing of duties.""",
    "1_3": """Days and Months are basic reading elements that appear often in beginner French texts, especially those related to routine, schedule, planning, and simple personal information. The learner may see them in calendars, short notes, introductory passages, appointment messages, and dialogues about activities. Because they identify when something happens, these terms help the reader place information within a weekly or monthly pattern. This content is important not because the words are difficult by themselves, but because they connect with dates, schedules, frequency, and sequence. A learner who understands days and months can read routine texts more accurately and answer simple comprehension questions with greater confidence.

The lesson introduces the French names for the days of the week and the months of the year, together with common reading contexts such as lundi matin, en avril, le mardi, and au mois de janvier. The learner should notice that these terms often appear with prepositions and date expressions. They are not usually presented alone in real reading material. Instead, they support a larger message, such as when a class happens, when an appointment is scheduled, or when a report is due. Recognizing these terms helps the trainee identify time reference points and understand how a text is organized.

A realistic example is a short notice about a workplace meeting or training schedule. The note may explain that orientation takes place on Monday, a follow-up meeting happens on Wednesday, and a review session is planned in May. If the learner recognizes the day and month terms correctly, the message becomes easy to follow. The reader can answer questions about when the events happen and which event comes first. This kind of practical reading is more useful than memorizing the calendar words without context because it shows how they operate inside actual communication.

Teaching should involve calendars, date charts, mini-dialogues, and short reading activities. Learners can highlight day and month words in a passage, match them with calendar positions, and then identify related activities. This approach builds comprehension rather than rote recall alone. The trainer should also encourage learners to distinguish similar forms carefully and observe spelling patterns, because visual recognition is a major part of reading skill. When learners see the same date words across multiple short texts, retention becomes stronger and reading speed improves.

In workplace and training contexts, days and months appear in meeting schedules, leave notices, orientation calendars, training plans, and written reminders. A learner who understands them can interpret simple organizational information in French more effectively. Common difficulties include reading the day word but not connecting it to the event, confusing date order, or treating months as isolated vocabulary with no role in comprehension. These problems can be reduced by asking learners to answer practical questions from schedule-based texts instead of only reciting the terms.

By the end of this content, the learner should be able to recognize French day and month vocabulary in simple texts, interpret basic date-related information, and use those references to understand routine schedules and short written notices. The major lesson is that calendar language supports reading accuracy. When the trainee can place an event on the correct day or month, the whole text becomes easier to understand and use.

The learner should also practice moving between a written text and a visual calendar so that the connection between words and schedule becomes automatic. When a trainee reads lundi, jeudi, or octobre and immediately links the term to a calendar position and event, comprehension improves. This kind of reinforcement is especially useful for workplace notices, training plans, and short appointment messages.

Another good strategy is to ask the learner to sort several written events by day or month after reading a short passage. This encourages accurate scanning and helps the trainee connect calendar language with real planning. As a result, date-based texts become easier to interpret in both school and office contexts.""",
    "2_1": """Formal vs Informal Speech is a key reading topic because French dialogues often change tone according to the relationship between speakers. A learner reading a simple exchange must notice whether the language is polite, familiar, professional, or casual. This affects how the message should be understood. In workplace-related texts, formal language usually appears in respectful requests, customer contact, staff introductions, and communication with supervisors or visitors. Informal language, on the other hand, often appears between friends, close classmates, or familiar coworkers in relaxed settings. If the learner does not recognize this contrast, comprehension may be incomplete because the social meaning of the dialogue will be missed.

This lesson focuses on markers that signal register, such as the use of vous versus tu, polite request forms, titles, and different levels of directness. The learner should understand that formality is not only about grammar. It also reflects relationship, role, and context. A simple phrase can sound appropriate in one situation and too casual in another. In reading dialogues, these clues help the learner determine who is speaking to whom and what kind of setting is being represented. This is especially important in texts about work, service, and school situations where social boundaries influence language choice.

A helpful example is a comparison between two short dialogues. In one dialogue, a staff member speaks to a client using polite forms, respectful greetings, and structured requests. In the other, two classmates speak informally using familiar expressions. Even if both dialogues use basic vocabulary, the tone and relationship are different. The learner should be able to identify these differences and explain why one dialogue sounds more formal. This kind of comparison helps the reader see language as social behavior, not just as isolated words on the page.

Teaching should involve paired readings, register comparison charts, and comprehension questions that focus on tone. Learners can underline clues that show formality, identify the likely relationship of the speakers, and decide which setting the dialogue fits best. This helps transform reading into interpretation. The trainer should also include beginner workplace exchanges, because reading service-oriented dialogue requires awareness of appropriate speech level. When learners notice formal signals early, they become more prepared for polite spoken and written French later on.

Workplace application is strong in this content. Staff members often need to read dialogues or sample scripts for greeting customers, receiving visitors, replying to simple requests, or speaking with supervisors. Formal speech supports professionalism, while informal speech may be acceptable only in limited peer interaction. Common learner problems include assuming all beginner French sounds the same, missing the difference between tu and vous, or misunderstanding why a phrase is too direct in a customer-facing context. Guided reading and comparison activities help correct these habits.

By the end of this lesson, the learner should be able to recognize formal and informal language cues in simple French dialogues and use those cues to interpret relationship and setting. The main lesson is that reading comprehension includes tone. When learners understand register, they read dialogues more accurately and become better prepared to use French appropriately in real social and workplace communication.

Further reinforcement can be provided by asking learners to justify why a line sounds formal or informal instead of only labeling it. This deeper explanation builds awareness of pronouns, titles, requests, and tone markers. As learners improve, they become more capable of reading short dialogues with social understanding and not just literal word recognition.

This content also prepares the learner for practical judgment. When a short text is clearly workplace-based, the reader can anticipate that respectful forms are likely to appear. That expectation improves reading speed and helps the trainee interpret dialogue purpose more accurately, especially in customer-facing and office-based communication samples.""",
    "2_2": """Workplace Etiquette is an important reading topic because many short French texts about work are not only about tasks. They are also about behavior, politeness, respect, and proper conduct in professional situations. The learner may encounter simple dialogues, notices, reminders, or scenario-based reading passages that show how employees greet others, respond to requests, wait their turn, apologize, and follow respectful communication practices. Understanding these texts requires more than knowing the vocabulary. The learner must also recognize the behavioral expectation being described. This content supports that kind of interpretation.

The lesson introduces the language of polite conduct in workplace situations, including respectful greetings, courteous replies, waiting expressions, and behavior-based instructions. A short text may describe how an employee should welcome a visitor, how a trainee should ask permission before entering, or how a staff member should respond to a complaint calmly. The learner should read these messages as both language samples and behavior guides. This is useful because beginner French reading often includes practical, situational content rather than abstract literary passages. In these texts, etiquette provides the logic behind the words.

A realistic example is a short office reminder that explains how to receive guests properly. The passage may instruct staff to greet visitors politely, confirm the appointment, ask them to wait, and notify the correct officer. If the learner understands workplace etiquette vocabulary, the passage becomes meaningful and easy to follow. The reader can identify what actions are expected and why they matter. This kind of reading directly supports employability because it connects language with professional conduct.

Instruction should include workplace notices, mini-dialogues, and comprehension tasks that ask what behavior is being modeled. Learners can read a short passage and determine whether the employee acted politely, whether the language used was respectful, and what should happen next. This builds practical understanding. The trainer should also point out common etiquette cues in French, such as formal greetings, polite request forms, and controlled response language. These clues help the reader interpret a workplace text more accurately.

In workplace application, etiquette appears in reception scripts, customer service exchanges, office reminders, and orientation reading materials. An employee who can read these messages in French has a better chance of responding appropriately in real interaction. Common learner problems include focusing only on concrete nouns, missing the respectful tone of the message, or reading a polite instruction as if it were only a direct command. Repeated exposure to workplace scenarios helps the learner see how conduct and language work together.

By the end of this content, the learner should be able to read simple French texts about professional behavior and identify the etiquette principles being expressed. The central lesson is that workplace communication is not only about what people say, but also about how and why they say it. When the learner understands etiquette language in reading, French workplace texts become more practical, understandable, and useful.

The learner should also be trained to compare appropriate and inappropriate behavior within short workplace scenarios. This comparison makes etiquette language more memorable because the trainee can see the practical effect of respectful and disrespectful actions. That awareness strengthens both reading interpretation and future workplace readiness in French-mediated situations.

When the learner can point to a specific line in the text and explain why it reflects good etiquette, comprehension becomes more active and useful. This is the kind of reading skill that supports real training outcomes because it connects language, behavior, and professional expectation in one task.

As learners gain confidence, they should also practice identifying the consequence of poor etiquette in a short scenario. This develops interpretive reading because the trainee is no longer only finding polite words, but also understanding the professional impact of communication choices in workplace texts.""",
    "2_3": """Basic Dialogues are central to beginner reading because they show how French is used in short, interactive exchanges. Unlike single-sentence examples, dialogues require the learner to follow turn-taking, speaker intention, and the connection between one line and the next. In workplace communication, basic dialogues may involve greetings, requests, clarifications, instructions, visitor assistance, or simple customer contact. The learner must therefore read not only for word meaning, but also for the flow of interaction. This content helps the trainee understand how a conversation develops in a practical situation.

The lesson teaches learners to identify speakers, sequence of response, and the purpose of each line in a short exchange. A beginner dialogue may include a greeting, a question, a response, a clarification, and a closing line. Each part performs a communication function. When the learner sees that structure, reading becomes easier because the exchange follows a recognizable pattern. This is especially useful in workplace texts where the dialogue is built around a task, such as receiving a visitor, asking for help, or confirming a schedule. Understanding the pattern helps the trainee predict likely meaning and follow the conversation with less confusion.

A helpful example is a short conversation at a reception desk. One speaker arrives, gives a greeting, states the purpose of the visit, and asks to meet a staff member. The receptionist responds politely, checks the information, and asks the visitor to wait. The learner can answer questions such as who arrived, why the person came, and what the receptionist did next. This kind of activity shows how dialogue reading supports both language recognition and practical inference. The learner is not only translating words. The learner is following an interaction from beginning to end.

Teaching should involve dialogue strips, role labels, comprehension questions, and sequencing tasks. Learners may reorder a dialogue, match lines with speaker roles, and identify which sentence is the request or response. This strengthens understanding of conversation logic. The trainer should also encourage learners to pay attention to punctuation and cues such as question marks, greetings, and polite formulas, because these markers guide interpretation. When learners see how a dialogue is organized, they become more confident readers and better prepared speakers.

In workplace application, basic dialogue reading supports customer service preparation, front-desk assistance, team coordination, and simple office interaction. Many practical scripts are built as short exchanges. A learner who can read and understand them can participate more effectively in real communication later. Common difficulties include reading each line separately without linking them, losing track of who is speaking, or missing the purpose of the exchange. Repeated guided reading of short dialogues helps solve these problems by teaching the learner to track interaction logically.

By the end of this content, the trainee should be able to read and understand simple French dialogues by identifying speakers, sequence, and communicative purpose. The main lesson is that dialogue comprehension depends on connection. When the learner follows how one line leads to the next, French conversations become clearer and more manageable in both classroom and workplace contexts.

Another useful exercise is to remove one line from a dialogue and ask the learner to determine what kind of reply or question is missing. This strengthens awareness of how exchanges are constructed. When learners can predict the next line based on the situation, their reading comprehension becomes more active and their understanding of workplace communication improves.

This skill is helpful in customer service and office coordination because many real interactions follow familiar patterns. The more the learner reads short exchanges in complete sequence, the easier it becomes to recognize requests, responses, and outcomes in practical French communication.""",
    "3_1": """Days and Dates are essential for reading schedules, notices, appointment slips, and routine planning texts in French. While the learner may already know day names and month names individually, this content develops the ability to interpret complete date references in practical written material. A date in a reading passage does more than provide vocabulary. It tells the learner when an activity is arranged, whether something is current or upcoming, and how multiple events are organized. This is especially useful in workplace and training contexts, where appointments, deadlines, and meeting announcements depend on accurate reading of day-date combinations.

The lesson focuses on common written patterns such as lundi 12 mai, le 5 juin, and vendredi prochain, together with the way dates function inside simple sentences. The learner should notice that date references are often attached to events, instructions, or reminders. They do not appear as isolated items. A short text might say that a meeting will happen on Tuesday the tenth, that a report must be submitted on the twenty-third, or that orientation starts next Monday. These date cues give order to the message. If the learner misses the date, the main practical meaning of the text may be lost.

A useful example is a printed appointment notice for workplace orientation. The notice may show the day, the full date, the time, and the location. A learner who reads the date accurately can answer key questions: when should the person arrive, what comes first, and what event belongs to which day. This is the kind of real-world reading skill that supports functional French. The learner is not only identifying calendar words but also using them to understand an organized text.

Teaching should use calendars, appointment cards, mini-schedules, and short reading passages. Learners can underline dates in a notice, match them with calendar positions, and explain what activity belongs to each date. This makes the content practical and comprehension-based. The trainer should also include comparison exercises so learners do not confuse similar numerical forms or overlook prepositions that help frame the date. Repetition across different text types improves recognition and confidence.

In workplace application, days and dates appear in meeting reminders, training schedules, delivery notes, appointment records, and deadline messages. Employees need to read these references correctly to avoid errors in attendance, planning, and coordination. Common learner problems include reading the numbers without understanding the full date reference, missing the difference between day name and date number, or ignoring the event attached to the date. These errors can be corrected by using documents that closely resemble real notices and schedule entries.

By the end of this content, the learner should be able to recognize and interpret French day-date combinations in simple texts and use them to understand routine scheduling information. The larger lesson is that dates organize action. When the learner reads days and dates accurately, workplace and daily-life reading tasks become clearer, more useful, and easier to manage.

The learner benefits further when day-date references are practiced in different text types, such as notices, appointment cards, and short emails. This variety shows that the same reading skill transfers across workplace tasks. As recognition improves, the learner becomes more efficient in locating essential schedule information without rereading the whole message repeatedly.

The trainer can strengthen this by asking the learner to compare two dates in a text and explain which event happens sooner. This simple comparison develops accuracy and helps the learner process written schedule information more confidently in both academic and workplace settings.

With enough guided practice, the learner begins to notice date references quickly and use them as anchors for the entire message. That skill is valuable in any text where timing matters, including appointment reminders, activity plans, and workplace announcements.""",
    "3_2": """Frequency Adverbs help the learner understand how often an action happens in a French text. In reading passages about daily routine, work schedule, personal habit, or appointment pattern, words such as toujours, souvent, parfois, rarement, and jamais give important information about repetition and regularity. These adverbs do not simply decorate the sentence. They tell the learner whether something happens every day, happens from time to time, or almost never happens. This makes them important for comprehension because the meaning of a routine text can change significantly depending on the adverb used.

The lesson teaches the learner to notice frequency words within sentences and connect them with the activity being described. A simple reading passage may explain that a worker always arrives early, sometimes attends meetings in the afternoon, and rarely misses a schedule. The learner should read these adverbs as clues that explain habit and consistency. This is especially useful in daily routine texts because frequency words often help distinguish between ordinary activity and exception. They also help the learner answer comprehension questions more accurately.

A practical example is a short paragraph about an employee's weekly schedule. The passage may state that the employee often checks messages in the morning, sometimes assists at reception, and never leaves before completing the required report. The learner who recognizes these adverbs can understand the worker's usual behavior more clearly. Without them, the passage would still contain actions, but the pattern of those actions would remain unclear. This is why frequency adverbs are valuable reading markers in simple French texts.

Teaching should include short habit-based passages, charts of adverb meaning, and comprehension questions that ask how often an event occurs. Learners can highlight the adverb, identify the related verb, and explain the habit in simple terms. This approach turns a small grammar item into a practical reading strategy. The trainer should also present frequency adverbs in workplace scenarios because professional routines often depend on repeated activity such as checking schedules, attending meetings, or responding to routine concerns.

In workplace application, frequency adverbs appear in instructions, routine reports, staff descriptions, and simple dialogues about work habits. A learner who reads them well can better understand expectations and patterns. Common learner errors include skipping the adverb while focusing only on the main action, confusing one frequency word with another, or assuming every routine text describes a daily event. Repeated exposure to short texts with clear contrasts helps correct these issues.

By the end of this content, the learner should be able to identify frequency adverbs in simple French reading passages and interpret what they reveal about routine and habit. The main lesson is that frequency changes meaning. When learners pay attention to how often an action happens, they gain a more accurate understanding of the text and improve their overall reading comprehension.

It is also helpful to compare several adverbs in one passage and discuss how each one changes the impression of the routine. A worker who always performs a task creates a different reading meaning from one who sometimes or rarely performs it. This contrast trains the learner to notice precision in simple texts and strengthens practical comprehension.

Another good reinforcement activity is to sort actions according to how often they happen after reading a short paragraph. By doing this, the learner practices connecting each adverb with the right event. This improves accuracy and prevents the reader from overlooking small words that carry important meaning.

Over time, this skill helps the learner read routine descriptions with better judgment. Instead of seeing a list of actions only, the learner begins to understand pattern, repetition, and exception. That deeper reading supports clearer answers to comprehension questions and better interpretation of workplace habits.""",
    "3_3": """Scheduling Expressions are important because they help the learner interpret how plans are arranged in French texts and dialogues. In simple workplace or daily-life reading materials, expressions for confirming, moving, fixing, or discussing schedules appear often. A reader may encounter phrases that indicate an appointment has been arranged, a meeting has been moved, or a time has been proposed. Understanding these expressions allows the learner to follow planning information instead of only recognizing isolated words. This content is therefore highly practical for reading tasks connected with routine coordination.

The lesson covers expressions commonly used in scheduling contexts, such as taking an appointment, setting a meeting, confirming availability, and indicating before or after a given time. The learner should pay attention to how these expressions function within a short message or dialogue. Often, the expression is the key to understanding the speaker's intention. A sentence may not simply report time. It may propose, confirm, postpone, or coordinate an activity. Recognizing that function helps the reader interpret the whole exchange more accurately.

A useful example is a short dialogue between two office workers arranging a meeting. One proposes a day, the other asks for another time, and both agree on a final schedule. The learner should be able to identify which line proposes the appointment, which line changes the plan, and which line confirms the final arrangement. This kind of reading goes beyond vocabulary recognition. It requires the learner to track planning language and notice how scheduling decisions are expressed. Because many beginner workplace dialogues revolve around simple coordination, this skill has immediate value.

Teaching should include appointment notes, schedule adjustment dialogues, and reading questions about what was planned, changed, or confirmed. Learners can underline scheduling expressions, connect them to the relevant time reference, and then explain the result of the exchange. This method helps the learner see that scheduling language is action-oriented. The text is usually trying to arrange something, not just describe it. That insight improves reading speed and practical comprehension.

In workplace application, scheduling expressions appear in meeting reminders, appointment confirmations, training notices, and coordination messages. Employees need to understand whether an event is fixed, delayed, rescheduled, or still being arranged. Common learner problems include focusing only on the day or hour while missing the planning expression, misreading whether the schedule is confirmed or proposed, or overlooking who is available and when. Guided reading of short schedule-focused dialogues helps reduce these problems and builds confidence.

By the end of this content, the learner should be able to identify common French scheduling expressions in simple texts and dialogues and use them to understand how plans are organized. The central lesson is that schedule reading depends on intention as well as time. When the learner sees whether a plan is being proposed, changed, or confirmed, the message becomes far more useful and understandable.

Learners should also practice tracing the final result of a scheduling exchange so they do not stop at the first proposed time. In many workplace dialogues, the first plan changes before the speakers agree. Recognizing that final arrangement is an important reading skill because it helps the trainee determine the actual schedule rather than the initial suggestion.

This is especially useful when reading coordination messages in training and office settings, where a revised plan may be the only one that matters operationally. When learners focus on the final confirmed arrangement, their reading becomes more practical, accurate, and aligned with real workplace needs.

The trainer can reinforce this skill by asking the learner to summarize the final schedule in one sentence after reading the full exchange. This encourages attention to outcome and helps prevent confusion between a proposed idea and the actual agreed plan.""",
}


content_entries = [
    {
        "field": "1_1",
        "title": "Reflexive Verbs",
        "apply": {
            "title": "Identify Reflexive Verbs in a Routine Passage",
            "objective": "Read a short French passage on daily routine and identify reflexive verbs accurately with their routine meaning.",
            "sup_mat": "Routine reading passage\nVerb recognition worksheet\nHighlighter",
            "equipment": "Printed handout\nPen\nDictionary or vocabulary guide",
            "steps": "1. Read the routine passage silently.\n2. Underline all reflexive verb forms.\n3. Match each verb with the action it expresses.\n4. Answer comprehension questions about sequence.\n5. Read the passage aloud with guidance.\n6. Review corrections with the trainer.",
            "assessment": "Reading comprehension and grammar recognition task using an observation checklist.",
            "pcs": [
                "Identified reflexive verbs correctly in the passage.",
                "Matched each reflexive form with its meaning.",
                "Used context to understand the daily routine sequence.",
                "Answered comprehension questions accurately.",
                "Completed the task with minimal assistance.",
            ],
        },
        "mcqs": [
            {"q": "Why are reflexive verbs important in routine texts?", "options": ["They often describe personal daily actions", "They replace all nouns", "They show only time", "They remove sentence order"], "answer": "A"},
            {"q": "Which type of passage often uses reflexive verbs?", "options": ["Daily routine passages", "Mathematics formulas", "Sports scores only", "Maps only"], "answer": "A"},
            {"q": "What should a learner notice besides the main verb?", "options": ["The reflexive marker", "The page color", "The paper size", "The font only"], "answer": "A"},
            {"q": "A common beginner text may describe", "options": ["waking up and getting ready", "advanced debate only", "scientific experiment only", "music theory only"], "answer": "A"},
            {"q": "Why does recognizing reflexive verbs improve reading?", "options": ["It helps the learner understand the action sequence", "It removes the need for comprehension", "It changes French into English", "It avoids all grammar"], "answer": "A"},
            {"q": "Which classroom activity supports this content?", "options": ["Highlighting reflexive verbs in a passage", "Ignoring the text", "Studying months only", "Counting punctuation only"], "answer": "A"},
            {"q": "What may happen if the reflexive marker is ignored?", "options": ["The sentence meaning may be misunderstood", "The clock changes", "The date disappears", "The page becomes blank"], "answer": "A"},
            {"q": "Reflexive verbs are useful in reading about", "options": ["personal and workplace routines", "weather maps only", "paint colors only", "song titles only"], "answer": "A"},
            {"q": "Which skill does this content strengthen most directly?", "options": ["Reading comprehension of routine actions", "Drawing ability", "Typing speed", "Mathematical calculation"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["spot reflexive forms and explain the routine", "memorize one word only", "skip comprehension questions", "avoid context"], "answer": "A"},
        ],
    },
    {
        "field": "1_2",
        "title": "Telling Time",
        "apply": {
            "title": "Read Time Expressions in a Schedule",
            "objective": "Interpret French time expressions in a short daily or workplace schedule and answer related questions correctly.",
            "sup_mat": "Schedule reading sheet\nClock visuals\nQuestion set",
            "equipment": "Printed activity sheet\nPen\nWall clock or visual clock chart",
            "steps": "1. Review the written time expressions in French.\n2. Read the schedule carefully.\n3. Match each written time with the correct event.\n4. Answer questions on sequence and timing.\n5. Explain one schedule entry orally.\n6. Check answers with the trainer.",
            "assessment": "Schedule-reading exercise with oral follow-up and checklist.",
            "pcs": [
                "Recognized common time expressions correctly.",
                "Connected each time with the proper activity.",
                "Used time references to understand sequence.",
                "Answered reading questions accurately.",
                "Explained schedule details clearly.",
            ],
        },
        "mcqs": [
            {"q": "Why are time expressions important in reading?", "options": ["They organize events in a text", "They replace verbs", "They identify colors", "They remove sequence"], "answer": "A"},
            {"q": "What can a learner understand from time expressions?", "options": ["When an action happens", "Only who is speaking", "Only the place name", "Only the title"], "answer": "A"},
            {"q": "Which document often requires reading time correctly?", "options": ["A schedule", "A drawing only", "A flag chart", "A map legend"], "answer": "A"},
            {"q": "If time is misunderstood, the learner may miss", "options": ["the order of events", "all French nouns", "every greeting", "all punctuation"], "answer": "A"},
            {"q": "Which classroom tool supports this lesson?", "options": ["Clock visuals", "Paintbrush only", "Calculator only", "Compass only"], "answer": "A"},
            {"q": "Time expressions in French help the learner read", "options": ["daily routine and workplace texts", "only songs", "only stories about animals", "only recipes"], "answer": "A"},
            {"q": "What does a schedule entry connect?", "options": ["A time and an activity", "A color and a number", "A noun and a picture only", "A title and a page"], "answer": "A"},
            {"q": "A good reading activity for this content is", "options": ["matching times to events", "skipping the text", "memorizing one hour only", "avoiding questions"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["interpret time references in a text", "ignore all schedules", "list months only", "avoid sequence"], "answer": "A"},
            {"q": "Which phrase best completes this idea: time tells the reader", "options": ["how events are arranged", "how to draw a picture", "what color to choose", "where to buy a pen"], "answer": "A"},
        ],
    },
    {
        "field": "1_3",
        "title": "Days and Months",
        "apply": {
            "title": "Interpret Calendar References in a Short Text",
            "objective": "Read French day and month references in a simple note or schedule and identify the related events correctly.",
            "sup_mat": "Mini-calendar\nShort schedule text\nComprehension worksheet",
            "equipment": "Printed handout\nPen\nCalendar chart",
            "steps": "1. Review French day and month names.\n2. Read the short text or note.\n3. Underline day and month references.\n4. Match each reference with its event.\n5. Answer comprehension questions.\n6. Check responses with the trainer.",
            "assessment": "Calendar-based reading activity with checklist scoring.",
            "pcs": [
                "Recognized day and month references accurately.",
                "Linked calendar words to the correct event.",
                "Used date clues to understand the message.",
                "Answered reading questions correctly.",
                "Completed the activity in logical sequence.",
            ],
        },
        "mcqs": [
            {"q": "Why are days and months important in reading?", "options": ["They help place events in time", "They replace dialogues", "They remove dates", "They identify furniture"], "answer": "A"},
            {"q": "Where do days and months often appear?", "options": ["Schedules and notices", "Paint labels only", "Number games only", "Shape charts only"], "answer": "A"},
            {"q": "What should the learner connect with a day or month word?", "options": ["The related activity", "Only pronunciation", "Only handwriting", "Only page order"], "answer": "A"},
            {"q": "A useful classroom support for this lesson is", "options": ["A calendar chart", "A ruler only", "A camera only", "A calculator only"], "answer": "A"},
            {"q": "What happens when a learner recognizes calendar terms in context?", "options": ["The text becomes easier to follow", "All grammar disappears", "The page becomes shorter", "The dialogue stops"], "answer": "A"},
            {"q": "Which task supports this content?", "options": ["Matching dates with events", "Ignoring the schedule", "Memorizing one month only", "Avoiding comprehension"], "answer": "A"},
            {"q": "Why should day and month words be studied in context?", "options": ["Because they support full message understanding", "Because they are never used in texts", "Because they replace nouns", "Because they are only decorative"], "answer": "A"},
            {"q": "In workplace reading, day and month words may appear in", "options": ["meeting and training schedules", "sports uniforms only", "recipe ingredients only", "music scales only"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["interpret calendar references in a short text", "avoid reading dates", "skip schedule details", "read only titles"], "answer": "A"},
            {"q": "What is the main reading value of calendar language?", "options": ["It organizes routine information", "It changes verbs to nouns", "It removes questions", "It shows furniture names"], "answer": "A"},
        ],
    },
    {
        "field": "2_1",
        "title": "Formal vs Informal Speech",
        "apply": {
            "title": "Compare Formal and Informal Dialogues",
            "objective": "Read two short French dialogues and identify which one uses formal workplace language and which one uses informal speech.",
            "sup_mat": "Dialogue comparison sheet\nRegister guide\nQuestionnaire",
            "equipment": "Printed dialogues\nPen\nHighlighter",
            "steps": "1. Read both dialogues carefully.\n2. Underline clues showing speech level.\n3. Identify formal and informal lines.\n4. Match each dialogue with the correct setting.\n5. Answer questions on speaker relationship.\n6. Review the register differences with the trainer.",
            "assessment": "Dialogue comparison exercise with checklist and oral explanation.",
            "pcs": [
                "Identified clues of formal speech correctly.",
                "Recognized features of informal speech accurately.",
                "Matched the dialogue to the proper setting.",
                "Explained the speaker relationship clearly.",
                "Completed the task with acceptable accuracy.",
            ],
        },
        "mcqs": [
            {"q": "Why is speech level important in dialogue reading?", "options": ["It helps show relationship and setting", "It replaces vocabulary", "It removes greetings", "It changes the date"], "answer": "A"},
            {"q": "Which contrast is central to this lesson?", "options": ["formal and informal language", "big and small objects", "past and future only", "open and closed doors"], "answer": "A"},
            {"q": "What can register clues help the learner understand?", "options": ["who is speaking to whom", "only the page number", "only the room color", "only the document length"], "answer": "A"},
            {"q": "Which setting usually requires formal speech?", "options": ["customer or supervisor interaction", "chat with a close friend", "personal diary only", "sports cheering"], "answer": "A"},
            {"q": "What is a good classroom activity for this topic?", "options": ["comparing two dialogues", "counting chairs", "drawing clocks only", "sorting colors only"], "answer": "A"},
            {"q": "A learner who ignores register may miss", "options": ["the social meaning of the dialogue", "all numbers", "all adjectives", "all verbs"], "answer": "A"},
            {"q": "Formal vs informal speech supports reading of", "options": ["workplace and social dialogues", "weather maps only", "recipes only", "math charts only"], "answer": "A"},
            {"q": "What should the learner identify in each dialogue?", "options": ["the tone and likely relationship", "the paper type", "the table size", "the ink color"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["recognize register cues in context", "ignore all tone differences", "memorize only greetings", "avoid dialogue reading"], "answer": "A"},
            {"q": "The main value of this content is that it teaches reading for", "options": ["tone as well as meaning", "paper quality only", "time only", "spelling only"], "answer": "A"},
        ],
    },
    {
        "field": "2_2",
        "title": "Workplace Etiquette",
        "apply": {
            "title": "Read a Workplace Etiquette Notice",
            "objective": "Interpret a short French workplace etiquette text and identify the expected professional behavior correctly.",
            "sup_mat": "Etiquette notice\nBehavior checklist\nComprehension questions",
            "equipment": "Printed notice\nPen\nHighlighter",
            "steps": "1. Read the etiquette notice silently.\n2. Highlight words showing polite conduct.\n3. Identify the expected staff behavior.\n4. Answer comprehension questions.\n5. Explain one rule in your own words.\n6. Review corrections with the trainer.",
            "assessment": "Reading and interpretation task using a checklist-based evaluation.",
            "pcs": [
                "Recognized etiquette language in the text.",
                "Identified the expected workplace behavior correctly.",
                "Used context to interpret the message accurately.",
                "Answered comprehension questions clearly.",
                "Explained the professional rule appropriately.",
            ],
        },
        "mcqs": [
            {"q": "Why is workplace etiquette important in reading?", "options": ["It shows expected professional behavior", "It replaces time expressions", "It removes dialogue", "It only names objects"], "answer": "A"},
            {"q": "What may a workplace etiquette text include?", "options": ["polite conduct and respectful actions", "weather symbols only", "sports statistics only", "music notes only"], "answer": "A"},
            {"q": "A learner should read etiquette texts as", "options": ["language samples and behavior guides", "decoration only", "random vocabulary only", "silent grammar charts only"], "answer": "A"},
            {"q": "Which setting often uses etiquette language?", "options": ["office and customer service situations", "playground games only", "art gallery labels only", "science formulas only"], "answer": "A"},
            {"q": "What helps learners interpret etiquette texts?", "options": ["noticing respectful tone and actions", "ignoring context", "skipping the verbs", "counting letters"], "answer": "A"},
            {"q": "A useful activity for this lesson is", "options": ["reading a workplace notice and identifying the rule", "avoiding all text", "memorizing one noun only", "drawing a map"], "answer": "A"},
            {"q": "If the learner misses the etiquette meaning, the learner may miss", "options": ["why the message matters", "the size of the paper", "the ink brand", "the page margin"], "answer": "A"},
            {"q": "Workplace etiquette texts connect language with", "options": ["professional conduct", "painting skill", "mathematical formulas", "sports drills"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["identify expected behavior from the text", "ignore the tone", "avoid comprehension questions", "read only the title"], "answer": "A"},
            {"q": "The central reading value of etiquette language is that it explains", "options": ["how people should act professionally", "how clocks work", "how colors mix", "how tools are stored"], "answer": "A"},
        ],
    },
    {
        "field": "2_3",
        "title": "Basic Dialogues",
        "apply": {
            "title": "Analyze a Short Workplace Dialogue",
            "objective": "Read a simple French workplace dialogue and identify the speakers, purpose, and sequence of the exchange.",
            "sup_mat": "Dialogue sheet\nSpeaker labels\nComprehension checklist",
            "equipment": "Printed dialogue\nPen\nHighlighter",
            "steps": "1. Read the dialogue from beginning to end.\n2. Mark each speaker's lines.\n3. Identify the purpose of each major line.\n4. Answer questions on sequence and outcome.\n5. Read the dialogue aloud with a partner.\n6. Review the answers with the trainer.",
            "assessment": "Dialogue reading and interpretation task with performance checklist.",
            "pcs": [
                "Identified the speakers correctly.",
                "Recognized the purpose of the main lines.",
                "Followed the dialogue sequence accurately.",
                "Answered comprehension questions based on the exchange.",
                "Read the dialogue with logical understanding.",
            ],
        },
        "mcqs": [
            {"q": "Why are dialogues important in reading?", "options": ["They show interaction in sequence", "They replace vocabulary", "They remove speakers", "They only show punctuation"], "answer": "A"},
            {"q": "What should a learner identify in a dialogue?", "options": ["the speakers and their purpose", "only the title", "only the paper size", "only the final word"], "answer": "A"},
            {"q": "A short workplace dialogue may involve", "options": ["requests and polite responses", "weather charts only", "painting steps only", "sports scoring only"], "answer": "A"},
            {"q": "Which task best supports dialogue reading?", "options": ["matching lines with speaker roles", "ignoring the sequence", "memorizing one greeting only", "skipping the questions"], "answer": "A"},
            {"q": "Why is sequence important in a dialogue?", "options": ["because one line leads to the next", "because all lines are separate", "because sequence is optional", "because only the last line matters"], "answer": "A"},
            {"q": "What happens if a learner reads each line in isolation?", "options": ["The interaction may be misunderstood", "The time becomes clearer", "The date changes", "The page shrinks"], "answer": "A"},
            {"q": "What can comprehension questions ask about?", "options": ["who said what and why", "only the room size", "only handwriting style", "only font choice"], "answer": "A"},
            {"q": "Dialogues are practical for preparing learners for", "options": ["real communication situations", "silent drawing only", "number drills only", "map reading only"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["follow the dialogue logically", "ignore the speakers", "avoid the context", "read only nouns"], "answer": "A"},
            {"q": "The main value of dialogue reading is understanding", "options": ["connected interaction", "paper texture", "ink color", "page order only"], "answer": "A"},
        ],
    },
    {
        "field": "3_1",
        "title": "Days and Dates",
        "apply": {
            "title": "Read a French Appointment Date Notice",
            "objective": "Interpret day-and-date combinations in a simple French notice and identify the related appointment details accurately.",
            "sup_mat": "Appointment notice\nCalendar worksheet\nQuestion set",
            "equipment": "Printed notice\nPen\nCalendar chart",
            "steps": "1. Read the notice carefully.\n2. Underline all day-and-date expressions.\n3. Match each date with the correct event or task.\n4. Answer questions about timing and order.\n5. Explain the appointment details orally.\n6. Review answers with the trainer.",
            "assessment": "Date-based reading activity checked through a performance checklist.",
            "pcs": [
                "Recognized day-and-date combinations correctly.",
                "Linked date expressions with the correct event.",
                "Used the date information to understand the notice.",
                "Answered timing questions accurately.",
                "Presented the appointment details clearly.",
            ],
        },
        "mcqs": [
            {"q": "Why are days and dates important in reading?", "options": ["They help organize appointments and events", "They replace dialogue lines", "They remove months", "They only show colors"], "answer": "A"},
            {"q": "Where are day-and-date expressions commonly found?", "options": ["notices and schedules", "sports uniforms only", "music lessons only", "kitchen labels only"], "answer": "A"},
            {"q": "A learner should connect a day-date expression with", "options": ["the event it refers to", "the paper color", "the desk height", "the pen brand"], "answer": "A"},
            {"q": "What is a good learning support for this lesson?", "options": ["a calendar worksheet", "a compass only", "a calculator only", "a paint chart only"], "answer": "A"},
            {"q": "If the learner misses the date, what may happen?", "options": ["the practical meaning of the notice may be lost", "the paper becomes blank", "the dialogue ends", "all verbs disappear"], "answer": "A"},
            {"q": "Which task supports this reading content?", "options": ["matching dates to appointments", "skipping the notice", "memorizing one number only", "ignoring sequence"], "answer": "A"},
            {"q": "Day-and-date reading is useful in", "options": ["workplace planning and coordination", "painting only", "sports only", "music only"], "answer": "A"},
            {"q": "What should the learner answer after reading the notice?", "options": ["when the event happens", "what color the paper is", "how the font looks", "who printed the page"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["interpret complete date references", "ignore calendar clues", "read only month names", "avoid notices"], "answer": "A"},
            {"q": "The central lesson of this content is that dates", "options": ["organize action in a text", "replace all nouns", "remove time", "only decorate the page"], "answer": "A"},
        ],
    },
    {
        "field": "3_2",
        "title": "Frequency Adverbs",
        "apply": {
            "title": "Interpret Habit Information Using Frequency Adverbs",
            "objective": "Read a short French passage and identify how often actions occur using frequency adverbs correctly.",
            "sup_mat": "Habit passage\nAdverb chart\nComprehension worksheet",
            "equipment": "Printed reading text\nPen\nHighlighter",
            "steps": "1. Read the habit-based passage.\n2. Highlight all frequency adverbs.\n3. Connect each adverb with the correct action.\n4. Answer questions on routine and habit.\n5. Summarize one habit from the text.\n6. Review the responses with the trainer.",
            "assessment": "Reading comprehension activity with frequency analysis and checklist.",
            "pcs": [
                "Identified frequency adverbs correctly.",
                "Matched each adverb with the related action.",
                "Used adverbs to interpret routine meaning accurately.",
                "Answered comprehension questions clearly.",
                "Summarized habit information correctly.",
            ],
        },
        "mcqs": [
            {"q": "Why are frequency adverbs important in reading?", "options": ["They show how often an action happens", "They replace all verbs", "They remove sequence", "They only show names"], "answer": "A"},
            {"q": "Which type of passage often uses frequency adverbs?", "options": ["routine or habit passages", "geometry formulas only", "tool catalogs only", "map legends only"], "answer": "A"},
            {"q": "What should a learner connect with the adverb?", "options": ["the action it modifies", "the paper size", "the page number only", "the handwriting"], "answer": "A"},
            {"q": "Why does this content improve comprehension?", "options": ["It clarifies habit and regularity", "It removes all grammar", "It changes nouns to verbs", "It ends the dialogue"], "answer": "A"},
            {"q": "A good classroom activity is", "options": ["highlighting adverbs in a passage", "ignoring the text", "memorizing one adverb only", "counting letters"], "answer": "A"},
            {"q": "What may happen if the adverb is skipped?", "options": ["The meaning of the routine may be misunderstood", "The date changes", "The room closes", "The worksheet tears"], "answer": "A"},
            {"q": "Frequency adverbs help the learner understand", "options": ["habit patterns", "desk arrangement only", "paper color only", "font size only"], "answer": "A"},
            {"q": "In workplace reading, they may appear in", "options": ["routine reports and schedule descriptions", "painting guides only", "weather charts only", "sports tickets only"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["interpret how often actions occur", "ignore adverbs", "read only nouns", "avoid passages"], "answer": "A"},
            {"q": "The main lesson is that frequency changes", "options": ["the meaning of a routine text", "the paper color", "the table size", "the room label"], "answer": "A"},
        ],
    },
    {
        "field": "3_3",
        "title": "Scheduling Expressions",
        "apply": {
            "title": "Read a Schedule Coordination Dialogue",
            "objective": "Interpret scheduling expressions in a short French dialogue and determine what plan was proposed, changed, or confirmed.",
            "sup_mat": "Coordination dialogue\nPlanning guide\nQuestion sheet",
            "equipment": "Printed dialogue\nPen\nHighlighter",
            "steps": "1. Read the schedule coordination dialogue.\n2. Underline scheduling expressions.\n3. Identify which line proposes the plan.\n4. Identify any change or confirmation in the dialogue.\n5. Answer comprehension questions.\n6. Discuss the final schedule with the trainer.",
            "assessment": "Dialogue-reading task with planning interpretation and checklist.",
            "pcs": [
                "Recognized scheduling expressions correctly.",
                "Identified proposed plans accurately.",
                "Detected changes or confirmations in the dialogue.",
                "Answered comprehension questions based on planning details.",
                "Explained the final schedule clearly.",
            ],
        },
        "mcqs": [
            {"q": "Why are scheduling expressions important in reading?", "options": ["They show how plans are arranged", "They replace all dates", "They remove dialogue", "They only identify rooms"], "answer": "A"},
            {"q": "What should a learner understand besides the time?", "options": ["the planning intention", "the paper size", "the font type", "the ink color"], "answer": "A"},
            {"q": "Which text often uses scheduling expressions?", "options": ["appointment and meeting dialogues", "sports posters only", "color charts only", "science diagrams only"], "answer": "A"},
            {"q": "A learner should identify whether a plan is", "options": ["proposed, changed, or confirmed", "painted, erased, or folded", "printed, cut, or glued", "numbered, colored, or boxed"], "answer": "A"},
            {"q": "What is a useful classroom activity for this content?", "options": ["underlining planning expressions in a dialogue", "ignoring the message", "memorizing one day only", "drawing clocks only"], "answer": "A"},
            {"q": "Why can a scheduling text be misunderstood?", "options": ["because the learner may miss the planning expression", "because French has no schedule words", "because all lines are identical", "because dates are never used"], "answer": "A"},
            {"q": "What practical value does this content have?", "options": ["It helps interpret coordination messages", "It teaches painting", "It replaces reading", "It removes sequence"], "answer": "A"},
            {"q": "Scheduling expressions often appear in", "options": ["meeting reminders and confirmations", "sports chants only", "food recipes only", "music scales only"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["explain the final arranged plan", "ignore the dialogue purpose", "read only hours", "avoid schedule texts"], "answer": "A"},
            {"q": "The central lesson is that schedule reading depends on", "options": ["intention as well as time", "paper quality only", "room color only", "pen type only"], "answer": "A"},
        ],
    },
]


payload = {
    "sector": "EDU",
    "qualification_title": qualification_title,
    "unit_of_competency": all_units[1],
    "module_title": all_modules[1],
    "next_unit_of_competency": all_units[2],
    "Module_Descriptor": (
        "This module develops the learner's ability to read and understand simple French texts and dialogues used in daily routine and workplace situations. "
        "It covers reading cues related to reflexive verbs, time, calendar references, speech level, workplace etiquette, basic dialogue structure, date expressions, frequency adverbs, and scheduling language. "
        "The trainee interprets short passages, notices, schedules, and practical exchanges to identify meaning, sequence, tone, and planning details. "
        "By the end of the module, the learner is expected to read beginner-level French texts with improved comprehension, contextual awareness, and readiness for routine communication tasks."
    ),
    "Laboratory": "Language and Computer Laboratory",
    "training_materials": "\n".join(
        [
            "Short French reading passages",
            "Dialogue comparison sheets",
            "Calendar and schedule worksheets",
            "Clock visuals and date charts",
            "Workplace notice samples",
            "Comprehension question sheets",
            "Highlighters and pens",
            "Laptop or desktop computer",
            "Printed assessment checklists",
        ]
    ),
    "uc_no": 2,
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
    "LO_1": "Daily Routine and Time",
    "LO_2": "Workplace Communication",
    "LO_3": "Talking About Schedules",
    "Contents_1_1": "Reflexive Verbs",
    "Contents_1_2": "Telling Time",
    "Contents_1_3": "Days and Months",
    "Contents_2_1": "Formal vs Informal Speech",
    "Contents_2_2": "Workplace Etiquette",
    "Contents_2_3": "Basic Dialogues",
    "Contents_3_1": "Days and Dates",
    "Contents_3_2": "Frequency Adverbs",
    "Contents_3_3": "Scheduling Expressions",
}

for entry in content_entries:
    slot = entry["field"]
    mcq_text, answer_text = mcq_block(entry["mcqs"])
    payload[f"Contents_{slot}_Key_Facts"] = rewritten_key_facts[slot]
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
    assert payload["uc_no"] == 2

    for entry in content_entries:
        slot = entry["field"]
        facts = payload[f"Contents_{slot}_Key_Facts"]
        assert wc(facts) >= 600, f"Short key facts for {slot}: {wc(facts)}"
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
