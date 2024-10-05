import os
import time
from pathlib import Path

import requests
from langchain.chains import LLMChain
from langchain.chains import MapReduceDocumentsChain
from langchain.chains import ReduceDocumentsChain
from langchain.chains import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.llms.ctransformers import CTransformers

# from amiribd.articles.editor.transcribe import
from .transcribe import generate_random_file_name

APPS_DIR = Path(__file__).resolve(strict=True).parent.parent

TRANSCRIPT_DOWNLOAD_DIR = Path(APPS_DIR/"media"/"transcripts"/ "files")

class TranscriptSummarizer:
    def __init__(self,filename):
        self.filename_url = filename
        self.config = {
            "max_new_tokens": 4096, "temperature": 0.7, "context_length": 4096}
        self.local_filepath = ""
    # Function to download the PDF file locally
    def download_pdf(self):
        instance_file_name = generate_random_file_name()
            # Ensure the directory exists
        if not Path.exists(TRANSCRIPT_DOWNLOAD_DIR):
            os.makedirs(TRANSCRIPT_DOWNLOAD_DIR)  # noqa: PTH103
        # Path for the local file
        local_file_path = os.path.join(  # noqa: PTH118
            TRANSCRIPT_DOWNLOAD_DIR, f"{instance_file_name}.txt")
        try:
            response = requests.get(self.filename_url, stream=True)  # noqa: S113
            response.raise_for_status()  # Raise an exception for HTTP errors
            with open(local_file_path, "wb") as f:  # noqa: PTH123
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            self.local_filepath = local_file_path
            return self.local_filepath  # noqa: TRY300
        except requests.exceptions.RequestException as e:  # noqa: F841
            return False

    def text_loader_to_docs(self):
        if not self.download_pdf():
            msg = "Could not process the file"
            raise ValueError(msg)
        loader = TextLoader(self.local_filepath)
        return loader.load()

    def prepare_llm(self):
        return CTransformers(
            model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
            model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            config=self.config,
            threads=os.cpu_count(),
        )
    def prepare_map_template_and_chain(self):
        # Map template and chain
        docs = self.text_loader_to_docs()  # noqa: F841
        map_template = """<s>[INST] The following is a part of a transcript:
        {docs}
        Based on this, please identify the main points.
        Answer:  [/INST] </s>"""
        map_prompt = PromptTemplate.from_template(map_template)
        return LLMChain(llm=self.prepare_llm(), prompt=map_prompt)

    def prepare_reduce_template_chain(self):
        # Reduce template and chain
        reduce_template = """
        <s>[INST] The following is set of summaries from the transcript:
        {doc_summaries}
        Take these and distill it into a final, consolidated summary of the main points.
        Construct it as a well organized summary of the main points and should be
        between 3 and 5 paragraphs.
        Answer:  [/INST] </s>"""
        reduce_prompt = PromptTemplate.from_template(reduce_template)
        return LLMChain(llm=self.prepare_llm(), prompt=reduce_prompt)

    def summarize(self):
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=self.prepare_reduce_template_chain(),
            document_variable_name="doc_summaries",
        )
        # Combines and iteratively reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            # This is final chain that is called.
            combine_documents_chain=combine_documents_chain,
            # If documents exceed context for `StuffDocumentsChain`
            collapse_documents_chain=combine_documents_chain,
            # The maximum number of tokens to group documents into.
            token_max=4000,
        )
        # Combining documents by mapping a chain over them, then combining results
        map_reduce_chain = MapReduceDocumentsChain(
            # Map chain
            llm_chain=self.prepare_map_template_and_chain(),
            # Reduce chain
            reduce_documents_chain=reduce_documents_chain,
            # The variable name in the llm_chain to put the documents in
            document_variable_name="docs",
            # Return the results of the map steps in the output
            return_intermediate_steps=True,
        )
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000, chunk_overlap=0,
        )
        docs = self.text_loader_to_docs()
        split_docs = text_splitter.split_documents(docs)
        start_time = time.time()  # noqa: F841
        result = map_reduce_chain.__call__(split_docs, return_only_outputs=True)
        return result["output_text"]



def download_pdf(filename):
    instance_file_name = generate_random_file_name()
        # Ensure the directory exists
    if not os.path.exists(TRANSCRIPT_DOWNLOAD_DIR):  # noqa: PTH110
        os.makedirs(TRANSCRIPT_DOWNLOAD_DIR)  # noqa: PTH103
    # Path for the local file
    local_file_path = os.path.join(TRANSCRIPT_DOWNLOAD_DIR, f"{instance_file_name}.txt")  # noqa: PTH118
    try:
        response = requests.get(filename, stream=True)  # noqa: S113
        response.raise_for_status()  # Raise an exception for HTTP errors
        with open(local_file_path, "wb") as f:  # noqa: PTH123
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return local_file_path  # noqa: TRY300
    except requests.exceptions.RequestException as e:  # noqa: F841
        return False




def summarize_transcript(filename):
    # Load transcript
    local_filename = download_pdf(filename)
    loader = TextLoader(local_filename)
    docs = loader.load()
    # Load LLM
    config = {"max_new_tokens": 4096, "temperature": 0.7, "context_length": 4096}
    llm = CTransformers(
        model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        config=config,
        threads=os.cpu_count(),
    )
    # Map template and chain
    map_template = """
    <s>[INST] The following is a part of a transcript:
    {docs}
    Based on this, please identify the main points.
    Answer:  [/INST] </s>"""
    map_prompt = PromptTemplate.from_template(map_template)

    map_chain = LLMChain(llm=llm, prompt=map_prompt)
    # Reduce template and chain
    reduce_template = """
    <s>[INST] The following is set of summaries from the transcript:
    {doc_summaries}
    Take these and distill it into a final, consolidated summary of the main points.
    Construct it as a well organized summary of the main points and should be
    between 3 and 5 paragraphs.
    Answer:  [/INST] </s>"""
    reduce_prompt = PromptTemplate.from_template(reduce_template)
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="doc_summaries",
    )
    # Combines and iteratively reduces the mapped documents
    reduce_documents_chain = ReduceDocumentsChain(
        # This is final chain that is called.
        combine_documents_chain=combine_documents_chain,
        # If documents exceed context for `StuffDocumentsChain`
        collapse_documents_chain=combine_documents_chain,
        # The maximum number of tokens to group documents into.
        token_max=4000,
    )
    # Combining documents by mapping a chain over them, then combining results
    map_reduce_chain = MapReduceDocumentsChain(
        # Map chain
        llm_chain=map_chain,
        # Reduce chain
        reduce_documents_chain=reduce_documents_chain,
        # The variable name in the llm_chain to put the documents in
        document_variable_name="docs",
        # Return the results of the map steps in the output
        return_intermediate_steps=True,
    )

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000, chunk_overlap=0,
    )
    split_docs = text_splitter.split_documents(docs)
    # Run the chain
    start_time = time.time()  # noqa: F841
    result = map_reduce_chain.__call__(split_docs, return_only_outputs=True)
    return result["output_text"]


