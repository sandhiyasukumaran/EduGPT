from utils.prepare_vectordb import PrepareVectorDB
from typing import List, Tuple
from utils.load_config import LoadConfig
import os

APPCFG = LoadConfig()


class UploadFile:
    """
    Utility class for handling file uploads and processing.

    This class provides static methods for checking directories and processing uploaded files
    to prepare a VectorDB.
    """

    @staticmethod
    def process_uploaded_files(files_dir: List, chatbot: List, rag_with_dropdown: str, uploaded_files_list: List) -> Tuple:
        """
        Process uploaded files to prepare a VectorDB.

        Parameters:
            files_dir (List): List of paths to the uploaded files.
            chatbot: An instance of the chatbot for communication.

        Returns:
            Tuple: A tuple containing an empty string and the updated chatbot instance.
        """

        # Convert the file objects to just their basenames
        new_filenames = [os.path.basename(str(f.name if hasattr(f, "name") else f)) 
                         for f in files_dir]

        # Merge them into the existing list
        all_files = uploaded_files_list + new_filenames


        if rag_with_dropdown == "Upload doc: Process for RAG":
            prepare_vectordb_instance = PrepareVectorDB(data_directory=files_dir,
                                                        persist_directory=APPCFG.custom_persist_directory,
                                                        embedding_model_engine=APPCFG.embedding_model_engine,
                                                        chunk_size=APPCFG.chunk_size,
                                                        chunk_overlap=APPCFG.chunk_overlap)
            prepare_vectordb_instance.prepare_and_save_vectordb()

            if all_files:
                file_list_str = "\n".join(f"- {fn}" for fn in all_files)
                message = (
                    "The following files have now been uploaded and processed:\n"
                    f"{file_list_str}\n\n"
                    "You can now ask questions about these documents."
                )
            else:
                message = "No files have been uploaded yet."

            chatbot.append(("", message))

        else:
            chatbot.append(
                (" ", "If you would like to upload a PDF, please select your desired action in 'rag_with' dropdown."))
        return "", chatbot, all_files
