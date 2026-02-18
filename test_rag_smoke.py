import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'Day-2'))
sys.path.insert(0, os.path.join(os.getcwd(), 'Day-3'))

from knowledge_base import KnowledgeBase
from rag_agent import RAGAgent

kb = KnowledgeBase('kb_test_script')
ids = kb.add_document('GDG events are free and open to all students. Register at gdg.community.dev', metadata={'source':'unit_test'})
print('Added chunks:', len(ids))

agent = RAGAgent(gemini_api_key=None, knowledge_base=kb)
res = agent.answer('How do I register for GDG?', verbose=True)
print('ANSWER:')
print(res['answer'])
print('\nSOURCES:', res['num_sources'])
