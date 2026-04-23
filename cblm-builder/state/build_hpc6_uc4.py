import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "state" / "payloads" / "HPC6_uc4_payload.json"


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
    "1_1": """Formal Writing is important in a French language module because it shows the learner how respect, structure, and tone are expressed in written communication. Cultural awareness is not only about knowing customs in theory. It is also about using language in a way that matches the situation and the relationship between people. In many French-speaking contexts, written communication in formal settings follows clear expectations. A short note, request, or message intended for a supervisor, client, teacher, or unfamiliar person should sound organized, courteous, and appropriate. This content helps learners understand that formal writing is a cultural behavior as much as it is a grammar exercise.

The lesson begins by examining the characteristics of formal written French. Formal writing often includes respectful greetings, controlled wording, and a more careful sentence structure than casual communication. The learner should notice that formality is reflected not only in vocabulary, but also in the overall arrangement of the message. A formal note usually presents its purpose clearly, avoids slang or overly familiar expressions, and closes politely. These features matter because written form creates an impression of professionalism. If the learner writes to a client or superior in a tone that is too casual, the message may appear disrespectful even when the information itself is correct.

A practical example is a short message sent to a school office or workplace supervisor. The learner may need to write to request information, confirm attendance, or explain a minor schedule issue. In that situation, the learner should use a respectful greeting, a concise statement of purpose, and a courteous closing line. This example shows how formal writing supports real communication. The message does not need advanced vocabulary, but it does need cultural appropriateness. When learners study such examples, they begin to see that written tone carries social meaning.

Teaching should include model formal notes, greetings and closings, short email samples, and contrast exercises that compare formal and informal versions of the same message. Learners can identify which expressions sound respectful and discuss why one version is more appropriate in a workplace context. The trainer should also emphasize that formality often reflects distance, hierarchy, and professional setting. This helps the learner understand that writing choices are part of cultural sensitivity.

In workplace and educational settings, formal writing is used in requests, notices, email greetings, absence explanations, appointment confirmations, and many routine administrative messages. A learner who can write formal French appropriately is better prepared for communication with people who expect professional conduct. Common learner problems include using casual openings in a formal message, forgetting polite closings, or writing too directly without cultural softening. Repeated guided practice helps reduce these issues and builds awareness of audience and purpose.

By the end of this content, the learner should be able to recognize and produce the basic features of formal French writing for short messages and notes. The major lesson is that formal writing reflects respect, role awareness, and cultural sensitivity. When the trainee learns to write with the proper level of formality, French becomes a more effective tool for professional and socially appropriate communication.

The learner should also practice checking whether the note would sound acceptable if sent to a person in authority. This kind of review helps the trainee think about social distance and expectation before sending a message. With repeated use of formal models, learners become more confident in writing short French notes that reflect maturity, respect, and awareness of the professional setting.

This content becomes even more useful when learners compare several formal notes written for different purposes, such as requesting information, reporting absence, or confirming attendance. Seeing how the tone stays respectful across different situations helps the trainee understand that formality is a stable communication attitude, not just a list of polite words.""",
    "1_2": """Informal Writing is also an important part of cultural awareness because not all communication in French requires a formal or highly structured tone. Learners need to understand when a relaxed, familiar style is suitable and how that style differs from professional or official writing. Informal writing appears in short notes to friends, casual reminders, personal messages, and everyday exchanges between people who already share familiarity. Cultural sensitivity includes knowing when such a tone is acceptable and when it is not. This content helps the learner distinguish friendly communication from communication that requires more distance and formality.

The lesson focuses on the characteristics of informal written French. Informal messages often use simpler greeting lines, shorter sentence structures, and a warmer or more familiar tone. They may be direct in a friendly way, but they still need to remain understandable and appropriate. The learner should observe that informal writing does not mean careless writing. The message still needs a clear purpose and complete meaning. What changes is the relationship implied by the wording. This distinction is central to cultural competence because tone should match the social context.

A useful example is a short written reminder sent to a classmate or friend about meeting time, a school activity, or a shared task. The learner may write a casual greeting, mention the needed information directly, and close with a simple friendly phrase. This example teaches that informal writing can be efficient and warm without becoming rude. If the learner uses formal language in every situation, the message may sound distant. If the learner uses overly familiar language with the wrong audience, it may sound disrespectful. Cultural appropriateness lies in making the correct choice.

Teaching should include paired examples of formal and informal notes, writing prompts for peer communication, and audience-matching exercises. Learners can identify which message fits a friend, classmate, or teammate, and explain why the tone works. The trainer should guide learners to notice not just vocabulary, but also closings, sentence length, and the level of directness used. These observations help the learner understand how written French reflects relationship.

In real communication, informal writing appears in quick reminders, friendly invitations, short updates, and everyday coordination messages. A learner who can use informal French appropriately is better prepared for natural social interaction. Common problems include confusing informality with poor structure, using slang in an inappropriate setting, or failing to adjust the tone when the audience changes. Practice with clear audience-based scenarios helps the learner become more flexible and more culturally aware.

By the end of this content, the learner should be able to identify the features of informal French writing and produce short informal messages that suit familiar social situations. The main lesson is that informal writing still requires awareness, even when the tone is relaxed. When learners understand how informality functions in French, they communicate more naturally and more respectfully across different relationships.

Another helpful activity is to revise the same message for two audiences, first for a friend and then for a supervisor. This comparison shows the learner exactly how tone changes with relationship. As the trainee becomes more skilled at this adjustment, informal writing becomes a useful tool for natural social communication without losing clarity or respect.

Learners also benefit from checking whether an informal note still gives enough information to be useful. A friendly tone should not make the message incomplete. This balance between warmth and clarity helps the trainee write messages that feel natural while still doing their practical job.

With enough practice, the learner becomes better at shifting tone without losing meaning. That flexibility is a strong sign of cultural awareness because it shows control of relationship, context, and purpose in everyday French communication.""",
    "1_3": """Common Expressions support cultural sensitivity because they reflect how French speakers often manage routine interaction, politeness, friendliness, and everyday response. A learner may know grammar rules but still sound unnatural if common expressions are missing or used in the wrong place. These expressions help written and spoken communication feel more authentic. They also show awareness of how meaning is softened, emphasized, or made more socially appropriate. In a cultural competence module, this content matters because language is not only about accuracy. It is also about fitting the social expectations of the community using the language.

The lesson includes expressions frequently used in greetings, closings, acknowledgment, thanks, apology, and everyday response. The learner should understand that these expressions often carry more than literal meaning. Some show respect, some show warmth, and some help the speaker or writer maintain harmony in the interaction. When these expressions are used correctly, the communication feels smoother and more culturally appropriate. The learner should therefore study not only translation, but also the social purpose of each expression and the situations in which it fits best.

A practical example is a short written or spoken exchange in which a learner greets someone, thanks the person, apologizes for a delay, and ends the message politely. Each common expression contributes to tone. Even if the information content is simple, these expressions shape how the message is received. In a customer service setting, for example, common polite expressions can make the exchange feel respectful and professional. In a familiar setting, different common expressions may help the interaction sound warmer and more natural.

Teaching should use short dialogues, note samples, and expression-matching tasks that connect phrases with situations. Learners can compare two messages that say the same thing but use different expressions, then discuss which one sounds more natural or more appropriate. The trainer should also show how common expressions vary according to audience and context. This helps the learner avoid using one expression everywhere without considering its social value.

In workplace and daily communication, common expressions appear in customer contact, office notes, personal reminders, brief emails, service replies, and routine spoken exchanges. A learner who can use them well demonstrates not only language knowledge but also cultural awareness. Common difficulties include overusing literal translations from another language, choosing expressions that are too casual for the context, or forgetting the small phrases that help maintain politeness. Repeated practice in realistic scenarios helps build better judgment.

By the end of this content, the learner should be able to recognize and use common French expressions in ways that suit the situation and relationship. The key lesson is that small expressions carry cultural meaning. When trainees learn to use these expressions appropriately, their communication becomes more natural, respectful, and sensitive to context.

The learner should also notice that common expressions often help transitions in interaction, such as opening, thanking, apologizing, and closing. These small phrases may look simple, but they shape how comfortable the exchange feels. Through repeated practice with realistic scenarios, the trainee becomes better at choosing expressions that match the context instead of relying on literal translation alone.

Another useful step is to ask the learner why a certain expression sounds more natural in one setting than another. This encourages judgment instead of memorization only. As that judgment improves, the learner becomes more capable of using French in ways that respect tone, relationship, and social expectation.

This kind of awareness helps the trainee sound less mechanical and more socially appropriate. Over time, common expressions become practical tools for smoother interaction instead of isolated phrases remembered without context.

When learners practice these expressions across greetings, thanks, apologies, and closings, they begin to hear how French interaction is shaped by routine phrasing. That awareness helps them communicate with more ease and better cultural fit in both personal and professional situations.""",
    "2_1": """Passe Compose is important in cultural and practical communication because people often talk about past events when sharing experience, explaining what happened, and building common understanding. In customer service, school, and workplace settings, short explanations about past actions are common. A learner may need to say what was done, what happened during a visit, or what action has already been completed. This content helps learners understand how French expresses completed past actions and how that structure supports clear communication in socially appropriate ways.

The lesson introduces the basic role of Passe Compose as a tense used to report finished events. Rather than treating it only as an abstract grammar topic, the learner should see it as a tool for meaningful communication. A short explanation about a missed appointment, a completed task, a previous visit, or a resolved concern often depends on this structure. When the learner understands how the tense functions, messages about the past become easier to follow and produce. This is especially important in situations where someone must explain an event politely and accurately.

A practical example is a learner writing a short note stating that a client already arrived, a file was already submitted, or a meeting already happened. These short past references are common in office and service communication. If the learner misuses the tense, the timing of the event may become unclear. When the tense is used correctly, the message tells the reader that the action is complete and no longer only planned. This is why the content matters in both grammar and real communication.

Teaching should involve short narratives, simple workplace updates, timeline activities, and comparison between present and past meaning. Learners can rewrite present-tense sentences into past event notes and identify when the action was completed. The trainer should keep examples practical and connected to routine communication. This helps the learner see the tense as part of useful expression rather than as isolated memorization.

In workplace use, Passe Compose can appear in short reports, absence explanations, customer follow-up notes, service updates, and brief summaries of completed tasks. A learner who can handle this tense at a beginner level is better prepared to communicate about what has already happened. Common problems include mixing present and past meaning, forgetting the helping verb, or using the tense without a clear completed event. Guided exercises with realistic context help reduce these errors.

By the end of this content, the learner should be able to recognize and use basic Passe Compose structures to refer to simple completed events in French. The major lesson is that past-event language supports clear and culturally appropriate explanation. When trainees can refer to completed actions properly, they communicate more accurately and more responsibly in daily and workplace settings.

The learner also benefits from comparing a present-tense statement with its past-event equivalent. This helps show exactly how the meaning shifts when the action has already happened. As trainees practice this contrast in realistic workplace examples, they become more confident in giving short explanations about completed activities, visits, or service actions in French.

The trainer can strengthen this content by asking the learner to identify which part of the sentence signals completion most clearly. This turns tense study into a reading and writing strategy. Over time, the trainee gains better control of how French marks finished action in practical communication.

As confidence improves, learners can use Passe Compose in short explanations that sound more accurate and more responsible. This is especially useful when describing completed duties, past visits, or previous service actions in French.

The learner should also practice checking whether the sentence clearly shows that the action is finished and not still in progress. This makes the tense more meaningful in context. Through repeated examples, past-event writing becomes clearer and more dependable in real communication.""",
    "2_2": """Auxiliary Verbs are central to understanding and using Passe Compose because they help build the tense structure that marks a completed event. In French, the auxiliary verb supports the main verb and allows the speaker or writer to communicate what has already happened. For learners, this is more than a grammar detail. It is a communication tool. If the auxiliary is missing or incorrect, the meaning of the sentence becomes unstable. This content therefore helps the learner see how small grammatical elements support accurate expression of time and action.

The lesson explains that certain past-event statements require a helping verb before the main past participle. The learner should understand the auxiliary as a support element that carries person and tense information. This is useful in short notes and explanations where the learner must say what was done, what occurred, or what has already been completed. Rather than learning a list without context, learners should study auxiliaries through short practical messages so they can see the pattern repeatedly in meaningful communication.

A useful example is a short service note explaining that a customer has called, a student has submitted a form, or a worker has completed a task. In each case, the auxiliary helps frame the completed action. If the learner recognizes the auxiliary correctly, reading and writing become more manageable. The trainee can also understand why two similar messages may differ if the auxiliary choice changes. This helps build more careful language awareness.

Teaching should use model sentences, matching tasks, fill-in activities, and short note-writing practice. Learners can identify the auxiliary in a sentence, explain its role, and then build their own short past-event messages. The trainer should keep examples tied to daily and workplace communication so the grammar remains connected to real use. This helps learners see pattern and function together.

In practical communication, auxiliary verbs matter in short updates, event summaries, absence notes, service records, and completed-task messages. A learner who can use them correctly gains more control over written and spoken French about the past. Common difficulties include forgetting the auxiliary, choosing the wrong one, or treating the past expression as if it were only vocabulary. Repeated guided practice helps reduce these issues and improves sentence confidence.

By the end of this content, the learner should be able to identify the role of auxiliary verbs in simple past-event French sentences and apply them in short practical communication. The key lesson is that small support verbs create major meaning. When the trainee understands auxiliaries, the structure of past communication becomes clearer and more accurate.

Another useful practice is to examine several short notes and identify how the auxiliary changes according to the subject and action. This repetition helps learners see patterns rather than isolated rules. As the trainee becomes more familiar with those patterns, past-event writing becomes less intimidating and more accurate in everyday communication.

The learner should also see that auxiliary verbs are small but essential parts of sentence control. Missing them weakens the whole message. When these supporting verbs are practiced often in short useful notes, the trainee becomes more accurate and more confident in basic past communication.

This repeated practice also helps learners read past-event messages more quickly because they start to recognize the pattern immediately. That stronger recognition supports both understanding and writing in routine French communication.

As the learner gains control of these helpers, short French updates about completed actions become easier to produce and easier to understand. This makes auxiliary practice especially useful in routine messages, workplace notes, and simple service records.

The trainer can also ask the learner to explain why the auxiliary is needed before the past participle. This reflection strengthens structural understanding instead of memorization alone. With that awareness, the trainee becomes more accurate when building short French messages about completed actions.""",
    "2_3": """Sentence Construction is important because cultural awareness and grammar competence become useful only when the learner can organize them into clear, meaningful French sentences. In communication about past events, customer interaction, and everyday writing, the learner must build statements that follow a logical order and sound understandable to the reader or listener. Sentence construction therefore connects vocabulary, tense, tone, and purpose. A learner may know the right words, but if the sentence is poorly built, the message can still fail.

The lesson focuses on arranging words and ideas in a way that supports clear meaning. This includes placing subject, verb, and important details in sensible order, using short supporting phrases carefully, and avoiding unnecessary confusion. In beginner French, sentence construction should remain manageable. The learner does not need very long statements to communicate effectively. What matters is building sentences that are complete, understandable, and appropriate to the context. This is especially useful when reporting a past event, giving a short explanation, or responding to a customer concern.

A practical example is a learner writing a short explanation that a customer has already visited, that a form was submitted yesterday, or that a complaint was received in the morning. Each message depends on sentence construction to show who did what and when. If the sentence is incomplete or the ideas are out of order, the reader may not understand the main point. This example helps the learner see why structure matters in routine communication.

Teaching should use sentence-building tasks, rearrangement exercises, short model notes, and guided correction work. Learners can start with word groups and organize them into full messages, then revise unclear sentences into stronger forms. The trainer should emphasize clarity over complexity. This helps the learner become confident in writing and speaking short useful French sentences rather than worrying only about long grammar explanations.

In workplace and service communication, sentence construction supports notes, updates, explanations, reminders, and short reports. A learner who can build clear sentences becomes more dependable in practical tasks. Common problems include missing subjects, confusing word order, or combining too many ideas in one line. Guided step-by-step practice reduces these issues and supports more effective use of French.

By the end of this content, the learner should be able to construct short French sentences that clearly express simple past-related information and routine meaning. The major lesson is that communication quality depends on structure as well as vocabulary. When trainees can build clear sentences, they show stronger readiness for culturally aware and professionally useful communication.

The learner should also practice improving sentences that are grammatically possible but hard to understand. This revision process teaches that good communication is reader-centered, not only rule-centered. When trainees learn to build short French statements with better order and focus, their messages become more reliable for practical school and workplace use.

Another good activity is to ask learners to explain why one sentence order sounds clearer than another. This reflection helps them notice the practical effect of structure. As sentence awareness grows, short French writing becomes easier to organize and easier for others to interpret correctly.

The learner also benefits from reducing one idea per sentence when the message becomes too crowded. This simple habit improves readability and makes short French notes more useful in classrooms, offices, and service contexts.

With continued practice, the trainee begins to recognize that sentence structure is a form of respect for the reader. Clear order helps the listener or reader process the message quickly. That is why sentence construction remains important in both culturally aware and professionally useful communication.

The trainer can strengthen this skill by asking the learner to revise a sentence until its main meaning becomes immediately visible. This teaches that clarity is an active writing choice. Over time, sentence construction becomes a dependable foundation for short, accurate, and reader-friendly French communication.""",
    "3_1": """Assisting Customers is an important part of cultural awareness because service communication is not only about solving a problem. It is also about making the customer feel respected, understood, and properly guided. In French-speaking contexts, assistance often includes polite language, attentive response, and clear explanation. A learner who can assist a customer appropriately shows both language skill and social sensitivity. This content helps the learner understand how service-oriented communication reflects cultural expectations of courtesy and professionalism.

The lesson focuses on the language and attitude used when helping a customer. A service interaction may involve greeting the customer, asking what is needed, providing simple information, and checking whether additional help is required. The learner should notice that assisting language is usually respectful, patient, and solution-oriented. It is not enough to provide a direct answer only. The way help is offered also matters. This is why assisting customers belongs in a module on cultural sensitivity.

A practical example is a short front-desk interaction in which a customer asks for the location of an office, clarification about a schedule, or help with a form. The learner responds with respectful language and simple guidance. This example shows how service communication combines clarity and tone. If the helper sounds impatient or abrupt, the customer experience becomes less positive even when the information is correct. When the language is supportive, the exchange feels more professional and culturally appropriate.

Teaching should use role plays, service scripts, customer question cards, and short dialogue comparisons. Learners can identify which responses sound helpful and which ones sound dismissive. The trainer should emphasize listening, courteous phrasing, and calm response. These features help the learner understand that service communication depends on attitude expressed through language.

In real workplace settings, assisting customers appears in reception tasks, office counters, information desks, school services, and support roles. A learner who can assist politely in French is better prepared for multilingual service interaction. Common problems include giving information too quickly, using overly direct language, or failing to acknowledge the customer's need. Practice with realistic scenarios helps improve empathy and communication control.

By the end of this content, the learner should be able to use simple French to assist customers in a respectful and effective way. The central lesson is that good service communication reflects both practical help and cultural sensitivity. When trainees learn to assist with patience and clarity, they demonstrate language use that is socially aware and professionally useful.

The learner should also develop the habit of checking whether the response actually answers the customer's need. This prevents helpful tone from becoming empty politeness. Through guided service scenarios, trainees learn that strong customer assistance combines listening, clear explanation, and supportive language in a way that fits real workplace expectations.

The trainer can reinforce this by asking the learner to identify the exact helpful action in each response. This helps separate vague politeness from real assistance. As a result, learners become more capable of offering support that is both respectful and practically useful in French-speaking service encounters.

This makes the learner's service language more dependable because the response does more than sound polite. It actually guides the customer toward the needed information or next action in a culturally appropriate way.

The learner should also practice brief follow-up lines that confirm whether the customer understood the guidance. This extra care reflects attentiveness and improves the quality of assistance. Over time, it helps the trainee deliver service communication that is both efficient and considerate.

Another valuable habit is to check whether the response would make the customer feel welcomed rather than merely processed. This helps connect language with attitude. As the trainee improves, customer assistance becomes more human, more culturally aware, and more effective in routine service situations.""",
    "3_2": """Handling Complaints requires cultural awareness because complaint situations are emotionally sensitive and can quickly become negative if the response is careless. A learner must understand that in French communication, as in many service contexts, tone, acknowledgment, and respectful language are essential when responding to dissatisfaction. The goal is not only to answer the complaint, but also to manage the interaction with calmness and professionalism. This content helps the learner see that language can reduce tension when it is used with care.

The lesson begins with the idea that a complaint should first be recognized and acknowledged. The learner should know how to respond politely, show attention, and avoid language that sounds defensive or dismissive. Even in short messages or simple spoken responses, this attitude matters. A culturally sensitive response often includes apology where appropriate, a calm explanation, and a step toward resolution. The learner should therefore treat complaint language as a social skill as well as a vocabulary topic.

A practical example is a customer explaining that an appointment was delayed, a requested document was not ready, or a service instruction was unclear. The learner responds by acknowledging the concern, apologizing politely if needed, and indicating the next step. This example shows that complaint handling depends on sequence: listen, recognize, respond, and move toward solution. If the learner skips acknowledgment and answers too directly, the customer may feel ignored. This makes the cultural dimension very clear.

Teaching should include complaint scenarios, response comparisons, apology phrases, and role-play correction activities. Learners can examine two different responses to the same complaint and discuss which one is more respectful and effective. The trainer should also emphasize emotional control. This is important because complaint communication can challenge the learner's confidence, especially at beginner level.

In workplace service, complaint handling appears in customer support, reception, office administration, school service counters, and other public-facing roles. A learner who can respond to complaints appropriately in French demonstrates both language ability and maturity. Common problems include reacting too quickly, giving an excuse before showing understanding, or sounding abrupt. Repeated practice helps learners build steadier response patterns and stronger empathy.

By the end of this content, the learner should be able to respond to simple complaints in French with respectful, calm, and solution-aware language. The main lesson is that complaint handling depends on cultural sensitivity as much as on grammar. When trainees can manage complaints politely, they show readiness for responsible communication in real service settings.

Another effective exercise is to compare a poor complaint response with an improved one and discuss the difference in impact. This helps the learner see how acknowledgment, tone, and calm sequencing change the whole interaction. As the trainee becomes more practiced, complaint handling feels less threatening and more manageable in French service communication.

The learner should also review whether the response gives the customer a sense that the concern has been taken seriously. This small cultural detail matters in service settings. When learners practice combining acknowledgment with next-step language, they become more effective and more empathetic communicators.

As learners repeat complaint scenarios, they become better at controlling tone under pressure. That steady control is important in real service situations where the quality of the response can affect trust and cooperation.

This practice also helps the learner separate personal reaction from professional response. When that separation becomes stronger, the trainee can answer complaints more calmly and more effectively in French, even when the situation is uncomfortable or emotionally charged.

The learner should also review whether the response keeps the conversation moving toward resolution instead of argument. This makes complaint language more practical and more culturally appropriate. With repeated scenarios, trainees build confidence in staying respectful while still responding clearly to dissatisfaction.""",
    "3_3": """Offering Solutions is the final step in many customer service interactions and an important sign of culturally sensitive communication. After listening, acknowledging, and clarifying a concern, the learner should be able to present a simple next step or possible solution in French. This content matters because good communication does not stop at sympathy. It should also guide the customer or other person toward resolution. In culturally aware service behavior, solutions should be explained clearly, respectfully, and without making the other person feel dismissed.

The lesson focuses on practical solution language: suggesting an alternative, explaining the next procedure, offering assistance, or indicating what can be done now. The learner should understand that the solution must fit the problem and the communication context. A response that is grammatically correct but socially abrupt may still sound insensitive. For that reason, the learner must combine clarity with tone. This makes solution language an important part of both service communication and cultural competence.

A useful example is a learner responding to a customer whose scheduled meeting must be moved. Instead of ending with an apology only, the learner offers a new time, explains who will assist next, or suggests an immediate alternative. This type of response shows initiative and respect. It also helps the customer feel that the concern is being addressed. The example highlights that a solution-oriented message often includes both action and reassurance.

Teaching should involve scenario cards, solution-building exercises, role plays, and guided response writing. Learners can study a problem, identify a realistic next step, and practice stating it in simple French. The trainer should encourage messages that are short but complete enough to move the interaction forward. This is especially useful for beginner learners, who may feel comfortable apologizing but less confident when proposing a solution.

In workplace use, offering solutions is important in front-desk service, office support, school administration, scheduling issues, and routine customer contact. A learner who can offer a simple solution in French is better prepared for real service work. Common difficulties include ending the response too early, giving a vague answer, or offering a solution without first showing understanding. Structured practice helps learners connect empathy with action.

By the end of this content, the learner should be able to offer a simple, respectful solution in French after a routine problem or concern is raised. The key lesson is that culturally sensitive communication should help move the interaction toward resolution. When trainees can propose useful next steps with the right tone, they demonstrate stronger service readiness and more mature language use.

The learner should also practice checking whether the proposed solution is realistic, clear, and connected to the concern that was raised. This prevents vague answers that sound polite but do not help. With repeated scenario practice, trainees become more confident in moving from understanding a problem to expressing a respectful and useful response in French.

Another valuable habit is to restate the final action in one simple sentence after proposing it. This helps the learner make the solution easy to remember and follow. Through repetition, the trainee becomes more skilled at turning service problems into clear, solution-oriented French communication.

This final clarity is especially useful in workplaces where several people may depend on the same message. A well-stated solution supports coordination, reduces confusion, and reflects both practical thinking and cultural sensitivity.

The learner should also review whether the proposed solution gives the other person a clear next action or expectation. This turns the response into something truly useful rather than simply polite. With repeated practice, trainees become better at offering solutions that are both respectful and operationally helpful.""",
}


content_entries = [
    {
        "field": "1_1",
        "title": "Formal Writing",
        "apply": {
            "title": "Write a Short Formal French Note",
            "objective": "Write a short formal French note using respectful greeting, clear purpose, and appropriate closing for a workplace or school setting.",
            "sup_mat": "Formal note sample\nTone guide\nChecklist",
            "equipment": "Printed worksheet\nPen\nReference phrases list",
            "steps": "1. Read the communication scenario.\n2. Identify the reader and purpose.\n3. Select an appropriate formal greeting.\n4. Write the short note in French.\n5. Add a suitable formal closing.\n6. Review the note for tone and completeness.",
            "assessment": "Short formal writing task with checklist and trainer feedback.",
            "pcs": [
                "Used an appropriate formal greeting.",
                "Stated the purpose clearly and respectfully.",
                "Maintained a formal tone throughout the note.",
                "Included a suitable closing line.",
                "Produced an organized and readable message.",
            ],
        },
        "mcqs": [
            {"q": "Why is formal writing important in cultural awareness?", "options": ["It shows respect and role awareness", "It removes the need for grammar", "It is used only in stories", "It replaces all speech"], "answer": "A"},
            {"q": "A formal note is commonly written for", "options": ["a supervisor or unfamiliar reader", "a close friend only", "a sports team only", "a drawing activity"], "answer": "A"},
            {"q": "What should a formal message include?", "options": ["respectful greeting and closing", "slang terms only", "no purpose statement", "casual abbreviations only"], "answer": "A"},
            {"q": "What is a common error in formal writing?", "options": ["using language that is too casual", "writing neatly", "checking the audience", "reviewing tone"], "answer": "A"},
            {"q": "Why does formal tone matter?", "options": ["It shapes how the message is received", "It changes the date", "It replaces vocabulary", "It removes sentence structure"], "answer": "A"},
            {"q": "Which activity supports this content?", "options": ["comparing formal and informal notes", "counting words only", "memorizing colors only", "drawing borders"], "answer": "A"},
            {"q": "Formal writing is useful in", "options": ["requests and professional notes", "games only", "songs only", "recipes only"], "answer": "A"},
            {"q": "What should the learner consider before writing formally?", "options": ["audience and purpose", "paper size only", "desk arrangement only", "ink brand only"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["write a respectful formal note", "ignore the reader role", "use slang in all settings", "skip the closing"], "answer": "A"},
            {"q": "The main lesson is that formality reflects", "options": ["cultural sensitivity and professionalism", "only handwriting style", "only grammar drills", "only spelling length"], "answer": "A"},
        ],
    },
    {
        "field": "1_2",
        "title": "Informal Writing",
        "apply": {
            "title": "Write a Friendly Informal Message",
            "objective": "Write a short informal French message for a familiar reader using suitable tone and clear everyday purpose.",
            "sup_mat": "Informal note sample\nAudience guide\nChecklist",
            "equipment": "Printed task sheet\nPen\nReference expressions list",
            "steps": "1. Read the familiar-reader scenario.\n2. Identify the purpose of the message.\n3. Choose an appropriate informal opening.\n4. Write the short message in French.\n5. Add a friendly closing line.\n6. Review the note for tone and clarity.",
            "assessment": "Short informal writing task with checklist review.",
            "pcs": [
                "Used a suitable informal greeting.",
                "Matched the tone to a familiar audience.",
                "Expressed the purpose clearly.",
                "Closed the message in a friendly way.",
                "Produced a clear and natural short note.",
            ],
        },
        "mcqs": [
            {"q": "Why is informal writing part of cultural awareness?", "options": ["Because tone should match familiar relationships", "Because all writing must be formal", "Because grammar becomes optional", "Because it replaces all notes"], "answer": "A"},
            {"q": "Informal writing is usually appropriate for", "options": ["friends or familiar peers", "formal clients only", "official reports only", "public speeches only"], "answer": "A"},
            {"q": "What should informal writing still include?", "options": ["clear purpose and understandable meaning", "no structure at all", "random vocabulary only", "formal titles only"], "answer": "A"},
            {"q": "A common learner error is", "options": ["using informal tone in the wrong setting", "reading the prompt", "checking the audience", "writing clearly"], "answer": "A"},
            {"q": "Why is audience important in informal writing?", "options": ["It determines whether relaxed tone is appropriate", "It changes the calendar", "It removes sentence meaning", "It replaces greetings"], "answer": "A"},
            {"q": "Which exercise supports this lesson?", "options": ["matching messages with the right audience", "counting lines only", "memorizing months only", "drawing shapes"], "answer": "A"},
            {"q": "Informal writing can still be", "options": ["clear and culturally appropriate", "disorganized and careless", "without meaning", "only slang-based"], "answer": "A"},
            {"q": "What should the learner avoid?", "options": ["confusing friendliness with carelessness", "using a friendly closing", "writing a clear purpose", "checking tone"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["write a suitable informal note for a familiar person", "use the same tone for everyone", "ignore relationship clues", "avoid purpose"], "answer": "A"},
            {"q": "The main lesson is that informal writing still needs", "options": ["awareness and audience fit", "formal titles only", "no grammar", "no structure"], "answer": "A"},
        ],
    },
    {
        "field": "1_3",
        "title": "Common Expressions",
        "apply": {
            "title": "Use Common Expressions Appropriately",
            "objective": "Select and use common French expressions in a short message or dialogue according to the situation and relationship.",
            "sup_mat": "Expression list\nSituation cards\nChecklist",
            "equipment": "Printed handout\nPen\nDialogue prompt",
            "steps": "1. Read the assigned situation.\n2. Identify the tone and relationship involved.\n3. Choose suitable common expressions.\n4. Write or complete the short message.\n5. Check if the expressions fit the context.\n6. Review the work with the trainer.",
            "assessment": "Situation-based expression task with checklist.",
            "pcs": [
                "Selected expressions appropriate to the situation.",
                "Matched expression tone with the relationship.",
                "Used common expressions naturally in the message.",
                "Avoided expressions that were too casual or too formal.",
                "Produced a context-appropriate short communication.",
            ],
        },
        "mcqs": [
            {"q": "Why are common expressions important?", "options": ["They carry social and cultural meaning", "They replace all verbs", "They are only decorative", "They remove tone"], "answer": "A"},
            {"q": "What should a learner study besides translation?", "options": ["the social purpose of the expression", "the paper color", "the table height", "the pen type"], "answer": "A"},
            {"q": "Common expressions can help a message sound", "options": ["more natural and appropriate", "more confusing only", "longer without meaning", "completely informal always"], "answer": "A"},
            {"q": "A common error is", "options": ["using one expression in every situation", "reading a sample", "matching situations", "reviewing tone"], "answer": "A"},
            {"q": "Which setting may use common expressions?", "options": ["daily and workplace communication", "mathematics formulas only", "map labels only", "sports scores only"], "answer": "A"},
            {"q": "Why does context matter for common expressions?", "options": ["Because expressions vary by audience and purpose", "Because expressions have no meaning", "Because all phrases are equal", "Because grammar disappears"], "answer": "A"},
            {"q": "Which classroom activity supports this topic?", "options": ["matching expressions with situations", "counting letters only", "drawing pictures only", "memorizing colors only"], "answer": "A"},
            {"q": "What do common expressions often help maintain?", "options": ["politeness and social harmony", "calendar order", "room size", "paper design"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["use common expressions appropriately by context", "ignore relationship clues", "avoid tone differences", "use slang everywhere"], "answer": "A"},
            {"q": "The main lesson is that small expressions can carry", "options": ["cultural meaning", "no useful meaning", "only spelling", "only punctuation"], "answer": "A"},
        ],
    },
    {
        "field": "2_1",
        "title": "Passe Composé",
        "apply": {
            "title": "Write a Short Past Event Note",
            "objective": "Write a short French note about a completed event using a basic Passe Compose structure correctly.",
            "sup_mat": "Past-event prompt\nModel sentences\nChecklist",
            "equipment": "Printed worksheet\nPen\nVerb reference list",
            "steps": "1. Read the past-event scenario.\n2. Identify the completed action to report.\n3. Build the sentence using Passe Compose.\n4. Add the needed time or context detail.\n5. Check the note for tense accuracy.\n6. Review the work with the trainer.",
            "assessment": "Short past-event writing task with checklist.",
            "pcs": [
                "Identified the completed event correctly.",
                "Used a basic Passe Compose structure appropriately.",
                "Maintained clear past meaning in the note.",
                "Included useful context detail such as time or action.",
                "Produced a clear short past-event message.",
            ],
        },
        "mcqs": [
            {"q": "Why is Passe Compose useful in communication?", "options": ["It helps refer to completed past actions", "It replaces all present tense", "It removes time meaning", "It is used only in poems"], "answer": "A"},
            {"q": "A practical use of Passe Compose is", "options": ["reporting what already happened", "giving colors only", "naming rooms only", "counting objects only"], "answer": "A"},
            {"q": "What can happen if the tense is misused?", "options": ["The event timing may become unclear", "The paper becomes smaller", "The message turns informal", "The reader forgets the name"], "answer": "A"},
            {"q": "Which setting may use short past-event notes?", "options": ["offices and service updates", "games only", "songs only", "painting tasks only"], "answer": "A"},
            {"q": "Why should learners study Passe Compose in context?", "options": ["So grammar connects to real communication", "So grammar can be ignored", "So only vocabulary matters", "So the past is never used"], "answer": "A"},
            {"q": "A useful classroom task is", "options": ["rewriting present statements as completed events", "counting lines only", "drawing borders only", "sorting paper"], "answer": "A"},
            {"q": "A common learner problem is", "options": ["mixing present and past meaning", "reading the prompt", "reviewing examples", "checking the audience"], "answer": "A"},
            {"q": "Passe Compose is most closely linked with", "options": ["finished actions", "future guesses", "color choices", "room labels"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["write a short clear completed-event note", "avoid all past references", "ignore tense meaning", "remove context detail"], "answer": "A"},
            {"q": "The key lesson is that past-event language supports", "options": ["accurate explanation", "only decoration", "only spelling", "only titles"], "answer": "A"},
        ],
    },
    {
        "field": "2_2",
        "title": "Auxiliary Verbs",
        "apply": {
            "title": "Identify and Use Auxiliary Verbs in a Past Message",
            "objective": "Use the correct auxiliary verb in a short French past-event note to support clear and accurate meaning.",
            "sup_mat": "Sentence models\nAuxiliary guide\nChecklist",
            "equipment": "Printed activity sheet\nPen\nVerb chart",
            "steps": "1. Review the model past-event sentences.\n2. Identify the auxiliary verb in each example.\n3. Select the correct auxiliary for the task.\n4. Write the short note in French.\n5. Check the sentence for complete tense structure.\n6. Review corrections with the trainer.",
            "assessment": "Guided past-message writing task with checklist review.",
            "pcs": [
                "Recognized the auxiliary verb correctly.",
                "Selected the proper auxiliary for the sentence.",
                "Used the auxiliary to support clear past meaning.",
                "Maintained complete sentence structure.",
                "Produced an accurate short past-event note.",
            ],
        },
        "mcqs": [
            {"q": "Why are auxiliary verbs important in Passe Compose?", "options": ["They help build the past-event structure", "They replace the main verb", "They remove time meaning", "They are only decorative"], "answer": "A"},
            {"q": "What can happen if the auxiliary is missing?", "options": ["The sentence meaning becomes unstable", "The page changes color", "The greeting disappears", "The note becomes informal"], "answer": "A"},
            {"q": "Auxiliary verbs are best studied through", "options": ["short meaningful sentences", "random word lists only", "maps only", "music notes only"], "answer": "A"},
            {"q": "A practical use of auxiliaries is", "options": ["writing completed-task updates", "drawing diagrams", "sorting colors", "naming furniture"], "answer": "A"},
            {"q": "What should the learner connect the auxiliary with?", "options": ["the completed action in the sentence", "the paper size", "the room number only", "the calendar month only"], "answer": "A"},
            {"q": "Which activity supports this lesson?", "options": ["identifying auxiliaries in model notes", "counting words only", "drawing borders only", "memorizing colors only"], "answer": "A"},
            {"q": "A common learner error is", "options": ["choosing the wrong auxiliary", "reading examples", "checking the sentence", "reviewing the prompt"], "answer": "A"},
            {"q": "Auxiliary verbs mainly support", "options": ["accurate tense meaning", "tone only", "page design", "title formatting"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["use an auxiliary correctly in a short note", "ignore tense structure", "write without verbs", "avoid past meaning"], "answer": "A"},
            {"q": "The main lesson is that small support verbs create", "options": ["major meaning", "no real meaning", "only decoration", "only punctuation"], "answer": "A"},
        ],
    },
    {
        "field": "2_3",
        "title": "Sentence Construction",
        "apply": {
            "title": "Build a Clear French Past-Event Sentence",
            "objective": "Construct a short French sentence that clearly expresses a simple past event in logical order.",
            "sup_mat": "Word groups\nSentence model\nChecklist",
            "equipment": "Printed worksheet\nPen\nReference sheet",
            "steps": "1. Review the given word groups.\n2. Identify the subject, action, and detail.\n3. Arrange the sentence in logical French order.\n4. Write the complete sentence.\n5. Check whether the meaning is clear.\n6. Revise the sentence based on feedback.",
            "assessment": "Sentence-building task with clarity and structure checklist.",
            "pcs": [
                "Placed the main sentence parts in logical order.",
                "Built a complete understandable sentence.",
                "Expressed the simple past-related meaning clearly.",
                "Avoided unnecessary confusion or missing parts.",
                "Produced a usable short French statement.",
            ],
        },
        "mcqs": [
            {"q": "Why is sentence construction important?", "options": ["It organizes vocabulary into clear meaning", "It replaces grammar", "It removes tense", "It is used only in long essays"], "answer": "A"},
            {"q": "What matters most in beginner sentence construction?", "options": ["clarity and completeness", "decoration only", "long length only", "complexity only"], "answer": "A"},
            {"q": "A short sentence can fail if", "options": ["its ideas are out of order", "the paper is white", "the pen is blue", "the room is quiet"], "answer": "A"},
            {"q": "Which practice supports this content?", "options": ["rearranging word groups into clear sentences", "counting syllables only", "drawing shapes only", "sorting colors only"], "answer": "A"},
            {"q": "Sentence construction is useful in", "options": ["notes, updates, and explanations", "sports flags only", "maps only", "songs only"], "answer": "A"},
            {"q": "A common learner problem is", "options": ["confusing word order", "reading the model", "using a checklist", "checking meaning"], "answer": "A"},
            {"q": "Why should learners avoid combining too many ideas?", "options": ["It can reduce clarity", "It improves decoration only", "It removes audience", "It changes the date"], "answer": "A"},
            {"q": "A clear sentence helps the reader", "options": ["understand who did what and when", "guess the paper color", "measure the desk", "find the pen brand"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["build a clear short French sentence", "avoid complete statements", "ignore order", "skip the action"], "answer": "A"},
            {"q": "The main lesson is that communication quality depends on", "options": ["structure as well as vocabulary", "paper size only", "ink type only", "font style only"], "answer": "A"},
        ],
    },
    {
        "field": "3_1",
        "title": "Assisting Customers",
        "apply": {
            "title": "Respond to a Customer Need Politely",
            "objective": "Use simple French to assist a customer respectfully by identifying the need and giving clear guidance or help.",
            "sup_mat": "Customer scenario card\nService phrases guide\nChecklist",
            "equipment": "Printed prompt\nPen\nRole-play cue cards",
            "steps": "1. Read the customer assistance scenario.\n2. Identify what the customer needs.\n3. Prepare a short respectful response in French.\n4. Include the needed guidance or information.\n5. Check the tone and clarity of the response.\n6. Present the response for review.",
            "assessment": "Customer-assistance response task with checklist.",
            "pcs": [
                "Identified the customer's need correctly.",
                "Used respectful service language.",
                "Provided clear and relevant assistance.",
                "Maintained a calm and helpful tone.",
                "Produced a practical customer response.",
            ],
        },
        "mcqs": [
            {"q": "Why is assisting customers part of cultural awareness?", "options": ["It combines help with respectful communication", "It replaces all grammar", "It is only about speed", "It removes tone"], "answer": "A"},
            {"q": "A helpful customer response should be", "options": ["clear and respectful", "abrupt and short only", "without guidance", "informal in every case"], "answer": "A"},
            {"q": "What should the learner identify first?", "options": ["the customer's need", "the desk size", "the paper type", "the calendar month"], "answer": "A"},
            {"q": "Why does tone matter in customer assistance?", "options": ["It affects how the service is experienced", "It changes the location", "It replaces information", "It removes the greeting"], "answer": "A"},
            {"q": "Which setting often uses assisting language?", "options": ["reception and information desks", "painting rooms only", "sports fields only", "music stages only"], "answer": "A"},
            {"q": "A common learner problem is", "options": ["sounding too abrupt", "reading the scenario", "checking tone", "reviewing guidance"], "answer": "A"},
            {"q": "A good classroom activity is", "options": ["comparing helpful and unhelpful service responses", "counting letters only", "drawing lines only", "memorizing colors only"], "answer": "A"},
            {"q": "Customer assistance language should be", "options": ["patient and solution-oriented", "careless and rushed", "without acknowledgment", "only formal titles"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["assist politely in simple French", "ignore the customer's concern", "avoid guidance", "skip respectful language"], "answer": "A"},
            {"q": "The main lesson is that good service communication reflects", "options": ["help plus cultural sensitivity", "only grammar drills", "only speed", "only vocabulary lists"], "answer": "A"},
        ],
    },
    {
        "field": "3_2",
        "title": "Handling Complaints",
        "apply": {
            "title": "Respond to a Simple Complaint Respectfully",
            "objective": "Respond to a simple customer complaint in French using acknowledgment, polite tone, and a calm next-step response.",
            "sup_mat": "Complaint scenario\nResponse model\nChecklist",
            "equipment": "Printed prompt\nPen\nRole-play note card",
            "steps": "1. Read the complaint situation.\n2. Identify the customer's concern.\n3. Begin with an appropriate acknowledgment.\n4. Write or state a calm French response.\n5. Include a respectful next step.\n6. Review the response with the trainer.",
            "assessment": "Complaint-response task with checklist and feedback.",
            "pcs": [
                "Recognized the complaint clearly.",
                "Used an appropriate acknowledgment or apology.",
                "Maintained a calm respectful tone.",
                "Included a suitable next-step response.",
                "Produced a controlled and effective reply.",
            ],
        },
        "mcqs": [
            {"q": "Why does complaint handling require cultural awareness?", "options": ["Because tone can reduce or increase tension", "Because grammar is unimportant", "Because complaints need no response", "Because only speed matters"], "answer": "A"},
            {"q": "What should come first in handling a complaint?", "options": ["acknowledging the concern", "giving an excuse immediately", "changing the topic", "ending the conversation"], "answer": "A"},
            {"q": "A complaint response should sound", "options": ["calm and respectful", "defensive and abrupt", "casual in every situation", "without empathy"], "answer": "A"},
            {"q": "Why is apology sometimes important?", "options": ["It shows recognition of the inconvenience", "It removes all solutions", "It replaces information", "It ends the service"], "answer": "A"},
            {"q": "Which setting may involve complaint handling?", "options": ["customer support and reception work", "painting only", "music practice only", "sports scoring only"], "answer": "A"},
            {"q": "A common learner problem is", "options": ["responding too quickly without acknowledgment", "reading the prompt", "using a checklist", "reviewing examples"], "answer": "A"},
            {"q": "What should follow acknowledgment?", "options": ["a respectful next step", "a random question", "silence only", "a change of language without meaning"], "answer": "A"},
            {"q": "Complaint practice helps learners build", "options": ["empathy and response control", "only speed", "only decoration", "only handwriting"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["manage a simple complaint politely", "ignore the concern", "avoid next steps", "skip tone awareness"], "answer": "A"},
            {"q": "The key lesson is that complaint handling depends on", "options": ["respect plus controlled response", "paper size", "font choice", "desk placement"], "answer": "A"},
        ],
    },
    {
        "field": "3_3",
        "title": "Offering Solutions",
        "apply": {
            "title": "Offer a Simple Service Solution",
            "objective": "Respond to a routine concern in French by proposing a respectful, clear, and practical solution or next step.",
            "sup_mat": "Problem scenario\nSolution phrases guide\nChecklist",
            "equipment": "Printed scenario sheet\nPen\nRole-play prompt",
            "steps": "1. Read the service problem scenario.\n2. Identify the concern and possible next step.\n3. Write or state a respectful French solution.\n4. Make sure the response is clear and realistic.\n5. Check whether the tone remains supportive.\n6. Review the response with the trainer.",
            "assessment": "Solution-offering response task with checklist evaluation.",
            "pcs": [
                "Identified a realistic solution to the concern.",
                "Expressed the next step clearly in French.",
                "Maintained respectful and supportive tone.",
                "Linked the solution to the actual problem.",
                "Produced a practical service-oriented response.",
            ],
        },
        "mcqs": [
            {"q": "Why is offering solutions important?", "options": ["It moves communication toward resolution", "It replaces listening", "It removes the need for tone", "It ends every problem immediately"], "answer": "A"},
            {"q": "A good solution response should be", "options": ["clear and respectful", "vague and abrupt", "without next steps", "only apologetic"], "answer": "A"},
            {"q": "What should the learner do after understanding the concern?", "options": ["propose a realistic next step", "ignore the problem", "change the language without explanation", "repeat the complaint only"], "answer": "A"},
            {"q": "Why is tone important when offering a solution?", "options": ["Because the response should still feel supportive", "Because tone replaces action", "Because tone changes the date", "Because solutions need no language"], "answer": "A"},
            {"q": "Which setting often requires solution language?", "options": ["front-desk and service communication", "painting tasks only", "music rehearsal only", "sports drills only"], "answer": "A"},
            {"q": "A common learner problem is", "options": ["ending with apology only and no action", "reading the prompt", "checking the scenario", "reviewing examples"], "answer": "A"},
            {"q": "What makes a solution useful?", "options": ["It fits the actual concern", "It is long only", "It avoids the issue", "It removes all explanation"], "answer": "A"},
            {"q": "Which activity supports this content?", "options": ["building a response from a service problem", "counting words only", "drawing shapes only", "sorting colors only"], "answer": "A"},
            {"q": "Competency is shown when the learner can", "options": ["offer a simple respectful solution in French", "ignore the next step", "avoid practical action", "skip supportive tone"], "answer": "A"},
            {"q": "The main lesson is that solution language should combine", "options": ["action and sensitivity", "paper and ink", "size and shape", "volume and speed"], "answer": "A"},
        ],
    },
]


payload = {
    "sector": "EDU",
    "qualification_title": qualification_title,
    "unit_of_competency": all_units[3],
    "module_title": all_modules[3],
    "next_unit_of_competency": "",
    "Module_Descriptor": (
        "This module develops the learner's cultural awareness and sensitivity in using French across written, explanatory, and service-oriented situations. "
        "It covers formal and informal writing, common expressions, basic past-event communication through Passe Compose, supporting auxiliaries, sentence construction, and customer service responses for assistance, complaints, and solutions. "
        "The trainee practices choosing language that fits the audience, context, and social expectation while maintaining clarity and respect. "
        "By the end of the module, the learner is expected to communicate in French with stronger tone awareness, cultural appropriateness, and practical readiness for school and workplace interaction."
    ),
    "Laboratory": "Language and Computer Laboratory",
    "training_materials": "\n".join(
        [
            "Formal and informal writing samples",
            "Common expression reference sheets",
            "Past-event sentence models",
            "Customer service scenario cards",
            "Complaint and solution response guides",
            "Printed note and message templates",
            "Role-play cue cards",
            "Laptop or desktop computer",
            "Pens, highlighters, and assessment checklists",
        ]
    ),
    "uc_no": 4,
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
    "LO_1": "Writing Communication",
    "LO_2": "Talking About Past Events",
    "LO_3": "Customer Service Situations",
    "Contents_1_1": "Formal Writing",
    "Contents_1_2": "Informal Writing",
    "Contents_1_3": "Common Expressions",
    "Contents_2_1": "Passé Composé",
    "Contents_2_2": "Auxiliary Verbs",
    "Contents_2_3": "Sentence Construction",
    "Contents_3_1": "Assisting Customers",
    "Contents_3_2": "Handling Complaints",
    "Contents_3_3": "Offering Solutions",
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
        "Module_Descriptor",
        "Laboratory",
        "training_materials",
        "uc_no",
    ]
    for key in required:
        assert str(payload.get(key, "")).strip(), f"Missing {key}"

    descriptor_wc = wc(payload["Module_Descriptor"])
    assert 80 <= descriptor_wc <= 120, f"Module_Descriptor must be 80-120 words, got {descriptor_wc}"
    assert payload["uc_no"] == 4

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
