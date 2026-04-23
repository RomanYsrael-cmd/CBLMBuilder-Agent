import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "state" / "payloads" / "HPC6_uc3_payload.json"


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
    "1_1": """Making and Receiving Calls develops the learner's ability to write short French telephone messages and simple call-related notes with clarity and purpose. In beginner workplace communication, a call is often followed by a written record. Someone may need to note who called, why the person called, whether a reply is needed, and what follow-up action should happen next. For that reason, this content is not limited to speaking on the phone. It also supports accurate written communication after the call. When learners understand how telephone exchanges are organized, they can write short message slips, call summaries, and communication notes that reflect the essential details of a conversation.

The lesson begins by showing the common structure of a call situation. A caller identifies himself or herself, asks for a person, states a purpose, leaves a number or message, and sometimes asks for a return call. The learner should recognize that each part can be converted into writing. A short French note may record the caller's name, time of call, reason for the call, and requested action. In practical terms, this means writing only the useful information, not copying every spoken line. The trainee should therefore learn to extract key details from a telephone scenario and represent them in concise French sentences or note fragments that remain understandable to another reader.

A useful example is a front-desk or office setting where a staff member answers a telephone call for a supervisor who is unavailable. The caller asks to speak with the supervisor, explains that a meeting time must be changed, and leaves a request for a return call. The staff member then writes a note in French. If the learner understands the flow of the call, the message can be written logically: who called, what the concern was, and what response is expected. This shows how telephone communication and note writing are connected. A poorly written note may omit the action needed, while a well-written one supports efficient follow-up.

Instruction should therefore combine simple telephone scenarios with written recording tasks. Learners can listen to or read a model call, identify the essential information, and rewrite that information as a short office message. The trainer should encourage accuracy, brevity, and readable organization. Short written telephone messages do not require long paragraphs. However, they do require correct information selection and basic French sentence control. Learners also benefit from practicing formal tone because many workplace calls involve polite business communication rather than casual conversation.

In workplace application, this content is highly practical. Offices, reception desks, clinics, schools, and service points often rely on written message-taking after calls. A learner who can write a short, accurate French phone note becomes more effective in coordination tasks. Common problems include writing too much irrelevant detail, omitting the action requested, confusing the name of the caller with the person being called, or failing to state whether a return call is needed. These errors can be reduced through repeated practice with realistic call scenarios and message forms.

By the end of this content, the learner should be able to write a short French note based on a telephone situation and include the key details needed for follow-up. The central lesson is that effective call writing depends on selection and clarity. When the trainee can convert a spoken interaction into a simple written message, French becomes a practical tool for workplace communication and daily coordination.

The learner should also practice distinguishing between urgent and routine calls when writing a message. This helps the trainee decide what information should appear first in the note and what kind of response is needed. With repeated scenario work, learners become more confident in handling call-based communication and in writing short French notes that are useful to another reader immediately.""",
    "1_2": """Telephone Expressions are important because they provide the fixed language patterns learners need when writing short call-related messages, reminders, and communication notes in French. In beginner courses, students often focus on general vocabulary, but telephone situations require specific phrases. Expressions for answering, requesting, asking someone to wait, saying a person is unavailable, and asking for a callback appear repeatedly in phone-based communication. When the learner understands these expressions, writing becomes easier because the phrases offer a predictable framework for short professional notes and simulated telephone messages.

The content includes useful forms such as asking who is speaking, saying that a person is not available, requesting that a caller wait, and indicating that someone will return the call later. These expressions help learners understand what must be written after a call interaction. For example, if a caller says that the matter is urgent or asks for a return call, the note should reflect that action clearly. The learner should not treat telephone expressions as speech only. In many work settings, they are directly linked to written follow-up. The short written output may include phrases like called this morning, asked for information, or requested a callback. These are practical writing outcomes based on standard call language.

A realistic example is a message form used in a small office. A caller phones to ask whether a document is ready. The receptionist uses simple telephone expressions during the call and then writes a message for the staff member concerned. The message does not need to reproduce the full dialogue. Instead, it records the essential request and any needed response. This example shows that telephone expressions help the learner identify the core communicative function of the call. Once that function is understood, writing becomes more focused and useful.

Teaching should include model phone lines, short call transcripts, and message-writing exercises. Learners may read a simple call exchange, underline the key telephone expressions, and then write a note based on the exchange. This helps them move from recognition to application. The trainer should emphasize tone, since workplace telephone notes often need respectful and professional wording. Even a short note should be understandable to another staff member who did not hear the call directly.

In workplace application, telephone expressions support reception work, office coordination, customer contact, appointment handling, and internal communication. A worker who knows how standard phone phrases function can prepare clearer written notes after calls. Common learner errors include copying too much dialogue into the note, missing the actual request, or forgetting to mention whether the caller expects a response. Another problem is using casual language where a formal phrase is more appropriate. Guided practice with simple forms and sample notes helps correct these issues.

By the end of this content, the learner should be able to recognize common French telephone expressions and use the information carried by those expressions to write short messages with correct focus and tone. The major lesson is that set expressions support efficient communication. When learners understand the structure of telephone language, they can write clearer notes, messages, and follow-up reminders in French.

Another helpful exercise is to compare two call situations and decide which telephone expressions signal urgency, courtesy, or callback expectation. This strengthens the learner's ability to write not only what happened during the call, but also what should happen after it. As that awareness improves, short French call messages become more accurate and more professional.

This content also helps learners build confidence with predictable language. When the trainee sees the same phone expressions appear in several scenarios, writing becomes faster because the structure is already familiar. That familiarity is useful in real office situations where quick but correct message writing is often necessary.""",
    "1_3": """Message Taking teaches the learner how to write short, accurate French messages based on information received from another person. In everyday and workplace communication, a message is often brief, but it still needs to contain the most important information. A learner may need to write who sent the message, what was requested, when the contact happened, and what action is expected. This content is therefore central to the competency of writing short messages, emails, or notes. It focuses on turning spoken or given information into a usable written form that someone else can read quickly and act on correctly.

The lesson highlights the main parts of a written message: sender or caller, recipient, date or time, purpose, and follow-up instruction. The learner should understand that message taking is not a free-form writing task. It is structured writing. The goal is to record information efficiently and accurately. A good message avoids unnecessary detail and makes the action clear. If the note is too vague, the receiver may not know what to do next. If the note is too long, the important point may be hidden. The learner therefore needs practice in selecting what matters most and writing it in simple, correct French.

A practical example is a training office where a staff member is away from the desk. Another person receives a message that a client will arrive later than expected and wants to reschedule the meeting. The learner writes a short French note to pass this information on. In this case, the written message should identify the sender, explain the reason for contact, and state the change requested. This type of exercise is useful because it shows how writing supports coordination. A message is not an academic paragraph. It is a tool for real action.

Teaching should involve message pads, short scenarios, reading-to-writing tasks, and peer checking. Learners can examine model messages, identify strong and weak examples, and then produce their own short notes from given situations. The trainer should encourage legibility, order, and directness. Short written communication becomes more effective when it follows a consistent structure. It is also helpful to compare messages that are complete with those that are missing key details so learners can see why certain information is essential.

In workplace use, message taking is valuable in offices, clinics, schools, service counters, and reception areas. Staff often need to receive information and pass it along in writing. A learner who can take a message in French is better prepared for multilingual coordination tasks. Common errors include forgetting the name of the sender, omitting the return action, writing a message with no time reference, or recording information in a confusing order. Repeated scenario practice helps the trainee avoid these problems and build confidence in concise written French.

By the end of this content, the learner should be able to write a short French message that records key information accurately and supports follow-up. The main idea is that message taking is purposeful writing. It requires attention to detail, simple grammar, and organized presentation. When the trainee can write messages clearly, French becomes a more useful tool for practical communication in daily and workplace settings.

The learner should also develop the habit of reviewing the message from the receiver's point of view. This means asking whether the note clearly states who contacted whom, why the message matters, and what should be done next. That final check improves accuracy and reduces confusion in office, classroom, and service-based communication tasks.

When learners compare strong and weak message samples, they become better at spotting missing details before the note is delivered. This simple review habit supports reliability and helps the trainee use French more effectively in everyday written coordination.""",
    "2_1": """Imperatives are important in short French writing because they allow the learner to give clear instructions, directions, and task reminders. In workplace notes, classroom instructions, labels, and brief written guidance, imperative forms are often the most direct and efficient way to tell someone what to do. This content supports the learner in writing short instructional messages that are understandable and action-oriented. Instead of writing long explanations, the trainee learns how to express commands or directions simply and appropriately.

The lesson begins with the function of the imperative in written communication. A note may tell someone to wait, sign, call back, bring a document, or follow a procedure. In each case, the written instruction should be direct but still suitable to the context. The learner should understand that imperatives can sound firm, helpful, or procedural depending on the setting. In a workplace or training environment, the purpose is not to sound rude. It is to communicate a necessary action with clarity. This means that the learner must pay attention not only to verb form, but also to tone and suitability.

A practical example is a short instruction note left on a desk. The note may ask a coworker to review a file, send an email, or call a client before a scheduled meeting. The trainee needs to write the instruction using simple French forms that make the action unmistakable. If the imperative is inaccurate or vague, the reader may not know what to do. If the note is too long, the action may be less clear. This is why imperative writing is useful in competency-based training: it encourages concise and functional sentences.

Teaching should use models of workplace reminders, instruction cards, step-by-step labels, and direction-based tasks. Learners can transform simple statements into written commands, compare strong and weak instruction notes, and practice writing short directives for everyday tasks. The trainer should also show where polite framing may still be appropriate, especially when instructions are part of a service-oriented or collaborative setting. This helps the learner balance clarity and professionalism.

In workplace application, imperatives appear in reminder notes, procedure cards, safety labels, task lists, classroom instructions, and simple service guidance. A learner who can write with the imperative is better prepared to give or record action points in French. Common problems include using the wrong verb form, writing an instruction that is too general, or forgetting to include the object or detail needed to complete the task. Guided practice with realistic office and classroom scenarios helps reduce these errors.

By the end of this content, the learner should be able to write short French instructions using appropriate imperative forms and clear action language. The larger lesson is that short writing becomes more effective when the action is explicit. When trainees master this content, they can produce concise notes and instructions that support daily tasks and workplace communication.

It is also useful for learners to compare an unclear instruction with a revised imperative version. Seeing how a sentence becomes stronger through direct action language helps the trainee understand why this grammar form matters in practical writing. With repetition, learners become more confident in preparing reminders, labels, and quick written directives in French.

This skill also supports teamwork because short written actions can be passed from one person to another without lengthy explanation. When the learner writes a clear imperative note, the reader can respond immediately. That practical value makes this content especially relevant in training and office environments.

With enough guided practice, the learner begins to choose stronger verbs and more complete action details automatically. This reduces hesitation during writing tasks and helps short French instructions become clearer, faster to produce, and easier for others to follow.""",
    "2_2": """Prepositions are essential in short written directions because they show location, movement, relation, and destination. When a learner writes instructions in French, it is not enough to know the verbs alone. The message must also explain where something is, where to go, where to place an item, or how one location connects to another. Prepositions make that possible. In practical writing tasks such as giving directions, writing procedural notes, or explaining where materials should be delivered, correct preposition use makes the difference between a useful instruction and a confusing one.

The lesson focuses on prepositions that commonly appear in simple written directions, such as words used for place, direction, position, and sequence. The learner should study these not as isolated grammar labels, but as writing tools. A short note that says place the file on the table, go to the office, or wait in front of the meeting room depends on accurate preposition use. If the wrong preposition is chosen, the instruction may still seem grammatical but the practical meaning may be wrong. This is why prepositions are especially important in action-oriented writing.

A useful example is a workplace orientation note that tells a new trainee how to move from reception to the assigned room. The learner writes a few short lines indicating where to turn, where to wait, and where the supervisor can be found. In this situation, prepositions create the map inside the sentence. They guide the reader through the physical or procedural space. This kind of writing is short, but it requires precision. The learner must think carefully about the relationship between objects and locations.

Teaching should therefore involve maps, object placement tasks, labeled rooms, and short written instruction exercises. Learners can complete sentences with the correct preposition, rewrite vague notes more clearly, and create mini-direction messages for workplace settings. The trainer should also emphasize that short written directions should remain simple. The goal is not to produce long descriptive paragraphs, but to write enough information for the reader to act confidently.

In workplace communication, prepositions are used in delivery notes, room directions, filing instructions, desk labels, equipment placement guides, and visitor assistance messages. A learner who can write these accurately in French is more prepared for practical coordination tasks. Common errors include selecting the wrong place word, omitting the preposition entirely, or writing instructions without a clear destination reference. Repetition with real or simulated office layouts helps the learner improve.

By the end of this content, the trainee should be able to use basic French prepositions to write short, clear directions and instructional notes. The main lesson is that small words carry important meaning. When prepositions are chosen well, written instructions become precise, usable, and appropriate for daily and workplace communication.

Another valuable practice is to rewrite vague notes by adding correct place and movement words. This shows the learner how a short sentence can become much more useful through accurate preposition choice. As trainees improve, they can produce clearer direction notes for visitors, coworkers, and classmates in routine French communication.

The learner should also notice that prepositions often work together with verbs of movement and location. Studying these combinations in short notes helps the trainee write more naturally and more precisely. This added control improves the usefulness of French directions in real settings.

As learners repeat this practice with rooms, desks, files, and meeting areas, they become more accurate in describing where people and objects should go. That repeated application turns grammar knowledge into practical written communication for daily and workplace use.

The learner should also compare directions that are technically grammatical but practically unclear. This helps show that correct writing must also be usable. When preposition choices guide the reader effectively, the written message becomes much more valuable in real workplace situations.""",
    "2_3": """Instruction Writing develops the learner's ability to produce short written French texts that guide another person through a task or process. This content combines grammar, vocabulary, and organization because a good instruction note must tell the reader what to do, in what order, and with enough clarity to avoid confusion. In beginner French, instruction writing does not require long explanations. It requires direct language, clear sequencing, and attention to the action being described. This makes it highly relevant to the competency of writing short messages, emails, or notes.

The lesson emphasizes structure. An instruction text often begins with the task or purpose, then lists or states the needed actions in logical sequence. The learner should decide what information is essential for the reader to complete the task. In a short French instruction note, every line should contribute to action. Unnecessary decoration weakens the message. For this reason, the trainee should learn to write short step-based guidance with simple vocabulary and correct verb forms. Numbered or clearly ordered instructions are often helpful because they make the note easier to follow.

A realistic example is a note explaining how to prepare a small meeting space or how to submit a document before a deadline. The learner may need to write two or three short instructions telling someone to bring materials, place the forms in the correct location, and inform the supervisor afterward. This kind of task reflects authentic workplace communication. The reader does not need a full essay. The reader needs a short written guide that supports immediate action. When learners practice this, they understand that writing can be practical, not only expressive.

Teaching should use task cards, office routines, classroom procedures, and simple workflow scenarios. Learners can observe a process, list the steps, and then rewrite them in short French instructions. The trainer should help them improve order, verb choice, and completeness. Peer checking is also useful because it shows whether another reader can follow the instruction successfully. If the partner cannot understand the steps, the writing needs to be revised.

In workplace application, instruction writing is useful in reminder notes, operating guidance, orientation tasks, classroom procedures, filing steps, and simple service directions. Staff often depend on short written instructions to maintain order and consistency. Common learner problems include writing steps in random order, omitting an important action, or using sentences that are too broad to be useful. Structured practice helps reduce these errors and builds confidence in practical written French.

By the end of this content, the learner should be able to write short French instructions that are orderly, understandable, and action-focused. The key lesson is that effective instruction writing depends on sequence and clarity. When trainees can guide another person through a simple task in writing, they demonstrate useful beginner-level competence for daily and workplace communication.

The learner should also practice testing the instructions with another reader. If the partner can follow the steps without confusion, the writing is effective. If not, the note needs revision. This habit encourages the trainee to think about the usefulness of the text, not only the grammar, which is essential in practical workplace writing.

Another effective exercise is to shorten a long explanation into two or three practical lines. This teaches the learner to keep only the information needed for action. As that skill develops, instruction writing becomes more efficient and better suited to notes, labels, and quick procedural messages.

The learner also benefits from checking whether the steps can be completed in the same order they are written. This simple review builds awareness of sequence and usefulness. When the order is sound, the written instruction becomes a reliable guide for another person.""",
    "3_1": """Dates and Invitations are important in short French writing because many messages, notes, and simple emails involve arranging or announcing an event. A learner may need to invite someone to a meeting, confirm a schedule, mention the day and date of an activity, or write a short reminder for an upcoming appointment. This content helps the trainee write these details clearly. In practical communication, a missing date or unclear invitation can create confusion even if the grammar is otherwise acceptable. For that reason, writing invitations requires attention to both information and tone.

The lesson shows how date information and invitation purpose work together. An invitation note often answers several simple questions: what is happening, when it will happen, where it will happen, and who is expected to attend. The learner should see that these elements create the usefulness of the message. A short written invitation does not need complex language, but it must include the necessary event details in a readable order. This makes the writing functional rather than decorative.

A realistic example is a short French note inviting a classmate or coworker to a meeting or training session. The learner writes the event title, date, time, and polite closing line. If one of these pieces is missing, the reader may not be able to act correctly. The example also shows how calendar language connects with short-form writing. Dates are not just vocabulary items to recognize. They are information points that allow an invitation to work in practice.

Teaching should involve invitation cards, event notices, and appointment-style notes. Learners can compare complete and incomplete invitations, then write their own short texts using the same structure. The trainer should encourage simple but correct wording. Learners also benefit from checking one another's drafts to see if the invitation answers the key questions clearly. This helps them understand the reader's perspective.

In workplace and school communication, dates and invitations appear in meeting notices, classroom reminders, training announcements, event invitations, and short email messages. A learner who can write these clearly in French becomes better prepared for coordination tasks. Common problems include omitting the date, confusing day and time, writing an invitation without a clear purpose, or using an unsuitable tone. Repeated practice with realistic event scenarios helps improve accuracy.

By the end of this content, the learner should be able to write a short French invitation or date-based note that clearly states the event details and purpose. The major lesson is that invitation writing depends on complete, organized information. When the trainee can combine date reference with a polite event message, short written French becomes more practical and effective.

Another helpful activity is to compare invitations for different audiences, such as a classmate, coworker, or supervisor. This allows the learner to notice how tone and presentation may shift while the basic information remains the same. Through this practice, event-based writing becomes more flexible and more suitable for real communication needs.

The learner should also check whether the note makes the event easy to attend by presenting the schedule information in a readable order. A clear invitation reduces the need for extra clarification. This supports both daily coordination and simple workplace event communication in French.

Repeated writing of short invitations also helps the learner become more comfortable combining calendar details with courteous event language. This strengthens confidence and prepares the trainee for simple announcements, reminders, and meeting notices in French.

The trainee should also practice checking whether the invitation gives enough information for the reader to respond without asking another question. This final review step improves completeness and makes the note more practical for real event coordination in school and workplace settings.""",
    "3_2": """Polite Requests are central to short written communication because many notes, messages, and simple emails ask another person to do something. In workplace and daily settings, the request must be clear, but it should also remain respectful. This content teaches the learner how to write simple French requests that balance action and politeness. A note asking for assistance, confirmation, attendance, or a reply becomes more effective when the reader understands both what is needed and the courteous tone of the message.

The lesson focuses on the function of request writing. A polite request may ask a person to call back, send a document, confirm an appointment, wait for a response, or attend a meeting. The learner should understand that a written request is not the same as a direct command. Even when the task is simple, tone matters. This is especially true in customer service, school administration, office coordination, and formal communication. The writing should therefore include clear action language while maintaining respect for the reader.

A useful example is a short note asking a supervisor or classmate to confirm availability for an appointment. The note includes a greeting, the request itself, and a brief courteous closing. The learner should notice that the note remains short, but still sounds professional. This shows that politeness does not require long sentences. Instead, it requires thoughtful wording. The trainee should learn to avoid abrupt writing while still keeping the message concise.

Teaching should include model request notes, role-based writing scenarios, and revision tasks that turn direct or blunt lines into more suitable written requests. Learners can compare two versions of the same note and discuss which one is more appropriate. This helps them see tone as part of writing quality. The trainer should also encourage learners to think about audience. A request to a friend may sound different from a request to a supervisor, client, or office staff member.

In practical use, polite request writing supports office notes, appointment follow-up, customer response messages, school communications, and workplace reminders. A learner who can write polite requests in French is better equipped for everyday coordination. Common errors include writing a request with no courteous marker, making the action unclear, or adding too much information so that the main request is hidden. Through structured practice, learners can develop balance between brevity and politeness.

By the end of this content, the learner should be able to write a short French request that is clear, respectful, and appropriate to the situation. The key lesson is that tone and purpose must work together. When the trainee can ask for action politely in writing, French becomes more useful for real communication in daily and workplace contexts.

The learner also benefits from revising direct notes into more courteous versions. This helps show that a request can remain short while still sounding respectful and professional. As the trainee practices this balance, written French becomes more effective for appointments, office reminders, and everyday coordination.

This content is especially valuable because a polite request often creates better response from the reader. When learners understand that tone affects cooperation, they become more thoughtful writers. That awareness strengthens short message quality in both personal and workplace communication.

Another strong practice is to identify the exact action requested before writing the note. This keeps the message focused and prevents polite wording from becoming vague. As the trainee improves, request notes become both respectful and easy to answer.

The learner should also compare request notes written for different readers, such as a classmate, staff member, or supervisor. This helps show how audience affects tone while the main action remains clear. Through this practice, polite request writing becomes more flexible and more appropriate to real communication situations.""",
    "3_3": """Appointment Dialogues help the learner understand how appointment-making language can be turned into short written notes, confirmations, and follow-up messages. Although a dialogue is spoken interaction, it often produces written communication afterward. A learner may need to write down the final appointment details, confirm them in a note, or send a short message based on the exchange. This content therefore supports writing by helping the trainee identify the essential appointment information contained in a dialogue and rewrite it accurately in French.

The lesson begins by showing the common structure of an appointment exchange. One person proposes a date or time, another responds, the schedule may be adjusted, and eventually a final arrangement is confirmed. The learner should focus on the outcome of the dialogue. In writing, the most important elements are usually the person involved, the agreed date, the time, the place if given, and any action that must happen before the appointment. This selective writing skill is important because short messages should emphasize the final arrangement, not every line of the conversation.

A realistic example is a phone or desk dialogue in which a client asks for an appointment, the office suggests another time, and both sides agree on the new schedule. The learner then writes a short confirmation note in French. This note may be used for internal coordination or to remind the client of the appointment details. The example teaches an important principle: the dialogue provides information, but the note must organize that information clearly for later use.

Teaching should include appointment transcripts, scheduling cards, and confirmation-writing tasks. Learners can read or listen to a short appointment dialogue, identify the final agreed details, and write a brief note or message from it. The trainer should help them distinguish between proposed times and confirmed times. This prevents a common mistake in appointment writing, where the learner records the first suggestion instead of the final agreement.

In workplace and service communication, appointment notes are used in clinics, offices, schools, salons, government counters, and customer service desks. Staff often need to summarize scheduled interactions in writing. A learner who can do this in French is better prepared for multilingual coordination tasks. Common problems include missing the final agreed time, omitting the purpose of the appointment, or writing the note without a clear confirmation statement. Scenario-based practice helps build accuracy and confidence.

By the end of this content, the learner should be able to write a short French appointment confirmation or note based on a simple dialogue. The main lesson is that useful writing depends on identifying the final agreed information and presenting it clearly. When trainees can convert an appointment exchange into a concise written record, they demonstrate practical skill in short-form French communication.

The learner should also practice checking whether the note reflects the final schedule rather than an early proposal in the conversation. This small habit prevents common errors in appointment writing. With repeated dialogue-to-note activities, the trainee becomes more reliable in writing confirmations, reminders, and short records for workplace and service situations.

Another useful step is to ask the learner to restate the final arrangement in one simple sentence before writing the note. This confirms understanding and reduces mistakes. As a result, appointment messages become more accurate, concise, and dependable for real follow-up use.

This content also helps the learner manage practical scheduling communication in offices and service desks where written records matter. When the final arrangement is captured correctly, the note becomes a dependable tool for reminder, coordination, and appointment follow-up.

The learner should also review whether the written note includes the appointment purpose as well as the schedule itself. This makes the message more useful to another staff member who may need to prepare for the meeting. Through repeated practice, appointment writing becomes clearer, more complete, and more dependable in real communication.""",
}


content_entries = [
    {
        "field": "1_1",
        "title": "Making and Receiving Calls",
        "apply": {
            "title": "Write a Call Follow-Up Note",
            "objective": "Write a short French message based on a simple telephone call scenario using correct key details and follow-up action.",
            "sup_mat": "Telephone scenario card\nMessage form\nReference expressions sheet",
            "equipment": "Printed task sheet\nPen\nTelephone role-play prompt",
            "steps": "1. Read the telephone scenario.\n2. Identify the caller, purpose, and requested action.\n3. Complete the short French note form.\n4. Review the note for clarity and completeness.\n5. Read the note aloud to the trainer.\n6. Revise the message based on feedback.",
            "assessment": "Scenario-based writing task with checklist and short oral explanation.",
            "pcs": [
                "Identified the key call details correctly.",
                "Wrote the message with clear purpose.",
                "Included the needed follow-up action.",
                "Used simple French expressions appropriately.",
                "Produced an organized and readable note.",
            ],
        },
        "mcqs": [
            {"q": "Why is making and receiving calls important in this lesson?", "options": ["It supports writing short follow-up notes", "It replaces all email writing", "It focuses only on pronunciation", "It removes message taking"], "answer": "A"},
            {"q": "What should a call follow-up note include?", "options": ["key details and requested action", "every spoken word", "only the caller's greeting", "no time reference"], "answer": "A"},
            {"q": "Which workplace task often follows a phone call?", "options": ["writing a short message", "drawing a map", "counting chairs", "checking weather only"], "answer": "A"},
            {"q": "A good phone note should be", "options": ["clear and concise", "long and unrelated", "unclear and informal only", "without purpose"], "answer": "A"},
            {"q": "Which detail is often necessary in a call note?", "options": ["who called", "what color the phone is", "the wallpaper design", "the desk length"], "answer": "A"},
            {"q": "Why should learners avoid writing every spoken line?", "options": ["Because the note should focus on essential information", "Because notes cannot contain verbs", "Because French notes use numbers only", "Because greetings are forbidden"], "answer": "A"},
            {"q": "What should happen if a caller asks for a return call?", "options": ["It should be written in the note", "It should be ignored", "It should replace the name", "It should be removed from the message"], "answer": "A"},
            {"q": "A reception scenario helps the learner practice", "options": ["phone-based workplace writing", "sports vocabulary", "recipe writing", "geography only"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["convert a call situation into a useful note", "memorize one greeting only", "avoid message forms", "write without key details"], "answer": "A"},
            {"q": "The main lesson of this content is that call writing depends on", "options": ["selection and clarity", "paper color", "typing speed only", "decoration"], "answer": "A"},
        ],
    },
    {
        "field": "1_2",
        "title": "Telephone Expressions",
        "apply": {
            "title": "Use Telephone Expressions in a Written Message",
            "objective": "Write a short French message that reflects a telephone situation using appropriate standard expressions and needed action details.",
            "sup_mat": "Call transcript\nTelephone expression list\nMessage template",
            "equipment": "Printed activity sheet\nPen\nHighlighter",
            "steps": "1. Read the sample call transcript.\n2. Underline the important telephone expressions.\n3. Identify the main request or response needed.\n4. Write a short French message from the transcript.\n5. Check the tone and completeness of the note.\n6. Review corrections with the trainer.",
            "assessment": "Transcript-to-message writing exercise with checklist.",
            "pcs": [
                "Recognized the standard telephone expressions correctly.",
                "Used the call information in a short written note.",
                "Maintained a suitable professional tone.",
                "Included the needed response or callback detail.",
                "Produced a clear and useful message.",
            ],
        },
        "mcqs": [
            {"q": "Why are telephone expressions useful in writing?", "options": ["They help structure short call-based messages", "They replace all nouns", "They are used only in songs", "They remove follow-up actions"], "answer": "A"},
            {"q": "What should a learner do after reading a call transcript?", "options": ["identify the important expressions and message purpose", "copy every line exactly", "ignore the request", "rewrite it as a poem"], "answer": "A"},
            {"q": "A telephone expression often signals", "options": ["what action the note should record", "the color of the desk", "the month only", "the number of chairs"], "answer": "A"},
            {"q": "Which workplace area often uses telephone expressions?", "options": ["reception and office coordination", "painting class only", "sports training only", "laboratory chemistry only"], "answer": "A"},
            {"q": "What should be avoided in a message based on a call?", "options": ["irrelevant dialogue detail", "the main request", "the caller's name", "the follow-up action"], "answer": "A"},
            {"q": "Why is tone important in a telephone message?", "options": ["Because workplace notes should remain professional", "Because notes must be musical", "Because grammar is optional", "Because tone replaces meaning"], "answer": "A"},
            {"q": "A callback request should be", "options": ["clearly included in the note", "left out completely", "replaced with a date only", "hidden at the end without meaning"], "answer": "A"},
            {"q": "What does this content mainly support?", "options": ["short formal message writing", "drawing ability", "calendar memorization only", "object labeling only"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["write a message from standard call language", "avoid all telephone scenarios", "use numbers only", "ignore message purpose"], "answer": "A"},
            {"q": "The central idea is that standard expressions support", "options": ["efficient communication", "page design", "faster walking", "equipment repair"], "answer": "A"},
        ],
    },
    {
        "field": "1_3",
        "title": "Message Taking",
        "apply": {
            "title": "Record a Short French Message",
            "objective": "Take and write a short French message from a given scenario using correct sender, purpose, and follow-up details.",
            "sup_mat": "Scenario prompt\nMessage pad format\nChecklist",
            "equipment": "Printed form\nPen\nDesk reference card",
            "steps": "1. Read or listen to the scenario.\n2. Identify the sender and intended receiver.\n3. Note the main purpose of the message.\n4. Write the message in simple French.\n5. Review if the action needed is clear.\n6. Submit the message for checking.",
            "assessment": "Short-form message-taking task with written checklist evaluation.",
            "pcs": [
                "Recorded the sender and receiver correctly.",
                "Captured the main purpose of the message.",
                "Included a clear time or action reference.",
                "Wrote the note in simple understandable French.",
                "Presented the message in an organized format.",
            ],
        },
        "mcqs": [
            {"q": "What is the main purpose of message taking?", "options": ["to record important information for follow-up", "to write a long story", "to avoid names", "to remove time details"], "answer": "A"},
            {"q": "Which element is important in a message?", "options": ["the sender", "the paper color", "the room size", "the pen brand"], "answer": "A"},
            {"q": "A useful message should be", "options": ["brief and complete", "very long and decorative", "unclear and unordered", "without purpose"], "answer": "A"},
            {"q": "Why should a message include action details?", "options": ["So the receiver knows what to do next", "So the note looks longer", "So grammar can be avoided", "So the note can replace the phone"], "answer": "A"},
            {"q": "Which setting commonly uses message taking?", "options": ["offices and reception areas", "art studios only", "sports fields only", "music halls only"], "answer": "A"},
            {"q": "What is a common learner error in message taking?", "options": ["omitting important information", "using a pen", "reading the prompt", "writing neatly"], "answer": "A"},
            {"q": "Why is structure important in a short message?", "options": ["It helps another reader understand quickly", "It changes French into English", "It removes the sender's name", "It replaces all verbs"], "answer": "A"},
            {"q": "A message-taking activity usually begins with", "options": ["identifying the key details of the situation", "drawing a border", "counting words only", "memorizing colors"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["write a usable message from a scenario", "avoid all receivers", "skip the purpose", "ignore follow-up action"], "answer": "A"},
            {"q": "The main lesson is that message taking is", "options": ["purposeful writing", "free decoration", "telephone repair", "calendar design"], "answer": "A"},
        ],
    },
    {
        "field": "2_1",
        "title": "Imperatives",
        "apply": {
            "title": "Write a Short Instruction Note",
            "objective": "Write a short French instruction using imperative forms to direct a simple workplace or classroom action clearly.",
            "sup_mat": "Task card\nImperative examples\nChecklist",
            "equipment": "Printed worksheet\nPen\nReference verbs list",
            "steps": "1. Read the task card.\n2. Identify the action that must be written.\n3. Choose the correct imperative verb form.\n4. Write a short instruction note.\n5. Check if the action is clear and complete.\n6. Review the note with the trainer.",
            "assessment": "Instruction-note writing exercise with checklist and revision.",
            "pcs": [
                "Used an appropriate imperative form.",
                "Made the required action clear.",
                "Included needed object or task detail.",
                "Maintained a suitable tone for the context.",
                "Wrote a concise and understandable note.",
            ],
        },
        "mcqs": [
            {"q": "Why are imperatives useful in writing?", "options": ["They help express clear instructions", "They replace all nouns", "They are used only in stories", "They remove action meaning"], "answer": "A"},
            {"q": "Where are imperatives often used?", "options": ["in reminders and instruction notes", "in weather maps only", "in sports scores only", "in family names only"], "answer": "A"},
            {"q": "A short instruction note should be", "options": ["direct and clear", "long and unrelated", "without action", "hidden in paragraph form only"], "answer": "A"},
            {"q": "What should a learner check after writing an imperative note?", "options": ["whether the action is clear", "whether the paper is blue", "whether the table is heavy", "whether the room is cold"], "answer": "A"},
            {"q": "Why is tone still important with imperatives?", "options": ["Because instructions should suit the context", "Because tone replaces verbs", "Because commands cannot be written", "Because notes must be casual"], "answer": "A"},
            {"q": "Which setting can use imperative writing?", "options": ["workplace and classroom tasks", "music rhythm only", "painting only", "gardening only"], "answer": "A"},
            {"q": "A common learner mistake is", "options": ["using an unclear action", "reading the task card", "checking the note", "reviewing feedback"], "answer": "A"},
            {"q": "Imperatives mainly help the writer express", "options": ["what should be done", "what color to use", "what song to sing", "what shape to draw"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["write a useful instruction note", "avoid the verb form", "ignore the task detail", "skip revision"], "answer": "A"},
            {"q": "The major lesson is that effective instructions depend on", "options": ["explicit action language", "paper thickness", "furniture size", "calendar color"], "answer": "A"},
        ],
    },
    {
        "field": "2_2",
        "title": "Prepositions",
        "apply": {
            "title": "Write Simple Directions Using Prepositions",
            "objective": "Write a short French direction note using correct basic prepositions to show place, destination, or relation.",
            "sup_mat": "Office map\nPreposition guide\nDirection task card",
            "equipment": "Printed map\nPen\nLabeled room sheet",
            "steps": "1. Study the office map or location prompt.\n2. Identify the path or position to describe.\n3. Choose the correct prepositions.\n4. Write the short direction note in French.\n5. Check the note for clarity of place and movement.\n6. Submit the note for review.",
            "assessment": "Direction-writing activity assessed with a checklist.",
            "pcs": [
                "Used correct prepositions for place or movement.",
                "Made the destination or location clear.",
                "Connected the direction steps logically.",
                "Used simple understandable French wording.",
                "Produced a practical written direction note.",
            ],
        },
        "mcqs": [
            {"q": "Why are prepositions important in direction writing?", "options": ["They show place and relation clearly", "They replace verbs", "They remove destinations", "They are used only in poetry"], "answer": "A"},
            {"q": "A direction note often explains", "options": ["where to go or where to place something", "how to draw a picture", "how to sing a song", "how to count quickly"], "answer": "A"},
            {"q": "What can happen if the wrong preposition is used?", "options": ["The instruction may become confusing", "The date will change", "The paper will fold", "The pen will stop"], "answer": "A"},
            {"q": "Which classroom support helps this lesson?", "options": ["an office map", "a recipe card only", "a sports ticket only", "a music sheet only"], "answer": "A"},
            {"q": "A good direction note should be", "options": ["simple and precise", "long and decorative", "without location", "without movement"], "answer": "A"},
            {"q": "Where can preposition writing be useful?", "options": ["in workplace coordination notes", "in painting only", "in weather forecasts only", "in jokes only"], "answer": "A"},
            {"q": "What is a common error in this content?", "options": ["omitting the needed preposition", "reading the map", "using a pen", "reviewing examples"], "answer": "A"},
            {"q": "Prepositions mainly support writing about", "options": ["location and direction", "calendar color", "desk material", "music volume"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["write clear location-based directions", "avoid all place words", "skip the destination", "ignore the map"], "answer": "A"},
            {"q": "The major lesson is that small words can carry", "options": ["important meaning", "no meaning at all", "only decoration", "only pronunciation"], "answer": "A"},
        ],
    },
    {
        "field": "2_3",
        "title": "Instruction Writing",
        "apply": {
            "title": "Prepare a Step-by-Step French Instruction",
            "objective": "Write a short step-by-step French instruction note for a simple task using clear order and action language.",
            "sup_mat": "Procedure prompt\nStep organizer\nChecklist",
            "equipment": "Printed task sheet\nPen\nReference phrase list",
            "steps": "1. Review the procedure prompt.\n2. Identify the key steps of the task.\n3. Arrange the steps in logical order.\n4. Write the short French instructions.\n5. Check whether another person can follow them.\n6. Revise the note using feedback.",
            "assessment": "Step-writing task evaluated through a practical checklist.",
            "pcs": [
                "Identified the needed steps correctly.",
                "Arranged the steps in logical sequence.",
                "Used clear action-based language.",
                "Included enough information to follow the task.",
                "Produced an organized instruction note.",
            ],
        },
        "mcqs": [
            {"q": "What is the main purpose of instruction writing?", "options": ["to guide another person through a task", "to tell a long story", "to list colors only", "to avoid action words"], "answer": "A"},
            {"q": "A good instruction note should follow", "options": ["a logical sequence", "random order", "alphabetical order only", "the longest possible format"], "answer": "A"},
            {"q": "Why is order important in instructions?", "options": ["because the reader needs to follow the task correctly", "because grammar disappears", "because notes must be artistic", "because steps do not matter"], "answer": "A"},
            {"q": "Which practice supports this content?", "options": ["rewriting a task as ordered steps", "ignoring the process", "memorizing one noun", "counting lines only"], "answer": "A"},
            {"q": "A workplace instruction note often contains", "options": ["task steps and action details", "only greetings", "only dates", "only titles"], "answer": "A"},
            {"q": "What happens if a step is missing?", "options": ["The instruction may become difficult to follow", "The room changes", "The date changes", "The paper disappears"], "answer": "A"},
            {"q": "Why should learners check whether another person can follow the note?", "options": ["To test clarity and completeness", "To make the note longer", "To avoid revision", "To remove action words"], "answer": "A"},
            {"q": "Instruction writing is useful in", "options": ["procedures and reminders", "painting only", "sports chanting only", "map coloring only"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["write short ordered instructions", "avoid sequence", "ignore task purpose", "skip revision"], "answer": "A"},
            {"q": "The central lesson is that instructions depend on", "options": ["clarity and sequence", "page shape", "font size only", "desk arrangement"], "answer": "A"},
        ],
    },
    {
        "field": "3_1",
        "title": "Dates and Invitations",
        "apply": {
            "title": "Write a Short Invitation Note",
            "objective": "Write a short French invitation note including date, time, event purpose, and polite event wording.",
            "sup_mat": "Invitation prompt\nSample invitation\nChecklist",
            "equipment": "Printed invitation form\nPen\nCalendar reference",
            "steps": "1. Read the event prompt.\n2. Identify the date, time, and purpose of the event.\n3. Write the invitation note in simple French.\n4. Check whether the invitation is complete.\n5. Add a suitable polite closing line.\n6. Review the note with the trainer.",
            "assessment": "Event-invitation writing task with checklist review.",
            "pcs": [
                "Included the event purpose clearly.",
                "Wrote the correct date and time details.",
                "Used simple and polite invitation wording.",
                "Organized the information clearly for the reader.",
                "Produced a complete short invitation note.",
            ],
        },
        "mcqs": [
            {"q": "Why are dates and invitations important in writing?", "options": ["They help organize event messages", "They replace all requests", "They remove time details", "They are used only in stories"], "answer": "A"},
            {"q": "What should a short invitation include?", "options": ["event details and purpose", "only the greeting", "only the place color", "no date"], "answer": "A"},
            {"q": "A complete invitation answers", "options": ["what, when, and where", "who drew the paper", "which pen was used", "how long the desk is"], "answer": "A"},
            {"q": "Which practice helps invitation writing?", "options": ["comparing complete and incomplete notes", "ignoring the reader", "memorizing colors only", "skipping the event purpose"], "answer": "A"},
            {"q": "Why is organization important in an invitation?", "options": ["It helps the reader understand the event quickly", "It removes the date", "It changes the language", "It replaces grammar"], "answer": "A"},
            {"q": "Where might invitation writing be used?", "options": ["meetings and training events", "sports flags only", "recipe lists only", "tool labels only"], "answer": "A"},
            {"q": "What is a common learner error in invitation writing?", "options": ["omitting the date or time", "using a checklist", "reading a sample", "checking the note"], "answer": "A"},
            {"q": "A polite closing line helps the invitation sound", "options": ["appropriate and complete", "unclear and abrupt", "too long only", "without purpose"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["write a complete short invitation", "ignore key event details", "skip the purpose", "avoid date references"], "answer": "A"},
            {"q": "The main lesson is that invitation writing depends on", "options": ["organized information", "page design", "desk arrangement", "ink color"], "answer": "A"},
        ],
    },
    {
        "field": "3_2",
        "title": "Polite Requests",
        "apply": {
            "title": "Write a Polite Request Note",
            "objective": "Write a short French note requesting an action politely and clearly for a workplace or school situation.",
            "sup_mat": "Request scenario\nSample note\nTone guide",
            "equipment": "Printed worksheet\nPen\nChecklist",
            "steps": "1. Read the request scenario.\n2. Identify the action needed from the reader.\n3. Write the short French request note.\n4. Check if the tone is polite and clear.\n5. Add a brief closing line if needed.\n6. Review and revise the note.",
            "assessment": "Tone-focused request writing task with checklist.",
            "pcs": [
                "Made the requested action clear.",
                "Used respectful written wording.",
                "Matched the tone to the reader and context.",
                "Kept the note concise and understandable.",
                "Produced a practical request message.",
            ],
        },
        "mcqs": [
            {"q": "Why are polite requests important in writing?", "options": ["They combine action with respect", "They replace all commands", "They remove the reader", "They are used only in songs"], "answer": "A"},
            {"q": "A polite request note should tell the reader", "options": ["what action is needed", "what color to choose", "what sport to play", "what chair to use"], "answer": "A"},
            {"q": "Why does tone matter in request writing?", "options": ["Because the note should remain respectful", "Because tone replaces verbs", "Because requests must be hidden", "Because grammar is unnecessary"], "answer": "A"},
            {"q": "Which situation may need a polite request?", "options": ["asking for confirmation or help", "drawing a map only", "memorizing months only", "counting numbers only"], "answer": "A"},
            {"q": "What should be avoided in a polite request?", "options": ["abrupt or unclear wording", "brief closing lines", "simple grammar", "clear purpose"], "answer": "A"},
            {"q": "A useful classroom activity for this content is", "options": ["revising a blunt note into a polite one", "skipping the reader", "removing the request", "counting sentences only"], "answer": "A"},
            {"q": "What is a common error in request writing?", "options": ["hiding the main action inside too much detail", "using a scenario prompt", "checking the audience", "reviewing examples"], "answer": "A"},
            {"q": "Polite requests are useful in", "options": ["office and school communication", "painting only", "weather reports only", "music notation only"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["write a clear respectful request", "ignore the audience", "avoid action language", "skip tone"], "answer": "A"},
            {"q": "The key lesson is that request writing must balance", "options": ["purpose and politeness", "paper and ink", "size and color", "speed and noise"], "answer": "A"},
        ],
    },
    {
        "field": "3_3",
        "title": "Appointment Dialogues",
        "apply": {
            "title": "Write an Appointment Confirmation Note",
            "objective": "Write a short French appointment note based on a simple dialogue using the final agreed details correctly.",
            "sup_mat": "Appointment dialogue\nConfirmation template\nChecklist",
            "equipment": "Printed dialogue sheet\nPen\nCalendar prompt",
            "steps": "1. Read the appointment dialogue carefully.\n2. Identify the final agreed date and time.\n3. Note the purpose of the appointment.\n4. Write the confirmation note in simple French.\n5. Check whether the final details are accurate.\n6. Review the note with the trainer.",
            "assessment": "Dialogue-to-note writing task with checklist evaluation.",
            "pcs": [
                "Identified the final agreed appointment details.",
                "Recorded the correct date and time in writing.",
                "Included the purpose of the appointment.",
                "Used clear and simple French confirmation wording.",
                "Produced a useful short appointment note.",
            ],
        },
        "mcqs": [
            {"q": "Why are appointment dialogues useful in writing lessons?", "options": ["They provide information for short confirmation notes", "They replace all invitations", "They remove dates", "They only teach pronunciation"], "answer": "A"},
            {"q": "What should the learner write from an appointment dialogue?", "options": ["the final agreed details", "every spoken line", "only the first time suggested", "no action information"], "answer": "A"},
            {"q": "Why is the final agreement important?", "options": ["Because it is the information that should be recorded", "Because the first idea is always correct", "Because dates are optional", "Because the note does not need time"], "answer": "A"},
            {"q": "A common learner error is", "options": ["recording the first proposed time instead of the final one", "using a checklist", "reading the dialogue", "checking the calendar"], "answer": "A"},
            {"q": "Which setting often uses appointment notes?", "options": ["offices and service counters", "sports fields only", "painting rooms only", "music stages only"], "answer": "A"},
            {"q": "What should an appointment note include?", "options": ["date, time, and purpose", "only a greeting", "only the room color", "only a signature"], "answer": "A"},
            {"q": "Why should the note be concise?", "options": ["Because the key information must be easy to use", "Because French cannot be written long", "Because time is forbidden", "Because names are not needed"], "answer": "A"},
            {"q": "A useful practice for this content is", "options": ["turning a dialogue into a confirmation note", "ignoring the dialogue", "counting words only", "memorizing unrelated verbs"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["write an accurate short appointment record", "avoid final details", "skip the purpose", "ignore the agreed time"], "answer": "A"},
            {"q": "The main lesson is that appointment writing depends on", "options": ["clear final information", "paper thickness", "font shape", "desk color"], "answer": "A"},
        ],
    },
]


payload = {
    "sector": "EDU",
    "qualification_title": qualification_title,
    "unit_of_competency": all_units[2],
    "module_title": all_modules[2],
    "next_unit_of_competency": all_units[3],
    "Module_Descriptor": (
        "This module develops the learner's ability to write short French messages, emails, and notes using simple but correct grammar for daily and workplace communication. "
        "It covers writing based on telephone situations, message-taking tasks, imperative forms, prepositions for directions, short instructional writing, invitations, polite requests, and appointment confirmations. "
        "The trainee organizes key details clearly, applies practical sentence patterns, and writes concise texts that support coordination, reminders, and follow-up action. "
        "By the end of the module, the learner is expected to produce brief French written communication with better clarity, tone, structure, and readiness for routine workplace use."
    ),
    "Laboratory": "Language and Computer Laboratory",
    "training_materials": "\n".join(
        [
            "Telephone scenario cards",
            "Short message and note templates",
            "Instruction-writing worksheets",
            "Office map and direction prompts",
            "Invitation and appointment samples",
            "Polite request reference sheet",
            "Printed comprehension and writing checklists",
            "Laptop or desktop computer",
            "Pens and highlighters",
        ]
    ),
    "uc_no": 3,
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
    "LO_1": "Telephone Conversations",
    "LO_2": "Giving Directions and Instructions",
    "LO_3": "Making Appointments",
    "Contents_1_1": "Making and Receiving Calls",
    "Contents_1_2": "Telephone Expressions",
    "Contents_1_3": "Message Taking",
    "Contents_2_1": "Imperatives",
    "Contents_2_2": "Prepositions",
    "Contents_2_3": "Instruction Writing",
    "Contents_3_1": "Dates and Invitations",
    "Contents_3_2": "Polite Requests",
    "Contents_3_3": "Appointment Dialogues",
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
    assert payload["uc_no"] == 3

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
