import gradio as gr
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from pdf_extractor.src.pdf_extractor.main import run
import time
# Global dictionary to store category-file mappings as a list of lists
category_files = []


def append_files(files):
    if not files:
        return get_files_summary()

    file_names = [os.path.basename(file.name) for file in files]
    category_files.append(file_names)
    # if category in category_files:
    #     category_files[category].append(file_names)
    # else:
    #     category_files[category] = [file_names]

    return get_files_summary()


def get_files_summary():
    if not category_files:
        return "No files uploaded."

    result = "Uploaded files by category:\n"
    return result


def clear_files():
    global category_files
    category_files = {}
    return None, "No files uploaded."


def category_changed(category):
    return None, get_files_summary()


def submit_files(prompt, files):
    """
    Process submitted files and generate submission summary
    Args:
        category: Currently selected category
        files: Currently selected files
    Returns:
        str: Submission status message
    """
    # Print statements for debugging
    print("Selected Files:", files)
    print("Current category_files dictionary:", category_files)

    if not category_files:
        return "No files uploaded yet!"

    if not files:
        return "Please select files to submit!"

    # Create a formatted submission summary
    # return main(prompt,files)
    # response = ""
    # for word in ["Processing", "your", "request", "now...", "\n"]:
    #     response+=word
    #     yield response  # Send output in chunks
    #     time.sleep(0.5)  # Simulate delay
    response = "Kindly wait till we analyze the given file <br>"
    yield response
    # def generator():
    #     yield from main(prompt, files)  # ✅ Use `yield from` to forward the generator
    # return generator
    file_path = ''
    if(len(files) > 0):
        file_path = files[0]
    data = run(prompt,file_path)
    for char in data:
        response += char
        time.sleep(0.01)
        yield response
    return 

css = """
    #component-1{
    position: fixed;
    z-index: 99;
    background: orange;
    left: 0;
    padding: 1rem 5rem;
    top: 0;
    }
    #component-2{
    margin-top: 90px;
    }
    #component-11{ height: 450px; overflow-y: auto !important; border-width: 1px !important ; border-color: e4e4e4 !important }
    """
# Create the Gradio interface
with gr.Blocks(css=css) as demo:
    gr.Markdown("# Invoice Validator Agent")
    with gr.Row():
        with gr.Column():
            files = gr.File(
                file_types=[".pdf",".jpg",".png",".jpeg",".xlsx",".csv"],
                file_count="multiple",
                label="Upload Files",
            )
            prompt_inputs = gr.Textbox(
                        label="Enter your prompt",  # Set label
                        placeholder="Type your prompt here...",  # Placeholder text
                        lines=2  # Set the number of lines for the input box
                    ) 
            submit_btn = gr.Button("Submit", variant="primary")
            clear_btn = gr.Button("Clear All")

        with gr.Column():
            # Add new textbox for submission results
            # submission_display = gr.Textbox(
            #     label="Submission Status", value="", interactive=False, lines=15
            # )
            gr.Markdown("### Submission Status")
            submission_display = gr.HTML(label="Submission Status", value="",show_label=True)


    # Event handlers
    files.change(fn=append_files, inputs=[files])

    clear_btn.click(fn=clear_files, inputs=None, outputs=[files])

    # Submit button functionality with proper inputs and debug prints
    submit_btn.click(
        fn=submit_files,
        inputs=[prompt_inputs , files],  # Taking category and files as inputs
        outputs=submission_display,  # Only updating the submission display
    )

# Launch the app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8751, share=False)
