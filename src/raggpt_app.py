"""
    This module uses Gradio to create an interactive web application for a chatbot with various features.

    The application interface is organized into three rows:
    1. The first row contains a Chatbot component that simulates a conversation with a language model, along with a hidden
    reference bar initially. The reference bar can be toggled using a button. The chatbot supports feedback in the form
    of like and dislike icons.

    2. The second row consists of a Textbox for user input. Users can enter text or upload PDF/doc files.

    3. The third row includes buttons for submitting text, toggling the reference bar visibility, uploading PDF/doc files,
    adjusting temperature for GPT responses, selecting the document type, and clearing the input.

    The application processes user interactions:
    - Uploaded files trigger the processing of the files, updating the input and chatbot components.
    - Submitting text triggers the chatbot to respond, considering the selected document type and temperature settings.
    The response is displayed in the Textbox and Chatbot components, and the reference bar may be updated.

    The application can be run as a standalone script, launching the Gradio interface for users to interact with the chatbot.

    Note: The docstring provides an overview of the module's purpose and functionality, but detailed comments within the code
    explain specific components, interactions, and logic throughout the implementation.
"""
import gradio as gr
from utils.upload_file import UploadFile
from utils.chatbot import ChatBot
from utils.ui_settings import UISettings


with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("EduGPT"):
            ##############
            # First ROW:
            ##############
            with gr.Row() as row_one:
                with gr.Column(visible=False) as reference_bar:
                    ref_output = gr.Markdown()
                    # ref_output = gr.Textbox(
                    #     lines=22,
                    #     max_lines=22,
                    #     interactive=False,
                    #     type="text",
                    #     label="References",
                    #     show_copy_button=True
                    # )

                with gr.Column() as chatbot_output:
                    chatbot = gr.Chatbot(
                        [],
                        elem_id="chatbot",
                        bubble_full_width=False,
                        height=700,
                        avatar_images=(
                            ("images/student.jpg"), "images/openai_.png"),
                        # render=False
                    )
                    # **Adding like/dislike icons
                    chatbot.like(UISettings.feedback, None, None)
            ##############
            # SECOND ROW:
            ##############
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=4,
                    scale=8,
                    placeholder="Enter text and press enter, or upload PDF files",
                    container=False,
                )

            ##############
            # Third ROW:
            ##############
            with gr.Row() as row_two:
                text_submit_btn = gr.Button(value="Submit text")
                sidebar_state = gr.State(False)
                btn_toggle_sidebar = gr.Button(
                    value="References")
                btn_toggle_sidebar.click(UISettings.toggle_sidebar, [sidebar_state], [
                    reference_bar, sidebar_state])
                
                rag_with_dropdown = gr.Dropdown(
                    label="RAG with", choices=["Preprocessed doc", "Upload doc: Process for RAG"], value="Preprocessed doc", interactive=True)
                
                upload_btn = gr.UploadButton(
                    "📁 Upload PDF", file_types=[
                        '.pdf'
                    ],
                    file_count="multiple", visible=False)
                
                #    Function to show/hide upload_btn
                # -------------------------------------
                def toggle_upload(mode):
                    if mode =="Upload doc: Process for RAG":
                        return gr.update(visible=True)
                    else:
                        return gr.update(visible=False)

                # Trigger the toggle each time docs_mode changes
                rag_with_dropdown.change(
                    toggle_upload,
                    inputs=[rag_with_dropdown],
                    outputs=[upload_btn]
                )
                uploaded_files_state = gr.State([])
                clear_button = gr.ClearButton([input_txt, chatbot])
            ##############
            # Process:
            ##############
            file_msg = upload_btn.upload(fn=UploadFile.process_uploaded_files, inputs=[
                upload_btn, chatbot, rag_with_dropdown, uploaded_files_state], outputs=[input_txt, chatbot, uploaded_files_state], queue=False)

            txt_msg = input_txt.submit(fn=ChatBot.respond,
                                       inputs=[chatbot, input_txt,
                                               rag_with_dropdown],
                                       outputs=[input_txt,
                                                chatbot, ref_output],
                                       queue=False).then(lambda: gr.Textbox(interactive=True),
                                                         None, [input_txt], queue=False)

            txt_msg = text_submit_btn.click(fn=ChatBot.respond,
                                            inputs=[chatbot, input_txt,
                                                    rag_with_dropdown],
                                            outputs=[input_txt,
                                                     chatbot, ref_output],
                                            queue=False).then(lambda: gr.Textbox(interactive=True),
                                                              None, [input_txt], queue=False)


if __name__ == "__main__":
    demo.launch()
