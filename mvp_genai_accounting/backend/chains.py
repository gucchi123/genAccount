import os, json, yaml
import openai, urllib3

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ❷ TLS 証明書検証を無効化（今回のポイント）
openai.verify_ssl_certs = False

# ❸ もし今後プロキシが必要になったら、環境変数から読む形で書いておくと便利
proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
if proxy:
    openai.proxy = {"https": proxy}    # ← ★アンコメント
else:
    print("⚠ HTTPS_PROXY が未設定です。")



from typing import Dict, Any, List
from langchain_openai import ChatOpenAI          # ← 新パッケージ
from langchain_core.prompts import PromptTemplate
from langchain.chains import SequentialChain, LLMChain



narrative_prompt = PromptTemplate(
    template="""You are a bilingual accounting case writer. Output ONLY valid Markdown. 
    Tone: concise but vivid. Target: CPA candidates in Japan. Include IFRS citations.
    Write a case narrative in ≤ 350 words using the following metadata:
    {yaml_dump}
    Structure sections:
    1. Background – 2 paragraphs
    2. Transaction Events – bullet list
    3. Exhibit – single table of key figures (JPY millions)""", 
    input_variables=["yaml_dump"]
)

qa_prompt = PromptTemplate(
    template="""
You are an authoritative CPA exam-prep author.
Output JSON with keys: questions (array), answers (array), rationale (array).
Each question: MCQ with 4 options labeled A–D.
Difficulty must equal metadata.difficulty.

Based on this narrative:
{narrative}

Generate 5 MCQs that test the stated learning_objectives.
Limit calculations to 2-step max.
""",
    input_variables=["narrative"],
)


def generate_case(yaml_meta: str) -> Dict[str, Any]:
    meta = yaml.safe_load(yaml_meta)
    yaml_dump = yaml.dump(meta, allow_unicode=True)
    narrative_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.4)
    exam_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

    narrative_chain = LLMChain(llm=narrative_llm, prompt=narrative_prompt, output_key="narrative")
    qa_chain = LLMChain(llm=exam_llm, prompt=qa_prompt, output_key="qa")

    chain = SequentialChain(chains=[narrative_chain, qa_chain], input_variables=["yaml_dump"], output_variables=["narrative", "qa"])

    result = chain.invoke({"yaml_dump": yaml_dump})
    return result

# Placeholder in-memory search (replace with Qdrant/Pinecone)
_STORE: List[Dict[str, Any]] = []

def search_cases(query: str) -> List[Dict[str, Any]]:
    return [case for case in _STORE if query.lower() in json.dumps(case).lower()]