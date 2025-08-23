import gradio as gr

with gr.Blocki() as demo:
   a = gr.Number(label='數字A',value=0)
   b = gr.Number(label='數字B',value=0)

   with gr.Row():
       add_btn = gr.Button("加法")
       sub_btn = gr.Button("減法")
       mul_btn = gr.Button("乘法")
       div_btn = gr.Button("除法")
       
   
       add_btn.click(inputs = [a,b], outputs = [c])
    