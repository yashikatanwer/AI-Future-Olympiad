from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent.parent
WEB = Path(__file__).resolve().parent

# AIFO is intentionally beginner-friendly: Grades 5–6 are very basic and playful;
# Grades 7–8 add a little more reasoning without becoming technical.
PRACTICE_Q = {
    '5-6': [
        ('Which one can use AI?', ['A voice assistant', 'A pencil', 'A ruler', 'A notebook'], 0),
        ('Where might you see AI?', ['In a video recommendation', 'Only in a classroom clock', 'Only in a paper book', 'Nowhere'], 0),
        ('If an AI gives an important answer, what should you do?', ['Check it', 'Believe it immediately', 'Share it without checking', 'Never ask questions'], 0),
        ('Which is a safe AI habit?', ['Keep private information private', 'Share passwords', 'Copy everything', 'Trust every answer'], 0),
        ('Why might YouTube suggest a football video?', ['You watched football videos before', 'Your phone knows the future', 'The video chooses itself', 'It is always the best video'], 0),
        ('Learning from examples means a system can:', ['Notice patterns in examples', 'Become a person', 'Never make mistakes', 'Know everything'], 0),
        ('If a voice assistant misunderstands you, can it be wrong?', ['Yes', 'No', 'Only on weekends', 'Never'], 0),
        ('Before using an AI tool, a student should:', ['Use it responsibly', 'Share a friend’s private information', 'Copy everything', 'Never check the result'], 0),
    ],
    '7-8': [
        ('A recommendation system usually tries to:', ['Suggest something a user may like', 'Guarantee the perfect choice', 'Make every user choose the same thing', 'Work without any information'], 0),
        ('Why can two students get different recommendations?', ['Their activity or interests may differ', 'AI gives random answers every time', 'Videos choose the students', 'Recommendations never change'], 0),
        ('Why should an important AI answer be checked?', ['AI can make mistakes', 'AI is always wrong', 'Checking is never useful', 'AI cannot use information'], 0),
        ('Which is responsible AI use?', ['Verify important information', 'Share private data', 'Copy without thinking', 'Assume confidence means truth'], 0),
        ('What can happen if examples used by an AI are poor?', ['It may learn a misleading pattern', 'It becomes human', 'It becomes perfect', 'It stops using information'], 0),
        ('Why should people stay involved in important AI-assisted decisions?', ['People can add context and judgment', 'People cannot understand technology', 'AI never needs checking', 'Decisions do not need context'], 0),
        ('If an AI answer conflicts with a reliable source, what should you do?', ['Verify the information', 'Choose AI automatically', 'Share both without checking', 'Delete the reliable source'], 0),
        ('What is one risk of seeing only one type of recommended content?', ['You may get a narrow view', 'You automatically know everything', 'Nothing can change', 'It guarantees the truth'], 0),
    ]
}

OLYMPIAD_Q = {
    '5-6': [
        ('A map app suggests a route after looking at roads and travel information. What is this an example of?', ['A possible use of AI', 'A paper-only activity', 'A ruler measuring distance', 'A pencil drawing'], 0),
        ('Which statement about AI is best?', ['AI can help with tasks but can also make mistakes', 'AI always knows the truth', 'AI has feelings like people', 'AI never needs information'], 0),
        ('Riya watches several drawing videos. Later, more drawing videos are suggested. Why?', ['The system noticed a pattern in what she watched', 'The phone became an artist', 'The videos talked to each other', 'The suggestions are guaranteed to be best'], 0),
        ('An AI gives an answer that sounds strange. What is the best first step?', ['Check the answer', 'Share it immediately', 'Assume it is true', 'Stop learning'], 0),
        ('Which information should a student avoid giving to an AI tool?', ['A private password', 'A general school topic', 'A public fact', 'A made-up example'], 0),
        ('Which is a good use of AI for learning?', ['Ask for an explanation and then think about it', 'Copy an entire assignment and submit it', 'Share someone’s private details', 'Never check the answer'], 0),
        ('Can machines think exactly like humans?', ['They can process information in ways that are different from human thinking', 'Yes, they have the same feelings', 'Yes, they have the same experiences', 'No machine can process information'], 0),
        ('A voice assistant misunderstands a question. What does this show?', ['AI systems can have limits and make mistakes', 'AI always understands everything', 'Humans never make mistakes', 'Voice assistants know every answer'], 0),
        ('Which action shows responsible AI use?', ['Protect privacy and check important information', 'Share another student’s details', 'Believe every output', 'Copy without understanding'], 0),
        ('Which is most like learning from examples?', ['Seeing several examples and noticing a pattern', 'Guessing without information', 'Becoming a human', 'Knowing every answer beforehand'], 0),
        ('Why can recommendations be different for different people?', ['People may have different interests and activity', 'Everyone receives exactly the same list', 'Recommendations are always facts', 'Videos decide the user’s interests'], 0),
        ('What is the main idea students should remember about AI?', ['Use it thoughtfully, safely and critically', 'Trust it without checking', 'Avoid all technology', 'Let it make every decision'], 0),
    ],
    '7-8': [
        ('A system recommends videos based on what a student watched before. What is it using?', ['A pattern in the student’s activity', 'A guaranteed prediction of the future', 'A fixed answer for everyone', 'No information'], 0),
        ('Why might an AI system make a wrong prediction?', ['Its examples or information may be limited or misleading', 'AI cannot process any information', 'AI always knows the context', 'Human checking makes predictions worse'], 0),
        ('Two students receive different recommendations. Which explanation makes the most sense?', ['Their previous activity or preferences may differ', 'The system must be broken', 'Recommendations are always identical', 'Videos choose randomly with no pattern'], 0),
        ('A student asks AI a factual question and gets a confident answer. What should happen next for important information?', ['Verify it with reliable sources', 'Treat confidence as proof', 'Share it immediately', 'Never question it'], 0),
        ('Why can the quality of examples matter when an AI learns patterns?', ['Poor examples can lead to misleading patterns', 'Examples make AI human', 'Examples guarantee perfect results', 'Examples remove the need for checking'], 0),
        ('Which is the strongest responsible-use choice?', ['Use AI as support while keeping human judgment', 'Let AI make every important decision', 'Upload private information whenever asked', 'Copy answers without understanding'], 0),
        ('An AI tool gives a student two different answers to the same question. What is a sensible response?', ['Check the information and compare reliable sources', 'Choose the longer answer automatically', 'Assume the newest answer is always true', 'Share both as facts'], 0),
        ('A recommendation system keeps showing only one kind of content. What could happen?', ['The user may see a narrower range of content', 'The system guarantees complete information', 'The user automatically becomes an expert', 'The content becomes true'], 0),
        ('Which example shows AI supporting learning rather than replacing thinking?', ['AI explains a concept and the student checks and understands it', 'AI completes an assignment for submission', 'AI chooses an answer without review', 'AI receives someone else’s private data'], 0),
        ('Why is human judgment important in an AI-assisted decision?', ['People can consider context, values and consequences', 'AI has no ability to process information', 'Humans must avoid all technology', 'AI decisions never have consequences'], 0),
        ('Which question is useful when checking an AI output?', ['How can I verify this?', 'How can I share it fastest?', 'Why should I never question it?', 'How can I hide the source?'], 0),
        ('What is a key goal of AIFO?', ['Help students understand AI and use it responsibly', 'Teach advanced coding to every student', 'Replace teachers with AI', 'Make students trust every AI answer'], 0),
    ]
}

ACTIVITIES = [
    ('Is It AI?', 'Identify everyday examples of AI and non-AI systems.', '/activities/is-it-ai'),
    ('Train the Machine', 'Use simple examples to see how a system can notice a pattern.', '/activities/train-machine'),
    ('Recommendation Detective', 'Change what a student watches and see how suggestions can change.', '/activities/recommendations'),
    ('AI Can Be Wrong', 'Discover why a confident AI answer still needs checking.', '/activities/ai-wrong'),
    ('Responsible AI Choices', 'Make safe choices about privacy, checking and responsible AI use.', '/activities/responsible'),
    ('AI & Technology Careers', 'Explore simple, age-appropriate ways people can work with technology.', '/activities/careers'),
]


def shell(title, body, next_href, next_label, back_href=None, back_label='← Back'):
    buttons = ''
    if back_href:
        buttons += f'<a class="btn ghost" href="{back_href}">{html.escape(back_label)}</a>'
    if next_href:
        buttons += f'<a class="btn" href="{next_href}">{html.escape(next_label)}</a>'
    pager = f'<div class="page-nav">{buttons}</div>' if buttons else ''
    nav = '''<nav><a class="brand" href="/">AIFO</a><div>
      <a href="/activities">Activities</a>
      <a href="/learn">Learn About AI</a>
      <a href="/practice">Practice</a>
      <a href="/olympiad">Olympiad</a>
      <a href="/about">About</a>
    </div></nav>'''
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | AIFO</title><link rel="stylesheet" href="/style.css"></head><body>{nav}<main>{body}{pager}</main><footer>AIFO · AI Future Olympiad · Educational program for Grades 5–8</footer></body></html>'''


def home():
    body = '''
    <section class="hero"><div>
      <span class="pill">AI Future Olympiad</span>
      <h1>Learn AI. Think critically. Use it responsibly.</h1>
      <p>A school-ready AI awareness and Olympiad program for Grades 5–8, built around simple learning, live demonstrations, guided practice and a friendly competition.</p>
      <div class="buttons"><a class="btn" href="/activities">Explore Activities</a><a class="btn ghost" href="/about">View School Proposal</a></div>
    </div><div class="hero-card"><div class="big">AI</div><p>Awareness → Learning → Olympiad</p></div></section>

    <section><span class="pill">AIFO structure</span><h2>Three simple phases</h2>
      <div class="grid three">
        <div><b>Phase 1 · Awareness</b><p>Simple explanations, real-life examples, live AI demos and interactive Q&A.</p></div>
        <div><b>Phase 2 · Guided Learning</b><p>Age-appropriate learning, hands-on activities, simulations, ethics and responsible-use lessons, plus practice.</p></div>
        <div><b>Phase 3 · Proposed Olympiad</b><p>A friendly 60-minute assessment using MCQs, cases and puzzles after students have learned and practiced.</p></div>
      </div>
    </section>'''
    return shell('Home', body, '/activities', 'Next: Activities →')


def learn():
    body = '''<h1>Learn About AI</h1><p>This section teaches the concepts first. <b>Practice</b> comes later and is for checking what students remember and understand.</p>
    <div class="grid two"><a class="card" href="/learn/5-6"><h2>Grades 5–6</h2><p><b>Understanding AI Around Us</b></p><p>What AI is, where students see it every day, humans vs machines, and using AI safely.</p></a>
    <a class="card" href="/learn/7-8"><h2>Grades 7–8</h2><p><b>Thinking Smarter with AI</b></p><p>How AI learns from examples, recommendations, mistakes, responsible use and technology careers.</p></a></div>
    <div class="info"><b>Learning style:</b> short explanations + familiar examples + live demos + reflection. No prior coding is needed.</div>'''
    return shell('Learn About AI', body, '/practice', 'Next: Practice →', '/', '← Home')


def track(g):
    topics = {
        '5-6': ['What is AI?', 'Where do we see AI every day? (maps, YouTube, voice assistants)', 'How are humans different from machines?', 'Can machines think like us?', 'Using AI safely and responsibly'],
        '7-8': ['How does AI learn from examples?', 'Why does YouTube recommend certain videos?', 'Can AI make mistakes? Why?', 'Good use vs misuse of AI tools', 'Exploring careers in AI & technology']
    }[g]
    focus = {'5-6': 'Awareness + Curiosity + Safe Use', '7-8': 'Logical Thinking + Responsibility + Future Readiness'}[g]
    lis = ''.join('<li>' + html.escape(x) + '</li>' for x in topics)
    body = f'<a class="back" href="/learn">← Learn About AI</a><h1>Grades {g}</h1><div class="card"><h2>What students learn</h2><ul>{lis}</ul><p><b>Focus:</b> {focus}</p></div><div class="info">Next, students use activities and guided practice to apply these ideas before the Olympiad.</div>'
    return shell('Learning Track', body, '/activities', 'Next: Activities →', '/learn')


def activities():
    cards_html = ''.join(f'<a class="card activity-card" href="{u}"><h2>{html.escape(t)}</h2><p>{html.escape(d)}</p><span class="activity-link">Open live demo →</span></a>' for t, d, u in ACTIVITIES)
    body = f'''<h1>Interactive Activities & Live Demos</h1><p>These are the hands-on part of AIFO. They are designed for the awareness session and guided-learning journey, so students can <b>see and try</b> ideas instead of only hearing about them.</p><div class="grid two">{cards_html}</div><div class="info"><b>Classroom use:</b> These demos can be projected during the school session and then reused by students for independent practice.</div>'''
    return shell('Activities', body, '/learn', 'Next: Learn About AI →', '/')


def activity_demo(slug):
    titles = dict((x[2].split('/')[-1], x[:2]) for x in ACTIVITIES)
    title, desc = titles[slug]
    next_map = {
        'is-it-ai': '/activities/train-machine', 'train-machine': '/activities/recommendations',
        'recommendations': '/activities/ai-wrong', 'ai-wrong': '/activities/responsible',
        'responsible': '/activities/careers', 'careers': '/learn'
    }
    next_label = 'Next Activity →' if slug != 'careers' else 'Next: Learn About AI →'
    if slug == 'is-it-ai':
        body = f'''<h1>{title}</h1><p>{desc}</p><div class="demo-card"><h2>Can you spot AI?</h2><p>Tap each example and decide.</p><div class="demo-options"><button type="button" class="demo-option" data-ai="true">YouTube recommends a video</button><button type="button" class="demo-option" data-ai="false">A normal pencil</button><button type="button" class="demo-option" data-ai="true">A voice assistant answers a question</button><button type="button" class="demo-option" data-ai="false">A ruler measures 10 cm</button></div><div id="demo-feedback" class="feedback" aria-live="polite">Choose an example.</div></div>'''
        script = '''<script>document.querySelectorAll('.demo-option').forEach(b=>b.addEventListener('click',()=>{const yes=b.dataset.ai==='true';document.getElementById('demo-feedback').textContent=yes?'Good thinking! This example can use AI.':'Correct — this basic task does not need AI.';}));</script>'''
    elif slug == 'train-machine':
        body = f'''<h1>{title}</h1><p>{desc}</p><div class="demo-card"><h2>Give the machine examples</h2><p>🍎 apple &nbsp; 🍎 apple &nbsp; 🍌 banana</p><button type="button" class="btn" id="train">Test the machine</button><div id="train-result" class="feedback" aria-live="polite">The machine is waiting for examples.</div></div>'''
        script = '''<script>document.getElementById('train').addEventListener('click',()=>document.getElementById('train-result').textContent='The machine notices a simple pattern and predicts a label for a similar example. A prediction is a guess based on patterns — it can still be wrong.');</script>'''
    elif slug == 'recommendations':
        body = f'''<h1>{title}</h1><p>{desc}</p><div class="demo-card"><h2>What did the student watch?</h2><div class="demo-options"><button type="button" class="demo-option" data-r="sports">⚽ Football</button><button type="button" class="demo-option" data-r="art">🎨 Drawing</button><button type="button" class="demo-option" data-r="science">🔬 Science</button></div><div id="rec-result" class="feedback" aria-live="polite">Recommendations will appear here.</div></div>'''
        script = '''<script>const recs={sports:'football highlights and sports videos',art:'drawing tutorials and creative videos',science:'space and science videos'};document.querySelectorAll('[data-r]').forEach(b=>b.addEventListener('click',()=>document.getElementById('rec-result').textContent='Because the student watched more of this type, a system might suggest: '+recs[b.dataset.r]+'. Different activity can lead to different suggestions.'));</script>'''
    elif slug == 'ai-wrong':
        body = f'''<h1>{title}</h1><p>{desc}</p><div class="demo-card"><h2>Confidence is not proof</h2><p><b>AI says:</b> “This answer must be correct because I am very confident.”</p><button type="button" class="demo-option" id="check">Should we trust it?</button><div id="wrong-result" class="feedback" aria-live="polite">Think before revealing the answer.</div></div>'''
        script = '''<script>document.getElementById('check').addEventListener('click',()=>document.getElementById('wrong-result').textContent='No. Confidence is not proof. Check important information using reliable sources.');</script>'''
    elif slug == 'responsible':
        body = f'''<h1>{title}</h1><p>{desc}</p><div class="demo-card"><h2>What would you do?</h2><p>An AI tool asks for your friend’s private phone number to answer a simple homework question.</p><div class="demo-options"><button type="button" class="demo-option" id="safe">Share it</button><button type="button" class="demo-option" id="private">Keep it private</button></div><div id="safe-result" class="feedback" aria-live="polite">Choose an action.</div></div>'''
        script = '''<script>document.getElementById('safe').addEventListener('click',()=>document.getElementById('safe-result').textContent='Not a good choice. Private information should be protected.');document.getElementById('private').addEventListener('click',()=>document.getElementById('safe-result').textContent='Great choice. Protect private information and find another way to complete the task.');</script>'''
    else:
        body = f'''<h1>{title}</h1><p>{desc}</p><div class="demo-card"><div class="career"><b>AI educator</b><span>Explains AI to people.</span></div><div class="career"><b>Data analyst</b><span>Finds useful patterns in data.</span></div><div class="career"><b>AI designer</b><span>Helps make technology useful and understandable.</span></div><div class="career"><b>AI engineer</b><span>Builds and improves AI systems.</span></div></div>'''
        script = ''
    return shell('Activity', body + script, next_map[slug], next_label, '/activities', '← Activities')


def selector(kind):
    if kind == 'practice':
        body = '''<h1>Practice</h1><p>Practice is separate from <b>Learn About AI</b>: here students answer short questions, check understanding and prepare for the Olympiad.</p><div class="grid two"><div class="card"><h2>Grades 5–6</h2><p>Very basic, friendly questions using familiar AI examples.</p><div class="buttons"><a class="btn" href="/practice/5-6">Start Practice</a><a class="btn ghost" href="/practice-pdf/5-6" target="_blank">Practice PDF ↗</a></div></div><div class="card"><h2>Grades 7–8</h2><p>Still beginner-friendly, with slightly more reasoning.</p><div class="buttons"><a class="btn" href="/practice/7-8">Start Practice</a><a class="btn ghost" href="/practice-pdf/7-8" target="_blank">Practice PDF ↗</a></div></div></div><div class="info"><b>Guided learning support:</b> use these questions alongside the booklet, activities and responsible-use lessons during the learning period.</div>'''
        return shell('Practice', body, '/olympiad', 'Next: Olympiad →', '/learn', '← Learn About AI')
    body = '''<h1>AIFO Olympiad</h1><p>The proposed Olympiad is a friendly, student-appropriate assessment of AI knowledge, reasoning and ethical judgment, designed to follow the learning and practice period.</p><div class="grid three"><div><b>Format</b><p>60 minutes with MCQs, cases and puzzles.</p></div><div><b>Purpose</b><p>Check understanding after learning and practice.</p></div><div><b>Outcome</b><p>Results and certificates can be part of a future school implementation.</p></div></div><div class="grid two"><a class="card" href="/olympiad/5-6"><h2>Grades 5–6</h2><p>Basic, enjoyable AI awareness and reasoning.</p></a><a class="card" href="/olympiad/7-8"><h2>Grades 7–8</h2><p>Basic concepts with slightly deeper reasoning.</p></a></div>'''
    return shell('Olympiad', body, '/about', 'Next: About →', '/practice', '← Practice')


def quiz(g, title, method_data=None):
    kind = 'practice' if title.startswith('Practice') else 'olympiad'
    qs = PRACTICE_Q[g] if kind == 'practice' else OLYMPIAD_Q[g]
    if method_data is not None:
        score = sum(int(method_data.get('q' + str(i), [-1])[0]) == q[2] for i, q in enumerate(qs))
        if kind == 'practice':
            body = f'<div class="result"><span class="pill">Practice Result</span><h1>{score} / {len(qs)}</h1><p>Review anything you missed, then continue learning before the AIFO Olympiad.</p><a class="btn" href="/practice/{g}">Try Again</a></div>'
            return shell('Practice Result', body, '/olympiad', 'Next: Olympiad →', '/practice', '← Practice')
        body = f'<div class="result"><span class="pill">Olympiad Demo Result</span><h1>{score} / {len(qs)}</h1><p>This is the proposed assessment experience. The real Olympiad would be conducted with a participating school after the learning period.</p><a class="btn" href="/olympiad/{g}">Try Again</a></div>'
        return shell('Olympiad Result', body, '/about', 'Next: About →', '/olympiad', '← Olympiad')
    blocks = []
    for i, (question, opts, ans) in enumerate(qs):
        labels = ''.join(f'<label><input type="radio" name="q{i}" value="{j}" required> {html.escape(o)}</label>' for j, o in enumerate(opts))
        blocks.append(f'<div class="question"><b>{i + 1}. {html.escape(question)}</b>{labels}</div>')
    body = f'<h1>{html.escape(title)} · Grades {g}</h1><form method="post">' + ''.join(blocks) + '<button class="btn" type="submit">Submit & See Score</button></form>'
    return shell(title, body, '/olympiad' if kind == 'practice' else '/about', 'Next: Olympiad →' if kind == 'practice' else 'Next: About →', f'/{kind}', '← Back')


def about():
    body = '''<h1>About AIFO</h1><div class="card"><p><b>AI Future Olympiad (AIFO)</b> is a proposed school program for Grades 5–8.</p><p>Its learning structure is: <b>Awareness → Guided Learning → Proposed Olympiad</b>. The website supports the idea with live demos, learning content, practice and a proposed assessment experience.</p><p>The school proposal below is the source document for the program concept and school-facing plan.</p></div><section><h2>Program Materials</h2><p>These AIFO resources are available for teachers, facilitators and students.</p><div class="grid three"><a class="card" href="/booklet/5-6" target="_blank"><h3>Student Booklet · Grades 5–6 ↗</h3><p>Understanding AI Around Us.</p></a><a class="card" href="/booklet/7-8" target="_blank"><h3>Student Booklet · Grades 7–8 ↗</h3><p>Thinking Smarter with AI.</p></a><a class="card" href="/resource/teacher" target="_blank"><h3>Teacher &amp; Facilitator Guide ↗</h3><p>Practical support for the AIFO learning experience.</p></a></div></section><section class="proposal-section"><div class="proposal-heading"><div><span class="pill">School Proposal</span><h2>AIFO Proposal</h2><p>The original school proposal is shown below.</p></div><a class="btn" href="/proposal" target="_blank">Open PDF ↗</a></div><iframe class="proposal-frame" src="/proposal" title="AIFO School Proposal"></iframe></section>'''
    return shell('About', body, '/', 'Back to Home →', '/olympiad', '← Olympiad')



class Handler(BaseHTTPRequestHandler):
    def send(self, content, status=200, ctype='text/html; charset=utf-8'):
        b = content.encode() if isinstance(content, str) else content
        self.send_response(status)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        p = urlparse(self.path).path
        if p == '/': return self.send(home())
        if p == '/style.css': return self.send((WEB / 'static/style.css').read_bytes(), ctype='text/css')
        if p == '/learn': return self.send(learn())
        if p.startswith('/learn/') and p.split('/')[-1] in PRACTICE_Q: return self.send(track(p.split('/')[-1]))
        if p == '/activities': return self.send(activities())
        if p.startswith('/activities/') and p.split('/')[-1] in {x[2].split('/')[-1] for x in ACTIVITIES}: return self.send(activity_demo(p.split('/')[-1]))
        if p == '/practice': return self.send(selector('practice'))
        if p == '/olympiad': return self.send(selector('olympiad'))
        for kind in ('practice', 'olympiad'):
            if p.startswith('/' + kind + '/') and p.split('/')[-1] in PRACTICE_Q:
                return self.send(quiz(p.split('/')[-1], 'Practice Quiz' if kind == 'practice' else 'AIFO Proposed Olympiad'))
        if p == '/about': return self.send(about())
        if p == '/proposal':
            data = (ROOT / '01_School_Proposal/AIFO-School-Proposal.pdf').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Disposition', 'inline; filename="AIFO-School-Proposal.pdf"')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        resource_map = {
            '/booklet/5-6': '04_Student_Materials/Grade_5-6/AIFO-Student-Booklet-Grades-5-6.pdf',
            '/booklet/7-8': '04_Student_Materials/Grade_7-8/AIFO-Student-Booklet-Grades-7-8.pdf',
            '/resource/teacher': '03_Teacher_Guide/AIFO-Teacher-Facilitator-Guide.pdf',
            '/practice-pdf/5-6': '06_Practice_Sets/AIFO-Practice-Questions-Grade-5-6.pdf',
            '/practice-pdf/7-8': '06_Practice_Sets/AIFO-Practice-Questions-Grade-7-8.pdf',
        }
        if p in resource_map:
            data = (ROOT / resource_map[p]).read_bytes()
            names = {
                '/booklet/5-6': 'AIFO-Student-Booklet-Grades-5-6.pdf',
                '/booklet/7-8': 'AIFO-Student-Booklet-Grades-7-8.pdf',
                '/resource/teacher': 'AIFO-Teacher-Facilitator-Guide.pdf',
                '/practice-pdf/5-6': 'AIFO-Practice-Questions-Grades-5-6.pdf',
                '/practice-pdf/7-8': 'AIFO-Practice-Questions-Grades-7-8.pdf',
            }
            filename = names.get(p, 'AIFO-Resource.pdf')
            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Disposition', f'inline; filename=\"{filename}\"')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        return self.send('Not found', 404)

    def do_POST(self):
        p = urlparse(self.path).path
        if p.startswith('/practice/') or p.startswith('/olympiad/'):
            g = p.split('/')[-1]
            if g in PRACTICE_Q:
                n = int(self.headers.get('Content-Length', '0'))
                data = parse_qs(self.rfile.read(n).decode())
                return self.send(quiz(g, 'Practice Quiz' if p.startswith('/practice') else 'AIFO Proposed Olympiad', data))
        return self.send('Not found', 404)


if __name__ == '__main__':
    print('AIFO is running at http://127.0.0.1:8000')
    HTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
