import gradio as gr



with gr.Blocks() as demo:
    n1_textbox = gr.Textbox(label="第一個數", placeholder="請輸入數字")
    op_radio   = gr.Radio(choices=["+", "-", "*", "/"], value="+", label="運算子")
    n2_textbox = gr.Textbox(label="第二個數", placeholder="請輸入數字")
    output_textbox = gr.Textbox(label="輸出", placeholder="輸出結果會顯示在這裡")
    calc_button = gr.Button("計算")

    # ✅ 注意：inputs 只能寫一次，且順序要對應 cal(i, op, j)
    @calc_button.click(
        inputs=[n1_textbox, op_radio, n2_textbox],
        outputs=output_textbox
    )

    # 計算函式：接收「第一個數」、「運算子」、「第二個數」
    def cal(i, op, j):
        # 將字串轉為浮點數，並處理格式錯誤
        try:
            a = float(i)
            b = float(j)
        except (TypeError, ValueError):
            return "Error：請輸入有效數字"
        
        # 依運算子計算，並處理除以 0
        if op == '+':
            res = a + b
        elif op == '-':
            res = a - b
        elif op == '*':
            res = a * b
        elif op == '/':
            if b == 0:
                return "Error：除數不可為 0"
            res = a / b
        else:
            return "Error：未知運算子"

        # 回傳字串或數字都可以；這裡回傳字串避免顯示格式問題
        return str(res)

demo.launch()