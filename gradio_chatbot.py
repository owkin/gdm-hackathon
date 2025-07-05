#!/usr/bin/env python3
"""
Gradio Chatbot Interface for GDM Hackathon Coding Agent

This provides a chat interface to interact directly with the smolagent coding agent.
"""

import io
import re
import traceback
from contextlib import redirect_stderr, redirect_stdout

import gradio as gr

from genetic_algo_code_agent import coding_agent


def filter_trace_output(output_text):
    """
    Filter the captured output to show only relevant execution trace information, and format as Markdown.
    """
    if not output_text.strip():
        return "No execution trace captured."

    # Remove ANSI escape codes
    ansi_escape = re.compile(r"\x1B\[[0-9;]*[mGKHF]")
    output_text = ansi_escape.sub("", output_text)

    # Split into lines and filter relevant information
    lines = output_text.split("\n")
    filtered_lines = []
    in_code_block = False
    in_tool_output = False

    for i, line in enumerate(lines):
        original_line = line
        line = line.strip()
        if not line:
            continue

        # Markdown formatting for step headers
        if re.match(r"^━━+ Step \d+ ━━+", line):
            filtered_lines.append(f"\n---\n**{line}**\n")
            continue
        if re.match(r"^Step \d+:", line):
            filtered_lines.append(f"\n### {line}\n")
            continue
        if "Executing parsed code:" in line:
            filtered_lines.append(f"\n**{line}**\n")
            continue

        # Code block markers
        if "<code>" in line:
            in_code_block = True
            filtered_lines.append("```python")
            continue
        elif "</code>" in line:
            in_code_block = False
            filtered_lines.append("```")
            continue
        if in_code_block:
            filtered_lines.append(original_line)
            continue

        # Tool output
        if line.startswith("Out -"):
            in_tool_output = True
            filtered_lines.append(f"\n**{line}**")
            continue
        if in_tool_output:
            filtered_lines.append(original_line)
            if i + 1 < len(lines) and any(
                marker in lines[i + 1] for marker in ["Step", "╭─", "━━━", "Executing"]
            ):
                in_tool_output = False
            continue

        # Patterns to look for in the trace
        relevant_patterns = [
            r"╭─.*─╮",  # Step headers
            r"━━━.*━━━",  # Step separators
            r"Step \d+:",  # Step numbers
            r"Executing parsed code:",  # Code execution
            r"Agent response:",  # Final response
            r"Thought:",  # Reasoning thoughts
            r"final_answer\(",  # Final answer calls
            r"Duration.*seconds",  # Timing information
            r"Input tokens:.*Output tokens:",  # Token usage
        ]
        tool_patterns = [
            r"load_.*_report",
            r"evaluate_report_relevance_in_zero_shot",
            r"print\(",
            r"final_answer_tool",
        ]
        is_relevant = any(re.search(pattern, line) for pattern in relevant_patterns)
        is_tool_call = any(re.search(pattern, line) for pattern in tool_patterns)
        if is_relevant or is_tool_call:
            filtered_lines.append(line)
        elif "error" in line.lower() or "exception" in line.lower():
            filtered_lines.append(f"**{original_line}**")
        elif "InterpreterError" in line or "Forbidden" in line:
            filtered_lines.append(f"**{original_line}**")

    if not filtered_lines:
        return "Execution completed without detailed trace information."

    # Collapse multiple blank lines
    result = "\n".join(filtered_lines)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result


def chat_with_agent(message, history, show_full_trace=True):
    """
    Chat function that sends user messages to the coding agent

    Args:
        message (str): User's message/prompt
        history (list): Chat history
        show_full_trace (bool): Whether to show the full execution trace

    Returns:
        list: Updated history with new messages
    """
    try:
        # Send the user's message to the coding agent
        print(f"User message: {message}")

        # Capture all output including intermediate steps
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()

        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            # Get response from the coding agent
            response = coding_agent.run(message)

        # Get the captured output
        captured_output = output_buffer.getvalue()
        captured_errors = error_buffer.getvalue()

        if show_full_trace:
            # Filter the output to show only relevant trace information
            filtered_trace = filter_trace_output(captured_output)

            # Combine the filtered trace with the final response
            full_trace = f"""🤖 **Agent Execution Trace:**

**User Message:** {message}

**Execution Steps:**
```
{filtered_trace}
```

**Final Response:** {response}

**Errors/Warnings:**
```
{captured_errors}
```
"""
            assistant_response = full_trace
        else:
            # Show only the final response
            assistant_response = f"🤖 **Agent Response:**\n\n{response}"

        print(f"Agent response: {response}")
        print(
            f"Trace captured: {len(captured_output)} characters, filtered to {len(filtered_trace) if show_full_trace else 0} characters"
        )

        # Convert to new message format
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": assistant_response})

        return history

    except Exception as e:
        error_msg = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(error_msg)

        # Convert to new message format
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_msg})

        return history


def clear_chat():
    """Clear the chat history"""
    return []


def get_available_tools():
    """Get list of available tools for reference"""
    tools_info = """
## Available Tools for Reference:

### Heatmap Tools (Spatial Transcriptomics):
- load_b_cell_heatmap_report
- load_cdk12_heatmap_report  
- load_dc_heatmap_report
- load_egfr_heatmap_report
- load_endothelial_heatmap_report
- load_epithelial_heatmap_report
- load_erbb2_heatmap_report
- load_fgfr3_heatmap_report
- load_fibroblast_heatmap_report
- load_granulocyte_heatmap_report
- load_il1b_heatmap_report
- load_krt7_heatmap_report
- load_malignant_bladder_heatmap_report
- load_mast_heatmap_report
- load_momac_heatmap_report
- load_muscle_heatmap_report
- load_other_heatmap_report
- load_pik3ca_heatmap_report
- load_plasma_heatmap_report
- load_rb1_heatmap_report
- load_s100a8_heatmap_report
- load_t_nk_heatmap_report
- load_tp53_heatmap_report

### Histopathological Tools:
- load_histopathological_immune_infiltration_report
- load_histopathological_tumor_nuclear_morphometry_report
- load_histopathological_tumor_stroma_compartments_report

### Evaluation Tool:
- evaluate_report_relevance_in_zero_shot(tool1_name, tool2_name)

### Available Patient IDs:
- test_patient
- CH_B_030a, CH_B_033a, CH_B_037a, CH_B_041a, CH_B_046a
- CH_B_059a, CH_B_062a, CH_B_064a, CH_B_068a, CH_B_069a
- CH_B_073a, CH_B_074a, CH_B_075a, CH_B_079a, CH_B_087a
"""
    return tools_info


# Create the Gradio interface
with gr.Blocks(
    title="GDM Hackathon - Coding Agent Chat", theme=gr.themes.Soft()
) as demo:
    gr.Markdown("# 🧬 GDM Hackathon - Coding Agent Chat")
    gr.Markdown(
        "Chat directly with the smolagent coding agent for biomarker discovery!"
    )

    with gr.Row():
        with gr.Column(scale=3):
            # Chat interface
            chatbot = gr.Chatbot(
                label="Chat with Coding Agent",
                height=600,
                show_label=True,
                container=True,
                type="messages",
                value=[],
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="Your message",
                    placeholder="Type your prompt here...",
                    lines=3,
                    scale=4,
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)

            with gr.Row():
                clear_btn = gr.Button("Clear Chat", variant="secondary")
                tools_btn = gr.Button("Show Available Tools", variant="secondary")
                show_trace_btn = gr.Button("Toggle Full Trace", variant="secondary")

        with gr.Column(scale=1):
            # Info panel
            gr.Markdown("## 📋 Quick Reference")
            gr.Markdown("""
            **Example prompts:**
            
            - "Test the load_tp53_heatmap_report tool on CH_B_030a"
            - "Evaluate the combination of load_cdk12_heatmap_report and load_dc_heatmap_report"
            - "Find the best 2 tools for survival prediction"
            - "Analyze patient CH_B_041a with histopathological tools"
            
            **Tips:**
            - Be specific about which tools to use
            - Include patient IDs when testing tools
            - Ask for evaluations of tool combinations
            """)

            # Tools info display
            tools_info = gr.Markdown(get_available_tools(), visible=False)

    # State for showing full trace
    show_full_trace = gr.State(True)

    # Event handlers
    def send_message(message, history, trace_state):
        if message.strip():
            # Ensure history is a list
            if history is None:
                history = []
            return chat_with_agent(message, history, trace_state)
        return history

    def toggle_tools_info():
        return gr.Markdown.update(visible=not tools_info.visible)

    def toggle_trace():
        return not show_full_trace.value

    # Connect components
    send_btn.click(
        send_message, inputs=[msg, chatbot, show_full_trace], outputs=[chatbot]
    ).then(lambda: "", outputs=[msg])

    msg.submit(
        send_message, inputs=[msg, chatbot, show_full_trace], outputs=[chatbot]
    ).then(lambda: "", outputs=[msg])

    clear_btn.click(clear_chat, outputs=[chatbot])

    tools_btn.click(toggle_tools_info, outputs=[tools_info])

    show_trace_btn.click(toggle_trace, outputs=[show_full_trace])

# Demo is created and ready to be launched
